BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "userstore" (
	"username"	VARCHAR(20) NOT NULL,
	"password"	VARCHAR(200),
	"timestamp"	DATETIME,
	PRIMARY KEY("username")
);
CREATE TABLE IF NOT EXISTS "CustomerStatus" (
	"SSN_ID"	INTEGER NOT NULL,
	"CustomerID"	INTEGER NOT NULL UNIQUE,
	"Name"	VARCHAR(50) NOT NULL,
	"Age"	INTEGER NOT NULL,
	"Address"	VARCHAR(40) NOT NULL,
	"State"	VARCHAR(20) NOT NULL,
	"City"	VARCHAR(20) NOT NULL,
	"Status"	VARCHAR(10),
	"Message"	VARCHAR(50),
	"Last_Updated"	VARCHAR(20),
	PRIMARY KEY("SSN_ID")
);
CREATE TABLE IF NOT EXISTS "AccountStatus" (
	"CustomerID"	INTEGER NOT NULL,
	"AccountID"	INTEGER UNIQUE,
	"AccountType"	VARCHAR(20),
	"AccStatus"	VARCHAR(10),
	"Message"	VARCHAR(50),
	"Last_Updated"	VARCHAR(20),
	"Balance"	INTEGER NOT NULL,
	"CRDate"	VARCHAR(20) NOT NULL,
	"CRLastDate"	VARCHAR(20) NOT NULL,
	"Duration"	INTEGER,
	PRIMARY KEY("CustomerID")
);
CREATE TABLE IF NOT EXISTS "Transactions" (
	"TranscationID"	INTEGER NOT NULL,
	"SAccountID"	INTEGER,
	"DAccountID"	INTEGER,
	"AccountType"	VARCHAR(20),
	"Amount"	INTEGER,
	"TrDate"	VARCHAR(20),
	"SAccountType"	VARCHAR(20),
	"DAccountType"	VARCHAR(20),
	PRIMARY KEY("TranscationID")
);
INSERT INTO "userstore" ("username","password","timestamp") VALUES ('SB1234567','12345678',''),
 ('CS1234567','87654321',NULL);
INSERT INTO "CustomerStatus" ("SSN_ID","CustomerID","Name","Age","Address","State","City","Status","Message","Last_Updated") VALUES (234343355,468686715,'Rocky Mohanty',23,'Khordha','Maharastra','Hydrabad','Active','Created','2020-06-17'),
 (455646567,911293139,'Rajat Mohanty',28,'KHORDHA','Andra pradesh','Hydrabad','Active','Created','2020-06-17');
INSERT INTO "AccountStatus" ("CustomerID","AccountID","AccountType","AccStatus","Message","Last_Updated","Balance","CRDate","CRLastDate","Duration") VALUES (144344354,288688713,'Saving Account','Active','Created','2020-06-18',0,'2020-06-18','2020-06-18',4),
 (323243434,646486873,'Saving Account','Active','Created','2020-06-18',8000,'2020-06-18','2020-06-18',4),
 (468686715,937373435,'Saving Account','Active','Created','2020-06-17',18000,'2020-06-17','2020-06-17',4);
INSERT INTO "Transactions" ("TranscationID","SAccountID","DAccountID","AccountType","Amount","TrDate","SAccountType","DAccountType") VALUES (30166,937373435,1822586283,'Saving Account',1000,'2020-06-18','Saving Account','Saving Account'),
 (505459,646486873,937373435,'Saving Account',2000,'2020-06-18','Saving Account','Saving Account'),
 (885155,937373435,646486873,'Saving Account',2000,'2020-06-18','Saving Account','Saving Account');
COMMIT;
