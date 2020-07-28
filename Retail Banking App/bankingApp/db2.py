import sqlite3

conn = sqlite3.connect('Bankdb.db')
print ("Opened database successfully")

conn.execute('''CREATE TABLE "AccountStatus2" (
	"CustomerID"	INT(20) NOT NULL,
	"AccontID"	INT(20) NOT NULL UNIQUE,
	"AccountType"	VARCHAR2(20) NOT NULL,
	"AccountStatus"	VARCHAR2(10),
	"Message"	VARCHAR2(50),
	"Last_Updated"	VARCHAR2(20),
	"Balance"	INT(20) NOT NULL,
	"CRDate"	VARCHAR2(20) NOT NULL,
	"CRLastDate"	VARCHAR2(20) NOT NULL,
	"Duration"	INT(10),
	PRIMARY KEY("CustomerID")
);''')
print ("Table created successfully")

conn.close()
