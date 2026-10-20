# -*- coding: utf-8 -*-
"""Иерархия классов отделочных материалов: обои, плитка, ламинат."""
import math
from abc import ABC, abstractmethod

from finishing.catalog import DEFAULT_RESERVE


class FinishMaterial(ABC):
    """Абстрактный отделочный материал с общим расчётом закупки."""

    def __init__(self, name, area, price, reserve):
        self.name = name
        self.area = area
        self.price = price
        self.reserve = reserve

    @staticmethod
    def _check_positive(value, message):
        """Проверка, что значение — конечное положительное число."""
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(message)
        if not (math.isfinite(value) and value > 0):
            raise ValueError(message)
        return float(value)

    @property
    def name(self):
        """Название материала."""
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError('название не может быть пустым')
        self._name = value.strip()

    @property
    def area(self):
        """Площадь поверхности, м²."""
        return self._area

    @area.setter
    def area(self, value):
        self._area = self._check_positive(value, 'площадь должна быть положительным числом')

    @property
    def price(self):
        """Цена единицы материала, руб."""
        return self._price

    @price.setter
    def price(self, value):
        self._price = self._check_positive(value, 'цена должна быть положительным числом')

    @property
    def reserve(self):
        """Запас на подрезку, %."""
        return self._reserve

    @reserve.setter
    def reserve(self, value):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError('запас должен быть числом')
        if not (math.isfinite(value) and value >= 0):
            raise ValueError('запас не может быть отрицательным')
        self._reserve = float(value)

    def work_area(self):
        """Площадь с учётом запаса на подрезку."""
        return round(self.area * (1 + self.reserve / 100), 6)

    @abstractmethod
    def unit_area(self):
        """Площадь одной единицы материала (рулона, плитки, упаковки)."""

    @abstractmethod
    def unit_title(self):
        """Название единицы в форме «рулонов», «плиток», «упаковок»."""

    @abstractmethod
    def params_str(self):
        """Описание размеров материала для отчёта."""

    def units_to_buy(self):
        """Количество единиц к закупке, округлённое вверх."""
        ratio = round(self.work_area() / self.unit_area(), 9)
        return math.ceil(ratio)

    def total_cost(self):
        """Стоимость закупки, руб."""
        return self.units_to_buy() * self.price

    def __str__(self):
        return (f'{self.name}: площадь {self.area:g} м², запас {self.reserve:g}%, '
                f'{self.unit_title()} к покупке: {self.units_to_buy()}, '
                f'стоимость: {self.total_cost():.2f} руб.')

    def __eq__(self, other):
        if not isinstance(other, FinishMaterial):
            return NotImplemented
        return (type(self) == type(other)
                and self.name == other.name
                and self.area == other.area
                and self.price == other.price
                and self.reserve == other.reserve
                and self.params_str() == other.params_str())


class Wallpaper(FinishMaterial):
    """Обои: расчёт по площади рулона."""

    def __init__(self, area, width, length, price, reserve=DEFAULT_RESERVE):
        super().__init__('Обои', area, price, reserve)
        self.width = width
        self.length = length

    @property
    def width(self):
        """Ширина рулона, м."""
        return self._width

    @width.setter
    def width(self, value):
        self._width = self._check_positive(value, 'ширина рулона должна быть положительным числом')

    @property
    def length(self):
        """Длина рулона, м."""
        return self._length

    @length.setter
    def length(self, value):
        self._length = self._check_positive(value, 'длина рулона должна быть положительным числом')

    def unit_area(self):
        return round(self.width * self.length, 6)

    def unit_title(self):
        return 'рулонов'

    def params_str(self):
        return f'рулон {self.width:g} x {self.length:g} м'

    def __repr__(self):
        return (f'Wallpaper({self.area:g}, {self.width:g}, {self.length:g}, '
                f'{self.price:g}, {self.reserve:g})')


class Tile(FinishMaterial):
    """Плитка: расчёт по площади плитки."""

    def __init__(self, area, side_a, side_b, price, reserve=DEFAULT_RESERVE):
        super().__init__('Плитка', area, price, reserve)
        self.side_a = side_a
        self.side_b = side_b

    @property
    def side_a(self):
        """Первая сторона плитки, м."""
        return self._side_a

    @side_a.setter
    def side_a(self, value):
        self._side_a = self._check_positive(value, 'сторона плитки должна быть положительным числом')

    @property
    def side_b(self):
        """Вторая сторона плитки, м."""
        return self._side_b

    @side_b.setter
    def side_b(self, value):
        self._side_b = self._check_positive(value, 'сторона плитки должна быть положительным числом')

    def unit_area(self):
        return round(self.side_a * self.side_b, 6)

    def unit_title(self):
        return 'плиток'

    def params_str(self):
        return f'плитка {self.side_a * 100:g} x {self.side_b * 100:g} см'

    def __repr__(self):
        return (f'Tile({self.area:g}, {self.side_a:g}, {self.side_b:g}, '
                f'{self.price:g}, {self.reserve:g})')


class Laminate(FinishMaterial):
    """Ламинат: расчёт по площади упаковки."""

    def __init__(self, area, pack_area, price, reserve=DEFAULT_RESERVE):
        super().__init__('Ламинат', area, price, reserve)
        self.pack_area = pack_area

    @property
    def pack_area(self):
        """Площадь одной упаковки, м²."""
        return self._pack_area

    @pack_area.setter
    def pack_area(self, value):
        self._pack_area = self._check_positive(value, 'площадь упаковки должна быть положительным числом')

    def unit_area(self):
        return self.pack_area

    def unit_title(self):
        return 'упаковок'

    def params_str(self):
        return f'упаковка {self.pack_area:g} м²'

    def __repr__(self):
        return (f'Laminate({self.area:g}, {self.pack_area:g}, '
                f'{self.price:g}, {self.reserve:g})')
