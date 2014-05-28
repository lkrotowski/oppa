#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages

setup(name         = "oppa",
      description  = "Presentation and lecture support tool",
      url          = "https://github.com/lkrotowski/oppa",
      version      = "0.0.1",
      packages     = find_packages("src"),
      package_dir  = {"": "src"},
      entry_points = {"console_scripts": ["oppa=oppa.main:main"]},
      author       = "Łukasz Krotowski",
      author_email = "lukasz.krotowski@gmail.com",
      license      = "GPLv3")
