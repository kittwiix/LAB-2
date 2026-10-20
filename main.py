# -*- coding: utf-8 -*-
"""ЛР №2, вариант 10. Консольный расчёт закупки отделочных материалов."""
import math

from finishing import (DEFAULT_RESERVE, LAMINATE_PACKS, TILE_SIZES, WALLPAPER_SIZES,
                       CalculationsDB, Laminate, Tile, Wallpaper,
                       export_docx, export_xlsx)

MENU = """
--- Отделочные материалы: расчёт закупки (вариант 10) ---
1 - Обои
2 - Плитка
3 - Ламинат
4 - Показать сохранённые расчёты
5 - Экспорт расчётов в docx
6 - Экспорт расчётов в xlsx
0 - Выход
"""


def read_positive(prompt):
    """Чтение положительного числа с повтором при ошибке."""
    while True:
        text = input(prompt).replace(',', '.').strip()
        try:
            value = float(text)
        except ValueError:
            print('Ошибка: нужно число')
            continue
        if not (math.isfinite(value) and value > 0):
            print('Ошибка: число должно быть положительным')
            continue
        return value


def read_reserve():
    """Чтение запаса на подрезку, по умолчанию 10 %."""
    while True:
        text = input(f'Запас на подрезку, % (Enter - {DEFAULT_RESERVE}): ').replace(',', '.').strip()
        if not text:
            return DEFAULT_RESERVE
        try:
            value = float(text)
        except ValueError:
            print('Ошибка: нужно число')
            continue
        if not (math.isfinite(value) and value >= 0):
            print('Ошибка: запас не может быть отрицательным')
            continue
        return value


def choose_size(title, options):
    """Выбор размера из справочника по номеру."""
    print(title)
    keys = list(options)
    for number, name in enumerate(keys, start=1):
        print(f'  {number} - {name}')
    while True:
        text = input('Номер варианта: ').strip()
        if text.isdigit() and 1 <= int(text) <= len(keys):
            return keys[int(text) - 1]
        print('Ошибка: введите номер из списка')


def make_material(choice):
    """Создание материала по пункту меню с вводом параметров."""
    area = read_positive('Площадь поверхности, м²: ')
    if choice == '1':
        name = choose_size('Размер рулона:', WALLPAPER_SIZES)
        width, length = WALLPAPER_SIZES[name]
        price = read_positive('Цена за рулон, руб.: ')
        return Wallpaper(area, width, length, price, read_reserve())
    if choice == '2':
        name = choose_size('Размер плитки:', TILE_SIZES)
        side_a, side_b = TILE_SIZES[name]
        price = read_positive('Цена за плитку, руб.: ')
        return Tile(area, side_a, side_b, price, read_reserve())
    name = choose_size('Площадь упаковки:', LAMINATE_PACKS)
    price = read_positive('Цена за упаковку, руб.: ')
    return Laminate(area, LAMINATE_PACKS[name], price, read_reserve())


def show_results(db):
    """Печать сохранённых расчётов."""
    rows = db.all()
    if not rows:
        print('Сохранённых расчётов нет')
        return
    print(f'{"ID":<4}{"Материал":<12}{"Площадь":<10}{"Параметры":<24}'
          f'{"К закупке":<12}{"Стоимость":<12}Дата')
    for id_, material, area, params, units, cost, created in rows:
        print(f'{id_:<4}{material:<12}{area:<10g}{params:<24}{units:<12}{cost:<12.2f}{created}')
    print(f'Всего записей: {len(db)}')


def main():
    """Главный цикл консольного меню."""
    db = CalculationsDB()
    while True:
        print(MENU)
        choice = input('Выберите пункт: ').strip()
        if choice == '0':
            db.close()
            print('Выход')
            break
        if choice in ('1', '2', '3'):
            try:
                material = make_material(choice)
            except ValueError as error:
                print('Ошибка:', error)
                continue
            print(material)
            db.add(material)
            print('Расчёт сохранён в calculations.db')
        elif choice == '4':
            show_results(db)
        elif choice == '5':
            print('Файл сохранён:', export_docx(db.all()))
        elif choice == '6':
            print('Файл сохранён:', export_xlsx(db.all()))
        else:
            print('Нет такого пункта меню')


if __name__ == '__main__':
    main()
