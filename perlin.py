#!/usr/bin/python
# -*-coding:Utf-8 -*


import random


def generate_table(seed):
    """docstring for generate_table"""
    random.seed(seed)
    table = []
    value = random.randint(0, 255)
    while len(table) < 256:
        if value not in table:
            table.append(value)
        value = random.randint(0, 255)
    return table


def duplicate_table(table):
    """docstring for duplicate_table"""
    result = []
    for i in range(0, len(table) * 2):
        result[i] = table[i % 255]
    return result


def check_table(table):
    """docstring for check_table"""
    dictionary = {}
    for i in range(0, 256):
        dictionary[i] = 0

    for i in range(0, 256):
        if i in table:
            dictionary[i] += 1

    result = {}
    for key, value in dictionary.iteritems():
        if value is not 1:
            result[key] = value

    return result


table = generate_table(1)
dictionary = check_table(table)
