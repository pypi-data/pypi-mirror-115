'''upgrades.py - defines the behaviour of upgrades.'''

import logging
from enum import Enum
from typing import Optional

import pygame
import math

from trosnoth.const import TICK_PERIOD
from trosnoth.messages import ShootMsg, BuyAmmoMsg, ShotFiredMsg, FireShoxwaveMsg, MineLaunchedMsg
from trosnoth.model.projectile import GrenadeProjectile, MineProjectile, LocalMine
from trosnoth.model.shot import GrenadeShot, PredictedRicochetTrajectory

log = logging.getLogger(__name__)

upgradeOfType = {}
allUpgrades = set()
gun_type_by_code = {}
team_boost_by_code = {}


class Categories(Enum):
    ITEM = ('Items', 'category-item.png')
    # TEAM = ('Team', 'category-team.png')
    WEAPON = ('Guns', 'category-weapon.png')

    def __init__(self, name, icon_filename):
        self.display_name = name
        self.icon_filename = icon_filename
        self.upgrades = []


def registerUpgrade(upgrade_class):
    '''
    Marks the given upgrade class to be used in the game.
    '''
    record_upgrade_class_string(upgrade_class)
    allUpgrades.add(upgrade_class)
    upgrade_class.category.upgrades.append(upgrade_class)
    upgrade_class.category.upgrades.sort(key=lambda u: u.sort_order)

    return upgrade_class


def specialUpgrade(upgradeClass):
    '''
    Marks the given upgrade class as a special upgrade that can be used only
    via the console.
    '''
    record_upgrade_class_string(upgradeClass)
    return upgradeClass


def record_upgrade_class_string(upgradeClass):
    '''
    Records the type string of the given upgrade class for use in network
    communication.
    '''
    if upgradeClass.upgradeType in upgradeOfType:
        raise KeyError('2 upgrades with %r' % (upgradeClass.upgradeType,))
    upgradeOfType[upgradeClass.upgradeType] = upgradeClass


def register_gun(gun_type):
    assert gun_type.gun_code not in gun_type_by_code
    gun_type_by_code[gun_type.gun_code] = gun_type
    return gun_type


def register_team_boost(team_boost):
    team_boost_by_code[team_boost.boost_code] = team_boost
    return team_boost


class ItemManager(object):
    '''
    Keeps track of which items are currently active for a given player.
    '''

    def __init__(self, world, owner):
        self.owner = owner
        self.world = world
        self.active = {}

        # Only used server-side. Set of upgrade classes for which the server
        # has sent UpgradeApprovedMsg, but has not yet received
        # PlayerHasUpgradeMsg from the client.
        self.serverApproved = set()

    def dump(self):
        return [item.dump() for item in list(self.active.values())]

    def restore(self, data):
        self.clear()

        for item_data in data:
            item_class = self.world.getUpgradeType(item_data['kind'])
            self.active[item_class] = item_class.restore(self.owner, item_data)

    def get(self, upgradeKind):
        '''
        :param upgradeKind: A subclass of :class Upgrade:
        :return: An instance of the given subclass, if this player/team
             has an active item of that type, else None.
        '''
        return self.active.get(upgradeKind)

    def has(self, upgradeKind):
        '''
        :param upgradeKind: A subclass of :class Upgrade:
        :return: True iff this player/team has an active item of the
            given type.
        '''
        return upgradeKind in self.active

    def hasAny(self):
        return bool(self.active)

    def activate(self, item_class, local):
        item = self.get(item_class)
        if not item:
            self.active[item_class] = item = item_class(self.owner)
        self.serverApproved.discard(item_class)

        if local:
            if item.doNotWaitForServer:
                local.addUnverifiedItem(item)
            item.localUse(local)
        else:
            item.use()
        return item

    def clear(self):
        '''
        Clears the player/team's upgrades, performing any finalisation
        needed.
        '''
        for item in list(self.active.values()):
            item.delete()

        self.active = {}
        self.serverApproved = set()

    def delete(self, activeItem):
        '''
        Deletes the item, assuming that the item's tear-down has already
        been done.
        '''
        upgradeKind = activeItem.__class__
        if self.get(upgradeKind) == activeItem:
            del self.active[upgradeKind]

    def server_approve(self, upgradeKind):
        assert self.world.isServer
        self.serverApproved.add(upgradeKind)

    def server_isApproved(self, upgradeKind):
        assert self.world.isServer
        return upgradeKind in self.serverApproved

    def tick(self):
        for item in list(self.active.values()):
            if item.timeRemaining is not None and not item.unverified:
                item.timeRemaining -= self.world.tickPeriod
                if item.timeRemaining <= 0:
                    item.delete()
                    item.timeRanOut()

        for item in list(self.active.values()):
            item.tick()

    def getActiveKinds(self):
        '''
        :return: A new list of the Upgrade classes that are currently active.
        '''
        return list(self.active.keys())

    def getAll(self):
        return list(self.active.values())


class TeamBoosts:
    def __init__(self, team):
        self.team = team
        self.world = team.world
        self.current = {}

    def dump(self):
        return [item.dump() for item in list(self.current.values())]

    def restore(self, data):
        self.clear_locally()

        for item_data in data:
            boost = TeamBoost.build_from_data(self.team, data)
            self.current[type(boost)] = boost

    def get(self, boost_kind):
        return self.current.get(boost_kind)

    def has(self, boost_kind):
        return boost_kind in self.current and self.current[boost_kind].activated

    def begin_purchase_locally(self, item_class):
        assert item_class not in self.current
        self.current[item_class] = item_class(self.team)

    def clear_locally(self):
        for item in list(self.current.values()):
            item.deleted()
        self.current = {}

    def tick(self):
        for boost in list(self.current.values()):
            boost.tick()
            if boost.expired:
                boost.deleted()
                del self.current[type(boost)]


class ShopItem:
    '''
    Base class for items that can be bought from the radial shop menu.
    '''
    name: str
    icon_path: str
    default_key: Optional[int] = None
    sort_order = 100

    @classmethod
    def get_required_coins(cls, player) -> Optional[int]:
        '''
        :return: the current cost in coins of the given player to
            purchase this shop item, or None if the given player cannot
            purchase this item at this time.
        '''
        raise NotImplementedError

    @classmethod
    def get_icon(cls, sprites, enabled=True):
        if not enabled:
            return sprites.disabled_shop_item(cls)
        return sprites.shop_item_image(cls)


class Upgrade(ShopItem):
    '''Represents an upgrade that can be bought.'''
    requiredCoins = None
    default_panda3d_key = None
    icon_path = 'upgrade-unknown.png'
    enabled = True
    applyLocally = False
    aggressive = False
    projectile_kind = None
    category = Categories.ITEM

    # If this flag is set, instead of waiting for a verdict from the server,
    # the client will guess whether a purchase of this upgrade will be allowed,
    # and go on that assumption until it finds out otherwise. This exists so
    # that grenades can feel responsive even if there's high latency.
    doNotWaitForServer = False

    # Upgrades have an upgradeType: this must be a unique, single-character
    # value.
    upgradeType = NotImplemented
    totalTimeLimit = NotImplemented
    name = NotImplemented

    def __init__(self, player):
        self.world = None
        if player:
            self.world = player.world
        self.player = player
        self.timeRemaining = self.totalTimeLimit
        self.unverified = False

    def __str__(self):
        return self.name

    @classmethod
    def get_required_coins(cls, player) -> Optional[int]:
        if not cls.pre_buy_check(player):
            return None
        upgrade = player.items.get(cls)
        if upgrade:
            return upgrade.getReactivateCost()
        return cls.requiredCoins

    @classmethod
    def pre_buy_check(cls, player):
        '''
        If this method returns False, the given player will not attempt
        to buy this upgrade.
        '''
        if cls.aggressive:
            return player.aggression
        return True

    def dump(self):
        return {
            'kind': self.upgradeType,
            'time': self.timeRemaining,
        }

    @classmethod
    def restore(cls, player, data):
        item = cls(player)
        item.timeRemaining = data['time']
        return item

    def tick(self):
        pass

    def getReactivateCost(self):
        '''
        :return: The cost required to activate the upgrade again before it's
            run out, or None if that's impossible.
        '''
        return None

    @classmethod
    def getActivateNotification(cls, nick):
        if cls.projectile_kind:
            return '{} has launched a {}'.format(nick, cls.name)
        return '{} is using a {}'.format(nick, cls.name)

    def use(self):
        '''Initiate the upgrade (server-side)'''
        pass

    def localUse(self, localState):
        '''Initiate the upgrade (client-side)'''
        if self.applyLocally:
            if self.doNotWaitForServer:
                self.unverified = True
            self.use()

    @classmethod
    def upgrade_approved_server_side(cls, game, agent, player):
        '''
        Called server-side when the purchase is requested, and all
        checks have succeeded, but before UpgradeApprovedMsg (or
        PlayerHasUpgradeMsg if doNotWaitForServer is true) is sent.
        This is a chance for upgrades to send server commands specific
        to the upgrade type.
        '''
        pass

    def serverVerified(self, localState):
        '''
        Called client-side when the server has confirmed that this upgrade is
        allowed. This is most useful as a hook for upgrade classes which set
        the doNotWaitForServer flag.
        '''
        if self.doNotWaitForServer:
            self.unverified = False
            localState.discardUnverifiedItem(self)

    def deniedByServer(self, localState):
        '''
        Called client-side when a doNotWaitForServer upgrade needs to be
        canceled because the server did not approve it.
        '''
        self.delete()

    def delete(self):
        '''
        Performs any necessary tasks to remove this upgrade from the game.
        '''
        self.player.items.delete(self)

    def timeRanOut(self):
        '''
        Called by the universe when the upgrade's time has run out.
        '''
        pass

    def cancelOthers(self, others):
        '''
        Helper function to cancel other incompatible items.

        :param others: the Upgrade classes to cancel
        '''
        for upgradeClass in others:
            item = self.player.items.get(upgradeClass)
            if item:
                item.delete()


class TeamBoost(ShopItem):
    boost_code: bytes
    deposit_cost: int
    extra_cost: int
    time_limit: float

    def __init__(self, team):
        self.team = team
        self.world = team.world
        self.remaining_cost = self.extra_cost
        self.time_remaining = self.time_limit

    @classmethod
    def get_required_coins(cls, player) -> Optional[int]:
        if player.team is None:
            return None
        boost = player.team.boosts.get(cls)
        if boost is None:
            return cls.deposit_cost
        return boost.remaining_cost

    @property
    def activated(self):
        return self.remaining_cost <= 0

    @property
    def expired(self):
        return self.activated and self.time_remaining <= 0

    def dump(self):
        return {
            'code': self.boost_code,
            'cost': self.remaining_cost,
            'time': self.time_remaining,
        }

    @staticmethod
    def build_from_data(team, data):
        subclass = team_boost_by_code[data['code']]
        result = subclass.rebuild(team, data)
        return result

    @classmethod
    def rebuild(cls, team, data):
        result = cls(team)
        result.remaining_cost = data['cost']
        result.time_remaining = data['time']
        return result

    def tick(self):
        if self.activated:
            self.time_remaining = max(0, self.time_remaining - TICK_PERIOD)


class GunType(ShopItem):
    gun_code: bytes
    max_ammo: int
    shot_lifetime: float = 1
    full_cost: int
    action: str
    reload_time_factor: float = 1
    shot_speed: float = 600
    neutral_shots = False
    attribute_shots_to_shooter = True
    shot_rebound_radius = 3
    shot_damage_radius = 3
    shot_visual_radius = 3
    shots_flicker = False
    shot_health = 1
    shots_rebound = False
    shots_rebound_at_zone_boundary = False
    shots_hurt_players = True
    shots_affect_projectiles = False
    obstacles_pierced = 0
    can_hold_mouse = False

    def __init__(self, player):
        self.player = player
        self.world = player.world
        self.ammo = 0

    def dump(self):
        return {
            'code': self.gun_code,
            'ammo': self.ammo,
        }

    @staticmethod
    def build_from_data(player, data):
        subclass = gun_type_by_code[data['code']]
        result = subclass.rebuild(player, data)
        return result

    @classmethod
    def rebuild(cls, player, data):
        result = cls(player)
        result.ammo = data['ammo']
        return result

    @property
    def ammo_is_full(self):
        return self.ammo >= self.max_ammo

    def fill_local_ammo_clip(self):
        self.ammo = self.max_ammo

    def please_buy_ammo(self):
        # Call getPlayer() so that this works on local players too
        real_player = self.player.world.getPlayer(self.player.id)
        if real_player.agent is None:
            raise ValueError('please_buy_ammo() can only be called on a player you control')

        if self.ammo == 0:
            self.player.guns.set_local_selection(self)
        real_player.agent.sendRequest(BuyAmmoMsg.create(type(self), self.world.lastTickId))

    def please_shoot(self):
        # Call getPlayer() so that this works on local players too
        real_player = self.player.world.getPlayer(self.player.id)
        if real_player.agent is None:
            raise ValueError('please_shoot() can only be called on a player you control')

        if self.ammo <= 0 < self.max_ammo:
            real_player.guns.please_select(DefaultGun)
            return

        real_player.agent.sendRequest(ShootMsg.create(type(self), self.world.lastTickId))

    @classmethod
    def get_required_coins(cls, player) -> Optional[int]:
        gun = player.guns.get(cls)
        if gun.ammo_is_full or cls.full_cost is None:
            return None

        if gun.ammo == 0:
            return cls.full_cost

        # Buying ammo for a gun you already have only costs 85% the initial cost
        return math.ceil((1 - gun.ammo / cls.max_ammo) * 0.85 * cls.full_cost)

    @classmethod
    def build_trajectory(cls, player):
        '''
        If this gun should show a predicted trajectory, returns it,
        otherwise returns None.
        '''
        return None

    def get_reload_ratio_and_colour(self, colours):
        '''
        :return: (ratio, colour) if this gun type wants to override what
            is shown in the gun reload gauge, or None otherwise.
        '''
        return None

    def build_shoot_msg(self, local_id):
        shot_id = self.world.idManager.shots.make_id()
        if shot_id is None:
            return None
        return ShotFiredMsg(self.player.id, self.gun_code, shot_id, local_id)

    def was_fired(self):
        if self.max_ammo > 0:
            self.ammo -= 1

    def tick(self):
        pass

    def check_projectile_collision(self, shot, projectile):
        '''
        Should be implemented if shots_affect_projectiles is True.
        '''
        pass


@register_gun
class DefaultGun(GunType):
    name = 'Blaster'
    icon_path = 'gun-blaster.png'
    default_key = pygame.K_1
    sort_order = 0
    gun_code = b'd'
    max_ammo = 0
    full_cost = None
    action = 'blaster'


@registerUpgrade
class Shield(Upgrade):
    '''
    shield: protects player from one shot
    '''
    upgradeType = b's'
    requiredCoins = 500
    totalTimeLimit = 30
    name = 'Shield'
    action = 'shield'
    sort_order = 20
    default_panda3d_key = 'F1'
    default_key = pygame.K_F1
    icon_path = 'upgrade-shield.png'

    def __init__(self, player):
        super(Shield, self).__init__(player)
        self.maxProtections = self.world.physics.playerRespawnHealth
        self.protections = self.maxProtections

    def hit(self, hitpoints, hitter, hitKind):
        '''
        Called when this shield is hit for the given number of hitpoints.

        :return: zero if the hit was entirely absorbed by the shield,
            otherwise returns the remainder of the hit that was not absorbed.
        '''
        self.protections -= hitpoints
        if self.protections <= 0:
            result = -self.protections
            self.delete()

            self.player.onShieldDestroyed(hitter, hitKind)
            if self.player.isCanonicalPlayer() and hitter:
                hitter.onDestroyedShield(self.player, hitKind)
        else:
            result = 0
        return result


@specialUpgrade
class MinimapDisruption(Upgrade):
    upgradeType = b'm'
    requiredCoins = 1500
    totalTimeLimit = 20
    name = 'Minimap Disruption'
    action = 'minimap disruption'
    sort_order = 30
    default_panda3d_key = 'F4'
    default_key = pygame.K_F4
    icon_path = 'upgrade-minimap.png'


@registerUpgrade
class LaunchGrenade(Upgrade):
    upgradeType = b'g'
    requiredCoins = 450
    totalTimeLimit = 0
    name = 'Grenade'
    action = 'grenade'
    sort_order = 50
    default_panda3d_key = 'F3'
    default_key = pygame.K_F3
    icon_path = 'upgrade-grenade.png'
    doNotWaitForServer = True
    aggressive = True
    projectile_kind = GrenadeProjectile

    def localUse(self, localState):
        localState.grenadeLaunched()
        self.unverified = True

    def serverVerified(self, localState):
        super().serverVerified(localState)
        localState.matchGrenade()

    def deniedByServer(self, localState):
        super().deniedByServer(localState)
        localState.grenadeRemoved()

    def use(self):
        '''Initiate the upgrade.'''
        self.world.addGrenade(GrenadeShot(self.world, self.player))


@register_gun
class Ricochet(GunType):
    gun_code = b'r'
    full_cost = 150
    name = 'Ricochet'
    action = 'ricochet'
    sort_order = 60
    default_panda3d_key = '2'
    default_key = pygame.K_2
    icon_path = 'gun-ricochet.png'
    max_ammo = 25
    shots_rebound = True

    @classmethod
    def build_trajectory(cls, player):
        return PredictedRicochetTrajectory(player.world, player)


@registerUpgrade
class Ninja (Upgrade):
    '''allows you to become invisible to all players on the opposing team'''
    upgradeType = b'n'
    requiredCoins = 325
    totalTimeLimit = 25
    name = 'Ninja'
    action = 'phase shift'  # So old phase shift hotkeys trigger ninja.
    sort_order = 40
    default_panda3d_key = 'F2'
    default_key = pygame.K_F2
    icon_path = 'upgrade-ninja.png'

    @classmethod
    def getActivateNotification(cls, nick):
        return '{} has become a {}'.format(nick, cls.name)


@register_gun
class Shoxwave(GunType):
    '''
    shockwave: upgrade that will replace shots with a shockwave like that of
    the grenade vaporising all enemies and enemy shots in the radius of blast.
    '''
    gun_code = b'w'
    full_cost = 250
    name = 'Shoxwave'
    action = 'shoxwave'
    sort_order = 80
    default_panda3d_key = '3'
    default_key = pygame.K_3
    icon_path = 'gun-shoxwave.png'
    max_ammo = 20
    reload_time_factor = 1 / 0.7

    def build_shoot_msg(self, local_id):
        xpos, ypos = self.player.pos
        return FireShoxwaveMsg(self.player.id, xpos, ypos)


@register_gun
class MachineGun(GunType):
    gun_code = b'x'
    full_cost = 500
    name = 'Machine Gun'
    action = 'turret'   # So that old turret hotkeys trigger machine gun.
    sort_order = 10
    default_panda3d_key = '4'
    default_key = pygame.K_4
    icon_path = 'gun-machinegun.png'
    max_ammo = 65
    can_hold_mouse = True

    firing_reload_time = 0.1
    standard_cooling_factor = 0.7
    reload_rate = 8
    BULLETS_BEFORE_OVERHEATING = 16

    def __init__(self, *args, **kwargs):
        super(MachineGun, self).__init__(*args, **kwargs)
        self.overheat_ratio = 0
        self.overheated = False

    def dump(self):
        result = super().dump()
        result['heat'] = self.overheat_ratio
        result['overheated'] = self.overheated
        return result

    @classmethod
    def rebuild(cls, player, data):
        result = super().rebuild(player, data)
        result.overheat_ratio = data['heat']
        result.overheated = data['overheated']
        return result

    def was_fired(self):
        super().was_fired()

        reload_time = self.reload_rate * self.player.guns.standard_reload_time
        self.overheat_ratio += 1 / self.BULLETS_BEFORE_OVERHEATING
        self.overheat_ratio += self.firing_reload_time * self.standard_cooling_factor / reload_time

        if self.overheat_ratio > 1:
            self.overheat_ratio = 0
            self.overheated = True
        else:
            reload_time = self.firing_reload_time
        self.player.guns.reload_time = self.player.guns.reload_from = reload_time

    def tick(self):
        self.cool_one_frame()

    def cool_one_frame(self):
        normal_reload_amount = self.world.tickPeriod / self.player.guns.standard_reload_time
        reload_amount = normal_reload_amount / self.reload_rate
        if not self.overheated:
            reload_amount *= self.standard_cooling_factor
        self.overheat_ratio = max(0, self.overheat_ratio - reload_amount)
        if self.overheated and self.player.guns.reload_time <= 0:
            self.overheated = False

    def get_reload_ratio_and_colour(self, colours):
        if not self.overheated:
            return (1 - self.overheat_ratio, colours.gaugeGood)
        return None


@registerUpgrade
class Bomber(Upgrade):
    upgradeType = b'b'
    requiredCoins = 50
    totalTimeLimit = 6
    name = 'Bomber'
    action = 'bomber'
    sort_order = 90
    default_panda3d_key = 'F9'
    default_key = pygame.K_F9
    icon_path = 'upgrade-bomber.png'
    applyLocally = True

    def __init__(self, *args, **kwargs):
        super(Bomber, self).__init__(*args, **kwargs)
        self.firstUse = True

    def timeRanOut(self):
        self.cancelOthers([Shield])

        if self.player.isCanonicalPlayer():
            self.world.bomberExploded(self.player)

    def getReactivateCost(self):
        return 0

    def use(self):
        if self.firstUse:
            self.firstUse = False
        else:
            # Hitting "use" a second time cancels bomber
            self.delete()


@specialUpgrade
class RespawnFreezer(Upgrade):
    '''
    Respawn freezer: upgrade that will render spawn points unusable.
    '''
    upgradeType = b'f'
    requiredCoins = 400
    totalTimeLimit = 30
    name = 'Respawn Freezer'
    action = 'respawn freezer'
    sort_order = 100
    default_panda3d_key = '9'
    default_key = pygame.K_9

    def use(self):
        '''Initiate the upgrade'''
        self.zone = self.player.getZone()
        self.zone.frozen = True

    def dump(self):
        result = super().dump()
        result['zone'] = self.zone.id
        return result

    @classmethod
    def restore(cls, player, data):
        result = super().restore(player, data)
        result.zone = player.world.getZone(data['zone'])
        return result

    def delete(self):
        '''Performs any necessary tasks to remove this upgrade from the game'''
        super(RespawnFreezer, self).delete()
        if self.zone:
            self.zone.frozen = False


@registerUpgrade
class LaunchMine(Upgrade):
    upgradeType = b'o'
    requiredCoins = 150
    totalTimeLimit = 0
    name = 'Mine'
    action = 'mine'
    sort_order = 130
    default_panda3d_key = 'F5'
    default_key = pygame.K_F5
    icon_path = 'upgrade-mine.png'
    doNotWaitForServer = True
    aggressive = True
    projectile_kind = MineProjectile

    local_projectile = None

    def localUse(self, local_state):
        self.local_projectile = LocalMine(local_state, self.world, player=self.player)
        self.unverified = True
        local_state.projectiles.add(self.local_projectile)

    def deniedByServer(self, localState):
        super().deniedByServer(localState)
        localState.projectiles.denied(self.local_projectile)

    def serverVerified(self, localState):
        super().serverVerified(localState)
        localState.projectiles.match(self.local_projectile)

    @classmethod
    def upgrade_approved_server_side(cls, game, agent, player):
        projectile_id = game.idManager.projectiles.make_id()
        game.sendServerCommand(MineLaunchedMsg(player.id, projectile_id))


@register_gun
class DetonationBeam(GunType):
    gun_code = b'b'
    full_cost = LaunchMine.requiredCoins
    name = 'Detonation Beam'
    action = 'detonation-beam'
    sort_order = 100
    default_panda3d_key = '9'
    default_key = pygame.K_9
    icon_path = 'gun-detonationbeam.png'
    max_ammo = round(6 / TICK_PERIOD)       # 6 seconds of continuous firing
    can_hold_mouse = True
    shot_lifetime = TICK_PERIOD
    shot_speed = DefaultGun.shot_speed * DefaultGun.shot_lifetime / shot_lifetime
    shot_visual_radius = 1
    shots_flicker = True
    shots_hurt_players = False
    shots_affect_projectiles = True

    def was_fired(self):
        super().was_fired()
        self.player.guns.reload_time = self.player.guns.reload_from = TICK_PERIOD

    def check_projectile_collision(self, shot, projectile):
        if not projectile.triggered_by_detonation_beam:
            return False
        return shot.checkCollisionsWithPoints(projectile.oldPos, projectile.pos)


@register_gun
class Piercing(GunType):
    gun_code = b'p'
    full_cost = 250
    name = 'Piercing'
    action = 'piercing'
    sort_order = 110
    default_panda3d_key = '5'
    default_key = pygame.K_5
    icon_path = 'gun-piercing.png'
    max_ammo = 20
    shot_lifetime = 2.5
    shot_health = 50
    obstacles_pierced = 1


@register_gun
class MeanderingMenace(GunType):
    gun_code = b'z'
    full_cost = 150
    name = 'Meandering Menace'
    action = 'menace'
    sort_order = 70
    default_panda3d_key = '7'
    default_key = pygame.K_7
    icon_path = 'gun-menace.png'
    max_ammo = 4
    shot_lifetime = 20
    neutral_shots = True
    attribute_shots_to_shooter = False
    shot_visual_radius = 25
    shot_damage_radius = 25
    shot_health = 4
    shots_rebound = True
    shots_rebound_at_zone_boundary = True


@register_gun
class Railgun(GunType):
    gun_code = b'i'
    full_cost = 250
    name = 'Railgun'
    action = 'railgun'
    sort_order = 120
    default_panda3d_key = '6'
    default_key = pygame.K_6
    icon_path = 'gun-railgun.png'
    max_ammo = 5
    reload_time_factor = 4
    shot_lifetime = TICK_PERIOD
    shot_speed = DefaultGun.shot_speed * 2 * DefaultGun.shot_lifetime / shot_lifetime


team_boosts = sorted(team_boost_by_code.values(), key=lambda b: (b.sort_order, b.boost_code))
gun_types = sorted(gun_type_by_code.values(), key=lambda g: (g.sort_order, g.gun_code))
