from datetime import datetime
from numbers import Real

class MedadRangi:
    discount_rate = 10
    longitude = 35.74317403843504
    latitude =  51.50185488303431
    objects = []

    def __init__(self, name, price, originCountry, factory, count):
        if type(name)!=str:
            raise TypeError("name must be a string")
        if not isinstance(price, Real):
            raise TypeError("price must be an integer")
        if type(originCountry)!=str:
            raise TypeError("originCountry must be a string")
        if type(factory)!=str:
            raise TypeError("factory must be a string")
        if type(count)!=int:
            raise TypeError("count must be an integer")
        
        self.name = name
        self.price = price
        self.originCountry = originCountry
        self.factory = factory
        self.count = count
        self.objects.append(self)
    def final_price(self):
        return (self.price - self.price * self.discount_rate/100) * self.count
    @staticmethod
    def welcome():
        h = datetime().now().hour
        if h>=6 and h<12:
            print("Good morning")
        if h>=12 and h<18:
            print("Good afternoon")
    @staticmethod
    def load_csv(file_name):
        with open(file_name, 'r') as f:
            
            for i in f:
                (name, price, originCountry, factory, count) = i.strip().split(', ')
                price = int(price); count = int(count)    
                MedadRangi(name, price, originCountry, factory, count)
        return
    @classmethod
    def calculate_distance(cls, xdest, ydest):
        return ((cls.longitude-xdest)**2 + (cls.latitude-ydest)**2)**0.5

import unittest
from random import randint

def entryGen():
    """ Create a string to write in csv file for unittest"""
    names = list("abcdefghij")
    originCountries = ["Iran", "USA", "Germany", "France", "Italy", "Spain", "China", "Russia", "Japan", "Korea"]
    factories = list("abcdefghij".upper())
    for i in range(10):
        name = names[i]
        originCountry = originCountries[i]
        factory = factories[i]
        price = 100*i
        count = 10
        ans = f"{name}, {price}, {originCountry}, {factory}, {count}\n"
        yield ans

entryGenerator = entryGen()
f = open("data.csv", 'w+')
for i in range(10):
    f.write(next(entryGenerator))
f.close()

class TestColorpencil(unittest.TestCase):
    def test_load_csv(self):
        MedadRangi.load_csv('data.csv')
        self.assertEqual(len(MedadRangi.objects), 10)
        MedadRangi.objects = []
    def test_initial(self):
        with(self.assertRaises(TypeError)):
            MedadRangi("A", 22.4j, "Iran", "c", 2)
        with(self.assertRaises(TypeError)):
            MedadRangi(12, 22.4, "Iran", "c", 2)
        self.assertEqual(MedadRangi.latitude, 51.50185488303431)
        self.assertEqual(MedadRangi.longitude, 35.74317403843504)
        self.assertEqual(MedadRangi.discount_rate, 10)
        MedadRangi.objects = []
    def test_final_price(self):
        MedadRangi.load_csv("data.csv")
        for i in range(1, 10):
            o = MedadRangi.objects[i]
            self.assertEqual((o.price-o.price*o.discount_rate/100)*o.count, o.final_price())
        MedadRangi.objects = []
    def test_calculate_distance(self):
        self.assertAlmostEqual(MedadRangi.calculate_distance(0, 0), 62, delta = 1)
if __name__ == '__main__':
    unittest.main()
