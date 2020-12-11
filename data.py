
# Example Python program to delete rows from a PostgreSQL database table

import psycopg2

 

# Obtain a database connection

con = psycopg2.connect("postgres://ddwbsshctrcopd:5873de1bae81aa8dd1c1680475d0f7a1674dd3ceb057f0c285c81179783333e7@ec2-174-129-224-33.compute-1.amazonaws.com:5432/d32641cd2da4vv")
print("Database opened successfully")

cur = con.cursor()

cur.execute("DELETE FROM users;")
con.commit()
print("Total deleted rows:", cur.rowcount)

cur.execute("SELECT * from users")
rows = cur.fetchall()
for row in rows:
    print(row)
    print(row[1])
    print(row[2])
    print(row[3])
    print(row[4])

print("Deletion successful")
con.close()