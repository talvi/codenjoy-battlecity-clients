from enum import Enum


class BattlecityAction(Enum):
  GO_LEFT = 'left'
  GO_RIGHT = 'right'
  GO_UP = 'up'
  GO_DOWN = 'down'
  BULLET_RIGHT = 'act,right'
  BULLET_LEFT = 'act,left'
  BULLET_UP = 'act,up'
  BULLET_DOWN = 'act,down'
  DO_NOTHING = ''
