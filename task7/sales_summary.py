import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect('sales.db')
cursor = conn.cursor()

cursor.execute("DROp TABLE IF EXISTS sales")

cursor.execute("""
              CREATE TABLE sales(
              product TEXT,
              quantity INTEGER,
              price REAL)
              """)

sales_data = [
    ('Apple',5,100),
    ('Banana',3,50),
    ('Orange',4,75),
    ('Pineapple',2,70),
    ('Mango',1,50),
    ('Pomagranate',3,90),
    ('Apple',4,100),
    ('Banana',2,50),
    ('Orange',5,75)
]

cursor.executemany("INSERT INTO sales VALUES (?,?,?)", sales_data)
conn.commit()
cursor.execute("SELECT * FROM sales")

query = """
    SELECT product, 
        SUM(quantity) AS total_quantity,
        SUM(quantity * price) AS revenue
    FROM sales
    GROUP BY price
"""
df = pd.read_sql_query(query, conn)
print(df)

df.plot(kind='bar', x='product', y='revenue', title='Total Revenue', color = 'red')
plt.xlabel('Product')
plt.ylabel('Revenue')  
plt.tight_layout()
plt.savefig('sales_summary.png')
plt.show()

conn.close()