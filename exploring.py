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

conn

#Bike_sharing_systems

bike_sharing_systems <- read.csv('C:/Users/LENOVO/Desktop/slides/FIXED_DATA/sharingSystems.CSV')
str(bike_sharing_systems)
dim(bike_sharing_systems)
View(bike_sharing_systems)


DF2 <- sqlQuery (conn, "CREATE TABLE sharingSystems(ID int NOT NULL, COUNTRY CHAR(14),
                    CITY CHAR(87),
                    SYSTEM CHAR(38),
                    BICYCLES1 num(16)
                 )",
                 errors = FALSE)

if(DF2 == -1){
  cat ("An error has occured.\n")
  msg <- odbcGetErrMsg(conn)
  print (msg)
} else {
  cat ("Table was createdd successfuly.\n")
}

sqlSave(conn,bike_sharing_systems,'sharingSystems',append=TRUE, fast=FALSE, rownames=FALSE, colnames=FALSE, verbose=FALSE)

query<-paste('select * from sharingSystems')
query<- sqlQuery(conn,query,believeNRow=FALSE)
query

#3rd seoul_bike_sharing (2)

seoul<-  read.csv('C:/Users/LENOVO/Desktop/slides/FIXED_DATA/seoul1.CSV')
str(seoul)
dim(seoul)
View(seoul)


class(seoul$No.Holiday)
write.csv(seoul,'C:/Users/LENOVO/Desktop/slides/FIXED_DATA/seoul1.CSV')

DF3 <- sqlQuery (conn, "CREATE TABLE seoul1(DATE char(10), RENTED_BIKE_COUNT int,
                    HOUR int,
                    TEMPERATURE num(16),
                    HUMIDITY int,
                    WIND_SPEED int,
                    VISIBILITY int,
                    DEW_POINT_TEMPERATURE num(5),
                    SOLAR_RADIATION num(4),
                    RAINFALL num(4),
                    SNOWFALL num(3),
                    SEASONS int,
                    FUNCTIONING_DAY char(3),
                    Holiday int,
                    No_Holiday int
                   )",
                 errors = FALSE)

if(DF3 == -1){
  cat ("An error has occured.\n")
  msg <- odbcGetErrMsg(conn)
  print (msg)
} else {
  cat ("Table was createdd successfuly.\n")
}


#weather

DF1<- sqlQuery (conn, "CREATE TABLE weather(ID int NOT NULL, CITY varchar(16), WEATHER varchar(6),
                    VISIBILITY int,
                    TEMP num(5),
                    TEMP_MIN num(5),
                    TEMP_MAX num(5),
                    PRESSURE int,
                    HUMIDITY int,
                    WIND_SPEED num(4),
                    WIND_DEG int,
                    SEASON varchar(6),
                    FORECAST_DATETIME VARCHAR(20)
                   )",
                errors = FALSE)

if(DF1 == -1){
  cat ("An error has occured.\n")
  msg <- odbcGetErrMsg(conn)
  print (msg)
} else {
  cat ("Table was createdd successfuly.\n")
}

WEATHER_FORECAST<- read.csv('C:/Users/LENOVO/Desktop/slides/FIXED_DATA/weather.csv')
#dim(WEATHER_FORECAST)
str(WEATHER_FORECAST)
sqlSave(conn,WEATHER_FORECAST, 'weather',append=TRUE, fast=FALSE, rownames=FALSE, colnames=FALSE, verbose=FALSE)

### WORLD

world_cities<- read.csv('C:/Users/LENOVO/Desktop/slides/FIXED_DATA/world.csv')
str(world_cities)
dim(world_cities)
View(world_cities)

DF4 <- sqlQuery (conn, "CREATE TABLE world(ID int NOT NULL, CITY VARCHAR(49),
                    CITY_ASCII VARCHAR(49),
                    LAT num(8),
                    LNG num(9),
                    COUNTRY VARCHAR(45),
                    ISO2 VARCHAR(2),
                    ISO3 VARCHAR(3),
                    ADMIN_NAME VARCHAR(55),
                    CAPITAL VARCHAR(7),
                    POPULATION num(16),
                    ID_NUMBER int
                   )",
                 errors = FALSE)

if(DF4 == -1){
  cat ("An error has occured.\n")
  msg <- odbcGetErrMsg(conn)
  print (msg)
} else {
  cat ("Table was createdd successfuly.\n")
}

#sqlSave(conn,world_cities,'world',append=TRUE, fast=FALSE, rownames=FALSE, colnames=FALSE, verbose=FALSE)


#-Queries:


#### 1 Determine how many records are in the seoul_bike_sharing dataset.
SYSTEMDB<- sqlFetch(conn, 'SHARINGSYSTEMS')
str(SYSTEMDB)
dim(SYSTEMDB)

query1 <- paste('select COUNT (*) from SHARINGSYSTEMS')
query1<- sqlQuery(conn, query1, believeNRows = FALSE)
query1

#### 2 Determine how many hours had non-zero rented bike count.
query2<- paste('select count (HOUR) from SEOUL1 
               where RENTED_BIKE_COUNT != 0 ')
query2 <- sqlQuery(conn, query2, believeNRow= FALSE)
query2 

#3 Query the the weather forecast for Seoul over the next 3 hours.
#Recall that the records in the CITIES_WEATHER_FORECAST dataset are 3 hours apart, so we just need the first record from the query.
WEATHERDB <-  sqlFetch(conn , 'WEATHER')
dim(WEATHERDB)
query3 <- paste('select CITY, WEATHER, SEASON, FORECAST_DATETIME FROM WEATHER')
query3<- sqlQuery(conn, query3, believeNRow= FALSE)
head(query3,1)


# Task 4 - Seasons Find which seasons are included in the seoul bike sharing dataset.¶
query4<- paste('select distinct SEASONS as seasons from SEOUL1')
query4 <- sqlQuery(conn, query4, believeNRow = FALSE)
query4

# 5 Find the first and last dates in the Seoul Bike Sharing dataset.

query5 <- paste('select DATE from SEOUL1 ')
query5<- sqlQuery(conn,query5, believeNRow= FALSE )
head(query5,1)
tail(query5,1)


# Task 6 - Subquery - 'all-time high' determine which date and hour had the most bike rentals.

query6 <-  paste(' select s. DATE, s.HOUR, s.RENTED_BIKE_COUNT FROM SEOUL1 s WHERE s.RENTED_BIKE_COUNT = (SELECT MAX(se.RENTED_BIKE_COUNT) from SEOUL1 se)')


query6 <- sqlQuery(conn, query6, believeNRow = FALSE) 
query6

# Task 7 - Hourly popularity and temperature by season¶
#Determine the average hourly temperature and the average number of bike rentals per hour over each season. List the top ten results by average bike count.

query7 <- paste('select HOUR, avg (TEMPERATURE) as avg_temp , avg (RENTED_BIKE_COUNT) as avg_rented_bikes
                FROM SEOUL1
                GROUP BY HOUR')
query7 <- sqlQuery(conn, query7, believeNRow = FALSE)
query7

#Task 8 - Rental Seasonality
#Find the average hourly bike count during each season.
#Also include the minimum, maximum, and standard deviation of the hourly bike count for each season.
#Hint : Use the SQRT(AVG(col*col) - AVG(col)*AVG(col) ) function where col refers to your column name for finding the standard deviation

query8 <- paste('select HOUR AS HOUR, AVG(RENTED_BIKE_COUNT) AS AVG_BIKES, 
                SQRT(AVG(RENTED_BIKE_COUNT*RENTED_BIKE_COUNT) - AVG(RENTED_BIKE_COUNT) * AVG (RENTED_BIKE_COUNT)) AS STD_BIKES,
                MAX(RENTED_BIKE_COUNT) AS MAXIMUM_BIKES,
                MIN(RENTED_BIKE_COUNT) AS MINIMUM_BIKES
                from SEOUL1 GROUP BY (HOUR)')
query8 <- sqlQuery(conn, query8, believeNRow= FALSE)
query8
#Task 9 - Weather Seasonality
#Consider the weather over each season. On average, what were the TEMPERATURE, HUMIDITY, WIND_SPEED, VISIBILITY, DEW_POINT_TEMPERATURE, SOLAR_RADIATION, RAINFALL, and SNOWFALL per season?
# Include the average bike count as well , and rank the results by average bike count so you can see if it is correlated with the weather at all.

query9 <- paste('select SEASONS as season, AVG(TEMPERATURE) as avg_temp, AVG (HUMIDITY) as avg_Humidity,
                AVG (WIND_SPEED) as avg_wind_speed, AVG (VISIBILITY) as avg_visibiity, 
                 AVG (DEW_POINT_TEMPERATURE) as avg_dew_point_temp,
                 AVG (SOLAR_RADIATION) as avg_solar_radiation, 
                  AVG (RAINFALL) as avg_rainfall, 
                  AVG (SNOWFALL) as avg_snowfall,
                  AVG (RENTED_BIKE_COUNT) as avg_bike_count
                  from SEOUL1 
                  group by (SEASONS) 
                  order by (avg_bike_count) 
                ') 
query9<- sqlQuery(conn, query9, believeNRow = FALSE)
query9


#Task 10 - Total Bike Count and City Info for Seoul
#Use an implicit join across the WORLD_CITIES and the BIKE_SHARING_SYSTEMS tables to determine the total number of bikes avaialble in Seoul, plus the following city information about Seoul: CITY, COUNTRY, LAT, LON, POPULATION, in a single view.
#Notice that in this case, the CITY column will work for the WORLD_CITIES table, but in general you would have to use the CITY_ASCII column.
conn
WORLDB<-sqlFetch(conn, 'WORLD2')
dim (SYSTEMDB)
quert10 <- paste('select * from 
                from SYSTEMDB s inner join WORLD2 w
                on s.CITY = w.CITY ')
query10<- sqlQuery(conn,query10,believeNRow = FALSE)
query10<- paste('select s.CITY as city, w.CITY as w_city, S.COUNTRY as country,w.COUNTRY AS W_COUNTRY,
                  W.LAT as lat, W.LNG as lang,
                  W.POPULATION as population,
                  s.BICYCLES as bicycles
              from sharingSystems s inner join WORLD2 w
                on s.CITY = w.CITY
                WHERE CITY = "Seoul"
                ')

query10 <- sqlQuery(conn, query10, believeNRow = FALSE)
query10

# 8+10

#TASKS:
#Load the seoul_bike_sharing data into a dataframe¶
datafram<- seoul
View(datafram)
#Task 2 - Recast DATE as a date- Use the format of the data, namely "%d/%m/%Y".
#seoul<-  read.csv('C:/Users/LENOVO/Desktop/slides/FIXED_DATA/seoul1.CSV')
#library(lubridate)
class(datafram$DATE)
#as.Date(datafram$DATE, "%m/%d/%y")
#datafram$Month<format(datafram$DATE,'%m')
datafram$DATE  <- as.Date(datafram$DATE, format = "%d/%m/%Y")
View(datafram)
class(datafram$DATE)
#Task 3 - Cast HOURS as a categorical variable
class(datafram$HOUR)
datafram$HOUR <- as.character(datafram$HOUR)
class(datafram$HOUR)

#Also, coerce its levels to be an ordered sequence. This will ensure your visualizations correctly utilize HOURS as a discrete variable with the expected ordering.
sqlQuery(select (*) from datafram)
level_query
#str
str(datafram)
#is.null
colSums(is.na(datafram))
#Descriptive Statistics
install.packages('psych ')
library(psych)
describe(datafram)
#Now you are all set to take a look at some high level statistics of the seoul_bike_sharing dataset.
# Task 4 - Dataset Summary - Use the base R sumamry() function to describe the seoul_bike_sharing dataset'''
summary(datafram)
#%% 
'''Some Basic Observations:
We can see from DATE that we have exactly a full year of data.done
No records have zero bike counts.done
Spring and Winter have the same count of records,
'''
query11<- paste('select COUNT (*) AS TOTAL_WINTER from SEOUL1 where SEASONS = 2 ')
query11<- sqlQuery(conn,query11, believeNRow= FALSE)
query11
query12<- paste('select COUNT (*) AS TOTAL_SPRING from SEOUL1 where SEASONS = 4 ')
query12<- sqlQuery(conn,query12, believeNRow= FALSE)
query12

# while autumn has the least and Summer has the most.
query13<- paste('select COUNT (*) AS TOTAL_SUMMER from SEOUL1 where SEASONS = 3 ')
query13<- sqlQuery(conn,query13, believeNRow= FALSE)
query13
query14<- paste('select COUNT (*) AS TOTAL_Autumn from SEOUL1 where SEASONS = 1 ')
query14<- sqlQuery(conn,query14, believeNRow= FALSE)
query14
'''
Temperature has a large range, so we might expect it to explain at least some of the variation in bike rentals.
Precipitation seems to be quite rare, only happening in the fourth quartiles for both RAINFALL and SNOWFALL.
The average WINDSPEED is very light at only 1.7 m/s, and even the maximum is only a moderate breeze (Google 'Beaufort Wind Scale' to find the different wind descriptions)
By now, you might agree that Exploratory Data Analysis can create more questions than answers. That's okay - you'll have a much deeper understanding and appreciation for your data as a result!
'''
##%%
#Task 5 - Based on the above stats, calculate how many Holidays there are.¶
query15<-paste('select count (HOLIDAY) from SEOUL1 where HOLIDAY=1 ')
query15 <- sqlQuery(conn,query15, believeNRow = FALSE)
query15
#Task 6 - Calculate the percentage of records that fall on a holiday.
query16<- paste('select No_Holiday, count(*) as NoHoliday_count,
                count(*) * 100.0/ sum(count(*)) over () as NoHoliday_percent from SEOUL1
                GROUP BY (No_Holiday)')
query16<- sqlQuery(conn, query16, believeNRow= FALSE)
query16


#Task 7 - Given there is exactly a full year of data, determine how many records we expect to have.
# fully next year

#Task 8 - Given the observations for the 'FUNCTIONING_DAY' how many records must there be?
query17<- paste('select count (FUNCTIONING_DAY) from SEOUL1 where ')
query17<- sqlQuery(conn, query17, believeNRow= FALSE)
query17

#Drilling Down
#Let's calculate some seasonally aggregated measures to help build some more context.

#Task 9 - Load the dplyr package, group the data by SEASONS, 
#and use the summarize() function to calculate the seasonal total rainfall and snowfall.
library(dplyr)
library(tidyverse)
dataset<-datafram
View(dataset)
dataset<- dataset %>% group_by(SEASONS)
dataset %>%
  summarise(summary = sum(RAINFALL))
dataset %>%
  summarise(summary = sum(SNOWFALL))
#library(psych)
#describe(dataset)

#Task 10 - Create a scatter plot of RENTED_BIKE_COUNT vs DATE.
#Tune the opacity using the alpha parameter such that the points don't obscure each other too much.
library(ggplot2)
#qplot(DATE,RENTED_BIKE_COUNT,data = dataset)
dataset$hour_factor <- factor(dataset$HOUR)

ggplot(dataset, aes(y= RENTED_BIKE_COUNT, x=DATE, color= hour_factor),alpha=1/5)+geom_point(shape = 19) + xlab('the date')+ ylab('The count of rented bikes')+ labs(color = 'Hours')+ ggtitle('Scatterplot')
#ggplot(dataset, aes(x=DATE,y=RENTED_BIKE_COUNT, shape= hour_factor))+
 # geom_point()


#Ungraded Task: We can see some patterns emerging here.
#Describe them and keep your findings for your presentation in the final project.

#!! so we can noticed that the most of bikes were estimated by 2k and increasing till 3k were rented during the year of 2012 between April to jul, then after that the rental was decreasing but no long the rental ratio was return to grow more that 3000 bikes were rented between August and September, Should be also notices that the most of rental processes were done around 7:pm or in another word 19:00

'''
#Using colour
#Lets see if we can enhance some of these features by incorporating colour. Given our observations so far, HOURS is a great candidate for this task.

#Task 11 - Create the same plot of the RENTED_BIKE_COUNT time series, but now add HOURS as the colour.
#Solution 11


#Ungraded Task: The trends are much more clear now.
#Describe them and keep your findings for your presentation in the final project.

#Distributions
Task 12 - Create a histogram overlaid with a kernel density curve
Normalize the histogram so the y axis represents density. This can be done by setting y=..density.. in the aesthetics of the histogram.
'''
p <- ggplot(dataset)+ geom_histogram(aes(x=RENTED_BIKE_COUNT, y= ..density..),
                                     binwidth = 19, fill= 'grey', color = 'black')
p
#Ungraded Task: Describe the main features you see in your plot.
#Consider what its shape tells you, and keep your findings for your presentation in the final project.
#13 SCATTER PLOT:
dataset$hour_factor <- factor(dataset$HOUR)

ggplot(dataset, aes(y= RENTED_BIKE_COUNT, x=TEMPERATURE, color= SEASONS),facet_wrap(~SEASONS), alpha=1/5)+geom_point(shape = 19) + xlab('Temprature')+ ylab('The count of rented bikes')+ ggtitle('Scatterplot')
#Outliers (boxplot)
#Task 14 - Create a display of four boxplots of RENTED_BIKE_COUNT vs. HOUR grouped by SEASONS.
#Use facet_wrap to generate four plots corresponding to the seasons.

ggplot(dataset, aes(x=HOUR, y= RENTED_BIKE_COUNT))+ geom_boxplot() +facet_wrap(~SEASONS)
ggplot()
#qplot(factor(HOUR), RENTED_BIKE_COUNT, data= dataset, geom = 'boxplot')

#Solution 14Ungraded Task: Compare and contrast the key features of these boxplots between seasons.¶
#At this point, a story should be taking shape. Again, keep your findings for your presentation in the final project.


#Task 15 - Group the data by DATE, and use the summarize() function to calculate the daily total rainfall and snowfall.
#Also, go ahead and plot the results if you wish.

dataset_date<- dataset %>% group_by(DATE)
summarise_rain<- dataset_date %>%
  summarise(summary = sum(RAINFALL))
plot(summarise_rain)
summarise_snow<- dataset_date %>%
  summarise(summary = sum(SNOWFALL))
plot(summarise_snow)

#Task 16 - Determine how many days had snowfall.

summarise_snow
total <- 0 
for (i in summarise_snow$summary){
  if  (i > 0)
    total = total+1
  return(total)
}

print(total)

#Solution 16
# provide your solution here
#There are many more visualizations we could have chosen to cover here, but the important thing was that you deepen your understanding of the dataset.
#I hope we succeeded in that endeavour!

#(Keep going, you are getting closer to the finish line with each step you take. :-) )
 install.packages('ggplot2')
 library(ggplot2)
 library(ggthemes)
ggplot(seoul)+geom_point(aes(x=TEMPERATURE, y=RENTED_BIKE_COUNT, color= HOUR),alpha=0.8)+
  labs(title = 'Scatter plot of rente bike count vs Date')+
  xlab(lab='TEMPERATURE')+
  ylab(lab='No. of rent bike')+
  facet_wrap(~SEASONS)+
  theme_base()+
  scale_colour_hue(h = c(0,270))
  
# Boxplots of RENTED_BIKE_COUNT vs. HOUR grouped by SEASONS
ggplot(seoul) +
  geom_boxplot(aes(x=HOUR,y=RENTED_BIKE_COUNT,fill=HOUR))+
  labs(title="Boxplot of Rent Bike Number vs Hour")+
  xlab(label = "Hour")+ ylab(label = "Rent No.")+
  theme_base()+
  facet_wrap(~SEASONS)+
  scale_colour_hue(h = c(0, 270))

