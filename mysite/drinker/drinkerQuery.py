from datetime import date, datetime, timedelta
import mysql.connector
import os
from math import ceil
import operator
import json
from random import randint,choice
from datetime import datetime, timedelta
from drinker import databaseconfig as confg

get_all_drinkers = ("SELECT d.d_id, d.first_name, d.last_name FROM Drinkers d")

get_drinker_id = ("SELECT d.d_id FROM Drinkers d",
                "WHERE d.first_name = '%s' AND d.last_name = '%s' ")

get_transactions = ("SELECT t.date, t.license FROM Transactions t WHERE t.d_id = {0};")
get_price_barlicense = ("SELECT t.date, (t.total_price + t.tip), t.license FROM Transactions t WHERE t.d_id = {0};")
get_bar_name_from_license = ("select name from Bars where license = '%s';")
get_most_ordered_item = (
    "select count(*), i.item from Items_Sold i "
    "where i.transaction in "
    "(select t.t_id from Transactions t where t.d_id = {0})"
    " group by i.item order by count(*) desc;"
)
get_bar_name = ("SELECT b.name from Bars b where b.license = '{0}';")

global_host = global_user = global_password = global_db = None

def getAllDrinkerNames():
    conn = mysql.connector.connect(
                                    host=confg.confg['host'],
                                    user=confg.confg['user'],
                                    password=confg.confg['password'],
                                    db = confg.confg['db'])
    dbcursor = conn.cursor()
    get_all_drinker_names = ("SELECT d.first_name, d.last_name FROM Drinkers d WHERE 1=1")
    dbcursor.execute(get_all_drinker_names)
    drinker_name_tuple = dbcursor.fetchall()

    drinkerNames = list()
    for drinker in drinker_name_tuple:
        drinkerNames.append(drinker[0]+" "+drinker[1])

    dbcursor.close()
    conn.close()

    return drinkerNames

class Drinker:

    def __init__(self, drinker_name):
        self.host=confg.confg['host']
        self.user=confg.confg['user']
        self.password=confg.confg['password']
        self.db = confg.confg['db']
        self.clean_drinker_name = self.cleanDrinkerNameInput(drinker_name)
        self.not_found = 1 if self.setDrinkerId(self.clean_drinker_name) is None else 0
    
    def cleanDrinkerNameInput(self, drinker_name):
        words = " ".join(drinker_name.split())
        words = words.title()

        return words

    def getConn(self):
        conn = mysql.connector.connect(
                                        host=self.host,
                                        user=self.user,
                                        password=self.password,
                                        db = self.db)
        return conn

    def setDrinkerId(self, drinker_name):
        if len(drinker_name.split())<2:
            return None
        get_drinker_id = ("SELECT d.d_id FROM Drinkers d WHERE d.first_name = '{0}' and d.last_name = '{1}'")
        conn = self.getConn()
        dbcursor = conn.cursor()
        first = drinker_name.split()[0]
        last = drinker_name.split()[1]
        dbcursor.execute(get_drinker_id.format(first,last))
        d_id_tuple = dbcursor.fetchall()
        if not d_id_tuple:
            dbcursor.close()
            conn.close()
            return None
        elif len(d_id_tuple)>1:
            self.d_id = d_id_tuple[0][0]
            print(self.d_id)
            dbcursor.close()
            conn.close()
            return 0
            #IF MULTIPLE PEOPLE WITH THE SAME NAME EXIST, RETURN ALL INFO ON THOSE PEOPLE, AND DISPLAY OPTIONS
            #ALERT WARNING

        else:
            self.d_id = d_id_tuple[0][0]
            print(self.d_id)
            dbcursor.close()
            conn.close()
            return 1
    def getDrinkersTransactions(self):
        conn = self.getConn()
        dbcursor = conn.cursor()

        get_transactions = ("SELECT * FROM Transactions t WHERE t.d_id = '{0}' order by t.date desc;")
        dbcursor.execute(get_transactions.format(self.d_id))
        transactions_tuple = dbcursor.fetchall()
        transactions_by_bar_license = {}
        items_on_transaction = {}

        for transaction in transactions_tuple:
            bar_license = transaction[7]

            transaction_entry = {}
            transaction_entry['t_id'] = transaction[0]
            transaction_entry['date'] = transaction[1]
            transaction_entry['time'] = transaction[2]
            transaction_entry['weekday'] = transaction[3]
            transaction_entry['total_price'] = transaction[4]
            transaction_entry['tip'] = transaction[5]
            transaction_entry['d_id'] = transaction[6]
            transaction_entry['license'] = transaction[7]

            if bar_license not in transactions_by_bar_license:
                transactions_by_bar_license[bar_license] = list()
            
            transactions_by_bar_license[bar_license].append(transaction_entry)

            #Build Dict key = t_id, value = list of items on order
            transaction_key = transaction[0]
            get_items_sold = ("SELECT * FROM Items_Sold i WHERE i.transaction = '{0}';")
            dbcursor.execute(get_items_sold.format(transaction_key))
            items_tuple = dbcursor.fetchall()
            
            for item in items_tuple:
                items = {}
                if transaction_key not in items_on_transaction:
                    items_on_transaction[transaction_key] = list()
                items['item'] = item[1]
                items['price'] = item[2]
                items_on_transaction[transaction_key].append(items)

            


        #Find Barname for the item
        bar_name_transactions = {}
        for bar_license, transactions in transactions_by_bar_license.items():
            get_bar = ("SELECT b.name FROM Bars b WHERE b.license = \"{0}\";")
            dbcursor.execute(get_bar.format(bar_license))
            bar = dbcursor.fetchall()
            bar_name = bar[0][0]
            bar_name_transactions[bar_name] = transactions


        dbcursor.close()
        conn.close()

        return [bar_name_transactions,items_on_transaction]


def initialize():
    global global_host
    global global_user
    global global_password
    global global_db

    path_to_json = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config.json')

    f = open(path_to_json, "r")
    contents = f.read()
    confdata = json.loads(contents)
    conn_info = confdata.get("conn_info")  
    
    global_host = conn_info.get("host")
    global_user = conn_info.get("user")
    global_password = conn_info.get("password")
    global_db = conn_info.get("db")


def getAllDrinker():
    if global_host is None or global_user is None or global_password is None or global_db is None:
        initialize()
        
    conn = mysql.connector.connect(
        host=global_host,
        user=global_user,
        password=global_password,
        db = global_db
    )
    dbcursor = conn.cursor()

    dbcursor.execute(get_all_drinkers)
    drinker_list = dbcursor.fetchall()

    dbcursor.close()
    conn.close()

    return drinker_list

def getIdFromName(full_name):
    drinker_list = getAllDrinker()

    first, last = getFirstLast(full_name)
    if first is None or last is None:
        return None

    d_id = 0
    for drinker_data in drinker_list:
        if drinker_data[1].strip() == first and drinker_data[2].strip() == last:
            d_id = drinker_data[0]
            break

    if d_id == 0:
        return None

    return d_id


def getSpendingFromName(name):
    ''' Returns total_price, tip, and the license. 
        Use this to see his/her spending in different bars, on different dates/weeks/months.      
        NOT ORDERED YET
    '''
    if global_host is None or global_user is None or global_password is None or global_db is None:
        initialize()

    conn = mysql.connector.connect(
        host=global_host,
        user=global_user,
        password=global_password,
        db = global_db
    )

    d_id = getIdFromName(name)
    if d_id is None:
        return None

    dbcursor = conn.cursor()
    dbcursor.execute(get_price_barlicense.format(str(d_id)))
    transaction = dbcursor.fetchall()

    transaction.sort(key = lambda x : x[0])

    dbcursor.close()
    conn.close()

    return transaction

def getFinalTransaction(name):
    if global_host is None or global_user is None or global_password is None or global_db is None:
        initialize()

    conn = mysql.connector.connect(
        host=global_host,
        user=global_user,
        password=global_password,
        db = global_db
    )

    raw_list = getTransactionFromName(name)
    if raw_list is None:
        return None
    bar_map = {}
    for data in raw_list:
        lic = data[1]
        date = data[0]
        if lic in bar_map:
            count, prev_date = bar_map[lic]
            if prev_date < date:
                prev_date = date
            count += 1
            bar_map[lic] = (count, prev_date)
        else:
            bar_map[lic] = (1, date)

    sorted_dict = sorted(bar_map.items(), key=lambda x: x[1][1], reverse=True)
    print(sorted_dict)

    final_dict = {}
    dbcursor = conn.cursor()
    for sd in sorted_dict:
        # print(get_bar_name.format(str(sd[0])))
        dbcursor.execute(get_bar_name.format(str(sd[0])))
        new_key = dbcursor.fetchall()
        new_final_key = " ".join(new_key[0][0].split())
        # print(bar_map[sd[0]])
        count, date = bar_map[sd[0]]
        final_dict[new_final_key] = (count, date.strftime('%m/%d/%y'))

    dbcursor.close()
    conn.close()
    
    return final_dict

def getFirstLast(full_name):
    first, last = full_name.split(" ")
    if first == "" or last == "":
        return (None, None)
    return first, last

def getMostItemsOrderedFromName(name):
    if global_host is None or global_user is None or global_password is None or global_db is None:
        initialize()

    conn = mysql.connector.connect(
        host=global_host,
        user=global_user,
        password=global_password,
        db = global_db
    )

    d_id = getIdFromName(name)
    if d_id is None:
        return None

    dbcursor = conn.cursor()
    dbcursor.execute(get_most_ordered_item.format(str(d_id)))
    transaction = dbcursor.fetchall()
    
    dbcursor.close()
    conn.close()

    return transaction

def getFinalSpending(name):
    raw_spending_list = getSpendingFromName(name)
    if raw_spending_list is None:
        return None
    
    date_map = {}
    week_map = {}
    month_map = {}
    for spending_data in raw_spending_list:
        date = spending_data[0]
        money = spending_data[1]
        lice = spending_data[2]
        # First date
        true_date = date.strftime('%m/%d/%Y')
        if true_date in date_map:
            tmp = date_map[true_date]
            tmp += money
            date_map[true_date] = tmp
        else:
            date_map[true_date] = money
        
        # Week
        week = week_of_month(date)
        if week in week_map:
            tmp = week_map[week]
            tmp += money
            week_map[week] = tmp
        else:
            week_map[week] = money

        month = date.month
        if month in month_map:
            tmp = month_map[month]
            tmp += money
            month_map[month] = tmp
        else:
            month_map[month] = money

    return date_map, week_map, month_map

def week_of_month(dt):
    first_day = dt.replace(day=1)

    dom = dt.day
    adjusted_dom = dom + first_day.weekday()

    return int(ceil(adjusted_dom/7.0))