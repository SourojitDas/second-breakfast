from enum import Enum

MIN_SCORE=0
MAX_SCORE=100
SHORT_TERM_OFFSET=1
LONG_TERM_OFFSET=0.1
SLOW_FADE_OFFSET=0.01
QUICK_FADE_OFFSET=0.1
BLOCKAGE_PENALTY=-100

class Actions(Enum):
  LIKE = 1
  DISLIKE = 2
  NOT_INTERESTED = 3

def get_new_value_for_attribute (action, currentAttributeValue, offset):
  reward = 0
  penalty = 0
  if (action == Actions.LIKE):
    if (currentAttributeValue == BLOCKAGE_PENALTY):
      return MIN_SCORE
    new_reward = +offset
    new_penalty = 0
  elif (action == Actions.DISLIKE):
    new_reward = 0
    new_penalty = -offset
  elif (action == Actions.NOT_INTERESTED):
    new_reward = 0
    new_penalty = BLOCKAGE_PENALTY
  newAttributeValue = currentAttributeValue + new_reward + new_penalty

  if (newAttributeValue>MAX_SCORE):
    return MAX_SCORE
  else:
    return newAttributeValue

def get_new_value_for_short_term_attribute (action, currentAttributeValue):
  return get_new_value_for_attribute(action, currentAttributeValue, SHORT_TERM_OFFSET)

def get_new_value_for_long_term_attribute (action, currentAttributeValue):
  return get_new_value_for_attribute(action, currentAttributeValue, LONG_TERM_OFFSET)