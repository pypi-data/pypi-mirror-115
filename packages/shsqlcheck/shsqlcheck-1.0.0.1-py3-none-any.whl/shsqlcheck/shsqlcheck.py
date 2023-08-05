###################################
## filename : shsqlcheck.py
###################################

import pymssql as sql

#BEMS 데이터베이스 연결 설정
class ShBemsSqlDb:
    # DB Server
    __dbServer = 'localhost'
    # Database Name
    __dbName = 'shbems'
    # UserName
    __userName = 'shbems'
    # Password
    __pswd = 'shbems'
    
    def __init__(self, dbServer='localhost'):
        self.__dbServer = dbServer
        
    # DB Connection
    def dbConnect(self):
        return sql.connect(self.__dbServer, self.__userName, self.__pswd, self.__dbName)

    # DB Close
    def dbClose(self, conn):
        if(conn != None):
            conn.close()
    
    # 사이트 코드 체크
    def siteCodeCheck(self, conn):
        cursor = conn.cursor()
        cursor.execute("SELECT TOP 1 SITECODE FROM T_SITE_INFORMATION WHERE OperationYN = 'Y'")
        
        siteCode = ''
        for row in cursor:
            siteCode = row[0]
            
        return siteCode

#BEN 데이터베이스 연결 설정
class ShBenSqlDb:
    # DB Server
    __dbServer = 'localhost'
    # Database Name
    __dbName = 'sunghan'
    # UserName
    __userName = 'sunghan'
    # Password
    __pswd = 'Sunghan!2345'
    
    def __init__(self, dbServer='localhost'):
        self.__dbServer = dbServer
        
    # DB Connection
    def dbConnect(self):
        return sql.connect(self.__dbServer, self.__userName, self.__pswd, self.__dbName)

    # DB Close
    def dbClose(self, conn):
        if(conn != None):
            conn.close()
    
    # 사이트 코드 체크
    def siteCodeCheck(self, conn):
        cursor = conn.cursor()
        cursor.execute("SELECT TOP 1 SITECODE FROM T_SITE_INFORMATION WHERE OperationYN = 'Y'")
        
        siteCode = ''
        for row in cursor:
            siteCode = row[0]
            
        return siteCode
