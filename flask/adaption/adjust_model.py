from enum import Enum

MIN_SCORE=0
MAX_SCORE=100
SHORT_TERM_OFFSET=1
LONG_TERM_OFFSET=0.1
SLOW_FADE_OFFSET=0.01
QUICK_FADE_OFFSET=0.1
BLOCKAGE_PENALTY=-100
FADE_LIMIT=1

class Actions(Enum):
  LIKE = "like"
  DISLIKE = "dislike"
  NOT_INTERESTED = "not_interested"

def get_new_value_for_attribute (action, currentAttributeValue, offset):
  reward = 0
  penalty = 0
  if (action == Actions.LIKE.value):
    if (currentAttributeValue < MIN_SCORE):
      return MIN_SCORE
    reward = +offset
    penalty = 0
  elif (action == Actions.DISLIKE.value):
    if (currentAttributeValue == MIN_SCORE):
      return MIN_SCORE
    reward = 0
    penalty = -offset
  elif (action == Actions.NOT_INTERESTED.value):
    reward = 0
    penalty = BLOCKAGE_PENALTY
  newAttributeValue = currentAttributeValue + reward + penalty

  if (newAttributeValue>MAX_SCORE):
    return MAX_SCORE
  else:
    return newAttributeValue

def get_faded_value_for_attribute (currentAttributeValue, offset):
  if (currentAttributeValue == FADE_LIMIT):
    return currentAttributeValue

  penalty = -offset
  newAttributeValue = currentAttributeValue + penalty
  return newAttributeValue

def get_new_value_for_short_term_attribute (action, currentAttributeValue):
  return get_new_value_for_attribute(action, currentAttributeValue, SHORT_TERM_OFFSET)

def get_new_value_for_long_term_attribute (action, currentAttributeValue):
  return get_new_value_for_attribute(action, currentAttributeValue, LONG_TERM_OFFSET)

def get_faded_value_for_short_term_attribute (currentAttributeValue):
  return get_faded_value_for_attribute(currentAttributeValue, QUICK_FADE_OFFSET)

def get_faded_value_for_long_term_attribute (currentAttributeValue):
  return get_faded_value_for_attribute(currentAttributeValue, SLOW_FADE_OFFSET)
