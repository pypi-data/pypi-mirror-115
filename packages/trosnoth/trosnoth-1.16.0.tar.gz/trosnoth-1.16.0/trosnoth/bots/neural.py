import pathlib
import random

import numpy as np
import tensorflow as tf
from tensorflow import keras

from trosnoth.bots.goalsetter import GoalSetterBot, Goal, RespawnNearZone


HERE = pathlib.Path(__file__).parent
SAVED_MODEL = HERE / 'neural'


class TopGoal(Goal):
    def __init__(self, bot, parent):
        super().__init__(bot, parent)
        self.next_check = None

    def start(self):
        self.schedule_next_check()

    def schedule_next_check(self):
        self.cancel_next_check()
        delay = 1.5 + random.random()
        self.next_check = self.bot.world.callLater(delay, self.reevaluate)

    def cancel_next_check(self):
        if self.next_check:
            self.next_check.cancel()
            self.next_check = None

    def reevaluate(self):
        self.cancel_next_check()

        player = self.bot.player
        if player.dead:
            zone = player.getZone()
            if zone is None:
                zone = random.choice(list(self.bot.world.zones))
            self.setSubGoal(RespawnNearZone(self.bot, self, zone))
            return

        self.setSubGoal(AvoidDyingGoal(self.bot, self))


class AvoidDyingGoal(Goal):
    def __init__(self, bot, parent):
        super().__init__(bot, parent)

    def start(self):
        self.bot.onTick.addListener(self.tick)
        super().start()

    def stop(self):
        super().stop()
        self.bot.onTick.removeListener(self.tick)

    def tick(self):
        if self.bot.player.dead:
            self.returnToParent()
            return
        # TODO: feed 5 closest enemy shots into model and interpret output
        ...


class NeuralBot(GoalSetterBot):
    nick = 'NeuralBot'
    generic = True

    MainGoalClass = TopGoal


def make_model():
    inputs = keras.Input(shape=(10,), dtype='float64')
    hidden = keras.layers.Dense(12, activation='relu')(inputs)
    outputs = keras.layers.Dense(2, activation='sigmoid')(hidden)
    return keras.Model(inputs=inputs, outputs=outputs)


if SAVED_MODEL.is_file():
    model = keras.models.load_model(SAVED_MODEL)
else:
    model = make_model()


BotClass = NeuralBot