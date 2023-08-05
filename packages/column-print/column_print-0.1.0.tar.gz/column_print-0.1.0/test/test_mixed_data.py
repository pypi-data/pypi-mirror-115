#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""Test ColumnPrinter class with default settings."""

from math import pi as PI
from column_print import ColumnPrinter

my_dict =	{
  "first": "John",
  "last": "Ford"
}

with ColumnPrinter(3) as cprint:
    cprint("Hello")
    cprint("World")
    cprint("Goodbye")
    cprint("Moon")
    cprint(12345)
    cprint(0.123)
    cprint(2 + 3 * 4)
    cprint(PI)
    cprint(print)   # built-in function
    cprint(ColumnPrinter)   # class
    cprint(['a', 'b', 'c'])
    cprint([0, 1, 2, 3, 4, 5])
    cprint(my_dict)
    cprint(my_dict['last'])
    cprint(None)
