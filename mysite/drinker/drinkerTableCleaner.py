from datetime import date, datetime, timedelta
import mysql.connector
import os
import operator
import json
from random import randint,choice
from datetime import datetime, timedelta
import databaseconfig as confg


class DrinkerTableCleaner:

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

    def getAllDrinkers(self):
        get_all_drinkers = ("SELECT * FROM Drinkers WHERE 1=1")
        conn = self.getConn()
        dbcursor = conn.cursor()
        dbcursor.execute(get_all_drinkers)

        result = dbcursor.fetchall()

        dbcursor.close()
        conn.close()

        return result

    def cleanDrinkers(self, drinkers):
    
        cleanList = list()

        for drinker in drinkers:
            cleanDict = {'d_id':'','first_name':'','last_name':'','phone_number':'','street':'','city':'','state':'','zip':''}
            
            cleanDict['d_id'] = drinker[0]
            cleanDict['first_name'] = drinker[1].rstrip().lstrip()
            cleanDict['last_name'] = drinker[2].rstrip().lstrip()
            cleanDict['phone_number'] = drinker[3].rstrip().lstrip()
            cleanDict['street'] = drinker[4].rstrip().lstrip()
            cleanDict['city'] = drinker[5].rstrip().lstrip()
            cleanDict['state'] = drinker[6].rstrip().lstrip()
            cleanDict['zip'] = drinker[7].rstrip().lstrip()
            
            cleanList.append(cleanDict)
        
        return cleanList

    def updateTable(self, cleanDrinkers):
        update = ('UPDATE Drinkers d SET d_id = {0}, first_name = "{1}",  last_name = "{2}", phone_number = "{3}",street = "{4}",city = "{5}",state = "{6}",zip = "{7}" WHERE d.d_id = {0};')
        conn = self.getConn()
        dbcursor = conn.cursor()
        for drinker in cleanDrinkers:
            print(drinker)

            d_id = drinker['d_id']
            first_name = drinker['first_name']
            last_name = drinker['last_name']
            phone_number = drinker['phone_number']
            street = drinker['street']
            city = drinker['city']
            state = drinker['state']
            zipcode = drinker['zip']
            dbcursor.execute(update.format(d_id, first_name, last_name, phone_number, street, city, state, zipcode))
            conn.commit()
        
        dbcursor.close()
        conn.close()


#Run Class
cleaner = DrinkerTableCleaner()
cleaner.updateTable(cleaner.cleanDrinkers(cleaner.getAllDrinkers()))
