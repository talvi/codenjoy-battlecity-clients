from battlecityclient.BattleCityClient import GameClient
import random
import logging

from battlecityclient.internals.actions import BattlecityAction
from battlecityclient.internals.board import Board

logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',
                    level=logging.INFO)

def turn(gcb: Board):
    action_id = random.randint(0, len(BattlecityAction)-1)
    return list(BattlecityAction)[action_id]

def main():
    gcb = GameClient("https://dojorena.io/codenjoy-contest/board/player/0?code=000000000000&gameName=battlecity")
    gcb.run(turn)
