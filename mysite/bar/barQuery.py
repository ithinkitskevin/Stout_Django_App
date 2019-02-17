from datetime import date, datetime, timedelta
import mysql.connector
import os
import operator
import json
from random import randint,choice
from datetime import datetime, timedelta
from bar import databaseconfig as confg

def getAllBarNames():
    conn = mysql.connector.connect(
                                    host=confg.confg['host'],
                                    user=confg.confg['user'],
                                    password=confg.confg['password'],
                                    db = confg.confg['db'])
    dbcursor = conn.cursor()
    get_all_bar_names = ("SELECT b.name FROM Bars b WHERE 1=1")
    dbcursor.execute(get_all_bar_names)
    bar_name_tuple = dbcursor.fetchall()

    barNames = list()
    for bar in bar_name_tuple:
        barNames.append(bar[0])

    dbcursor.close()
    conn.close()

    return barNames

class Bar:

    def __init__(self, bar_name):
        self.host=confg.confg['host']
        self.user=confg.confg['user']
        self.password=confg.confg['password']
        self.db = confg.confg['db']
        self.clean_bar_name = self.cleanBarNameInput(bar_name)
        self.not_found = 1 if self.setBarLicense(self.clean_bar_name) is None else 0
    
    def cleanBarNameInput(self, bar_name):
        words = " ".join(bar_name.split())
        words = words.title()

        return words

    def getConn(self):
        conn = mysql.connector.connect(
                                        host=self.host,
                                        user=self.user,
                                        password=self.password,
                                        db = self.db)
        return conn
    def setBarLicense(self, bar_name):
        get_bar_license = ("SELECT b.license FROM Bars b WHERE b.name = '{0}'")
        conn = self.getConn()
        dbcursor = conn.cursor()
        dbcursor.execute(get_bar_license.format(str(bar_name)))
        license_tuple = dbcursor.fetchall()
        if not license_tuple:
            dbcursor.close()
            conn.close()
            return None
        else:
            self.license = license_tuple[0][0]
            print(self.license)
            dbcursor.close()
            conn.close()
            return 1

    def getTopBarTransactions(self):
        conn = self.getConn()
        dbcursor = conn.cursor()

        get_bar_transactions = ("SELECT d_id, sum(t.total_price) FROM Transactions t WHERE t.license = '{0}' GROUP BY d_id ORDER BY sum(t.total_price) desc limit 10")
        dbcursor.execute(get_bar_transactions.format(self.license))
        top_10_tuple = dbcursor.fetchall()
        
        top_10 = { "d_id": list() , "total": list(), "name": list()}
        for drinker in top_10_tuple:
            get_drinkers_name = ("SELECT d.first_name, d.last_name FROM Drinkers d WHERE d.d_id = {0};")
        
            dbcursor.execute(get_drinkers_name.format(int(drinker[0])))
            name = dbcursor.fetchall()
         
            top_10["d_id"].append(int(drinker[0]))
            top_10["total"].append(float(drinker[1]))
            top_10["name"].append(" ".join([str(name[0][0]).rstrip() , str(name[0][1]).rstrip()]))
        
        dbcursor.close()
        conn.close()

        return top_10
        
        #Clean Bar Name
        #" ".join(name.split())
        #
    
    def getTopItems(self):
        conn = self.getConn()
        dbcursor = conn.cursor()

        get_items_sold = ("SELECT i.item FROM Transactions t, Items_Sold i WHERE t.license = '{0}' and i.transaction = t.t_id;")
        dbcursor.execute(get_items_sold.format(self.license))
        items_sold = dbcursor.fetchall()
        item_count = {}

        for item in items_sold:
            if item[0] not in item_count:
                item_count[item[0]] = 1
            else:
                item_count[item[0]] += 1

        #Find Manf for the item
        manf_count = {}
        for item, count in item_count.items():
            get_manf = ("SELECT i.manf FROM Items i WHERE i.name = \"{0}\";")
            dbcursor.execute(get_manf.format(item))
            manf = dbcursor.fetchall()
            manf = manf[0][0]
            if manf not in manf_count:
                manf_count[manf] = count
            else:
                manf_count[manf] += count
        
            
        
        top_performers = {'item' : list(), 'item_sold': list(), 'manf' : list(), 'manf_sold': list()}
        for i in range(10):

            if manf_count:
                manf_highest = max(manf_count.items(), key=operator.itemgetter(1))
                manf_key = manf_highest[0]
                manf_value = manf_highest[1]
                del manf_count[manf_key]
                top_performers['manf'].append(manf_key)
                top_performers['manf_sold'].append(manf_value)
            
            if item_count:
                item_highest = max(item_count.items(), key=operator.itemgetter(1))
                item_key = item_highest[0]
                item_value = item_highest[1]
                del item_count[item_key]
                top_performers['item'].append(item_key)
                top_performers['item_sold'].append(item_value)
        
        dbcursor.close()
        conn.close()
        return top_performers

    def getSalesByTime(self):
        conn = self.getConn()
        dbcursor = conn.cursor()

        get_bar_transactions = ("SELECT t.date, t.time FROM Transactions t WHERE t.license = '{0}';")
        dbcursor.execute(get_bar_transactions.format(self.license))
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

    def insertTransaction(self, total_amount, tip, date, time, d_id, weekday, bar_license):
        conn = self.getConn()
        dbcursor = conn.cursor()

        get_items_sold = ("INSERT INTO Transactions "
                            "(t_id,date,time,weekday,total_price,tip,d_id,license)"
                            "VALUES (DEFAULT,{0},{1},'{2}',{3},{4},'{5}','{6}');")
        dbcursor.execute(get_items_sold.format(date,time,weekday,total_amount,tip,d_id,bar_license))
    def checkTransactionTime(self, day, time):

        conn = self.getConn()
        dbcursor = conn.cursor()

        get_bar_transactions = ("SELECT h.open_hour, h.close_hour FROM Hours h WHERE h.day = '{0}' and h.bar_license = '{1}';")
        dbcursor.execute(get_bar_transactions.format(day,self.license))
        hours = dbcursor.fetchall()

    def prepareTransaction(self, total_amount, tip, d_id):

        
        date = datetime.now().date()
        weekday = date.weekday()
        time = datetime.now().time()
        #TODO: GET HOURS FOR BAR THEN CHECK IF OPEN

        self.insertTransaction(total_amount, tip, date, time, d_id, weekday, self.license)