from enum import Enum

"""
Use functions in this module to 
manipulate repeating actions on 
data
"""

#Constant File Paths
"""
SQL_CLEAR_DATA = "SQL/clear.sql"
DATA_HOSPITAL_PAYMENT = "DATA/PaymentAndValue.xml"
DATA_COMPLICATIONS = "DATA/CompAndDeath.xml"
"""
paymentFile = "DATA/Payment_and_value_of_care_-_Hospital.csv"
compFile = "DATA/Complications_and_Deaths_-_Hospital.csv"

conStr = "dbname = 'postgres' user = 'postgres' password= 'postgres'"

class PaymentTags(Enum):
    PID = "provider_id"
    NAME = "hospital_name"
    ADDRESS = "address"
    CITY = "city"
    STATE = "state"
    ZIP = "zip_code"
    COUNTY = "county_name"
    PHONE = "phone_number"
    MEASURE = "measure_name"
    MID = "measure_id"
    CATEGORY = "category"
    DENOM = "denominator"
    PAYMENT = "payment"
    LOWE = "lower_estimate"
    HIGHE = "higher_estimate"
    FOOTNOTE = "payment_footnote"
    VOCNAME = "value_of_care_display_name"
    VOCID = "value_of_care_display_id"
    VOCCATEGORY = "value_of_care_category"
    VOCFOOTNOTE = "value_of_care_footnote"
    STARTDATE = "measure_start_date"
    ENDDATE = "measure_end_date"
    LOCATION = "location"

class CompTags(Enum):
    PID = "provider_id"
    NAME = "hospital_name"
    ADDRESS = "address"
    CITY = "city"
    STATE = "state"
    ZIP = "zip_code"
    COUNTY = "county_name"
    PHONE = "phone_number"
    MEASURE = "measure_name"
    MID = "measure_id"
    COMPARE = "compared_to_national"
    DENOM = "denominator"
    SCORE = "score"
    LOWE = "lower_estimate"
    HIGHE = "higher_estimate"
    STARTDATE = "measure_start_date"
    ENDDATE = "measure_end_date"
    LOCATION = "location"

#clear all rows in existing tables
def Clear_Data(conn):
    fd = open(SQL_CLEAR_DATA, "r")
    queryStr = fd.read()
    fd.close()
    
    allQueries = queryStr.split(";")
    for query in allQueries:
        try:
            conn.execute(query)
        except OperationalError as e:
            print("Invalid query: ", e)

    conn.commit()
