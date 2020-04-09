import os
import numpy as np
import pandas as pd
from numpy import loadtxt
from keras.models import load_model
import h5py
import psycopg2
# Let's import sqlalchemy
import sqlalchemy as db
import math
from keras.models import model_from_json

os.getcwd()

# create connection with the database
con = db.create_engine('postgresql://iti:iti@localhost/abdlrahman')

# Find out the tables in this DB
print(" Tables are : ",con.table_names())

try:
    connection = psycopg2.connect(user = "iti",
                                  password = "iti",
                                  host = "127.0.0.1",
                                  port = "5432",
                                  database = "abdlrahman")

    cursor = connection.cursor()

    query = """ select Pregnancies , Glucose ,BloodPressure ,
                SkinThickness , Insulin , BMI ,
                DiabetesPedigreeFunction ,Age
                from diabetes_unscored
                Except
                select Pregnancies , Glucose , BloodPressure ,
                SkinThickness , Insulin , BMI ,
                DiabetesPedigreeFunction ,Age
                from diabetes_scored ;   """
    diabetes_csv_data = pd.read_sql(query, connection)


except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
finally:
    #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

diabetes_csv_data['outcome']= ''


# load json and create model
json_file = open('model.json', 'r')
model_json = json_file.read()
json_file.close()
model = model_from_json(model_json)
# load weights into new model
model.load_weights("model.h5")
print("Loaded model Successfully")

X = diabetes_csv_data.iloc[:,:-1].values
y_predicted = model.predict(X)

y_pred_binary = []
for i in y_predicted:
    for element in i :
        if element >= 0.5:
            binary_element = 1
        else :
            binary_element = 0
        y_pred_binary.append(binary_element)

diabetes_csv_data['outcome'] = y_pred_binary


try:
    con = db.create_engine('postgresql://iti:iti@localhost/abdlrahman')

    #cursor = connection.cursor()
    diabetes_csv_data.to_sql(name = 'diabetes_scored',
                con=con ,index = False ,
                if_exists='append')
    print("Loaded the dataframe to the diabetes_scored Successfully .. ")
except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
finally:
    #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
