

import sqlite3

con=sqlite3.connect("en_US.db")
cur=con.cursor()
res = cur.execute("""
SELECT * FROM dictionary
WHERE word NOT LIKE '%''%' 
ORDER BY RANDOM()
LIMIT 1000;""")

allres=res.fetchall()

v=[]
for i in allres:
    if i[2][0].lower()==i[2][0]: 
        v.append(i)

from requests import get
randomWord=v[0][0]
print(f"REAL WORD: {randomWord}\n\n")

r=get(f"https://api.datamuse.com/words?ml={randomWord}&max=5")
c=eval(r.content.decode())
print("Related words:")
for i in c:
    print(i['word'])


# import pandas as pd
# import sqlite3
#
# # Load the CSV file into a DataFrame
# csv_file = "en_US.csv"
# df = pd.read_csv(csv_file)
#
# # Connect to SQLite database (or create one)
# conn = sqlite3.connect("en_US.db")
# cursor = conn.cursor()
#
# # Create table (if it doesn't exist)
# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS dictionary (
#         id INTEGER PRIMARY KEY,
#         word TEXT NOT NULL,
#         definition TEXT NOT NULL
#     )
# """)
#
# # Insert the data into the table
# df.to_sql("dictionary", conn, if_exists="replace", index=False)
#
# # Verify by querying the data
# for row in cursor.execute("SELECT * FROM dictionary"):
#     print(row)
#
# # Close the connection
# conn.close()
#

