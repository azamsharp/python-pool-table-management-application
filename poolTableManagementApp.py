import os
import time
import json
import csv
import datetime
import cPickle as pickle


class poolTable:
    def __init__(self, poolTableNumber, startDateTime, endDateTime):
        self.poolTableNumber = poolTableNumber
        self.startDateTime = startDateTime
        self.endDateTime = endDateTime

    def toDictionary(self):
        return{"PoolTableID":self.poolTableNumber, "Start-Date-Time":self.startDateTime,"End-Date-Time":self.endDateTime}

    def toString(self):
        return "Pool Table # " + str(self.poolTableNumber) + ";" + "Start Time: " + str(datetime.datetime.fromtimestamp(self.startDateTime))+";" + "End Time: " + str(datetime.datetime.fromtimestamp(self.endDateTime))

filename = 'poolTableManagement.json'

tables = []
tableAvailable=True
tableExist=False
fileExist=False

while True:

    with open(filename) as file_object:
         tableArray= json.load(file_object)

    input_options = raw_input("\nplease choose what you want to do: \n '1' Table checkin\n '2' Table checkout\n '3' View current occupied tables\n 'q' Quit the program\n")

    if input_options == "1":
        poolNumber = raw_input("please enter the table number you want to checkin(1 to 12)\n")
        if int(poolNumber) > 12 or int(poolNumber)<1:
            tableAvailable=False
            print("you have entered a wrong number, please enter a number between 1 and 12")

        else:
            for element in tableArray:
                if poolNumber == element["PoolTableID"]:
                    tableAvailable=False
                    print("Table {} is currenly occupied, please select another table".format(poolNumber))
                    break

        if tableAvailable:
            date_time=datetime.datetime.now()
            timestamp = time.mktime(date_time.timetuple())
            table=poolTable(poolNumber, timestamp, "")
            tableArray.append(table.toDictionary())
            with open(filename,"w") as file_object:
                 json.dump(tableArray,file_object)
            print("The pool table {} has been checkedin, and the start time is {} ".format(poolNumber, date_time))


    elif input_options == "2":
        removePoolNumber = raw_input("please enter the table number you want to check out\n")
        for element in tableArray:
            if removePoolNumber == element["PoolTableID"]:
                tableExist=True
                tableRemove = poolTable(element["PoolTableID"], element["Start-Date-Time"], element["End-Date-Time"])
                tableArray.remove(element)

            else:
                tableExist=False

        if tableExist:
            with open(filename,"w") as file_object:
                 json.dump(tableArray,file_object)
            date_time1=datetime.datetime.now()
            timestamp1 = time.mktime(date_time1.timetuple())
            tableRemove.endDateTime=timestamp1
            totalTime=round((tableRemove.endDateTime-tableRemove.startDateTime)/60)
            charge = 0.08*totalTime

            print("Table {}: Check-in time: {} \n Check-out time: {} \n Total time: {} min\n Charge per min: $0.08\n Total charge: ${}".format(tableRemove.poolTableNumber, datetime.datetime.fromtimestamp(tableRemove.startDateTime), datetime.datetime.fromtimestamp(tableRemove.endDateTime), totalTime, charge))

            filename1 = '{}.txt'.format(datetime.datetime.now().date())
            f = open(filename1, 'a')

            with open(f.name,'a') as text_file:
                text_file.write(tableRemove.toString()+"charge per min:0.08"+"Total charge:"+str(charge)+"\n")

        else:
            print("Table {} is not in system".format(removePoolNumber))

    elif input_options == "3":
        with open(filename) as file_object:

             tableArray= json.load(file_object)
             for element in tableArray:
                 t = poolTable(element["PoolTableID"], element["Start-Date-Time"], element["End-Date-Time"])
                 print("Table {} was checked in at {} ".format(t.poolTableNumber, datetime.datetime.fromtimestamp(t.startDateTime)))

    elif input_options == "q":
        break
