from typing import Tuple
from cooptools.coopEnum import CardinalPosition
import cooptools.geometry.rectangles.utils as rect
import cooptools.geometry.vectors.utils as vect

class Rectangle:

    @classmethod
    def from_tuple(cls, rect: Tuple[float, float, float, float]):
        return Rectangle(rect[0], rect[1], rect[2], rect[3])

    def __init__(self, x: float, y: float, height: float, width: float):
        self.top_left: Tuple[float, float] = x, y
        self.dims: Tuple[float, float] = width, height

    def points_tuple(self):
        return ((self.x, self.y), (self.x + self.width, self.y), (self.x + self.width, self.y + self.height),
                (self.x, self.y + self.height))

    def contains_point(self, point: Tuple[float, float]):
        return rect.rect_contains_point(self.as_tuple(), point)


    def overlaps(self, other):
        if not type(other) == Rectangle and not type(other) == Tuple:
            raise TypeError(f"Cannot compare object of type {type(other)} to Rectangle for overlaps()")

        if type(other) == Rectangle:
            other = other.as_tuple()

        return rect.overlaps(self.as_tuple(), other)

    def align(self, anchor: Tuple[float, float], alignment: CardinalPosition):
        self.top_left = CardinalPosition.top_left_from_alignment(dims=self.dims, anchor=anchor, cardinality=alignment)

    def corner_generator(self):
        yield self.TopLeft
        yield self.TopRight
        yield self.BottomLeft
        yield self.BottomRight

    @property
    def Center(self) -> Tuple[float, float]:
        return CardinalPosition.alignment_from_top_left(self.dims, self.top_left, CardinalPosition.CENTER)

    @property
    def TopRight(self) -> Tuple[float, float]:
        return CardinalPosition.alignment_from_top_left(self.dims, self.top_left, CardinalPosition.TopRight)

    @property
    def TopLeft(self) -> Tuple[float, float]:
        return CardinalPosition.alignment_from_top_left(self.dims, self.top_left, CardinalPosition.TopLeft)

    @property
    def BottomRight(self) -> Tuple[float, float]:
        return CardinalPosition.alignment_from_top_left(self.dims, self.top_left, CardinalPosition.BottomRight)

    @property
    def BottomLeft(self) -> Tuple[float, float]:
        return CardinalPosition.alignment_from_top_left(self.dims, self.top_left, CardinalPosition.BottomLeft)

    @property
    def TopCenter(self) -> Tuple[float, float]:
        return CardinalPosition.alignment_from_top_left(self.dims, self.top_left, CardinalPosition.TopCenter)

    @property
    def BottomCenter(self) -> Tuple[float, float]:
        return CardinalPosition.alignment_from_top_left(self.dims, self.top_left, CardinalPosition.BottomCenter)

    @property
    def RightCenter(self) -> Tuple[float, float]:
        return CardinalPosition.alignment_from_top_left(self.dims, self.top_left, CardinalPosition.RightCenter)

    @property
    def LeftCenter(self) -> Tuple[float, float]:
        return CardinalPosition.alignment_from_top_left(self.dims, self.top_left, CardinalPosition.LeftCenter)

    @property
    def Corners(self):
        return [
            self.TopLeft,
            self.TopRight,
            self.BottomRight,
            self.BottomLeft
        ]

    @property
    def BoundingCircleRadius(self) -> float:
        return vect.distance_between(self.TopLeft, self.Center)

    @property
    def CornerTuples(self):
        return [x for x in self.Corners]

    def as_tuple(self):
        return (self.x, self.y, self.width, self.height)

    @property
    def x(self):
        return self.top_left[0]

    @x.setter
    def x(self, value):
        self.top_left = (value, self.top_left[1])


    @property
    def y(self):
        return self.top_left[1]

    @y.setter
    def y(self, value):
        self.top_left = (self.top_left[0], value)

    @property
    def width(self):
        return self.dims[0]

    @width.setter
    def width(self, value):
        self.dims = (value, self.dims[1])

    @property
    def height(self):
        return self.dims[1]

    @height.setter
    def height(self, value):
        self.dims = (self.dims[0], value)


    def __str__(self):
        return f"TopLeft: <{self.x}, {self.y}>, Size: H{self.height} x W{self.width}"







