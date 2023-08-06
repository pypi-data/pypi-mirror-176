from enum import Enum, auto
import random as rnd
from typing import Tuple

class CoopEnum(Enum):

    @classmethod
    def has_name(cls, name):
        return name in cls._member_names_

    @classmethod
    def has_value(cls, value):
        return value in set([item.value for item in cls])

    @classmethod
    def as_list(cls):
        return [e.name for e in cls]

    @classmethod
    def by_str(cls, str_name):

        # TODO: Not the best lookup strategy for large lists. Should better use the functions of Enum
        try:
            ret = cls[str_name]
        except:
            ret = next((item for item in cls if str(item) == str_name), None)

        return ret

    @classmethod
    def by_val(cls, val):
        return next(item for item in cls if item.value == val)

    @classmethod
    def random(cls):
        return rnd.choice(list(cls))

class CardinalPosition(CoopEnum):
    TOP_LEFT = (0, 0)
    TOP_RIGHT = (1, 0)
    TOP_CENTER = (0.5, 0)
    BOTTOM_LEFT = (0, 1)
    BOTTOM_RIGHT = (1, 1)
    RIGHT_CENTER = (1, 0.5)
    BOTTOM_CENTER = (0.5, 1)
    LEFT_CENTER = (0, 0.5)
    CENTER = (0.5, 0.5)

    @classmethod
    def top_left_from_alignment(cls,
                                dims: Tuple[float, float],
                                anchor: Tuple[float, float],
                                cardinality) -> Tuple[float, float]:

        tl_x = anchor[0] - cardinality.value[0] * dims[0]
        tl_y = anchor[1] - cardinality.value[1] * dims[1]

        return tl_x, tl_y

    @classmethod
    def alignment_from_top_left(cls,
                                dims: Tuple[float, float],
                                top_left: Tuple[float, float],
                                cardinality) -> Tuple[float, float]:
        x = top_left[0] + cardinality.value[0] * dims[0]
        y = top_left[1] + cardinality.value[1] * dims[1]

        return x, y

    @classmethod
    def alignment_conversion(cls,
                             dims: Tuple[float, float],
                             anchor: Tuple[float, float],
                             from_cardinality,
                             to_cardinality) -> Tuple[float, float]:
        tl = CardinalPosition.top_left_from_alignment(dims, anchor, from_cardinality)
        ret = CardinalPosition.alignment_from_top_left(dims, tl, to_cardinality)
        return ret



if __name__=="__main__":
    class Dummy(CoopEnum):
        A = auto()
        B = auto()
        C = auto()

    print(Dummy.random())