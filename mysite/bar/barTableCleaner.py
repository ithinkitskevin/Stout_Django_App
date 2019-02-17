from datetime import date, datetime, timedelta
import mysql.connector
import os
import operator
import json
from random import randint,choice
from datetime import datetime, timedelta
import databaseconfig as confg


class BarTableCleaner:

    def __init__(self):
        self.host=confg.confg['host']
        self.user=confg.confg['user']
        self.password=confg.confg['password']
        self.db = confg.confg['db']
    
    def getConn(self):
        conn = mysql.connector.connect(
                                        host=self.host,
                                        user=self.user,
                                        password=self.password,
                                        db = self.db)
        return conn

    def getAllBars(self):
        get_all_bars = ("SELECT * FROM Bars WHERE 1=1")
        conn = self.getConn()
        dbcursor = conn.cursor()
        dbcursor.execute(get_all_bars)

        result = dbcursor.fetchall()

        dbcursor.close()
        conn.close()

        return result

    def cleanBars(self, bars):
    
        cleanList = list()

        for bar in bars:
            cleanDict = {'name':'','license':'','phone_number':'','street':'','city':'','state':'','zip':''}
            cleanDict['license'] = bar[1]
            cleanDict['phone_number'] = bar[2].rstrip().lstrip()
            cleanDict['street'] = bar[3].rstrip().lstrip()
            cleanDict['city'] = bar[4].rstrip().lstrip()
            cleanDict['state'] = bar[5].rstrip().lstrip()
            cleanDict['zip'] = bar[6].rstrip().lstrip()
            cleanDict['name'] = " ".join(bar[0].split()).title()
            
            cleanList.append(cleanDict)
        
        return cleanList

    def updateTable(self, cleanBars):
        update = ("UPDATE Bars b SET name = '{0}',  license = '{1}', phone_number = '{2}',street = '{3}',city = '{4}',state = '{5}',zip = '{6}' WHERE b.license = '{1}';")
        conn = self.getConn()
        dbcursor = conn.cursor()
        for bar in cleanBars:
            print(bar)
    
            name = bar['name']
            barLicense = bar['license']
            phone_number = bar['phone_number']
            street = bar['street']
            city = bar['city']
            state = bar['state']
            zipcode = bar['zip']
            dbcursor.execute(update.format(name,barLicense,phone_number,street,city,state,zipcode))
            conn.commit()
        
        dbcursor.close()
        conn.close()


#Run Class
cleaner = BarTableCleaner()
cleaner.updateTable(cleaner.cleanBars(cleaner.getAllBars()))
