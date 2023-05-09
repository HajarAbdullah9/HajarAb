install.packages("RSQLite")
library("RSQLite")
library(RODBC);
library(odbc)
dsn_driver <- "{IBM DB2 ODBC Driver}"
dsn_database <- "bludb"            # e.g. "bludb"
dsn_hostname <- "fbd88901-ebdb-4a4f-a32e-9822b9fb237b.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud" # e.g "54a2f15b-5c0f-46df-8954-.databases.appdomain.cloud"
dsn_port <- "32731"   # e.g. "32733" 
dsn_protocol <- "TCPIP"            # i.e. "TCPIP"
dsn_uid <- "jtm62400"        # e.g. "zjh17769"
dsn_pwd <- "fDYVCgshF7cbMaCE"      # e.g. "zcwd4+8gbq9bm5k4"  
dsn_security <- "ssl"

conn_string <- paste0("Driver={", dsn_driver, "};",

                      "DATABASE=", dsn_database, ";",

                      "HOSTNAME=", dsn_hostname, ";",

                      "PORT=", dsn_port, ";",

                      "PROTOCOL=", dsn_protocol, ";",

                      "UID=", dsn_uid, ";",

                      "PWD=", dsn_pwd, ";",

                      "SECURITY=", dsn_security)

conn <- odbcConnect(conn_string, uid = dsn_uid, pwd = dsn_pwd)


sql.info <- sqlTypeInfo(conn)
conn.info <- odbcGetInfo(conn)
conn.info["DBMS_Name"]
conn.info["DBMS_Ver"]
conn.info["Driver_ODBC_Ver"]
myschema <- "jtm62400" # e.g. "ZJH17769"
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
#df1 <- sqlQuery (conn, "CREATE TABLE ANNUAL_CROP(
 #                   CD_ID char (6) NOT NULL,
  #                  YEAR CHAR (20),
   #                 CROP_TYPE varchar (50),
    #                GEO varchar (50),
    #                SEEDED_AREA CHAR (50) ,
     #               HARVESTED_AREA CHAR (50),
      #              PRODUCTION CHAR (50),
       #             AVG_YIELD CHAR (50),
        #            PRIMARY KEY (CD_ID))",
                  #  errors = FALSE)
#if(df1 == -1){
 #   cat ("An error has occured.\n")
  #  msg <- odbcGetErrMsg(conn)
   # print (msg)
    #} else {
    #cat ("Table was createdd successfuly.\n")
#}

df2 <- sqlQuery (conn, "CREATE TABLE FARM_PRICES(
                    CD_ID CHAR (6) NOT NULL,
                    DATE date (20),
                    CROP_TYPE VARCHAR (50),
                    GEO VARCHAR (50),
                    PRICE_PRERMT INTEGER WITH DEFAULT 20,
                    PRIMARY KEY (CD_ID))",
                    errors = FALSE)

#df3<- sqlQuery (conn, "CREATE TABLE MONTHLY(
#CD_ID CHAR (6) NOT NULL ,
#DATE VARCHAR(20),
#FXUSDCAD INTEGER WITH DEFAULT 20,
#PRIMARY KEY (CD_ID))",
#errors = FALSE)

#df4<- sqlQuery (conn, "CREATE TABLE DAILY_PRICES(
#DFX_ID CHAR (6) NOT NULL ,
#DATE VARCHAR(20),
#FXUSDCAD INTEGER WITH DEFAULT 20,
#PRIMARY KEY (DFX_ID))",
#errors = FALSE)



#if(df4 == -1){
 #   cat ("An error has occured.\n")
  #  msg <- odbcGetErrMsg(conn)
   # print (msg)
    #} else {
    #cat ("Table was createdd successfuly.\n")
#}
#anual_cropdf <- read.csv("/resources/labs/MYDATA/data1.csv")
#sqlSave(conn, anual_cropdf, 'ANNUAL_CROP', append=TRUE, fast=FALSE, rownames=FALSE, colnames=FALSE, verbose=FALSE)
farm_pricesdf <- read.csv("/resources/labs/MYDATA/datatwo.csv")
sqlSave(conn, farm_pricesdf,'FARM_PRICES', append=TRUE, fast=FALSE, rownames=FALSE, colnames=FALSE, verbose=FALSE)
#monthly_pricesdf <- read.csv("/resources/labs/MYDATA/data5.csv")
#sqlSave(conn, monthly_pricesdf,"MONTHLY", append=TRUE, fast=FALSE, rownames=FALSE, colnames=FALSE, verbose=FALSE)
#daily_pricesdf <- read.csv("/resources/labs/MYDATA/data4.csv")
#sqlSave(conn, daily_pricesdf,"DAILY_PRICES", append=TRUE, fast=FALSE, rownames=FALSE, colnames=FALSE, verbose=FALSE)

#FARMDB <- sqlFetch(conn, "FARM_PRICES")
#tail(FARMDB)
#dim(farm_pricesdf)
#info <- paste("select distinct geo from FARM_PRICES")
#query <- sqlQuery(conn,info,believeNRows = FALSE)
#query
#close(conn)
#FARMDB <- sqlFetch(conn, "ANNUAL_CROP")
#tail(FARMDB)
#dim(farm_pricesdf)
info <- paste("select count (*) as total
                from ANNUAL_CROP a
                where a.CROP_TYPE='Rye' and a.GEO = 'Canada'
                and substring(a.YEAR,7,10)=1968 ")
query <- sqlQuery(conn,info,believeNRows = FALSE)
query
info <- paste("select *
                from FARM_PRICES p
                where p.CROP_TYPE='Rye'")
query <- sqlQuery(conn,info,believeNRows = FALSE)
head(query)
------------------------------------#
info <- paste("select distinct a.HARVESTED_AREA
                from ANNUAL_CROP a
                where a.CROP_TYPE='Barley'")
query <- sqlQuery(conn,info,believeNRows = FALSE)
query
info <- paste("select p.date
                from FARM_PRICES p")
query <- sqlQuery(conn,info,believeNRows = FALSE)
head(query,1)
tail(query,1)
info <- paste("select distinct p.crop_type
                from FARM_PRICES p
                where PRICE_PRERMT >= 350")
query <- sqlQuery(conn,info,believeNRows = FALSE)
query
info <- paste("select a.year,a.crop_type, a.AVG_YIELD
                from Annual_crop a
                where a.GEO = 'Saskatchewan' and
                substr(a.year,7,10) = '2000'
                order by AVG_YIELD desc ")
query <- sqlQuery(conn,info,believeNRows = FALSE)
query
info <- paste("select a.year,a.crop_type,a.geo, a.AVG_YIELD
                from Annual_crop a
                where substr(a.year,7,10) >= '2000'
                order by AVG_YIELD desc ")
query <- sqlQuery(conn,info,believeNRows = FALSE)
query
info <- paste("select avg_yield as Avg_Yield, year as year
                from (select * 
                from Annual_crop a
                where substr(a.year,7,10) = '2020')
                order by avg_yield ")

query1 <- sqlQuery(conn,info,believeNRows = FALSE)
query1

total <- paste("select sum ( avg_yield ) as Total_Avg_Yield
                from (select * 
                from Annual_crop a
                where substr(a.year,7,10) = '2020')
                ")
query2 <- sqlQuery(conn,total,believeNRows = FALSE)
query2
info <- (" select p.CROP_TYPE,  p.GEO, p.PRICE_PRERMT, m.FXUSDCAD, p.date,
            p.PRICE_PRERMT * m.FXUSDCAD AS MONTHLY_PRICE 
            FROM FARM_PRICES p inner join MONTHLY m 
            on p.date = m.date 
            where P.CROP_TYPE='Canola'
            AND P.GEO= 'Saskatchewan'  AND SUBSTR(P.date,7,10) = '2020' and substr(p.date,4,5) >= '06' ")

query <- sqlQuery (conn,info,believeNRows = FALSE)
query
#" select p.PRICE_PRERMT,p.CROP_TYPE,p.GEO, m.FXUSDCAD 
#FROM FARM_PRICES p JOIN MONTHLY_PRICES m ON p.CD_ID = m.DFX_ID"

