"""Utility class for numerical operations."""

from __future__ import annotations

from typing import Union

__author__ = "730554887"


class Simpy:
    """Simpy class."""
    values: list[float]

    def __init__(self, nums: list[float]):
        """Initializes."""
        self.values = nums

    def __repr__(self) -> str:
        """Returns a string."""
        return f"Simpy({self.values})"

    def fill(self, num: float, repeat: int) -> None:
        """Fills list with values."""
        self.values = []
        for time in range(repeat):
            self.values.append(num)

    def arange(self, start: float, stop: float, step: float = 1.0) -> None:
        """Fills list with a range of numbers."""
        assert step != 0.0
        value: float = start
        if step > 0:
            while value < stop:
                self.values.append(value)
                value += step
        if step < 0:
            while value > stop:
                self.values.append(value)
                value += step

    def sum(self) -> float:
        """Sums list."""
        result: float = sum(self.values)
        return result

    def __add__(self, rhs: Union[float, Simpy]) -> Simpy:
        """Adds values to list."""
        result: Simpy = Simpy([])
        if isinstance(rhs, float):
            for item in self.values:
                result.values.append(item + rhs)
        else:
            assert len(self.values) == len(rhs.values)
            for i in range(len(self.values)):
                result.values.append(self.values[i] + rhs.values[i])
        return result
    
    def __pow__(self, rhs: Union[float, Simpy]) -> Simpy:
        """Takes values in list to a power."""
        result: Simpy = Simpy([])
        if isinstance(rhs, float):
            for item in self.values:
                result.values.append(item ** rhs)
        else:
            assert len(self.values) == len(rhs.values)
            for i in range(len(self.values)):
                result.values.append(self.values[i] ** rhs.values[i])
        return result

    def __eq__(self, rhs: Union[float, Simpy]) -> list[bool]:
        """Checks if values are equal."""
        result: list[bool] = []
        if isinstance(rhs, float):
            for item in self.values:
                if item == rhs:
                    result.append(True)
                else:
                    result.append(False)
        else:
            assert len(self.values) == len(rhs.values)
            for i in range(len(self.values)):
                if self.values[i] == rhs.values[i]:
                    result.append(True)
                else:
                    result.append(False)
        return result

    def __gt__(self, rhs: Union[float, Simpy]) -> list[bool]:
        """Checks if values are greater than each other."""
        result: list[bool] = []
        if isinstance(rhs, float):
            for item in self.values:
                if item > rhs:
                    result.append(True)
                else:
                    result.append(False)
        else:
            assert len(self.values) == len(rhs.values)
            for i in range(len(self.values)):
                if self.values[i] > rhs.values[i]:
                    result.append(True)
                else:
                    result.append(False)
        return result

    def __getitem__(self, rhs: Union[int, list[bool]]) -> Union[float, Simpy]:
        """Gets item."""
        if isinstance(rhs, int):
            return self.values[rhs]
        else:
            result: list[float] = []
            for i in range(len(self.values)):
                if rhs[i] is True:
                    result.append(self.values[i])
            return Simpy(result)