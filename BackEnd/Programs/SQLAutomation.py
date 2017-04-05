import MySQLdb as sqlDB

myUser = "The username"
myPasswd = "the passwd for the sql database"
myDb = "Name of the db"

def updateSQLDatabase(listingsArray):
	connect = setupConnection()
	for listing in listingsArray:
		cursor.execute("UPDATE " + myDB + "SET ApartmentName=%f, Location=%s, Latitude=%f, Longitude=%s, Price=%d, Link=%s", tuple(listing))
		connect.commit()
	connect.close()

def clearSQLDatabase():
	connect = setupConnection()
	cursor = connect.cursor()
	cursor.execute("DROP TABLE " + myDb)
	connect.commit()
	connect.close()

def setupConnection():
	connect = sqlDB.connect(host="localhost", port="8081", user=myUser, passwd=myPasswd, db=myDb, charset="utf-8")
	return connect