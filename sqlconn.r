install.packages('RODBC')
install.packages('odbc')
install.packages('RSQLite')
library(RODBC)
library(odbc)
dsn_driver <- "{IBM DB2 ODBC Driver}"
    dsn_database <- "bludb"
dsn_hostname <- "b0aebb68-94fa-46ec-a1fc-1c999edb6187.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud"
dsn_port <- "31249"
dsn_protocol <- "TCPIP"
dsn_uid <- "gjb11938"
dsn_pwd <- "v1Q7dBZHJea3aNMf"
dsn_security <- "ssl"

conn <- odbcDriverConnect(paste0("DRIVER=", dsn_driver,
                                 ";DATABASE=", dsn_database,
                                 ";HOSTNAME=", dsn_hostname,
                                 ";PORT=", dsn_port,
                                 ";PROTOCOL=", dsn_protocol,
                                 ";UID=", dsn_uid,
                                 ";PWD=", dsn_pwd,
                                 ";SECURITY=", dsn_security))

conn
sql.info <- sqlTypeInfo(conn)
conn.info <- odbcGetInfo(conn)
conn.info["DBMS_Name"]
conn.info["DBMS_Ver"]
conn.info["Driver_ODBC_Ver"]

myschema <- "gjb11938" # e.g. "ZJH17769"
tables <- c("FARM_PRICES")
    
    for (table in tables){  
      # Drop School table if it already exists
        out <- sqlTables(conn, tableType = "TABLE", schema = myschema, tableName =table)
      if (nrow(out)>0) {
        err <- sqlDrop (conn, paste(myschema,".",table,sep=""), errors=FALSE)  
        if (err==-1){
          cat("An error has occurred.\n")
          err.msg <- odbcGetErrMsg(conn)
          for (error in err.msg) {
            cat(error,"\n")
          }
        } else {
          cat ("Table: ",  myschema,".",table," was dropped\n")
        }
      } else {
          cat ("Table: ",  myschema,".",table," does not exist\n")
      }
    }
    
    df1 <- sqlQuery (conn, "CREATE TABLE ANNUAL_CROP(
                    CD_ID char (6) NOT NULL,
                    YEAR CHAR (20),
                    CROP_TYPE varchar (50),
                    GEO varchar (50),
                    SEEDED_AREA CHAR (50) ,
                    HARVESTED_AREA CHAR (50),
                    PRODUCTION CHAR (50),
                    AVG_YIELD CHAR (50),
                    PRIMARY KEY (CD_ID))",
                    errors = FALSE)
if(df1 == -1){
    cat ("An error has occured.\n")
    msg <- odbcGetErrMsg(conn)
    print (msg)
    } else {
    cat ("Table was createdd successfuly.\n")
}

df2 <- sqlQuery (conn, "CREATE TABLE FARM_PRICES(
                    CD_ID CHAR (6) NOT NULL,
                    DATE date (20),
                    CROP_TYPE VARCHAR (50),
                    GEO VARCHAR (50),
                    PRICE_PRERMT INTEGER WITH DEFAULT 20,
                    PRIMARY KEY (CD_ID))",
                    errors = FALSE)

df3<- sqlQuery (conn, "CREATE TABLE MONTHLY(
CD_ID CHAR (6) NOT NULL ,
DATE VARCHAR(20),
FXUSDCAD INTEGER WITH DEFAULT 20,
PRIMARY KEY (CD_ID))",
errors = FALSE)

df4<- sqlQuery (conn, "CREATE TABLE DAILY_PRICES(
DFX_ID CHAR (6) NOT NULL ,
DATE VARCHAR(20),
FXUSDCAD INTEGER WITH DEFAULT 20,
PRIMARY KEY (DFX_ID))",
errors = FALSE)
if(df4 == -1){
    cat ("An error has occured.\n")
    msg <- odbcGetErrMsg(conn)
    print (msg)
    } else {
    cat ("Table was createdd successfuly.\n")
}
df2 <- sqlQuery (conn, "CREATE TABLE FARM_PRICES(
                    CD_ID CHAR (6) NOT NULL,
                    DATE date ,
                    CROP_TYPE VARCHAR (50),
                    GEO VARCHAR (50),
                    PRICE_PRERMT INTEGER WITH DEFAULT 20,
                    PRIMARY KEY (CD_ID))",
                    errors = FALSE)
if(df2 == -1){
    cat ("An error has occured.\n")
    msg <- odbcGetErrMsg(conn)
    print (msg)
    } else {
    cat ("Table was createdd successfuly.\n")
}

# read and appendit to the tables in IBM cloud:

#1 
anual_cropdf <- read.csv("resources/SQL/data1.csv")
sqlSave(conn, anual_cropdf, 'ANNUAL_CROP', append=TRUE, fast=FALSE, rownames=FALSE, colnames=FALSE, verbose=FALSE)
#2
farm_pricesdf <- read.csv('resources/SQL/datatwo.csv')
sqlSave(conn, farm_pricesdf,'FARM_PRICES', append=TRUE, fast=FALSE, rownames=FALSE, colnames=FALSE, verbose=FALSE)
#3
monthly_pricesdf <- read.csv("resources/SQL/data5.csv")
sqlSave(conn, monthly_pricesdf,"MONTHLY", append=TRUE, fast=FALSE, rownames=FALSE, colnames=FALSE, verbose=FALSE)
#4
daily_pricesdf <- read.csv("resources/SQL/data4.csv")
sqlSave(conn, daily_pricesdf,"DAILY_PRICES", append=TRUE, fast=FALSE, rownames=FALSE, colnames=FALSE, verbose=FALSE)


