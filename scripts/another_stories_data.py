from another_stories_jan import JAN
from another_stories_feb import FEB
from another_stories_mar import MAR
from another_stories_apr import APR
from another_stories_may import MAY
from another_stories_jun import STORIES_JUN
from another_stories_jul import STORIES_JUL
from another_stories_aug import STORIES_AUG
from another_stories_sep import STORIES_SEP
from another_stories_oct import STORIES_OCT
from another_stories_nov import STORIES_NOV
from another_stories_dec import STORIES_DEC


def _normalize(stories):
    """Convert month/day int format to date-string format if needed."""
    result = []
    for s in stories:
        if "date" not in s:
            s = dict(s, date=f"{s['month']:02d}-{s['day']:02d}")
        result.append(s)
    return result


STORIES = (
    JAN + FEB + MAR + APR + MAY
    + _normalize(STORIES_JUN)
    + _normalize(STORIES_JUL)
    + _normalize(STORIES_AUG)
    + _normalize(STORIES_SEP)
    + _normalize(STORIES_OCT)
    + _normalize(STORIES_NOV)
    + _normalize(STORIES_DEC)
)
