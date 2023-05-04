library(tidyverse)
library(reader)
dataset1 <-read_csv('C:/Users/LENOVO/Documents/Hajar/raw_bike_sharing_systems.csv')
dataset2 <-read_csv('C:/Users/LENOVO/Documents/Hajar/raw_worldcities.csv')
dataset3 <-read_csv('C:/Users/LENOVO/Documents/Hajar/raw_seoul_bike_sharing.csv')
dataset4 <-read_csv('C:/Users/LENOVO/Documents/Hajar/raw_cities_weather_forecast.csv')
#1

colnames(dataset1) <- str_replace_all(names(dataset1),' ','_')
colnames(dataset1) <- toupper(colnames(dataset1))

write_csv(dataset4,'raw_bike_sharing_systems.csv')

#2
colnames(dataset2) <- str_replace_all(names(dataset2),' ','_')
colnames(dataset2) <- toupper(colnames(dataset2))

write_csv(dataset2,'raw_seoul_bike_sharing.csv')

#3
colnames(dataset3) <- str_replace_all(names(dataset3),' ','_')
colnames(dataset3) <- toupper(colnames(dataset3))

write_csv(dataset3,'raw_cities_weather_forecast.csv')


#4
colnames(dataset4) <- str_replace_all(names(dataset4),' ','_')
colnames(dataset4) <- toupper(colnames(dataset4))

write_csv(dataset4,'raw_cities_weather_forecast.csv')

'''
dataset_list<- c(dataset1, dataset2, dataset3)
for (data_name in dataset_list){
  dataset<-read_csv(data_name)
  colnames(data_name) <- str_replace_all(colnames(data_name),' ','_')
  colnames(data_name) <- toupper(colnames(data_name))  
  write.csv(data_name,row_names,row.names = False)
  }
'''
