from abc import ABC, abstractmethod
from dataclasses import dataclass
from math import sqrt, fabs, degrees, acos, cos, asin, sin, radians
from functools import lru_cache, wraps, cached_property, reduce
from typing import Iterable, Callable, Union, Generator, Self

from beautiful_repr import StylizedMixin, Field, TemplateFormatter, parse_length
from pyoverload import overload

from sim32.interfaces import IUpdatable, IZone, IZoneFactory
from sim32.errors.geometry_errors import *
from sim32.tools import *


class DegreeMeasure:
    """Class for holding degrees in normalized form and manipulations with them."""

    __slots__ = ('__degrees')

    def __init__(self, degrees: int | float):
        self.__degrees = self._bring_number_into_degrees(degrees)

    @property
    def degrees(self) -> int | float:
        """Property for unprotected degree form."""

        return self.__degrees

    def __int__(self) -> int:
        return int(self.degrees)

    def __float__(self) -> float:
        return float(self.degrees)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.degrees})"

    def __hash__(self) -> int:
        return self.degrees

    def _degree_measure_creation_from_degrees(
        method: Callable[[Self, any], int | float]
    ) -> Callable[[any], Self]:
        """Method decorator for native creation of DegreemMeasure from output numeric degrees."""

        @wraps(method)
        def wrapper(self: Self, *args, **kwargs) -> Self:
            return self.__class__(method(self, *args, **kwargs))

        return wrapper

    def _interpret_input_measure_in_degrees(
        method: Callable[[int | float], any]
    ) -> Callable[[Union[int, float, Self]], any]:
        """Decorator for methods that converts the input DegreeMeasure to its bare degrees."""

        @wraps(method)
        def wrapper(
            self,
            other: Union[int, float, Self],
            *args,
            **kwargs
        ) -> any:
            return method(
                self,
                self._get_number_from_degrees_or_number(other),
                *args,
                **kwargs
            )

        return wrapper

    @_interpret_input_measure_in_degrees
    def __eq__(self, number: int | float) -> bool:
        return self.degrees == number

    @_interpret_input_measure_in_degrees
    def __ne__(self, number: int | float) -> bool:
        return self.degrees != number

    @_interpret_input_measure_in_degrees
    def __lt__(self, number: int | float) -> bool:
        return self.degrees < number

    def __le__(self, number: int | float | Self) -> bool:
        return self < number or self == number

    @_interpret_input_measure_in_degrees
    def __gt__(self, number: int | float) -> bool:
        return self.degrees > number

    def __ge__(self, number: int | float | Self) -> bool:
        return self > number or self == number

    @_degree_measure_creation_from_degrees
    @_interpret_input_measure_in_degrees
    def __add__(self, number: int | float) -> int | float:
        return self.degrees + number

    def __radd__(self, number: int | float) -> Self:
        return self + number

    @_degree_measure_creation_from_degrees
    @_interpret_input_measure_in_degrees
    def __sub__(self, number: int | float) -> int | float:
        return self.degrees - number

    def __rsub__(self, number: int | float) -> Self:
        return -(self) + number

    @_degree_measure_creation_from_degrees
    @_interpret_input_measure_in_degrees
    def __mul__(self, number: int | float) -> int | float:
        return self.degrees * number

    def __rmul__(self, number: int | float) -> Self:
        return self * number

    @_degree_measure_creation_from_degrees
    @_interpret_input_measure_in_degrees
    def __truediv__(self, number: int | float) -> int | float:
        return self.degrees / number

    @_degree_measure_creation_from_degrees
    @_interpret_input_measure_in_degrees
    def __floordiv__(self, number: int | float) -> int | float:
        return (self.degrees / number) // 1

    @_degree_measure_creation_from_degrees
    def __neg__(self) -> Self:
        return self.degrees * -1

    def _get_number_from_degrees_or_number(
        cls,
        number_or_degrees: Union[int, float, Self]
    ) -> int | float:
        """
        Method for natively converting the input DegreeMeasure to its bare
        numeric form, or non-converting if a number is entered.
        """

        return (
            number_or_degrees.degrees if isinstance(number_or_degrees, DegreeMeasure)
            else number_or_degrees
        )

    @staticmethod
    def _bring_number_into_degrees(number: int | float) -> int | float:
        """Method for resetting a number on overflow greater than 359."""

        return number - (number // 360)*360


@dataclass(repr=False, frozen=True)
class AxisPlaneDegrees:
    """Dataclass for positioning degrees on an axial plane."""

    first_axis: int
    second_axis: int
    degrees: DegreeMeasure

    def __post_init__(self) -> None:
        if self.first_axis == self.second_axis:
            raise AxisPlaneDegreesError(f"{self.__class__.__name__} must be on two axes, not one ({self.first_axis})")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({str(self.axes)[1:-1]}, degrees={self.degrees.degrees})"

    @cached_property
    def axes(self) -> tuple[int, int]:
        """Property representing axes in collection format."""

        return (self.first_axis, self.second_axis)

    def is_on_same_plane_with(self, axis_degrees: Self) -> bool:
        """Method for comparing axes of two AxisPlaneDegrees."""

        return frozenset(self.axes) == frozenset(axis_degrees.axes)

    def get_external(self) -> Self:
        """Method for getting the other degrees located in the same plane."""

        return self.__class__(self.first_axis, self.second_axis, -self.degrees)


@dataclass(repr=False, frozen=True)
class DegreeArea(AxisPlaneDegrees):
    """Class representing degrees on a plane in a certain zone."""

    shift_degrees: DegreeMeasure

    def __repr__(self) -> str:
        return "{class_name}({axes}, degrees={degree_diapason})".format(
            class_name=self.__class__.__name__,
            axes=str(self.axes)[1:-1],
            degree_diapason=f"({self.shift_degrees.degrees} ~ {self.border_degrees.degrees})"
        )

    def __contains__(self, degrees: int | float | DegreeMeasure) -> bool:
        return self.is_degrees_inside(degrees)

    @cached_property
    def border_degrees(self) -> DegreeMeasure:
        """Property for defining the top border of the area."""

        return self.degrees + self.shift_degrees

    @cached_property
    def is_empty(self) -> bool:
        """Property for determining the emptiness of an area."""

        return self.shift_degrees == self.border_degrees

    def is_degrees_inside(self, degrees: int | float | DegreeMeasure) -> bool:
        """Method for determining the presence of degrees in an area."""

        if self.is_empty:
            return False

        is_degrees_in_diapason = degrees in self._diapason

        return (
            is_degrees_in_diapason
            if self.shift_degrees <= self.border_degrees
            else (
                not is_degrees_in_diapason
                or degrees == self.shift_degrees
                or degrees == self.border_degrees
            )
        )

    def get_external(self) -> Self:
        return self.__class__(
            self.first_axis,
            self.second_axis,
            -self.degrees,
            self.border_degrees
        )

    @cached_property
    def _diapason(self) -> Diapason:
        """Degree range rough shape property."""

        return Diapason(
            self.shift_degrees,
            self.border_degrees,
            is_end_inclusive=True
        )


class Vector:
    """Class for manipulating vectors. Are not strict to the number of measurements."""

    def __init__(self, coordinates: Iterable[float | int] = tuple()):
        self.__coordinates = tuple(coordinates)

    @property
    def coordinates(self) -> tuple[int | float]:
        """Vector Coordinate Property."""

        return self.__coordinates

    @cached_property
    def length(self) -> float:
        """Vector length property."""

        return sqrt(sum(coordinate**2 for coordinate in self.coordinates))

    @cached_property
    def degrees(self) -> tuple[AxisPlaneDegrees]:
        """Property of degrees of a vector sliced on a plane."""

        perpendicular_vector = Vector((1, ))

        return tuple(
            AxisPlaneDegrees(
                first_axis,
                second_axis,
                self.__class__((
                    self.coordinates[first_axis],
                    self.coordinates[second_axis]
                )).get_degrees_between(
                    perpendicular_vector,
                    0 > self.coordinates[second_axis]
                )
            )
            for first_axis in range(len(self.coordinates))
            for second_axis in range(first_axis + 1, len(self.coordinates))
            if any(map(
                lambda coordinate: coordinate != 0,
                (self.coordinates[first_axis], self.coordinates[second_axis])
            ))
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({str(tuple(self.coordinates))[1:-1]})"

    def __hash__(self) -> int:
        return hash(self.coordinates)

    def __eq__(self, other: Self) -> Self:
        return self.coordinates == other.coordinates

    @lru_cache(maxsize=8192)
    def __add__(self, other: Self) -> Self:
        return self.__class__(
            tuple(map(
                lambda first, second: first + second,
                *(
                    vector.coordinates
                    for vector in self.get_mutually_normalized((self, other))
                )
            ))
        )

    def __sub__(self, other: Self) -> Self:
        return self + (-other)

    @lru_cache(maxsize=4096)
    def __mul__(self, other: Union[int, float, Self]) -> Self:
        return (
            self.get_scalar_by(other) if isinstance(other, Vector)
            else self.get_multiplied_by_number(other)
        )

    def __rmul__(self, number: int | float) -> Self:
        return self * number

    def __truediv__(self, number: int | float) -> Self:
        return self*(1 / number)

    def __floordiv__(self, number: int | float) -> Self:
        return self.__class__(
            tuple(int(coordinate) for coordinate in (self / number).coordinates)
        )

    def __neg__(self) -> Self:
        return self.get_reflected_by_axes()

    def __len__(self) -> int:
        return len(self.coordinates)

    @lru_cache(maxsize=1024)
    def get_normalized_to_measurements(
        self,
        number_of_measurements: int,
        default_measurement_point: int | float = 0
    ) -> Self:
        """
        Method for getting a vector expanded or reduced to a certain number of
        dimensions.
        """

        measurement_difference = number_of_measurements - len(self.coordinates)

        return self.__class__(
            self.coordinates + (default_measurement_point,)*measurement_difference if measurement_difference > 0
            else self.coordinates[:number_of_measurements if number_of_measurements >= 0 else 0]
        )

    @lru_cache(maxsize=128)
    def get_reflected_by_axes(
        self,
        axis_indexes: Iterable[int] | None = None
    ) -> Self:
        """Method for getting a vector unfolded in a plane."""

        if axis_indexes is None:
            axis_indexes = range(len(self.coordinates))

        return self.__class__(tuple(
            coordinate * (-1 if coordinate_index in axis_indexes else 1)
            for coordinate_index, coordinate in enumerate(self.coordinates)
        ))

    @lru_cache(maxsize=128)
    def get_reduced_to_length(self, length: int | float) -> Self:
        """Method for getting a similar vector but with an input length."""

        if self.length == 0:
            raise VectorError("Vector with length == 0 can't be lengthened")

        return (self / self.length) * length

    def get_rotated_many_times_by(self, axis_degree_measures: Iterable[AxisPlaneDegrees]) -> Self:
        """Method for getting a rotated vector along many axes many times."""

        result_vector = self

        for axis_degree_measure in axis_degree_measures:
            result_vector = result_vector.get_rotated_by(axis_degree_measure)

        return result_vector

    def get_rotated_by(self, axes_degrees: AxisPlaneDegrees) -> Self:
        """Method for getting a vector rotated on a plane."""

        number_of_measurements = max(axes_degrees.axes) + 1
        reduced_vector = (
            self.get_normalized_to_measurements(number_of_measurements)
            if len(self.coordinates) < number_of_measurements else self
        )

        axes_section_vector = self.__class__((
            reduced_vector.coordinates[axes_degrees.first_axis],
            reduced_vector.coordinates[axes_degrees.second_axis]
        ))

        if all(coordinate == 0 for coordinate in axes_section_vector.coordinates):
            return self

        coordinates = list(reduced_vector.coordinates)

        reduced_axes_section_vector = axes_section_vector.get_reduced_to_length(1)

        coordinates[axes_degrees.first_axis] = axes_section_vector.length * cos(radians(
                axes_section_vector.degrees[0].degrees
                + axes_degrees.degrees
        ))

        coordinates[axes_degrees.second_axis] = axes_section_vector.length * sin(radians(
                axes_section_vector.degrees[0].degrees
                + axes_degrees.degrees
        ))

        return self.__class__(coordinates)

    def get_rounded_by(self, rounder: NumberRounder) -> Self:
        """Method for getting rounded vector with rounding input implementation."""

        return self.__class__(tuple(
            rounder(coordinate)
            for coordinate in self.coordinates
        ))

    def get_multiplied_by_number(self, number: int | float) -> Self:
        """Method for getting a vector multiplied by a number."""

        return self.__class__(
            tuple(number * coordinate for coordinate in self.coordinates)
        )

    def get_scalar_by(self, vector: Self) -> int | float:
        """Method to get a scalar between two vectors."""

        return sum(tuple(map(
            lambda first, second: first * second,
            *(
                normalized_vector.coordinates
                for normalized_vector in self.get_mutually_normalized((self, vector))
            )
        )))

    def get_degrees_between(self, vector: Self, is_external: bool = False) -> DegreeMeasure:
        """Method for getting angle degrees between two vectors."""

        return DegreeMeasure(degrees(acos(
            (self * vector) / (self.length * vector.length)
        ))) * (-1 if is_external else 1)

    @staticmethod
    def get_mutually_normalized(vectors: Iterable[Self]) -> tuple[Self]:
        """Method for getting vectors in the same dimensions."""

        maximum_number_of_measurements = max((len(vector.coordinates) for vector in vectors))

        return tuple(
            vector.get_normalized_to_measurements(maximum_number_of_measurements)
            for vector in vectors
        )

    @classmethod
    def create_by_degrees(cls, length: int | float, axis_degree_measures: Iterable[AxisPlaneDegrees]) -> Self:
        """
        Method for creating a vector of an input length unfolded along the
        degrees of input certain planes.

        Doesn't guarantee the creation of a vector with degrees contradicting
        the input.
        """

        fill_axis = axis_degree_measures[0].first_axis if len(axis_degree_measures) else 0

        return cls(
            (0, )*fill_axis + (length, )
        ).get_rotated_many_times_by(axis_degree_measures)


@dataclass(repr=False)
class PositionVector:
    """Dataclass to emulate a vector with a specific start and end."""

    start_point: Vector
    end_point: Vector

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(from {self.start_point} to {self.end_point})"

    @property
    def virtual_vector(self) -> Vector:
        """Property for immediate vector lying between start and end."""

        return self.end_point - self.start_point

    def get_rounded_by(self, rounder: NumberRounder) -> Self:
        """Method for rounding vectors annotating start and end."""

        return self.__class__(
            self.start_point.get_rounded_by(rounder),
            self.end_point.get_rounded_by(rounder)
        )


class IPointChanger(ABC):
    """
    Vector changer interface for changing a vector without dependencies on a
    specific change implementation.
    """

    @abstractmethod
    def __call__(self, point: Vector) -> Vector:
        """Method for getting a vector modified according to the similarity of the input."""


class DynamicTransporter(IPointChanger):
    """
    PointChanger class which returns a vector sum of the input and that contained in
    the changer itself.

    Abstracts addition.
    """

    def __init__(self, shift: Vector):
        self.shift = shift

    def __call__(self, point: Vector) -> Vector:
        return point + self.shift


class PointRotator(StylizedMixin, IPointChanger):
    """
    PointChanger class returning the rotated analog of the input vector.

    Abstracts rotation.
    Rotates the vector from the center_point vector by axis_degree_measures degrees.
    """

    _repr_fields = (
        Field('center_point', formatter=TemplateFormatter('about {value}')),
        Field(
            'axis_degree_measures',
            formatter=TemplateFormatter('{value}'),
            value_transformer=lambda value: str(list(value))[1:-1] if len(value) > 0 else value
        )
    )

    def __init__(self, axis_degree_measures: Iterable[AxisPlaneDegrees], center_point: Vector = Vector()):
        self.axis_degree_measures = tuple(axis_degree_measures)
        self.center_point = center_point

    def __call__(self, point: Vector) -> Vector:
        return reduce(
            lambda result_point, axis_degree_measure: (
                (result_point - self.center_point).get_rotated_by(axis_degree_measure)
                + self.center_point
            ),
            (point, *self.axis_degree_measures)
        )


class VectorDivider(Divider, StylizedMixin):
    """Class dividing a vector into points."""

    _repr_fields = (Field('distance_between_points'), )

    def __init__(self, distance_between_points: int | float, rounder: NumberRounder):
        self.distance_between_points = distance_between_points
        self.rounder = rounder

    def is_possible_to_divide(self, data: Vector) -> Report:
        return Report.create_error_report(
            UnableToDivideVectorIntoPointsError(
                f"Can't divide vector {data} into points with length 0"
            )
        ) if data.virtual_vector.length == 0 else super().is_possible_to_divide(data)

    def _divide(self, vector: PositionVector) -> frozenset[Vector]:
        distance_factor = self.distance_between_points / vector.virtual_vector.length

        vector_to_next_point = Vector(tuple(
            coordinate * distance_factor for coordinate in vector.virtual_vector.coordinates
        ))

        return self.__create_points(
            vector.start_point,
            vector.virtual_vector.length / vector_to_next_point.length,
            vector_to_next_point
        )

    def __create_points(
        self,
        start_point: Vector,
        number_of_points_to_create: int,
        vector_to_next_point: Vector
    ) -> frozenset[Vector]:
        created_points = [start_point]

        for created_point_index in range(1, int(number_of_points_to_create) + 1):
            created_points.append(
                created_points[created_point_index - 1] + vector_to_next_point
            )

        return frozenset(
            point.get_rounded_by(self.rounder) for point in created_points
        )


class Figure(IZone, ABC):
    """
    Base zone class.

    Template-wise implements finding vectors in the zone by dividing them into
    points and working with them already.
    """

    _vector_divider_factory: Callable[['Line'], VectorDivider] = (
        lambda _: VectorDivider(0.1, ShiftNumberRounder(AccurateNumberRounder(), 1))
    )

    def __init__(self):
        self._vector_divider = self._vector_divider_factory()

    @overload
    def __contains__(self, point: Vector) -> bool:
        return self.is_point_inside(point)

    @overload
    def __contains__(self, vector: PositionVector) -> bool:
        return self.is_vector_passes(vector)

    def is_vector_passes(self, vector: PositionVector) -> bool:
        return any(
            self.is_point_inside(point)
            for point in self._vector_divider(vector)
        )

    def is_vector_entered(self, vector: PositionVector) -> bool:
        return self.is_point_inside(
            vector.end_point
        )


class AxisZone(Figure, StylizedMixin):
    """
    Class that implements a zone representation as a space between two points.

    Similar to a rectangle, but only because of its implementation of finding a
    point in it compared to its coordinates with its own diapasons of valid
    coordinates of certain axes.
    """

    _repr_fields = Field('axis_diapasons', formatter=lambda value, _: f"{str(value)[1:-1]}"),

    def __init__(self, first_point: Vector, second_point: Vector):
        super().__init__()
        self.__first_point = first_point
        self.__second_point = second_point

        self._update()

    @property
    def first_point(self) -> Vector:
        return self.__first_point

    @first_point.setter
    def first_point(self, new_point: Vector) -> Vector:
        self.__first_point = new_point
        self._update()

    @property
    def second_point(self) -> Vector:
        return self.__second_point

    @second_point.setter
    def second_point(self, new_point: Vector) -> Vector:
        self.__second_point = new_point
        self._update()

    @property
    def size(self) -> tuple[int | float]:
        """Virtual rectangle size property."""

        return self.__size

    @property
    def axis_diapasons(self) -> tuple[Diapason]:
        """Property of diapasons of available coordinates along the axes."""

        return self.__axis_diapasons

    def move_by(self, point_changer: IPointChanger) -> None:
        self.first_point = point_changer(self.first_point)
        self.second_point = point_changer(self.second_point)

    def is_point_inside(self, point: Vector) -> bool:
        return all(
            coordinate in self.axis_diapasons[axis]
            for axis, coordinate in enumerate(
                point.get_normalized_to_measurements(len(self.size)).coordinates
            )
        )

    @classmethod
    def create_with_generated_points_by(
        cls,
        center_point: Vector,
        size: Iterable[int | float]
    ) -> Self:
        """Creation method using point generation by size and center point."""

        vector_to_extreme_point = Vector(size) / 2

        return cls(
            center_point + vector_to_extreme_point,
            center_point - vector_to_extreme_point
        )

    @classmethod
    def create_as_square(
        cls,
        center_point: Vector,
        side_length: int | float,
        number_of_measurements: int
    ) -> Self:
        """
        Method of creating by the shape of a square using the generation of
        points by the center point and the length of the edge of the square.
        """

        return cls.create_with_generated_points_by(
            center_point,
            (side_length, ) * number_of_measurements
        )

    def _update(self) -> None:
        """Method for updating the whole body of a zone."""

        self.__first_point, self.__second_point = Vector.get_mutually_normalized((
            self.__first_point,
            self.__second_point
        ))

        self.__axis_diapasons = tuple(
            Diapason(first_point_coordinate, second_point_coordinate, True)
            for first_point_coordinate, second_point_coordinate  in zip(
                self.__first_point.coordinates,
                self.__second_point.coordinates
            )
        )

        self.__size = tuple(
            axis_diapason.end - axis_diapason.start
            for axis_diapason in self.__axis_diapasons
        )


class Angle(Figure, StylizedMixin):
    """Class of providing a zone of an angle originating from some point."""

    _repr_fields = Field('center_point'),

    def __init__(self, center_point: PositionVector, degree_areas: Iterable[DegreeArea]):
        self._center_point = center_point
        self._degree_areas = tuple(degree_areas)

        self.update_by_points(self.create_ray_vertices_by(1))

    @property
    def center_point(self) -> Vector:
        """Center point property."""

        return self._center_point

    @property
    def degree_areas(self) -> tuple[DegreeArea]:
        """Angle degree property."""

        return self._degree_areas

    def move_by(self, point_changer: IPointChanger) -> None:
        self._center_point = point_changer(self._center_point)

        self.update_by_points(tuple(
            point_changer(vertex) for vertex in self.create_ray_vertices_by(1)
        ))

    def create_ray_vertices_by(self, length: int | float) -> frozenset[Vector]:
        """Method for creating vectors with a fixed length from center point."""

        return frozenset(
            self.center_point + Vector.create_by_degrees(
                length,
                (AxisPlaneDegrees(
                        degree_area.first_axis,
                        degree_area.second_axis,
                        degrees
                ), )
            )
            for degree_area in self._degree_areas
            for degrees in (degree_area.shift_degrees, degree_area.border_degrees)
        )


    def update_by_points(self, points: Iterable[Vector]) -> None:
        self._degree_areas = tuple(self.__create_degree_areas_from(
            tuple(get_collection_with_reduced_nesting_level_by(
                1,
                (
                    (point - self._center_point).degrees
                    for point in Vector.get_mutually_normalized(points)
                )
            ))
        ))

    def become_external(self) -> None:
        """Angle reversal method."""

        self._degree_areas = tuple(
            degree_area.get_external()
            for degree_area in self._degree_areas
        )

    def is_point_inside(self, point: Vector) -> bool:
        return point == self._center_point or not any(
            degree_measure.degrees.degrees not in self.get_degree_area_by_axes(
                degree_measure.first_axis,
                degree_measure.second_axis
            )
            for degree_measure in (point - self._center_point).degrees
        )

    def get_degree_area_by_axes(self, first_axis: int, second_axis: int) -> DegreeArea:
        """Vector to get the axial degrees of the angle along the input plane."""

        for degree_area in self.degree_areas:
            if degree_area.first_axis == first_axis and degree_area.second_axis == second_axis:
                return degree_area
        else:
            return DegreeArea(first_axis, second_axis, DegreeMeasure(0), DegreeMeasure(0))

    @classmethod
    def created_by_points(cls, center_point: PositionVector, points: Iterable[Vector]) -> Self:
        """
        Method for creating from a set of points. Creates an angle capable of
        accommodating all input.
        """

        angle = cls(center_point, tuple())
        angle.update_by_points(points)

        return angle

    def __create_degree_areas_from(self, axis_degree_measures: Iterable[AxisPlaneDegrees]) -> Generator[DegreeArea, any, None]:
        """
        Method for creating degree areas from multiple axial degrees.
        Is a generator.
        """

        max_axes = 1 + max(get_collection_with_reduced_nesting_level_by(
            1,
            (point_degree_measure.axes for point_degree_measure in axis_degree_measures)
        ))

        for first_axis in range(max_axes):
            for second_axis in range(first_axis + 1, max_axes):
                degree_multitude = frozenset(
                    degree_measure.degrees.degrees
                    for degree_measure in axis_degree_measures
                    if (
                        degree_measure.first_axis == first_axis
                        and degree_measure.second_axis == second_axis
                    )
                )

                min_degrees, max_degrees = min(degree_multitude), max(degree_multitude)

                yield DegreeArea(
                    first_axis,
                    second_axis,
                    DegreeMeasure(max_degrees - min_degrees),
                    DegreeMeasure(min_degrees)
                )


class Site(Figure):
    """Class representation of a point with a zone interface."""

    def __init__(self, point: Vector):
        self.point = point

    def move_by(self, point_changer: IPointChanger) -> None:
        self.point = point_changer(self.point)

    def is_point_inside(self, point: Vector) -> bool:
        return self.point == point


class CompositeFigure(Figure, StylizedMixin):
    """Zone proxy class consisting of multiple zones."""

    _repr_fields = (
        Field(
            'main_figures',
            value_getter=parse_length,
            formatter=TemplateFormatter("{value} main figures")
        ),
        Field(
            'subtraction_figures',
            value_getter=parse_length,
            formatter=TemplateFormatter("{value} subtraction figures")
        )
    )

    def __init__(
        self,
        main_figures: Iterable[Figure],
        subtraction_figures: Iterable[Figure] = tuple()
    ):
        super().__init__()
        self.main_figures = set(main_figures)
        self.subtraction_figures = set(subtraction_figures)

    def move_by(self, point_changer: IPointChanger) -> None:
        for figure in (*self.main_figures, *self.subtraction_figures):
            figure.move_by(point_changer)

    def is_point_inside(self, point: Vector) -> bool:
        return (
            any(figure.is_point_inside(point) for figure in self.main_figures)
            if all(not figure.is_point_inside(point) for figure in self.subtraction_figures)
            else False
        )


class Line(Figure, StylizedMixin):
    """Position vector representation class with zone interface."""

    _repr_fields = (
        Field(
            value_getter=lambda line, _: (line.first_point, line.second_point),
            formatter=lambda values, _: f"between {values[0]} and {values[1]}"
        ),
    )

    def __init__(self, first_point: Vector, second_point: Vector):
        super().__init__()

        self._rounder = self._vector_divider.rounder

        self.__first_point = first_point
        self.__second_point = second_point

        self._update_points()

    @property
    def first_point(self) -> Vector:
        return self.__first_point

    @first_point.setter
    def first_point(self, new_point: Vector) -> None:
        self.__first_point = new_point
        self._update_points()

    @property
    def second_point(self) -> Vector:
        return self.__second_point

    @second_point.setter
    def second_point(self, new_point: Vector) -> None:
        self.__second_point = new_point
        self._update_points()

    @property
    def all_available_points(self) -> tuple[Vector]:
        """Class of all possible line points."""

        return self.__all_available_points

    def move_by(self, point_changer: IPointChanger) -> None:
        self.__first_point, self.__second_point = map(
            point_changer, (self.first_point, self.second_point)
        )

        self._update_points()

    def is_vector_passes(self, vector: PositionVector) -> bool:
        return super().is_vector_passes(vector) if (
            vector.start_point in self.__proposed_location_area or
            vector.end_point in self.__proposed_location_area or
            vector.end_point - vector.virtual_vector*0.5 in self.__proposed_location_area
        ) else False

    def is_point_inside(self, point: Vector) -> bool:
        return (
            point.get_rounded_by(self._rounder) in self.__all_available_points
            if not point in self.__proposed_location_area else True
        )

    def _update_points(self) -> None:
        """Method for updating all possible points."""

        self.__first_point, self.__second_point = map(
            lambda vector: vector.get_rounded_by(self._rounder),
            (self.__first_point, self.__second_point)
        )

        self.__all_available_points = self._vector_divider(
            PositionVector(self.first_point, self.second_point)
        )
        self.__proposed_location_area = AxisZone(self.first_point, self.second_point)


class Polygon(Figure, StrictToStateMixin, StylizedMixin):
    """Polygon Face (!) Zone Class."""

    _repr_fields = (
        Field(
            'summits',
            value_getter=parse_length,
            formatter=TemplateFormatter("{value} summits")
        ),
    )
    _line_factory: Callable[[Vector, Vector], Line] = Line
    _report_analyzer = ReportAnalyzer(
        (BadReportHandler(FigureIsNotCorrect, "Polygon not viable"), )
    )

    def __init__(self, points: Iterable[Vector]):
        super().__init__()
        self._update_lines_by(points)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({len(self.summits)} summit{'s' if len(self.summits) > 0 else ''})"

    @property
    def summits(self) -> tuple[Vector]:
        return self.__summits

    def move_by(self, point_changer: IPointChanger) -> None:
        self._update_lines_by(
            tuple(map(point_changer, self.summits))
        )
        self._check_state_errors()

    def is_point_inside(self, point: Vector) -> bool:
        return any(line.is_point_inside(point) for line in self._lines)

    def _is_correct(self) -> Report:
        number_of_measurements = max(
            map(lambda point: len(point.coordinates), self.summits)
        )

        if len(self.summits) <= number_of_measurements:
            return Report.create_error_report(FigureIsNotClosedError(
                f"{number_of_measurements}D figure must contain more than {number_of_measurements} links for closure"
            ))
        else:
            return Report(True)

    def _update_lines_by(self, points: Iterable[Vector]) -> tuple[Line]:
        self._lines = tuple(
            self._line_factory(
                points[point_index - 1],
                points[point_index]
            )
            for point_index in range(len(points))
        )

        self.__summits = tuple(line.first_point for line in self._lines)
        self._check_state_errors()


class Circle(Figure, StylizedMixin):
    """Zone class of a circle or its multidimensional variations."""

    _repr_fields = (Field('radius'), Field('center_point'))

    def __init__(self, center_point: Vector, radius: int | float):
        super().__init__()
        self.center_point = center_point
        self.radius = radius

    def move_by(self, point_changer: IPointChanger) -> None:
        self.center_point = point_changer(self.center_point)

    def is_point_inside(self, point: Vector) -> bool:
        return (self.center_point - point).length <= self.radius
