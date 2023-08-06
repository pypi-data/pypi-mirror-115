
import math

import matplotlib.pyplot as plt
import matplotlib.patches as patches

from magnumapi.geometry.Point import Point


class Arc:
    """ Arc class implementing a 2D line made of two end points and center along with basic geometric transformations

    """

    def __init__(self, p_start: Point, p_center: Point, theta: float) -> None:
        """ Constructor of an Arc object from start point, center point, and theta

        :param p_start: start point of an arc
        :param p_center: arc center
        :param theta: theta of an arc (in degrees)
        """
        self.p_start = p_start
        self.p_center = p_center
        self.theta = theta

    @staticmethod
    def of_end_points_center(p_start: Point, p_end: Point, p_center=Point.of_cartesian(0.0, 0.0)) -> "Arc":
        """ Method constructing an arc from two end points and a center

        :param p_start: start point
        :param p_end: end point
        :param p_center: center point
        :return: an Arc object with initialized start point, end point and theta
        """
        theta = Arc.calculate_theta(p_start.translate(-p_center),
                                    p_end.translate(-p_center))
        return Arc(p_start, p_center, theta)

    @staticmethod
    def calculate_theta_in_rad(p_start: Point, p_end: Point) -> float:
        """ Static method calculating theta angle (in radians) of an arc from two end points

        :param p_start: start point
        :param p_end: end point
        :return: theta angle of an arc instance expressed in radians
        """
        theta = p_end.get_phi_in_rad() - p_start.get_phi_in_rad()
        return theta

    @staticmethod
    def calculate_theta(p_start: Point, p_end: Point) -> float:
        """ Static method calculating theta angle (in degrees) of an arc from two end points

        :param p_start: start point
        :param p_end: end point
        :return: theta angle of an arc instance expressed in degrees
        """
        theta = p_end.get_phi() - p_start.get_phi()
        return theta

    def plot(self, ax: plt.Axes) -> None:
        """ Method plotting an arc on a matplotlib axis

        :param ax: input matplotlib axis
        """
        start_angle_deg = self.get_start_angle()
        end_angle_deg = self.get_end_angle()
        radius = self.get_radius()
        center = (self.p_center.x, self.p_center.y)
        if start_angle_deg > end_angle_deg:
            arc = patches.Arc(center, 2 * radius, 2 * radius, 0, end_angle_deg, start_angle_deg)
        else:
            arc = patches.Arc(center, 2 * radius, 2 * radius, 0, start_angle_deg, end_angle_deg)
        ax.add_patch(arc)

    def get_radius(self) -> float:
        """ Method calculating and returning an Arc instance radius

        :return: the radius of an arc instance
        """
        return (self.p_start - self.p_center).det()

    def get_start_angle_in_rad(self) -> float:
        """ Method returning a start angle of an arc instance in radians

        :return: start angle of an arc in radians
        """
        return (self.p_start - self.p_center).get_phi_in_rad()

    def get_start_angle(self) -> float:
        """ Method returning a start angle of an arc instance in degrees

        :return: start angle of an arc in degrees
        """
        return (self.p_start - self.p_center).get_phi()

    def get_end_angle_in_rad(self) -> float:
        """ Method returning an end angle of an arc instance in radians

        :return: end angle of an arc in radians
        """
        return self.get_start_angle_in_rad() + math.radians(self.theta)

    def get_end_angle(self) -> float:
        """ Method returning an end angle of an arc instance in degrees

        :return: end angle of an arc in degrees
        """
        return self.get_start_angle() + self.theta

    def copy(self) -> "Arc":
        """ Method returning a copy of a current Arc instance

        :return: a copy of a Arc instance
        """
        return Arc(self.p_start, self.p_center, self.theta)
