get_weather_forcasting<- function(city_name){
  df<-data.frame()
  for (city_name in city_name){
    forecast_url <- 'https://api.openweathermap.org/data/2.5/forecast'
    forecast_quer <- list(q = city_name, appid = '0999031957056343b00afa47c6adec5a', units= 'metric')
    response<- GET(forecast_url,query= forecast_quer)
    jsonresult<- content(response, as='parsed')
    results<-jsonresult$list
  
    for(result in results){
      city <- c(city, city_name)
      weather <- c(weather, weather[[1]]$main)
      visibility <- c(visibility,visibility)
      temp <- c(temp,temp)
      temp_min <- c(temp_min,temp_min)
      temp_max <- c(temp_max,temp_max)
      pressure <- c(pressure,pressure)
      humidity <- c(humidity,humidity)
      wind_speed <- c(wind_speed,wind_speed)
      wind_deg <- c(wind_deg,wind_deg)
      forecast_datetime <- c(forecast_datetime,forecast_datetime)
      # Season column
      # Note that for season, you can hard code a season value from levels Spring, Summer, Autumn, and Winter based on your current month.
      season <- c(season,season)
     
    }
  
  }
  
  return(df)
  
  }

cities = c ('Seoul',"Washington, D.C.", "Paris", "Suzhou")
get_weather_forcasting(cities)
