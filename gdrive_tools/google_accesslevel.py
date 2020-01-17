from enum import Enum

class GoogleAccessLevel(Enum):
  WRITE='writer'
  COMMENT='commenter'
  READ='reader'
