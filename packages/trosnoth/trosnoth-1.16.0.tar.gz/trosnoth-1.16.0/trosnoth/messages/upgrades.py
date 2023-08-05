import logging

from trosnoth.const import (
    NOT_ENOUGH_COINS_REASON, PLAYER_DEAD_REASON, CANNOT_REACTIVATE_REASON,
    GAME_NOT_STARTED_REASON,
    INVALID_UPGRADE_REASON, DISABLED_UPGRADE_REASON,
)
from trosnoth.messages.base import (
    AgentRequest, ServerCommand, ServerResponse, ClientCommand,
)
from trosnoth.model.universe_base import NO_PLAYER

log = logging.getLogger(__name__)


class BuyUpgradeMsg(AgentRequest):
    '''
    Signal from interface that a buy has been requested.

    In order for everything to stay in sync, an upgrade purchase works in 3
    steps.

    1. The client sends BuyUpgradeMsg.
    2. The server checks that the coins are avaliable, and replies with
        UpgradeApprovedMsg.
    3. The client sends PlayerHasUpgradeMsg, which is then broadcast to all
        clients.

    To make launching of grenades more responsive, there is a special flag on
    Upgrade classes called doNotWaitForServer. If this flag is set, the client
    assumes that the purchase is successful unless it hears otherwise, and the
    server broadcasts PlayerHasUpgradeMsg immediately at step 2. Step 3 is not
    performed in this case.
    '''
    idString = b'GetU'
    fields = 'upgradeType', 'tickId'
    packspec = 'cH'
    timestampedPlayerRequest = True

    def clientValidate(self, localState, world, sendResponse):
        upgrade = world.getUpgradeType(self.upgradeType)
        if not upgrade.doNotWaitForServer:
            # Don't bother trying to validate locally, let the server decide.
            return True

        player = localState.player
        denialReason = self.getDenialReason(player, upgrade)
        if denialReason:
            response = CannotBuyUpgradeMsg(denialReason)
            response.local = True
            sendResponse(response)
            return False
        return True

    def applyRequestToLocalState(self, localState):
        upgrade = localState.world.getUpgradeType(self.upgradeType)
        if upgrade.doNotWaitForServer:
            localState.player.activateItemByCode(
                self.upgradeType, local=localState)

    def serverApply(self, game, agent):
        player = agent.player
        if player is None:
            return

        upgrade = player.world.getUpgradeType(self.upgradeType)
        denialReason = self.getDenialReason(player, upgrade)
        if denialReason:
            agent.messageToAgent(CannotBuyUpgradeMsg(denialReason))
        else:
            if player.items.server_isApproved(upgrade):
                # Silently ignore requests for an item that's already approved
                return
            self._processUpgradePurchase(game, agent, player, upgrade)

    def getDenialReason(self, player, upgrade):
        from trosnoth.model.upgrades import allUpgrades

        if not player.world.abilities.upgrades:
            return GAME_NOT_STARTED_REASON
        if player.dead:
            return PLAYER_DEAD_REASON

        if upgrade not in allUpgrades:
            return INVALID_UPGRADE_REASON

        if not upgrade.enabled:
            return DISABLED_UPGRADE_REASON

        requiredCoins = self._getRequiredCoins(player, upgrade)
        if requiredCoins is None:
            return CANNOT_REACTIVATE_REASON

        if player.coins < requiredCoins:
            return NOT_ENOUGH_COINS_REASON

        return None

    def _getRequiredCoins(self, player, upgradeClass):
        existing = player.items.get(upgradeClass)
        if existing:
            return existing.getReactivateCost()
        return upgradeClass.requiredCoins

    def _processUpgradePurchase(self, game, agent, player, upgrade):
        '''
        Sends the required sequence of messages to gameRequests to indicate
        that the upgrade has been purchased by the player.
        '''
        requiredCoins = self._getRequiredCoins(player, upgrade)
        game.sendServerCommand(PlayerCoinsSpentMsg(player.id, requiredCoins))

        upgrade.upgrade_approved_server_side(game, agent, player)
        if upgrade.doNotWaitForServer:
            game.sendServerCommand(PlayerHasUpgradeMsg(
                upgrade.upgradeType, self.tickId, player.id))
        else:
            player.items.server_approve(upgrade)
            agent.messageToAgent(UpgradeApprovedMsg(upgrade.upgradeType))


class StartTeamBoostPurchaseMsg(ClientCommand):
    idString = b'TBSt'
    fields = 'boost_code', 'team_id'
    packspec = 'cc'
    team_id = b'\x00'

    @property
    def boost_class(self):
        from trosnoth.model.upgrades import team_boost_by_code
        return team_boost_by_code[self.boost_code]

    def clientValidate(self, local_state, world, send_response):
        denial_reason = self.get_denial_reason(local_state.player)
        if denial_reason:
            response = CannotBuyUpgradeMsg(denial_reason)
            response.local = True
            send_response(response)
            return False
        return True

    def serverApply(self, game, agent):
        player = agent.player
        if player is None or player.team is None:
            return

        denial_reason = self.get_denial_reason(player)
        if denial_reason:
            agent.messageToAgent(CannotBuyUpgradeMsg(denial_reason))
            return

        game.sendServerCommand(PlayerCoinsSpentMsg(player.id, self.boost_class.deposit_cost))

        self.team_id = agent.player.team.id
        game.sendServerCommand(self)

    def get_denial_reason(self, player):
        if not player.world.abilities.upgrades:
            return GAME_NOT_STARTED_REASON

        try:
            boost_class = self.boost_class
        except KeyError:
            return INVALID_UPGRADE_REASON

        team = player.world.getTeam(self.team_id)
        if team.boosts.get(boost_class):
            return CANNOT_REACTIVATE_REASON

        if player.coins < boost_class.deposit_cost:
            return NOT_ENOUGH_COINS_REASON

        return None

    def applyOrderToWorld(self, world):
        world.getTeam(self.team_id).boosts.begin_purchase_locally(self.boost_class)


class ContributeToTeamBoostMsg(ClientCommand):
    idString = b'TBAd'
    fields = 'boost_code', 'coins', 'team_id'
    packspec = 'cIc'
    team_id = b'\x00'

    @property
    def boost_class(self):
        from trosnoth.model.upgrades import team_boost_by_code
        return team_boost_by_code[self.boost_code]

    def clientValidate(self, local_state, world, send_response):
        return self._validate(local_state.player)

    def serverApply(self, game, agent):
        player = agent.player
        if not self._validate(player):
            return

        game.sendServerCommand(PlayerCoinsSpentMsg(player.id, self.boost_class.deposit_cost))
        self.team_id = agent.player.team.id
        game.sendServerCommand(self)

    def _validate(self, player):
        if self.coins <= 0:
            return False
        if player is None or player.team is None:
            return False
        if player.coins < self.coins:
            return False
        try:
            boost_class = self.boost_class
        except KeyError:
            return False

        boost = player.team.boosts.get(boost_class)
        if boost is None:
            # Deposit has not been paid yet
            return False
        if boost.activated:
            # Boost is already active
            return False

        return True

    def applyOrderToWorld(self, world):
        boost = world.getTeam(self.team_id).boosts.get(self.boost_class)
        boost.remaining_cost = max(0, boost.remaining_cost - self.coins)


class PlayerHasUpgradeMsg(ClientCommand):
    '''
    Sent by the local client when it receives word from the server that an
    upgrade purchase has been approved.
    '''
    idString = b'GotU'
    fields = 'upgradeType', 'tickId', 'playerId'
    packspec = 'cHc'
    playerId = NO_PLAYER
    timestampedPlayerRequest = True

    def applyRequestToLocalState(self, localState):
        if __debug__:
            # If doNotWaitForServer is set, this message does not originate
            # from the client, so applyRequestToLocalState() is never called.
            upgradeClass = localState.world.getUpgradeType(self.upgradeType)
            assert not upgradeClass.doNotWaitForServer

        item = localState.player.activateItemByCode(
            self.upgradeType, local=localState)

    def serverApply(self, game, agent):
        upgradeClass = game.world.getUpgradeType(self.upgradeType)
        if agent.player and agent.player.items.server_isApproved(upgradeClass):
            self.playerId = agent.player.id
            game.sendServerCommand(self)

    def applyOrderToWorld(self, world):
        player = world.getPlayer(self.playerId)
        player.activateItemByCode(self.upgradeType)

    def applyOrderToLocalState(self, localState, world):
        if localState.player and self.playerId == localState.player.id:
            upgradeClass = world.getUpgradeType(self.upgradeType)
            upgrade = localState.player.items.get(upgradeClass)
            if upgrade:
                upgrade.serverVerified(localState)


class BuyAmmoMsg(ClientCommand):
    idString = b'Ammo'
    fields = 'gun_code', 'tickId', 'player_id'
    packspec = 'cHc'
    timestampedPlayerRequest = True
    player_id = NO_PLAYER

    @classmethod
    def create(cls, gun_type, tick_id):
        return cls(gun_type.gun_code, tick_id)

    @property
    def gun_type(self):
        from trosnoth.model.upgrades import gun_type_by_code
        return gun_type_by_code[self.gun_code]

    def clientValidate(self, local_state, world, send_response):
        return self.validate(local_state.player)

    def applyRequestToLocalState(self, localState):
        localState.player.guns.get(self.gun_type).fill_local_ammo_clip()

    def serverApply(self, game, agent):
        player = agent.player
        if not self.validate(player):
            player.sendResync()
            return

        cost = self.gun_type.get_required_coins(player)
        game.sendServerCommand(PlayerCoinsSpentMsg(player.id, cost))
        self.player_id = player.id
        game.sendServerCommand(self)

    def validate(self, player):
        if player is None or not player.aggression:
            return False

        from trosnoth.model.upgrades import gun_type_by_code
        try:
            gun_type = gun_type_by_code[self.gun_code]
        except KeyError:
            return False

        cost = gun_type.get_required_coins(player)
        if cost is None:
            return False

        if player.coins < cost:
            return False

        return True

    def applyOrderToWorld(self, world):
        player = world.getPlayer(self.player_id)
        player.guns.get(self.gun_type).fill_local_ammo_clip()


class PlayerCoinsSpentMsg(ServerCommand):
    '''
    This message is necessary, because without it a client can't always tell
    where the PlayerHasUpgradeMsg pulled all its coins from.
    '''
    idString = b'Spnt'
    fields = 'playerId', 'count'
    packspec = 'cI'


class AwardPlayerCoinMsg(ServerCommand):
    idString = b'Coin'
    fields = 'playerId', 'count', 'sound'
    packspec = 'cI?'
    sound = False

    def applyOrderToWorld(self, world):
        player = world.getPlayer(self.playerId)
        if player:
            player.incrementCoins(self.count)
            if self.sound:
                world.onCoinSound(player)


class SetPlayerCoinsMsg(ServerCommand):
    idString = b'SetC'
    fields = 'playerId', 'value'
    packspec = 'cI'

    def applyOrderToWorld(self, world):
        player = world.getPlayer(self.playerId)
        if player:
            player.setCoins(self.value)


class CannotBuyUpgradeMsg(ServerResponse):
    '''
    Valid reasonId values are defined in trosnoth.const.
    '''
    idString = b'NotU'
    fields = 'reasonId'
    packspec = 'c'
    local = False

    def applyOrderToLocalState(self, localState, world):
        if self.local:
            return
        item = localState.popUnverifiedItem()
        if item:
            item.deniedByServer(localState)


class UpgradeApprovedMsg(ServerResponse):
    '''
    Signals to the player that's trying to buy an upgrade that the purchase has
    been successful, and the player should proceed to send a
    PlayerHasUpgradeMsg to use the upgrade. This back and forth is necessary
    because the using of the upgrade needs to happen based on the location of
    the player on their own client's screen, not based on the server's idea of
    where the client is.
    '''
    idString = b'ByOk'
    fields = 'upgradeType'
    packspec = 'c'


class UpgradeChangedMsg(ServerCommand):
    '''
    A message for the clients that informs them of a change in an upgrade stat.
    statType may be:
        'S' - coin cost
        'T' - time limit
        'X' - explosion radius
        'E' - enabled
    '''
    idString = b'UpCh'
    fields = 'upgradeType', 'statType', 'newValue'
    packspec = 'ccf'


class ProjectileLaunchedMsg(ServerCommand):
    fields = 'player_id', 'projectile_id'
    packspec = 'cI'

    def applyOrderToWorld(self, world):
        player = world.getPlayer(self.player_id)
        if not player:
            return
        world.projectile_by_id[self.projectile_id] = self.build_projectile(world, player)

    def build_projectile(self, world, player):
        raise NotImplementedError()

    def applyOrderToLocalState(self, local_state, world):
        if self.player_id == local_state.player.id:
            projectile = world.projectile_by_id[self.projectile_id]
            local_state.projectiles.official_projectile_added(projectile)


class MineLaunchedMsg(ProjectileLaunchedMsg):
    idString = b'Mine'

    def build_projectile(self, world, player):
        from trosnoth.model.projectile import MineProjectile
        return MineProjectile(world, player=player, id_=self.projectile_id)


class MineExplodedMsg(ServerCommand):
    idString = b'KBam'
    fields = 'projectile_id'
    packspec = 'I'

    def applyOrderToWorld(self, world):
        mine = world.projectile_by_id.get(self.projectile_id)
        from trosnoth.model.projectile import MineProjectile
        if not mine or not isinstance(mine, MineProjectile):
            log.error(f'No mine with ID {self.projectile_id}')
            return

        world.on_mine_explosion(mine.pos)
        world.remove_projectile(mine)

    def applyOrderToLocalState(self, local_state, world):
        local_state.projectiles.remove_by_id(self.projectile_id)


class RemoveProjectileMsg(ServerCommand):
    idString = b'Blip'
    fields = 'projectile_id'
    packspec = 'I'

    def applyOrderToWorld(self, world):
        projectile = world.projectile_by_id.get(self.projectile_id)
        if not projectile:
            log.error(f'No projectile with ID {self.projectile_id}')
            return
        world.remove_projectile(projectile)

    def applyOrderToLocalState(self, local_state, world):
        local_state.projectiles.remove_by_id(self.projectile_id)
