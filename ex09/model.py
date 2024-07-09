"""The model classes maintain the state and logic of the simulation."""

from __future__ import annotations
from random import random
from exercises.ex09 import constants
from math import sin, cos, pi
from math import sqrt


__author__ = "730554887"  


class Point:
    """A model of a 2-d cartesian coordinate Point."""
    x: float
    y: float

    def __init__(self, x: float, y: float):
        """Construct a point with x, y coordinates."""
        self.x = x
        self.y = y

    def add(self, other: Point) -> Point:
        """Add two Point objects together and return a new Point."""
        x: float = self.x + other.x
        y: float = self.y + other.y
        return Point(x, y)
    
    def distance(point_1: Point, point_2: Point) -> float:
        """Calculate the distance between two points."""
        dist: float = sqrt((point_2.x - point_1.x)**2 + (point_2.y - point_1.y)**2)
        return dist


class Cell:
    """An individual subject in the simulation."""
    location: Point
    direction: Point
    sickness: int = constants.VULNERABLE
    
    def __init__(self, location: Point, direction: Point):
        """Construct a cell with its location and direction."""
        self.location = location
        self.direction = direction

    def tick(self) -> None:
        """Reassigns cell location."""
        self.location = self.location.add(self.direction)
        if self.is_infected():
            self.sickness += 1
            if self.sickness == constants.RECOVERY_PERIOD:
                self.immunize()

    def contract_disease(self) -> None:
        """Gives disease to cell."""
        self.sickness = constants.INFECTED

    def is_vulnerable(self) -> bool:
        """Checks if a cell is vulnerable to a disease."""
        if self.sickness == constants.VULNERABLE:
           return True
        else:
            return False 

    def is_infected(self) -> bool:
        """Checks if a cell is infected."""
        if self.sickness >= constants.INFECTED:
           return True
        else:
            return False

    def color(self) -> str:
        """Assigns a color based on cell condition."""
        if self.is_vulnerable():
            return "gray"
        elif self.is_infected():
            return "pink"
        elif self.is_immune():
            return "purple"

    def contact_with(self, cell_2: Cell) -> None:
        """Gives a vulnerable cell the disease."""
        if self.is_vulnerable() and cell_2.is_infected():
            self.contract_disease()
        if cell_2.is_vulnerable() and self.is_infected():
            cell_2.contract_disease()

    def immunize(self) -> None:
        """Makes a cell immune."""
        self.sickness = constants.IMMUNE

    def is_immune(self) -> bool:
        """Checks if a cell is immune."""
        if self.sickness == constants.IMMUNE:
            return True
        else:
            return False

        
class Model:
    """The state of the simulation."""

    population: list[Cell]
    time: int = 0

    def __init__(self, cells: int, speed: float, infected: int, immune: int = 0):
        """Initialize the cells with random locations and directions."""
        if infected >= cells:
            raise ValueError("Check the number of cell objects")
        if infected <= 0:
            raise ValueError("Check the number of cell objects")
        if immune >= cells:
            raise ValueError("Check the number of cell objects")
        if immune < 0:
            raise ValueError("Check the number of cell objects")
        self.population = []
        for i in range(cells):
            start_location: Point = self.random_location()
            start_direction: Point = self.random_direction(speed)
            cell: Cell = Cell(start_location, start_direction)
            if infected > 0:
                cell.contract_disease()
                infected -= 1
            if immune > 0:
                cell.immunize()
                immune -= 1
            self.population.append(cell)

    def check_contacts(self) -> None:
        """Checks if two cells come in contact."""
        low: int = 0
        high: int = low + 1
        while low < constants.CELL_COUNT - 1:
            while high < constants.CELL_COUNT:
                if self.population[low].location.distance(self.population[high].location) < constants.CELL_RADIUS:
                    self.population[low].contact_with(self.population[high])
                high += 1
            low += 1
            high = low + 1
      
    def tick(self) -> None:
        """Update the state of the simulation by one time step."""
        self.time += 1
        for cell in self.population:
            cell.tick()
            self.enforce_bounds(cell)
        self.check_contacts()

    def random_location(self) -> Point:
        """Generate a random location."""
        start_x: float = random() * constants.BOUNDS_WIDTH - constants.MAX_X
        start_y: float = random() * constants.BOUNDS_HEIGHT - constants.MAX_Y
        return Point(start_x, start_y)

    def random_direction(self, speed: float) -> Point:
        """Generate a 'point' used as a directional vector."""
        random_angle: float = 2.0 * pi * random()
        direction_x: float = cos(random_angle) * speed
        direction_y: float = sin(random_angle) * speed
        return Point(direction_x, direction_y)
    
    def enforce_bounds(self, cell: Cell) -> None:
        """Cause a cell to 'bounce' if it goes out of bounds."""
        if cell.location.x > constants.MAX_X:
            cell.location.x = constants.MAX_X
            cell.direction.x *= -1.0
        if cell.location.x < constants.MIN_X:
            cell.location.x = constants.MIN_X
            cell.direction.x *= -1.0
        if cell.location.y > constants.MAX_Y:
            cell.location.y = constants.MAX_Y
            cell.direction.y *= -1.0
        if cell.location.y < constants.MIN_Y:
            cell.location.y = constants.MIN_Y
            cell.direction.y *= -1.0

    def is_complete(self) -> bool:
        """Method to indicate when the simulation is complete."""
        for cell in self.population:
            if cell.is_infected():
                return False
        return True