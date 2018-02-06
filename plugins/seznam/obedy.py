import requests
import os
import datetime
from bs4 import BeautifulSoup


MEAT_IDENTIFIERS = [
    'kuře', 'vepř', 'hově', 'bologne', 'boloň', 'krůt', 'maso', 'masem', 'šunk', 'slanin', 'salám', 'ančo', 'pstruh',
    'beef', 'kanč', 'kanec', ' medailon', 'vrabec', 'býč', 'býk', 'kachn', 'klobás', 'krkovič', 'tresk', 'pancett', 
    'špek', 'losos', 'svíč', 'králí', 'krkov', 'krevet', 'uzenin', 'slávk', 'telec', 'fish'
]


class Restaurants:
    def __init__(self):
        self.list = [Tradice(),
                     ZomatoRestaurant("Formanka", "16506447"),
                     ZlatyKlas(),
                     ZomatoRestaurant("Mediterane", "16506335"),
                     ZomatoRestaurant("Cyril's Pub", "16506663")
                     ]
        self.list = [restaurant for restaurant in self.list if restaurant.meals]


# noinspection PyUnresolvedReferences
class Restaurant:
    def __init__(self):
        web_content = requests.get(self.url).content
        self.meals = []
        self.parse_menu(web_content)

    def parse_menu(self, web_content):
        pass


class ZomatoRestaurant:
    def __init__(self, name, zomato_id):
        self.name = name
        self.zomato_id = zomato_id
        self.meals = []
        self.parse_menu()

    @property
    def url(self):
        return f'https://developers.zomato.com/api/v2.1/dailymenu?res_id={self.zomato_id}'

    def parse_menu(self):
        headers = {"User-agent": "curl/7.43.0", 'user_key': os.environ.get('ZOMATO_KEY'),
                   'Accept': 'application/json'}
        r = requests.get(self.url, headers=headers).json()
        try:
            for meal in r['daily_menus'][0]['daily_menu']['dishes']:
                name = meal['dish']['name']
                price = meal['dish']['price']
                if price:
                    self.meals.append(Meal(name, price))
        except (KeyError, IndexError):
                pass


class Meal:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    @property
    def is_vegetarian(self):
        for identifier in MEAT_IDENTIFIERS:
            if identifier in self.name.lower():
                return False

        return True


class ZlatyKlas(Restaurant):
    name = "Zlatý Klas"
    url = "http://www.zlatyklas.cz/index.php?sec=today-menu&lang=cz"

    def parse_menu(self, r):
        soup = BeautifulSoup(r, "html.parser")
        try:
            menu = soup.findAll("div", {"class": "jidelak"})[0].findAll("h2", {"class": "today"})
        except IndexError:
            return
        for meal in menu:
            try:
                price = meal.findAll("span", {"class": "price"})[0].getText()
                name = meal.findAll("span", {"class": "name"})[0].getText()
                self.meals.append(Meal(name, price))

            except IndexError:
                continue


class Tradice(Restaurant):
    name = "Tradice"
    url = "http://www.tradiceandel.cz/cz/denni-nabidka/"

    def parse_menu(self, r):
        days = [0, 6, 12, 18, 24]
        try:
            x = days[datetime.datetime.now().weekday()]
        except IndexError:
            return

        soup = BeautifulSoup(r, "html.parser")
        try:
            menu = soup.findAll("div", {"class": "menu"})[0].findAll("div", {"class": "item"})
        except IndexError:
            return
        for meal in menu[x:x+6]:
            try:
                price = meal.findAll("div", {"class": "price"})[0].getText()
                name = meal.findAll("strong")[0].getText()
                self.meals.append(Meal(name, price))

            except IndexError:
                continue


# TODO Il nostro (nema zomato daily menu)
