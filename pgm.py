#!/usr/bin/python
# -*-coding:Utf-8 -*


import Image


def convertListToImage(liste, width, height):
    """docstring for convertListToImage"""
    buff = Image.new('L', (width, height))

    for y in range(0, width):
        for x in range(0, height):
            buff.putpixel((x, y), liste[width * y + x])

    return buff


def convertDictToImage(dictionary, width, height):
    """docstring for convertDictToImage"""
    buff = Image.new('L', (width, height))
    for key, value in dictionary.iteritems():
        buff.putpixel(key, value * 255)
    return buff


def convertImageToList(image):
    """docstring for convertImageToList"""
    pass
