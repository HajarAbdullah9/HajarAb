install.packages('tidymodels')
install.packages('rlang')
install.packages('dplyr')
library(rlang)
remove.packages('tidymodels')
library('tidymodels')
library(stringr)
library(dplyr)
#library(tidymodels)
seoul<-  read.csv('C:/Users/LENOVO/Desktop/slides/FIXED_DATA/seoul1.CSV')
seoul$SEASONS = factor(seoul$SEASONS ,
                       levels = c(1, 2, 3, 4),
                       labels = c('Autumn', 'Winter', 'Summer', 'Spring'))
                      
seoul$HOUR = factor(seoul$HOUR ,
                       levels = c( 1, 2, 3, 4, 5 ,6 ,7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23),
                    labels = c('1', '2', '3', '4', '5' ,'6' ,'7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23'))
                     
                      




install.packages('tidyverse')
install.packages('caTools')
library(caTools)
set.seed(1234)
split = sample.split(seoul, SplitRatio = 0.7)
test_set = subset(seoul, split == FALSE)
training_set = subset(seoul, split == TRUE)

install.packages('caret')
library(caret) 

lm_model_weather<- lm (RENTED_BIKE_COUNT ~ TEMPERATURE + HUMIDITY + WIND_SPEED + VISIBILITY + DEW_POINT_TEMPERATURE + SOLAR_RADIATION + RAINFALL + SNOWFALL, data= training_set)
summary(lm_model_weather)

lm_model_all<- lm(RENTED_BIKE_COUNT ~ TEMPERATURE + HUMIDITY + WIND_SPEED + VISIBILITY + DEW_POINT_TEMPERATURE + SOLAR_RADIATION + RAINFALL + SNOWFALL+ Holiday+ SEASONS+ HOUR,data= training_set)
summary(lm_model_all)

#evaluating
install.packages('uroot')
library(uroot)
install.packages('mtools')
library(mltools)

install.packages("tidyverse")


#install.packages('dplyr')
#library(dplyr)
test_result_weather <- test_set %>% 
  select(RENTED_BIKE_COUNT) %>%
  mutate(data.frame(predicted= c(predict(lm_model_weather,test_set))))
test_result_weather<- rename(test_result_weather, Truth='RENTED_BIKE_COUNT',Predicted=predicted)

test_result_all<- test_set %>% select(RENTED_BIKE_COUNT) %>% mutate(data.frame(predicted=c(predict(lm_model_all,test_set))))
test_result_all<- rename(test_result_all, Truth='RENTED_BIKE_COUNT', Predicted = predicted) 

rmse(test_result_weather, Truth, Predicted)
rsq(test_result_weather, Truth, Predicted)

rmse(test_result_all, Truth, Predicted)
rsq(test_result_all, Truth, Predicted)
# so we can conclude that the linear model for all metrics (lm_model_all)
#is better that linear model for weather factors (lm_model_weather) since
#the RMSE for the 2nd model is
#lower that the 1st one, and also the RSQ is larger than the 1st model.

lm_model_all$coefficients

# THE MODEL FORMULA : 
# RENTED_BIKE_COUNT = 581.39 + 52.2333* TEMPRATURE - 8.5209761* HUMIDITY +
#24.4882551 * WIND_SPEED + 0.1363615 * VISIBILITY + 10.79* DEW_POINT_TEMPRATURE 
#- 180.4345 * SOLAR_RADIATION - 27.8 * RAINFALL + 108.1 * SNOWFALL - 369.3 *Holiday +24.4225*HOUR 

lm_all_coefficients <- abs(lm_model_all$coefficients)
sorted_cofficients<- sort(lm_all_coefficients,decreasing =  TRUE)
sorted_cofficients
#converting to df
cofficients_df<- as.data.frame(sorted_cofficients)
#create plot
ggplot(cofficients_df, aes(x= sorted_cofficients,y= row.names(cofficients_df)))+
  geom_bar(stat = 'identity')+
  xlab('cofficients value')+
  ylab('cofficients namd')+
  ggtitle('Sorted cofficients')


library(ggplot2)

# temprature
ggplot(data=training_set, aes(RENTED_BIKE_COUNT,TEMPERATURE)) + 
  geom_point() + 
  geom_smooth(method = "lm", formula = y ~ x, color="red") + 
  geom_smooth(method = "lm", formula = y ~ poly(x , 2), color="yellow")+
  geom_smooth(method = "lm", formula = y ~ poly(x, 4), color="green") + 
  geom_smooth(method = "lm", formula = y ~ poly(x, 6), color="blue")

#Humidity
ggplot(data=training_set, aes(RENTED_BIKE_COUNT,HUMIDITY)) + 
  geom_point() + 
  geom_smooth(method = "lm", formula = y ~ x, color="red") + 
  geom_smooth(method = "lm", formula = y ~ poly(x , 2), color="yellow")+
  geom_smooth(method = "lm", formula = y ~ poly(x, 4), color="green") + 
  geom_smooth(method = "lm", formula = y ~ poly(x, 6), color="blue")
#wind_speed
ggplot(data=training_set, aes(RENTED_BIKE_COUNT,WIND_SPEED)) + 
  geom_point() + 
  geom_smooth(method = "lm", formula = y ~ x, color="red") + 
  geom_smooth(method = "lm", formula = y ~ poly(x , 2), color="yellow")+
  geom_smooth(method = "lm", formula = y ~ poly(x, 4), color="green") + 
  geom_smooth(method = "lm", formula = y ~ poly(x, 6), color="blue")

#visibility
ggplot(data=training_set, aes(RENTED_BIKE_COUNT,VISIBILITY)) + 
  geom_point() + 
  geom_smooth(method = "lm", formula = y ~ x, color="red") + 
  geom_smooth(method = "lm", formula = y ~ poly(x , 2), color="yellow")+
  geom_smooth(method = "lm", formula = y ~ poly(x, 4), color="green") + 
  geom_smooth(method = "lm", formula = y ~ poly(x, 6), color="blue")

#DEW_POINT_TEMPERATURE
ggplot(data=training_set, aes(RENTED_BIKE_COUNT,DEW_POINT_TEMPERATURE)) + 
  geom_point() + 
  geom_smooth(method = "lm", formula = y ~ x, color="red") + 
  geom_smooth(method = "lm", formula = y ~ poly(x , 2), color="yellow")+
  geom_smooth(method = "lm", formula = y ~ poly(x, 4), color="green") + 
  geom_smooth(method = "lm", formula = y ~ poly(x, 6), color="blue")


#SOLAR_RADIATION
ggplot(data=training_set, aes(RENTED_BIKE_COUNT,SOLAR_RADIATION)) + 
  geom_point() + 
  geom_smooth(method = "lm", formula = y ~ x, color="red") + 
  geom_smooth(method = "lm", formula = y ~ poly(x , 2), color="yellow")+
  geom_smooth(method = "lm", formula = y ~ poly(x, 4), color="green") + 
  geom_smooth(method = "lm", formula = y ~ poly(x, 6), color="blue")

#RAINFALL
ggplot(data=training_set, aes(RENTED_BIKE_COUNT,RAINFALL)) + 
  geom_point() + 
  geom_smooth(method = "lm", formula = y ~ x, color="red") + 
  geom_smooth(method = "lm", formula = y ~ poly(x , 2), color="yellow")+
  geom_smooth(method = "lm", formula = y ~ poly(x, 4), color="green") + 
  geom_smooth(method = "lm", formula = y ~ poly(x, 6), color="blue")

#snowfall
ggplot(data=training_set, aes(RENTED_BIKE_COUNT,SNOWFALL)) + 
  geom_point() + 
  geom_smooth(method = "lm", formula = y ~ x, color="red") + 
  geom_smooth(method = "lm", formula = y ~ poly(x , 2), color="yellow")+
  geom_smooth(method = "lm", formula = y ~ poly(x, 4), color="green") + 
  geom_smooth(method = "lm", formula = y ~ poly(x, 6), color="blue")

#HOUR
ggplot(data=training_set, aes(RENTED_BIKE_COUNT,HOUR)) + 
  geom_point() + 
  geom_smooth(method = "lm", formula = y ~ x, color="red") + 
  geom_smooth(method = "lm", formula = y ~ poly(x , 2), color="yellow")+
  geom_smooth(method = "lm", formula = y ~ poly(x, 4), color="green") + 
  geom_smooth(method = "lm", formula = y ~ poly(x, 6), color="blue")

#install.packages('polynom')
#ggplot(data=training_set) + geom_point()+ geom_smooth(method = "lm", formula = lm_poly)

#poly1<-lm(RENTED_BIKE_COUNT~poly(TEMPERATURE,6,raw=TRUE))

lm_poly<-lm(RENTED_BIKE_COUNT~ poly(TEMPERATURE,6)  + poly(WIND_SPEED,6) + poly(SNOWFALL ,6)+ poly(HOUR,6) , data= training_set)
summary(lm_poly$fit)


library(dplyr)

lm_poly_predict<- test_set %>% select (RENTED_BIKE_COUNT) %>% mutate(data.frame(predicted=c(predict(lm_poly, test_set))))
lm_poly_predict_result<- rename(lm_poly_predict, Truth='RENTED_BIKE_COUNT', predicted= predicted)

#converting negative predicted result into positive
lm_poly_predict_result['predicted1']<-abs(lm_poly_predict_result$predicted)
lm_poly_predict_result



#lm_poly_predict_result3['predicted']<-lm_poly_predict_result$predicted[which(lm_poly_predict_result$predicted>0)]
#lm_poly_predict_result2['Truth']<- lm_poly_predict_result$Truth
install.packages('Metrics')
head(lm_poly_predict_result)

rmse(lm_poly_predict_result, Truth, predicted1)
rsq(lm_poly_predict_result, Truth, predicted1)


# interaction poly linear model:

lm_poly_interacted<-lm(RENTED_BIKE_COUNT~ poly(TEMPERATURE,6)  * poly(WIND_SPEED,6) * poly(SNOWFALL ,6) * poly(HOUR,6) , data= training_set)
summary(lm_poly_interacted$fit)

#interacted_predicted<- test_set %>% select (RENTED_BIKE_COUNT) %>% mutate(data.frame(predicted=c(predict(lm_poly_interacted, test_set))))
#interacted_predicted_result<- rename(interacted_predicted, Truth='RENTED_BIKE_COUNT', predicted= predicted)

prediction <- lm_poly_interacted %>% predict(test_set)
RMSE(prediction, test_set$RENTED_BIKE_COUNT)
R2(prediction,test_set$RENTED_BIKE_COUNT)
#tail(interacted_predicted_result)
#interacted_predicted_result['predicted1']<-abs(interacted_predicted_result$predicted)
#lm_poly_interacted_predicted_result
#library(tidymodels)
#RMSE(interacted_predicted_result, Truth , predicted1)
#res (interacted_predicted_result, Truth , predicted1)

#regularization
all_recipe<- 
  recipe(RENTED_BIKE_COUNT~. , data= training_set ,  filter= ('DATE'+'SEASONS'+'FUNCTIONING_DAY' ))
ridge_spec <- linear_reg(penalty = 0.1, mixture =  0) %>% 
  set_engine('glmnet')

install.packages('glmnet')
library('glmnet')

ridge_wf <- workflow() %>% add_recipe(all_recipe)
ridge_fit<- ridge_wf %>% add_model(ridge_spec) %>% fit(data = training_set)
