#Script to insert data(huge data) from excel file into database.
import os
import xlrd
import psycopg2
from image_encoder.image_encoder import *
import xmlrpc.client 
import base64
import time
 

# Establishing database connectivity.
def db_connection():
    connection = None
    try:
        connection = psycopg2.connect(user="ubuntu",password="12345",host="127.0.0.1",port="",database="testodoo111")
        print(connection)
    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
    return connection

# Reading data from excel file and fetching data to the database.
def get_excel_data():
    list_of_items = []
    os.chdir(os.path.dirname(__file__))
    work_book = xlrd.open_workbook("items.xlsx")
    sheet = work_book.sheet_by_name("List of Items")
    os.chdir("photos")
    
    for i in range(2,200):
        column = sheet.row(i)
        record = {}
        record["default_code"] = column[0].value
        record["name"] = column[1].value
        record["part_no"] = column[2].value

        connection = db_connection()
        cursor = connection.cursor()
        cursor.execute("""SELECT id FROM catagory WHERE name = %s """,(column[3].value,))
        cat_id = cursor.fetchone()
        record["catagory_id"] = cat_id[0]
        
            
        if column[4].value != '' and column[4].value != 'N/A':
            if os.path.isfile(column[4].value):
                f = open(column[4].value,"rb")
                record["image_1920"] = base64.b64encode(f.read()).decode('utf-8')
                
        else:
            print("Image not existed.")
        
        if record !='' and record != 'N/A':
            list_of_items.append(record)
        else:
            print("Empty row")
    return list_of_items

# Creating xmlrpc connection
def create_connection():
    url ="http://127.0.0.1:9090"
    db = "testodoo111"
    username = "admin"
    password = "admin"
    common   = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid      = common.authenticate(db,username,password,{})
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    records = get_excel_data()
    models.execute_kw(db,uid,password,'product.template','create',[records])
    

start_time = time.time()
create_connection()

print(time.time()-start_time)