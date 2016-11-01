import requests
import os
from itertools import tee
import requests_cache
from bs4 import BeautifulSoup


class Restaurants:
    def __init__(self):
        self.list = [Tradice(),
                     Formanka(),
                     ZlatyKlas(),
                     Mediterane(),
                     Cyril()
                     ]


def get_restaurant(url):
    """
    Cache restaurant

    :return:    JSON with commits api
    """
    requests_cache.install_cache('restaurants_cache', expires_after=10)
    r = requests.get(url)
    return r.content


# noinspection PyUnresolvedReferences
class Restaurant:
    def __init__(self):
        r = get_restaurant(self.url)
        self.meals = []
        self.parse_menu(r)


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
                self.meals.append({"name": name, "price": price})

            except IndexError:
                continue


class Tradice(Restaurant):
    name = "Tradice"
    url = "http://www.tradiceandel.cz/cz/denni-nabidka/"

    def parse_menu(self, r):
        soup = BeautifulSoup(r, "html.parser")
        try:
            menu = soup.findAll("div", {"class": "menu"})[0].findAll("div", {"class": "item"})
        except IndexError:
            return
        for meal in menu[:6]:
            try:
                price = meal.findAll("div", {"class": "price"})[0].getText()
                name = meal.findAll("strong")[0].getText()
                self.meals.append({"name": name, "price": price})

            except IndexError:
                continue


class Formanka(Restaurant):
    name = "Formanka"
    url = "http://www.smichovskaformanka.cz/2-denni-menu"

    def parse_menu(self, r):
        soup = BeautifulSoup(r, "html.parser")
        try:
            row = soup.findAll("th")[0]
        except IndexError:
            return
        for i in range(1, 7):
            new_row = row.findNext('tr')
            name = new_row.findAll('td')[0].text
            price = new_row.findAll('td')[1].text
            self.meals.append({"name": name, "price": price})
            row = new_row


class Cyril(Restaurant):
    name = "Cyril's pub"
    url = "http://www.cyrilspub.cz/denni-menu/"

    def parse_menu(self, r):
        soup = BeautifulSoup(r, "html.parser")
        try:
            menu = soup.findAll("table")[0].findAll("td")
            menu = [menu[i:i+2] for i in range(0, len(menu), 2)]
        except IndexError:
            return
        for name, price in menu:
            name = name.getText()
            price = price.getText()
            if name not in ("DENNÍ MENU", "TÝDENNÍ POLEDNÍ NABÍDKA"):
                self.meals.append({"name": name, "price": price})


class Mediterane:
    name = "Mediterane"
    url = "https://developers.zomato.com/api/v2.1/dailymenu?res_id=16506335"

    def __init__(self):
        self.meals = []
        self.zomato()

    def zomato(self):
        headers = {"User-agent": "curl/7.43.0", 'user_key': os.environ.get('ZOMATO_KEY'), 'Accept': 'application/json'}
        requests_cache.install_cache('zomato_cache', expires_after=60)
        r = requests.get(self.url, headers=headers).json()
        try:
            for meal in r['daily_menus'][0]['daily_menu']['dishes']:
                name = meal['dish']['name']
                price = meal['dish']['price']
                self.meals.append({"name": name, "price": price})
        except KeyError:
            pass


def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)
