import math
from unittest import TestCase

from magnumapi.geometry.Arc import Arc
from magnumapi.geometry.Point import Point


class TestArc(TestCase):
    def test_calculate_theta_in_rad(self):
        # arrange
        p_start = Point.of_cartesian(10, 0)
        p_end = Point.of_cartesian(0, 10)

        # act
        # assert
        self.assertAlmostEqual(math.radians(90), Arc.calculate_theta_in_rad(p_start, p_end), places=6)

    def test_get_start_angle_in_rad(self):
        # arrange
        p_start = Point.of_cartesian(10, 0)
        p_end = Point.of_cartesian(0, 10)

        # act
        arc = Arc.of_end_points_center(p_start, p_end)
        # assert
        self.assertAlmostEqual(math.radians(0), arc.get_start_angle_in_rad(), places=6)

    def test_get_start_angle(self):
        # arrange
        p_start = Point.of_cartesian(10, 0)
        p_end = Point.of_cartesian(0, 10)

        # act
        arc = Arc.of_end_points_center(p_start, p_end)
        # assert
        self.assertAlmostEqual(0, arc.get_start_angle(), places=6)

    def test_get_end_angle_in_rad(self):
        # arrange
        p_start = Point.of_cartesian(10, 0)
        p_end = Point.of_cartesian(0, 10)

        # act
        arc = Arc.of_end_points_center(p_start, p_end)
        # assert
        self.assertAlmostEqual(math.radians(90), arc.get_end_angle_in_rad(), places=6)

    def test_get_end_angle(self):
        # arrange
        p_start = Point.of_cartesian(10, 0)
        p_end = Point.of_cartesian(0, 10)

        # act
        arc = Arc.of_end_points_center(p_start, p_end)
        # assert
        self.assertAlmostEqual(90, arc.get_end_angle(), places=6)

    def test_get_radius(self):
        # arrange
        p_start = Point.of_cartesian(10, 0)
        p_end = Point.of_cartesian(0, 10)

        # act
        arc = Arc.of_end_points_center(p_start, p_end)
        # assert
        self.assertAlmostEqual(10, arc.get_radius(), places=6)
