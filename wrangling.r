library(tidyverse)
library(reader)
sharingSystems <-read_csv('C:/Users/LENOVO/Documents/Hajar/raw_bike_sharing_systems.csv')
world <-read_csv('C:/Users/LENOVO/Documents/Hajar/raw_worldcities.csv')

seoul <-read_csv('C:/Users/LENOVO/Documents/Hajar/raw_seoul_bike_sharing.csv')
weather <-read_csv('C:/Users/LENOVO/Documents/Hajar/raw_cities_weather_forecast.csv')
#1

colnames(sharingSystems) <- str_replace_all(names(sharingSystems),' ','_')
colnames(sharingSystems) <- toupper(colnames(sharingSystems))

#write_csv(dataset4,'raw_bike_sharing_systems.csv')

#2
colnames(world) <- str_replace_all(names(world),' ','_')
colnames(world) <- toupper(colnames(world))

#write_csv(dataset2,'raw_seoul_bike_sharing.csv')

#3
colnames(seoul) <- str_replace_all(names(seoul),' ','NA')
colnames(seoul) <- toupper(colnames(seoul))

write_csv(dataset3,'raw_cities_weather_forecast.csv')


#4
colnames(weather) <- str_replace_all(names(weather),' ','_')
colnames(weather) <- toupper(colnames(weather))

#write_csv(dataset4,'raw_cities_weather_forecast.csv')

'''
dataset_list<- c(dataset1, dataset2, dataset3)
for (data_name in dataset_list){
  dataset<-read_csv(data_name)
  colnames(data_name) <- str_replace_all(colnames(data_name),' ','_')
  colnames(data_name) <- toupper(colnames(data_name))  
  write.csv(data_name,row_names,row.names = False)
  }
'''

head(sharingSystems)
sub_sharingSystems<- sharingSystems %>% select(COUNTRY,CITY,SYSTEM, BICYCLES)
head(sub_sharingSystems)
sub_sharingSystems %>% summarize_all(class) %>% gather(variable, class)


find_character <- function(strings) grepl('[^0:9]', strings)
sub_sharingSystems %>% select(BICYCLES) %>% filter(find_character(BICYCLES)) %>% slice(0:10)

ref_pattern <- "\\[[A-z0-9]+\\]"
find_reference_pattern <- function(strings) grepl(ref_pattern,strings)
sub_sharingSystems %>% select(COUNTRY) %>% filter(find_reference_pattern(COUNTRY)) %>% slice(0:10)

sub_sharingSystems %>% select(CITY) %>% filter(find_reference_pattern(CITY)) %>% slice(0:10)
sub_sharingSystems %>% select(SYSTEM) %>% filter(find_reference_pattern(SYSTEM)) %>% slice(0:10)

# remove the reference links:

remove_ref <- function(string) {
  ref_pattern <- "\\[[A-Z 0-9]+\\]"
  result <- str_replace_all(string,ref_pattern,' ')
  str_trim(result)
  return(result)
}

# str_trim() removes whitespace from start and end of string; str_squish() removes whitespace at the start and end, and replaces all internal whitespace with a single space

library(dplyr)
result <- sub_sharingSystems %>% mutate(CITY=remove_ref(sub_sharingSystems$CITY), SYSTEM=remove_ref(sub_sharingSystems$SYSTEM))
result %>% select(CITY, SYSTEM) %>% filter(find_reference_pattern(CITY) |  find_reference_pattern(SYSTEM))

result %>% select(CITY) %>% filter(find_reference_pattern(CITY)) %>% slice(0:10)
result %>% select(SYSTEM) %>% filter(find_reference_pattern(SYSTEM)) %>% slice(0:10)

sub_sharingSystems <- result
sharingSystems <- sub_sharingSystems
#check:
sharingSystems %>% select(CITY) %>% filter(find_reference_pattern(CITY)) %>% slice(0:10)
sharingSystems %>% select(SYSTEM) %>% filter(find_reference_pattern(SYSTEM)) %>% slice(0:10)

#extracting numeric values:

library(dplyr)


#extract_num<- function(columns){
 # digital_pattern <- '/+d'
  #f <- str_extract(columns, digital_pattern)
#  as.numeric(f)
#}

sharingSystems$BICYCLES1 <- as.numeric(gsub("\\D", "", sharingSystems$BICYCLES))
#result2 <- sub_dataset1 %>% mutate(BICYCLES=extract_num(BICYCLES))
sharingSystems <- sharingSystems[,-4]
str(sharingSystems)
#class(result2$BICYCLES)
#sub_dataset1<- result2
sharingSystems %>% summarize_all(class) %>% gather(variable, class)

sum(is.na(sharingSystems))
colSums(sapply(sharingSystems, is.na))
dim(sharingSystems)
#HANDLING THE MISSING VALUES IN BICYCLES COLUMN WITH MEAN VALUE SINCE THE TOTAL OF THE OBS IS 480 
mean(sharingSystems$BICYCLES1)
sharingSystems$BICYCLES1 = ifelse(is.na(sharingSystems$BICYCLES1),
                     ave(sharingSystems$BICYCLES1, FUN = function(x) mean(x, na.rm = TRUE)),
                     sharingSystems$BICYCLES1)
colSums(sapply(sharingSystems, is.na))

#HANDEL THE MISSING VALUES IN SYSTEM COLUMN WITH MODE VALUE
getmode <- function(x) {
  ux <-na.omit(unique(x))
  tab <- tabulate(match(x, ux)); ux[tab == max(tab)]
}

getmode(sharingSystems$SYSTEM)
# "3 Gen. nextbike"
sharingSystems =sharingSystems %>% mutate(SYSTEM = replace (SYSTEM, SYSTEM == NA,'3 Gen. nextbike'))
sharingSystems <- sharingSystems[complete.cases(sharingSystems$SYSTEM),] 
sum(is.na(sharingSystems$SYSTEM))

colSums(sapply(sharingSystems, is.na))
#write_csv(sub_dataset1, 'C:/Users/LENOVO/Desktop/slides/IBM Capiston/final/first_wrangling.csv')

#2nd part for wrangling process:

# so the predicting process will be conducted on the 3rd dataset (row Swoul bike sharig dataset):

head(colnames(seoul))
summary(seoul)
dim(seoul)
sum(is.na(seoul))
colSums(sapply(seoul, is.na))
# 3% missing values in row_bike_count so its safely to drop it 

seoul %>% na.omit(seoul$RENTED_BIKE_COUNT)
seoul <- seoul[complete.cases(seoul$RENTED_BIKE_COUNT),]
sum(is.na(seoul))
#filter_temp<-dataset3 %>% filter(is.na(TEMPERATURE))
#View(filter_temp)
#mean(filter_temp$SEASONS)
## all the missing values in tempreture column is related with just summer season, so its reasonble to imput the missing values for TEMP with average tempreture for summer:

summer_df <- seoul  %>% select (SEASONS=SEASONS,TEMPERATURE=TEMPERATURE) %>% filter (SEASONS == 'Summer') 
summer <- mean(summer_df$TEMPERATURE , na.rm = TRUE)
seoul$TEMPERATURE[is.na(seoul$TEMPERATURE)] <- summer
colSums(is.na(seoul))

#dataset3 %>% mutate(summer_df$TEMPERATURE,TEMPERATURE)
#colSums(is.na(seoul))

#convert categorical variables to numeric
seoul <- seoul %>% mutate_at(c('SEASONS', 'HOLIDAY', 'FUNCTIONING_DAY', 'HOUR'), as.factor) 

#one-hot encoding
class(seoul$HOLIDAY)
install.packages('mltools')
library(mltools)
library(data.table)

data= one_hot(as.data.table(seoul[13:13]))
View(data)
library(dplyr)

seoul <- cbind(seoul, data$Holiday, data$`No Holiday`)
seoul<- rename(seoul,'Holiday'= 'data$Holiday')
seoul=rename(seoul,'No Holiday'='data$`No Holiday`')

seoul <- seoul[,-13]

#newdata <- one_hot(as.data.table(dataset3))
seoul$SEASONS = factor(seoul$SEASONS ,
                         levels = c('Autumn', 'Winter', 'Summer', 'Spring'),
                         labels = c(1, 2, 3, 4))


#normaliz data
#Columns RENTED_BIKE_COUNT, TEMPERATURE, HUMIDITY, WIND_SPEED, VISIBILITY, DEW_POINT_TEMPERATURE, SOLAR_RADIATION, RAINFALL, SNOWFALL are numerical variables/columns with different value units and range. Columns with large values may adversely influence (bias) the predictive models and degrade model accuracy. Thus, we need to perform normalization on these numeric columns to transfer them into a similar range.
normalize <- function(x) {
  return ((x - min(x)) / (max(x) - min(x)))
}


seoul %>% mutate(RENTED_BIKE_COUNT=normalize(RENTED_BIKE_COUNT), TEMPERATURE = normalize(TEMPERATURE),HUMIDITY = normalize(HUMIDITY), 
                                                WIND_SPEED = normalize(WIND_SPEED),VISIBILITY =normalize(VISIBILITY),
                                                DEW_POINT_TEMPERATURE =normalize(DEW_POINT_TEMPERATURE),SOLAR_RADIATION =normalize(SOLAR_RADIATION),
                                                RAINFALL = normalize(RAINFALL), SNOWFALL= normalize(SNOWFALL))


seoul %>% mutate_each(funs(normalize), RENTED_BIKE_COUNT, TEMPERATURE, HUMIDITY, WIND_SPEED,
                         VISIBILITY, DEW_POINT_TEMPERATURE, SOLAR_RADIATION, RAINFALL, SNOWFALL )

#clean weather dataset
colSums(sapply(weather, is.na))# no missing values
colSums(sapply(world, is.na))
dim(world)
# population column has 963 out of 26569 with mean
mean(world$POPULATION)
# 162345.7
world$POPULATION = ifelse(is.na(world$POPULATION),
                                  ave(world$POPULATION, FUN = function(x) mean(x, na.rm = TRUE)),
                                   world$POPULATION)
colSums(sapply(world, is.na))

world1<-world

world1$POPULATION <-as.double(as.numeric(world1$POPULATION))
#world1$POPULATION <- noquote(sprintf("%1.3f",world1$POPULATION))   # converts character type to float type

str(world1$POPULATION)
# ISO2 31 - drop it + 
world %>% na.omit(world$ISO2)
world <- world[complete.cases(world$ISO2),]
colSums(sapply(world, is.na))


#ADMIN_NAME 76 ALSO WILL REPLACED BY "-" SINCE IT NOT necessary INFO
world <- world %>% mutate(ADMIN_NAME = replace(ADMIN_NAME,is.na(ADMIN_NAME),"-"))
colSums(sapply(world, is.na))

# CAPITAL handle it with replacing it with - since this info not necessary BUT I will not delet the eows
world <- world %>% mutate(CAPITAL = replace(CAPITAL,is.na(CAPITAL),"-"))
colSums(sapply(world, is.na))
library(tidyverse)

# save all cleaned datasets again :
write_csv(seoul,'C:/Users/LENOVO/Desktop/slides/FIXED_DATA/seoul.csv')
write.csv(seoul,'C:/Users/LENOVO/Desktop/slides/FIXED_DATA/seoul1.csv')
write_csv(sharingSystems,'C:/Users/LENOVO/Desktop/slides/FIXED_DATA/sharingSystems.csv')
write_csv(world,'C:/Users/LENOVO/Desktop/slides/FIXED_DATA/world.csv')
write_csv(world1,'C:/Users/LENOVO/Desktop/slides/FIXED_DATA/world1.csv')
write_csv(weather,'C:/Users/LENOVO/Desktop/slides/FIXED_DATA/weather.csv')

#standarize the columns names again
