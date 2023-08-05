import logging
import random
from typing import Optional

import pygame

from trosnoth.const import (
    MAP_TO_SCREEN_SCALE,
    ACTION_SETTINGS_MENU, ACTION_QUIT_MENU,
    ACTION_REALLY_QUIT, ACTION_JOIN_GAME, ACTION_PAUSE_GAME, ACTION_MAIN_MENU,
    ACTION_TERMINAL_TOGGLE, ACTION_FOLLOW, ACTION_RADIAL_UPGRADE_MENU, ACTION_USE_UPGRADE, ACTION_RESPAWN,
    ACTION_READY, ACTION_CLEAR_UPGRADE, ACTION_CHAT,
    ACTION_JUMP, ACTION_RIGHT, ACTION_LEFT, ACTION_DOWN,
    ACTION_HOOK, ACTION_SHOW_TRAJECTORY, ACTION_DEBUGKEY, ACTION_EMOTE,
    MAX_EMOTE, ACTION_NEXT_WEAPON, ACTION_PREVIOUS_WEAPON, ACTION_BUY_AMMO,
)
from trosnoth.gui.framework import framework
from trosnoth.gui.framework.elements import TextElement, PictureElement, SolidRect
from trosnoth.gui.common import (
    Location, FullScreenAttachedPoint, ScaledSize, Area, CanvasX, Screen,
    RelativePoint, Region, Abs,
)
from trosnoth.messages import (
    BuyUpgradeMsg, RespawnRequestMsg, EmoteRequestMsg,
    PlayerIsReadyMsg, ThrowTrosballMsg,
)
from trosnoth.model.player import Player
from trosnoth.model.shot import (
    PredictedGhostShotTrajectory,
)
from trosnoth.model.trosball import PredictedTrosballTrajectory
from trosnoth.model.unit import PredictedTrajectory, PredictedProjectileTrajectory
from trosnoth.model.upgrades import allUpgrades, gun_types
from trosnoth.trosnothgui.ingame.messagebank import MessageBank
from trosnoth.trosnothgui.ingame import mainMenu
from trosnoth.trosnothgui.ingame.gamevote import GameVoteMenu
from trosnoth.trosnothgui.ingame.gauges import (
    RespawnGauge, SingleUpgradeGauge, GunGauge, ItemCoinGauge, SingleAmmoGauge,
)
from trosnoth.trosnothgui.ingame.achievementBox import AchievementBox
from trosnoth.trosnothgui.ingame.chatBox import ChatBox
from trosnoth.trosnothgui.ingame.utils import mapPosToScreen

from trosnoth.trosnothgui.ingame.upgradeinterface import RadialUpgradeMenu
from trosnoth.utils.aio import create_safe_task
from trosnoth.welcome.keygrab import hidden_qt_toplevels, KeyGrabberElement

log = logging.getLogger(__name__)


class DetailsInterface(framework.CompoundElement):
    '''Interface containing all the overlays onto the screen:
    chat messages, player lists, gauges, coins, etc.'''
    def __init__(self, app, gameInterface):
        super(DetailsInterface, self).__init__(app)
        self.gameInterface = gameInterface
        self.settings_screen_task = None
        self.settings_screen = None

        # Maximum number of messages viewable at any one time
        maxView = 8

        self.world = gameInterface.world
        self.player = None
        font = app.screenManager.fonts.messageFont
        self.currentMessages = MessageBank(self.app, maxView, 50,
                Location(FullScreenAttachedPoint(ScaledSize(-40,-40),
                'bottomright'), 'bottomright'), 'right', 'bottom', font)

        # If we want to keep a record of all messages and their senders
        self.input = None
        self.inputText = None
        self.unobtrusiveGetter = None
        self.reloadGauge = GunGauge(self.app, Area(
                FullScreenAttachedPoint(ScaledSize(0,-60), 'midbottom'),
                ScaledSize(100,30), 'midbottom'))
        self.respawn_gauge = None
        self._update_respawn_gauge()
        self.itemGauge = ItemGauge(self.app, self.player)
        self.gun_gauge = AllGunsGauge(self.app, self.player)
        self.achievementBox = None
        self.currentUpgrade = None

        self.chatBox = ChatBox(app, self.world, self.gameInterface)

        menuloc = Location(FullScreenAttachedPoint((0,0), 'bottomleft'),
                'bottomleft')
        self.menuManager = mainMenu.MainMenu(self.app, menuloc, self,
                self.gameInterface.keyMapping)
        self.upgradeDisplay = UpgradeDisplay(app)
        self.trajectoryOverlay = TrajectoryOverlay(app, gameInterface.gameViewer.viewManager, self.upgradeDisplay)
        self.radialUpgradeMenu = RadialUpgradeMenu(app, self.player, self._setCurrentUpgrade)
        self.radialUpgradeMenu.start()
        self.gameVoteMenu = GameVoteMenu(app, self.world, on_change=self._castGameVote)
        self._gameVoteUpdateCounter = 0
        self.elements = [
            self.currentMessages, self.upgradeDisplay, self.reloadGauge, self.respawn_gauge,
            self.gameVoteMenu, self.chatBox,
            self.trajectoryOverlay, self.menuManager, self.itemGauge, self.gun_gauge,
            self.radialUpgradeMenu,
        ]

        self.upgradeMap = dict((upgradeClass.action, upgradeClass) for
                upgradeClass in allUpgrades)
        self.gun_map = {gun_type.action: gun_type for gun_type in gun_types}

    def stop(self):
        if self.achievementBox:
            self.achievementBox.stop()
        self.radialUpgradeMenu.stop()

    def sendRequest(self, msg):
        return self.gameInterface.sendRequest(msg)

    def tick(self, deltaT):
        super(DetailsInterface, self).tick(deltaT)

        self._updateGameVoteMenu()

        if self.player is None:
            return

        self._updateAchievementBox()

    def _castGameVote(self, msg):
        self.sendRequest(msg)

    def _updateGameVoteMenu(self):
        show_vote_menu = self.world.uiOptions.showReadyStates and self.player is not None
        self.gameVoteMenu.set_active(show_vote_menu)
        self.gameInterface.gameInfoDisplay.set_active(not show_vote_menu)

        if show_vote_menu:
            if self._gameVoteUpdateCounter <= 0:
                self.gameVoteMenu.update(self.player)
                self._gameVoteUpdateCounter = 25
            else:
                self._gameVoteUpdateCounter -= 1

    def localAchievement(self, achievementId):
        if self.achievementBox is None:
            self.achievementBox = AchievementBox(self.app, self.player,
                                                 achievementId)
            self.elements.append(self.achievementBox)
        else:
            self.achievementBox.addAchievement(achievementId)

    def _updateAchievementBox(self):
        if (self.achievementBox is not None and
                len(self.achievementBox.achievements) == 0):
            self.elements.remove(self.achievementBox)
            self.achievementBox = None

    def _update_respawn_gauge(self):
        if self.respawn_gauge is not None:
            self.elements.remove(self.respawn_gauge)
        self.respawn_gauge = RespawnGauge(
            self.app,
            Area(
                FullScreenAttachedPoint(ScaledSize(0, -60), 'midbottom'),
                ScaledSize(100, 30),
                'midbottom'),
            self.player,
            self.world)
        self.elements.append(self.respawn_gauge)

    def setPlayer(self, player):
        if self.player is not None:
            self.player.onPrivateChatReceived.removeListener(self.privateChat)

        self.player = player
        if player:
            self.player.onPrivateChatReceived.addListener(self.privateChat)

        self.reloadGauge.player = player
        self._update_respawn_gauge()
        self.upgradeDisplay.setUpgrade(self.currentUpgrade, self.player)
        self.itemGauge.set_player(player)
        self.gun_gauge.set_player(player)
        self.radialUpgradeMenu.set_player(player)

    def show_settings(self):
        from trosnoth.welcome.settings import SettingsScreen
        if self.settings_screen_task and not self.settings_screen_task.done():
            self.settings_screen.raise_to_top()
            return
        self.settings_screen = SettingsScreen(self.grab_hotkey)
        self.settings_screen_task = create_safe_task(self._show_settings_then_update_key_map())

    async def _show_settings_then_update_key_map(self):
        try:
            await self.settings_screen.run()
        finally:
            self.gameInterface.updateKeyMapping()

    async def grab_hotkey(self, parent_window, prompt, title=None):
        with hidden_qt_toplevels():
            return await KeyGrabberElement(self.app, prompt).show()

    def _setCurrentUpgrade(self, upgradeType):
        self.currentUpgrade = upgradeType
        self.upgradeDisplay.setUpgrade(self.currentUpgrade, self.player)
        self.menuManager.manager.reset()

    def _requestUpgrade(self):
        if self.player.hasTrosball():
            self.sendRequest(ThrowTrosballMsg(self.getTickId()))
        elif self.currentUpgrade is not None and self.currentUpgrade.pre_buy_check(self.player):
            self.sendRequest(BuyUpgradeMsg(
                self.currentUpgrade.upgradeType, self.getTickId()))

    def getTickId(self):
        return self.world.lastTickId

    def doAction(self, action):
        '''
        Activated by hotkey or menu.
        action corresponds to the action name in the keyMapping.
        '''
        if action == ACTION_SETTINGS_MENU:
            self.show_settings()
        elif action == ACTION_QUIT_MENU:
            self.menuManager.showQuitMenu()
        elif action == ACTION_REALLY_QUIT:
            # Disconnect from the server.
            self.gameInterface.disconnect()
        elif action == ACTION_JOIN_GAME:
            # Join if currently spectating
            self.gameInterface.spectatorWantsToJoin()
        elif action == ACTION_PAUSE_GAME:
            if self.world.isServer:
                self.world.pauseOrResumeGame()
                if self.world.paused:
                    self.newMessage('Game paused')
                else:
                    self.newMessage('Game resumed')
            else:
                self.newMessage(
                    'You can only pause games from the server', error=True)
        elif action == ACTION_MAIN_MENU:
            # Return to main menu and show or hide the menu.
            self.menuManager.escape()
        elif action == ACTION_TERMINAL_TOGGLE:
            self.gameInterface.toggleTerminal()
        elif self.gameInterface.is_spectating():
            # Replay-specific actions
            if action in (ACTION_FOLLOW, ACTION_USE_UPGRADE):
                # Follow the game action
                self.gameInterface.gameViewer.setTarget(None)
        else:
            # All actions after this line should require a player.
            if self.player is None:
                return

            paused = self.world.uiOptions.showPauseMessage
            if action == ACTION_RESPAWN:
                if not paused:
                    self.sendRequest(
                        RespawnRequestMsg(tickId=self.getTickId()))
            elif action == ACTION_READY:
                if self.player.readyToStart:
                    self._castGameVote(PlayerIsReadyMsg(self.player.id, False))
                else:
                    self._castGameVote(PlayerIsReadyMsg(self.player.id, True))
            elif action in self.upgradeMap:
                self._setCurrentUpgrade(self.upgradeMap[action])
            elif action == ACTION_CLEAR_UPGRADE:
                self._setCurrentUpgrade(None)
                self.menuManager.manager.reset()
            elif action in self.gun_map:
                gun = self.player.guns.get(self.gun_map[action])
                cost = gun.get_required_coins(self.player)
                if gun.ammo > 0 or gun.max_ammo == 0 or (
                        cost is not None and self.player.coins >= cost):
                    self.player.guns.please_select(gun)
            elif action == ACTION_CHAT:
                self.chat()
                self.menuManager.manager.reset()
            elif action == ACTION_USE_UPGRADE:
                if not paused:
                    self._requestUpgrade()
            elif action == ACTION_BUY_AMMO:
                self.player.current_gun.please_buy_ammo()
            elif action == ACTION_EMOTE:
                self.sendRequest(
                    EmoteRequestMsg(
                        tickId=self.getTickId(),
                        emoteId=random.randrange(MAX_EMOTE + 1)))
            elif action == ACTION_RADIAL_UPGRADE_MENU:
                self.radialUpgradeMenu.toggle()
            elif action == ACTION_NEXT_WEAPON:
                self.player.guns.scroll_selection(1)
            elif action == ACTION_PREVIOUS_WEAPON:
                self.player.guns.scroll_selection(-1)
            elif action not in (
                    ACTION_JUMP, ACTION_RIGHT, ACTION_LEFT, ACTION_DOWN,
                    ACTION_HOOK, ACTION_SHOW_TRAJECTORY, ACTION_DEBUGKEY):
                log.warning('Unknown action: %r', action)

    def newMessage(self, text, colour=None, error=False):
        if colour is None:
            if error:
                colour = self.app.theme.colours.errorMessageColour
            else:
                colour = self.app.theme.colours.grey
        self.currentMessages.newMessage(text, colour)

    def privateChat(self, text, sender):
        # Destined for the one player
        text = " (private): " + text
        self.newChat(text, sender)

    def newChat(self, text, sender: Optional[Player]):
        if sender is None:
            self.chatBox.newServerMessage(text)
        else:
            colour = sender.team.shade(0.5, 1) if sender.team else (192, 192, 192)
            self.chatBox.newMessage(text, sender.nick, colour)

    def endInput(self):
        if self.input:
            self.elements.remove(self.input)
            self.input = None
        if self.inputText:
            self.elements.remove(self.inputText)
            self.inputText = None
        if self.unobtrusiveGetter:
            self.elements.remove(self.unobtrusiveGetter)
            self.unobtrusiveGetter = None
        if self.menuManager not in self.elements:
            self.elements.append(self.menuManager)
        self.input = self.inputText = None


    def inputStarted(self):
        self.elements.append(self.input)
        self.elements.append(self.inputText)
        self.input.onEsc.addListener(lambda sender: self.endInput())
        self.input.onEnter.addListener(lambda sender: self.endInput())

        try:
            self.elements.remove(self.menuManager)
        except ValueError:
            pass

    def chat(self):
        if not self.player:
            return

        if self.chatBox.isOpen():
            self.chatBox.close()
        else:
            pygame.key.set_repeat(300, 30)
            self.chatBox.open()
            self.chatBox.setPlayer(self.player)

    def upgradeUsed(self, player, upgradeCode):
        upgradeClass = player.world.getUpgradeType(upgradeCode)
        message = upgradeClass.getActivateNotification(player.nick)

        self.newMessage(message)


class MultiGauge(framework.CompoundElement):
    '''
    Keeps track of currently active items.
    '''

    def __init__(self, app):
        super().__init__(app)
        self.elements = []
        self.modification_key = None

    def tick(self, delta_t):
        key = self.get_modification_key()
        if key != self.modification_key:
            self.modification_key = key
            self.rebuild_gauges()
        super().tick(delta_t)

    def get_modification_key(self):
        raise NotImplementedError

    def rebuild_gauges(self):
        raise NotImplementedError

    def gauge_areas(self, items, y):
        items = list(items)
        x_offset = 80
        x = -0.5 * (len(items) - 1) * x_offset

        for item in items:
            area = Area(
                FullScreenAttachedPoint(ScaledSize(x, y), 'midbottom'),
                ScaledSize(40, 10), 'midbottom')

            yield area, item
            x += x_offset


class ItemGauge(MultiGauge):
    def __init__(self, app, player):
        super().__init__(app)
        self.player = player

    def set_player(self, player):
        self.player = player

    def get_modification_key(self):
        return self.get_items()

    def get_items(self):
        if self.player is None:
            return []
        return sorted(self.player.items.getAll(), key=lambda i: (i.sort_order, i.upgradeType))

    def rebuild_gauges(self):
        self.elements = []
        for area, item in self.gauge_areas(self.get_items(), y=-40):
            self.elements.append(SingleUpgradeGauge(self.app, area, item))


class AllGunsGauge(MultiGauge):
    def __init__(self, app, player):
        super().__init__(app)
        self.player = player

    def set_player(self, player):
        self.player = player

    def get_modification_key(self):
        if self.player is None:
            return ()
        return (list(self.player.guns), self.player.current_gun)

    def rebuild_gauges(self):
        self.elements = []
        if self.player is None:
            return
        for area, gun in self.gauge_areas(self.player.guns, y=-10):
            gauge = SingleAmmoGauge(
                self.app, area,
                gun=gun,
                draw_panel=self.player.current_gun == gun,
            )
            self.elements.append(gauge)


class UpgradeDisplay(framework.CompoundElement):

    def __init__(self, app):
        super(UpgradeDisplay, self).__init__(app)
        self.player = None
        self.upgrade = None
        self.coinsText = TextElement(
            self.app, '', self.app.screenManager.fonts.coinsDisplayFont,
            Location(Screen(0.65, 0.01), 'midtop'),
            self.app.theme.colours.coinsDisplayColour,
            shadow=True)
        self.elements = [self.coinsText]

    def refresh(self):
        self.setUpgrade(self.upgrade, self.player)

    def tick(self, deltaT):
        super(UpgradeDisplay, self).tick(deltaT)
        if self.player:
            self.coinsText.setText('${}'.format(self.player.coins))
        else:
            self.coinsText.setText('')

    def setUpgrade(self, upgradeType, player):
        self.player = player
        self.upgrade = upgradeType
        if player is None or upgradeType is None:
            self.elements = [self.coinsText]
        else:
            pos = Location(Screen(0.6, 0), 'midtop')
            image = upgradeType.get_icon(self.app.theme.sprites)
            area = Area(
                RelativePoint(Screen(0.6, 0), (0, 52)),
                ScaledSize(50, 10), 'midtop')
            self.elements = [
                SolidRect(self.app, (192, 128, 128), 192, Region(
                    midtop=Screen(0.6, 0),
                    size=Abs(70, 70),
                )),
                PictureElement(self.app, image, pos),
                self.coinsText,
            ]

            if upgradeType.enabled:
                self.elements.append(
                    ItemCoinGauge(self.app, area, player, upgradeType))
            else:
                self.elements.append(
                    TextElement(self.app, 'DISABLED',
                        self.app.screenManager.fonts.ingameMenuFont,
                        Location(CanvasX(620, 68), 'midbottom'),
                        self.app.theme.colours.errorMessageColour))


class TrajectoryOverlay(framework.Element):
    def __init__(self, app, viewManager, upgradeDisplay):
        super(TrajectoryOverlay, self).__init__(app)
        self.viewManager = viewManager
        self.upgradeDisplay = upgradeDisplay
        self.enabled = False

    def setEnabled(self, enable):
        self.enabled = enable

    def isActive(self):
        return self.getTrajectory() is not None

    def getTrajectory(self) -> Optional[PredictedTrajectory]:
        if not self.enabled:
            return None

        player = self.viewManager.getTargetPlayer()
        if player.dead:
            if not player.inRespawnableZone():
                return None
            return PredictedGhostShotTrajectory(
                player.world, player, self.viewManager)

        if player.hasTrosball():
            return PredictedTrosballTrajectory(player.world, player)

        selected_upgrade = self.upgradeDisplay.upgrade
        if selected_upgrade and selected_upgrade.projectile_kind:
            if player.coins >= selected_upgrade.requiredCoins:
                return PredictedProjectileTrajectory(player, selected_upgrade.projectile_kind)

        return player.current_gun.build_trajectory(player)

    def draw(self, surface):
        trajectory = self.getTrajectory()
        if trajectory is None:
            return

        focus = self.viewManager._focus
        area = self.viewManager.sRect

        points = list(trajectory.predictedTrajectoryPoints())
        numPoints = len(points)
        if numPoints == 0:
            return
        greenToYellow = [(i, 255, 0) for i in range(
            0, 255, 255 // (numPoints // 2 + numPoints % 2))]
        yellowToRed = [(255, i, 0) for i in range(
            255, 0, -255 // (numPoints // 2))]

        colours = [(0, 255, 0)] + greenToYellow + yellowToRed

        lastPoint = None
        for item in zip(points, colours):
            point = item[0]
            colour = item[1]
            # Set first point
            if lastPoint is None:
                lastPoint = point
                adjustedPoint = mapPosToScreen(point, focus, area)
                pygame.draw.circle(surface, colour, adjustedPoint, 2)
                continue


            adjustedPoint = mapPosToScreen(point, focus, area)
            adjustedLastPoint = mapPosToScreen(lastPoint, focus, area)

            pygame.draw.line(surface, colour, adjustedLastPoint, adjustedPoint, 5)

            lastPoint = point

        pygame.draw.circle(surface, colour, adjustedPoint, 2)

        radius = int(trajectory.explosionRadius() * MAP_TO_SCREEN_SCALE)
        if radius > 0:
            pygame.draw.circle(surface, (0,0,0), adjustedPoint, radius, 2)
