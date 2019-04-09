import sqlite3

def show_rests():
    conn = sqlite3.connect('menu.db')
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    all = c.fetchall()
    lst = list()
    for e in all:
        e = e[0]
        if e != "Cart":
            lst.append(e)
    return lst

def show_menu(rest):
    conn = sqlite3.connect('menu.db')
    c = conn.cursor()
    queryvar = "SELECT dish FROM " + rest
    c.execute(queryvar)
    all = c.fetchall()
    lst = list()
    for e in all:
        e = e[0]
        lst.append(e)
    return lst

def show_descr(rest, item):
    conn = sqlite3.connect('menu.db')
    c = conn.cursor()
    queryvar = "SELECT description FROM " + rest + " WHERE dish =:dish"
    c.execute(queryvar, {"dish" :item})
    all = c.fetchall()
    lst = list()
    for e in all:
        e = e[0]
        lst.append(e)
    return lst[0]


def show_photo(rest, item):
    conn = sqlite3.connect('menu.db')
    c = conn.cursor()
    queryvar = "SELECT picture FROM " + rest + " WHERE Dish =:dish"
    c.execute(queryvar, {"dish" :item})
    all = c.fetchall()
    lst = list()
    for e in all:
        e = e[0]
        lst.append(e)
    return lst[0]


def addtocart(id, item):
    conn = sqlite3.connect('menu.db')
    c = conn.cursor()
    queryvar = "INSERT INTO cart VALUES(?,?)"
    c.execute(queryvar, (id, item))
    conn.commit()



def showcart(id):
    conn = sqlite3.connect('menu.db')
    c = conn.cursor()
    queryvar = "SELECT Dish FROM cart WHERE user =:user"
    c.execute(queryvar, {"user" :id})
    return c.fetchall()


def empty_cart(id):
    conn = sqlite3.connect('menu.db')
    c = conn.cursor()
    queryvar = "DELETE from cart WHERE user =:user"
    c.execute(queryvar, {"user" :id})
    conn.commit()

def send_order(id):
    pass

def record_location(id,lat,lng):
    conn = sqlite3.connect('menu.db')
    c = conn.cursor()
    queryvar = "SELECT Dish FROM cart WHERE user =:user"
    users = []




class MenuItem():
    def __init__(self,name,price):
        self.name = name
        self.amount = amount



class CartItem():
    def __init__(self,name,amount):
        self.name = name
        self.amount = amount
    def add(name,amount):
        pass


class Cart():
    def __init__(self,list):
        self.list = list
