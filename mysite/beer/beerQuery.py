from datetime import date, datetime, timedelta
import mysql.connector
import os
import operator
import json
from random import randint,choice
from datetime import datetime, timedelta
from bar import databaseconfig as confg

def getAllItemNames():
    conn = mysql.connector.connect(
                                    host=confg.confg['host'],
                                    user=confg.confg['user'],
                                    password=confg.confg['password'],
                                    db = confg.confg['db'])
    dbcursor = conn.cursor()
    get_all_item_names = ("SELECT i.name FROM Items i WHERE 1=1")
    dbcursor.execute(get_all_item_names)
    item_name_tuple = dbcursor.fetchall()

    itemNames = list()
    for item in item_name_tuple:
        itemNames.append(item[0])

    dbcursor.close()
    conn.close()

    return itemNames
    


class Beer:

    def __init__(self, item_name):
        self.host=confg.confg['host']
        self.user=confg.confg['user']
        self.password=confg.confg['password']
        self.db = confg.confg['db']
        self.clean_item_name = self.cleanItemNameInput(item_name)
        self.not_found = 1 if self.setItemManf(self.clean_item_name) is None else 0


    def cleanItemNameInput(self, item_name):
        words = item_name.split()
        for i in range(len(words)):
            words[i] = words[i][0].upper()+words[i][1:len(words[i])]

        words = " ".join(words)
        return words

    def getConn(self):
        conn = mysql.connector.connect(
                                        host=self.host,
                                        user=self.user,
                                        password=self.password,
                                        db = self.db)
        return conn
    def setItemManf(self, item_name):
        get_item_manf = ("SELECT i.manf FROM Items i WHERE i.name = '{0}'")
        conn = self.getConn()
        dbcursor = conn.cursor()
        dbcursor.execute(get_item_manf.format(str(item_name)))
        manf_tuple = dbcursor.fetchall()
        if not manf_tuple:
            dbcursor.close()
            conn.close()
            return None
        else:
            self.manf = manf_tuple[0][0]
            dbcursor.close()
            conn.close()
            return 1
    # WANT: barname where beer sells most, item_sold -> t_id:license
    def getTopSold(self):
        conn = self.getConn()
        dbcursor = conn.cursor()

        get_bar_sold = ("SELECT b.name, t.license FROM Transactions t, Items_Sold i, Bars b WHERE i.item = '{0}' and i.transaction = t.t_id and t.license = b.license")
        dbcursor.execute(get_bar_sold.format(self.clean_item_name))
        bars_sold = dbcursor.fetchall()

        bar_count = {}

        for bar in bars_sold:
            if bar[0] not in bar_count:
                bar_count[bar[0]] = 1
            else:
                bar_count[bar[0]] += 1

        top_performers = {'bar' : list(), 'amount_sold': list()}
        for i in range(10):

            if bar_count:
                bar_highest = max(bar_count.items(), key=operator.itemgetter(1))
                bar_key = bar_highest[0]
                bar_value = bar_highest[1]
                del bar_count[bar_key]
                top_performers['bar'].append(bar_key)
                top_performers['amount_sold'].append(bar_value)

        return top_performers

    def getTopConsumers(self):
        conn = self.getConn()
        dbcursor = conn.cursor()

        get_consumers = ("SELECT d.first_name, d.last_name, t.d_id FROM Transactions t, Items_Sold i, Drinkers d WHERE i.item = '{0}' and i.transaction = t.t_id and t.d_id = d.d_id")
        dbcursor.execute(get_consumers.format(self.clean_item_name))
        consumers = dbcursor.fetchall()

        consumer_count = {}

        for consumer in consumers:

            name = " ".join([str(consumer[0]).rstrip() , str(consumer[1]).rstrip()])
            if name not in consumer_count:
                consumer_count[name] = 1
            else:
                consumer_count[name] += 1

        top_performers = {'drinker_name' : list(), 'amount_consumed': list()}
        for i in range(10):

            if consumer_count:
                consumer_highest = max(consumer_count.items(), key=operator.itemgetter(1))
                consumer_key = consumer_highest[0]
                consumer_value = consumer_highest[1]
                del consumer_count[consumer_key]
                top_performers['drinker_name'].append(consumer_key)
                top_performers['amount_consumed'].append(consumer_value)
        
        return top_performers

    def getSalesByTime(self):
        conn = self.getConn()
        dbcursor = conn.cursor()

        get_bar_transactions = ("SELECT t.date, t.time FROM Transactions t, Items_Sold i WHERE i.item = '{0}' and i.transaction = t.t_id ")
        dbcursor.execute(get_bar_transactions.format(self.clean_item_name))
        sale_times = dbcursor.fetchall()

        output = {'weekday': list(),'hour':list()}
        for i in range(24):
            output['hour'].append(i)
        output['hour_sold'] = [0]*24
        output['day_sold'] = [0]*7
        output['weekday'].append('Monday')
        output['weekday'].append('Teusday')
        output['weekday'].append('Wednsday')
        output['weekday'].append('Thursday')
        output['weekday'].append('Friday')
        output['weekday'].append('Saturday')
        output['weekday'].append('Sunday')

        for time in sale_times:
            date = time[0].weekday()
            hour = time[1].seconds//3600

            output['day_sold'][date] += 1 
            output['hour_sold'][hour] += 1 
        
        return output