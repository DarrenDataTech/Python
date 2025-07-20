# Python Cheat Sheet for Data Engineers

# ---------------------------
# Basics
# ---------------------------
# Variables and Data Types
int_var = 10
float_var = 10.5
str_var = "Data Engineer"
bool_var = True
list_var = [1, 2, 3]
tuple_var = (1, 2, 3)
dict_var = {'key': 'value'}
set_var = {1, 2, 3}

# Control Flow
if int_var > 5:
    print("Greater than 5")
elif int_var == 5:
    print("Equal to 5")
else:
    print("Less than 5")

for i in range(3):
    print(i)

while int_var > 0:
    int_var -= 1

# Functions
def add(x, y):
    return x + y

result = add(3, 4)

# Lambda functions
square = lambda x: x * x
print(square(5))

# List comprehensions
squares = [x*x for x in range(10)]

# ---------------------------
# File I/O
# ---------------------------
# Reading a file
with open('file.txt', 'r') as f:
    lines = f.readlines()

# Writing to a file
with open('output.txt', 'w') as f:
    f.write("Hello Data Engineering\n")

# ---------------------------
# Working with CSV
# ---------------------------
import csv

# Reading CSV
with open('data.csv', mode='r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        print(row['column_name'])

# Writing CSV
with open('output.csv', mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['col1', 'col2'])
    writer.writeheader()
    writer.writerow({'col1': 'value1', 'col2': 'value2'})

# ---------------------------
# JSON Handling
# ---------------------------
import json

# Parse JSON string
json_data = '{"name": "John", "age": 30}'
data = json.loads(json_data)

# Convert dict to JSON string
json_string = json.dumps(data, indent=4)

# ---------------------------
# Working with Dates
# ---------------------------
from datetime import datetime, timedelta

now = datetime.now()
formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")
parsed_date = datetime.strptime("2025-07-20", "%Y-%m-%d")

# Date arithmetic
yesterday = now - timedelta(days=1)

# ---------------------------
# Data Processing with pandas
# ---------------------------
import pandas as pd

# Read CSV into DataFrame
df = pd.read_csv('data.csv')

# Inspect data
df.head()
df.info()

# Filter rows
filtered = df[df['column'] > 10]

# Add new column
df['new_col'] = df['column1'] + df['column2']

# Group by and aggregate
grouped = df.groupby('category')['value'].sum()

# Write DataFrame to CSV
df.to_csv('output.csv', index=False)

# ---------------------------
# Working with databases (example: psycopg2 for PostgreSQL)
# ---------------------------
import psycopg2

conn = psycopg2.connect(
    dbname="mydb", user="user", password="pass", host="localhost", port="5432"
)
cur = conn.cursor()

# Execute query
cur.execute("SELECT * FROM my_table WHERE id = %s", (1,))
rows = cur.fetchall()

# Insert data
cur.execute("INSERT INTO my_table (col1, col2) VALUES (%s, %s)", ('val1', 'val2'))
conn.commit()

cur.close()
conn.close()

# ---------------------------
# Working with APIs (requests)
# ---------------------------
import requests

response = requests.get('https://api.example.com/data')
if response.status_code == 200:
    data = response.json()

# POST request with payload
payload = {'key1': 'value1'}
response = requests.post('https://api.example.com/post', json=payload)

# ---------------------------
# Parallelism / Concurrency
# ---------------------------
from concurrent.futures import ThreadPoolExecutor

def process(item):
    return item * item

items = [1, 2, 3, 4]
with ThreadPoolExecutor(max_workers=2) as executor:
    results = list(executor.map(process, items))

# ---------------------------
# Logging
# ---------------------------
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info("This is an info message")
logging.error("This is an error message")

# ---------------------------
# Error Handling
# ---------------------------
try:
    x = 1 / 0
except ZeroDivisionError as e:
    print("Error:", e)
finally:
    print("Cleanup code runs here")

# ---------------------------
# Environment Variables
# ---------------------------
import os

db_password = os.getenv('DB_PASSWORD', 'default_password')

# ---------------------------
# Useful Libraries for Data Engineering
# ---------------------------
# numpy (numerical operations)
import numpy as np

arr = np.array([1, 2, 3])
mean = np.mean(arr)

# pyarrow (working with Parquet files)
import pyarrow.parquet as pq
import pyarrow as pa

table = pa.Table.from_pandas(df)
pq.write_table(table, 'file.parquet')

# airflow (workflow management) - example import
# from airflow import DAG

# ---------------------------
# Helpful Tips
# ---------------------------
# Virtual environments
# python -m venv venv
# source venv/bin/activate (Linux/Mac)
# venv\Scripts\activate (Windows)

# Package management
# pip install pandas psycopg2-binary requests numpy pyarrow

# Run scripts
# python script.py
