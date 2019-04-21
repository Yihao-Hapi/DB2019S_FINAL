import psycopg2
import psycopg2.extras
import csv
import os
import Utils
from datetime import datetime

if __name__ == '__main__':

    conn = psycopg2.connect("dbname = 'postgres' user = 'postgres'")
    cur = conn.cursor()

    paymentFile = "DATA/Payment_and_value_of_care_-_Hospital.csv"
    compFile = "DATA/Complications_and_Deaths_-_Hospital.csv"

    #To ensure idempotent behavior, wipe the tables at the start
    cur.execute("DELETE FROM hospital;")
    cur.execute("DELETE FROM hospital_payment;")
    cur.execute("DELETE FROM hospital_comp;")
    cur.execute("DELETE FROM city;")
    cur.execute("DELETE FROM payment;")
    cur.execute("DELETE FROM complication;")
    cur.execute("DELETE FROM time_range;")
    conn.commit()

    #Now populate the tables
    hospitalCols = [0,1,2,5,7] #providerID, hospitalName, address, zip, phone (COMP FILE)
    hospPayCols = [0,9,12,13,14,11,10] #providerID, paymentID, paymentAmount, payLow, payHigh, quantity, compare (PAYMENT FILE)
    hospCompCols = [0,9,12,13,14,11,10] #providerID, measureID, compScore, compLow, compHigh, quantity, compare (COMP FILE)
    cityCols = [3,6,5,4] #cityName, countyName, zip, stateName (EITHER FILE)
    paymentCols = [9,8] #paymentID, paymentDesc (PAYMENT FILE)
    compCols = [9,8] #measureID, measureDesc (COMP FILE)
    trCols = [16,17,0] #dateStart, dateEnd, providerID (COMP FILE)

    with open(compFile,'r') as cf:
        next(cf) #skip the header
        reader = csv.reader(cf)
        for row in reader:
            info1 = list(row[a] for a in hospitalCols)

            info2 = list(row[b] for b in hospCompCols)
            #Corrections for data types for hospital_comp
            try:
                holder = float(info2[2])
            except ValueError:
                continue #if no score, exlude it
            try:
                holder = float(info2[3])
            except ValueError:
                info2[3] = -1.0
            try:
                holder = float(info2[4])
            except ValueError:
                info2[4] = -1.0
            try:
                holder = int(info2[5])
            except ValueError:
                info2[5] = -1


            info3 = list(row[c] for c in cityCols)
            info4 = list(row[d] for d in compCols)
            info5 = list(row[e] for e in trCols)

            cur.execute("INSERT INTO hospital VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;", (str(info1[0]),str(info1[1]),str(info1[2]),str(info1[3]),str(info1[4])))
            cur.execute("INSERT INTO hospital_comp VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;", (str(info2[0]),str(info2[1]), str(info2[2]),str(info2[3]), \
                                                                                                                  str(info2[4]),str(info2[5]),str(info2[6])))
            cur.execute("INSERT INTO city VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING;",(str(info3[0]),str(info3[1]),str(info3[2]),str(info3[3])))
            cur.execute("INSERT INTO complication VALUES (%s, %s) ON CONFLICT DO NOTHING;", (str(info4[0]),str(info4[1])))
            
            #parse date: str -> timestamp
            dStart = datetime.strptime(str(info5[0]), "%m/%d/%Y")
            dEnd = datetime.strptime(str(info5[1]), "%m/%d/%Y")
            cur.execute("INSERT INTO time_range VALUES (%s, %s, %s) ON CONFLICT DO NOTHING;", (dStart,dEnd,str(info5[2])))

    with open(paymentFile,'r') as pf:
        next(pf) #skip the header
        reader = csv.reader(pf)
        for row in reader:
            #Corrections for data types for hospital_payment
            info6 = list(row[f] for f in hospPayCols)
            info6[2] = info6[2][1:]
            info6[2]= info6[2].replace(",","")

            info6[3] = info6[3][1:]
            info6[3] = info6[3].replace(",","")

            info6[4] = info6[4][1:]
            info6[4] = info6[4].replace(",","")

            info6[5] = info6[5][1:]
            info6[5] = info6[5].replace(",","")
            try:
                holder = int(info6[2])
            except ValueError:
                continue #if no payment, exclude it
            try:
                holder = int(info6[3])
            except ValueError:
                info6[3] = -1
            try:
                holder = int(info6[4])
            except ValueError:
                info6[4] = -1
            try:
                holder = int(info6[5])
            except ValueError:
                info6[5] = -1
            info7 = list(row[g] for g in paymentCols)

            cur.execute("INSERT INTO payment VALUES (%s, %s) ON CONFLICT DO NOTHING;", (str(info7[0]),str(info7[1])))

            if str(info6[4]) != str(-1):
                cur.execute("INSERT INTO hospital_payment VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;", (str(info6[0]),str(info6[1]), str(info6[2]),str(info6[3]), \
                                                                                                                    str(info6[4]),str(info6[5]),str(info6[6])))





    conn.commit()
