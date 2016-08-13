import requests
import os
import requests_cache
from bs4 import BeautifulSoup


class Restaurants:
    def __init__(self):
        self.list = [ZlatyKlas(),
                     Purtes(),
                     Formanka(),
                     Mediterane(),
                     ]


def get_restaurant(url):
    """
    Cache restaurant

    :return:    JSON with commits api
    """
    requests_cache.install_cache('restaurants_cache', expires_after=60 * 10)
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
        menu = soup.findAll("div", {"class": "jidelak"})[0].findAll("h2", {"class": "today"})
        for meal in menu:
            try:
                price = meal.findAll("span", {"class": "price"})[0].getText()
                name = meal.findAll("span", {"class": "name"})[0].getText()
                self.meals.append({"name": name, "price": price})

            except Exception as e:
                pass


class Formanka(Restaurant):
    name = "Formanka"
    url = "http://www.smichovskaformanka.cz/1-denni-menu"

    def parse_menu(self, r):
        soup = BeautifulSoup(r, "html.parser")
        row = soup.findAll("th")[0]
        for i in range(1, 7):
            new_row = row.findNext('tr')
            name = new_row.findAll('td')[0].text
            price = new_row.findAll('td')[1].text
            self.meals.append({"name": name, "price": price})
            row = new_row


class Purtes(Restaurant):
    name = "Purtes"
    url = "https://purtes.cz/cs/menu/todays-specials"

    def parse_menu(self, r):
        soup = BeautifulSoup(r, "html.parser")
        menu = soup.findAll("div", {"class": "food"})
        for meal in menu:
            name = meal.findAll("h5")[0].text
            price = meal.findAll("div", {"class": "price"})[0].text
            self.meals.append({"name": name, "price": price})


class Mediterane:
    name = "Mediterane"
    url = "https://developers.zomato.com/api/v2.1/dailymenu?res_id=16506335"

    def __init__(self):
        self.meals = []
        self.zomato()

    def zomato(self):
        headers = {"User-agent": "curl/7.43.0", 'user_key': os.environ.get('ZOMATO_KEY'), 'Accept': 'application/json'}
        requests_cache.install_cache('zomato_cache', expires_after=60 * 10)
        r = requests.get(self.url, headers=headers).json()
        for meal in r['daily_menus'][0]['daily_menu']['dishes']:
            name = meal['dish']['name']
            price = meal['dish']['price']
            self.meals.append({"name": name, "price": price})
