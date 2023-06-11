# Load required libraries
require(leaflet)


# Create a RShiny UI
shinyUI(
  fluidPage(padding=5,
  titlePanel("Bike-sharing demand prediction app"), 
  # Create a side-bar layout
  sidebarLayout(
    # Create a main panel to show cities on a leaflet map
     mainPanel(
         leafletOutput ('city_bike_map', height = 1000)
    ),
    # Create a side bar to show detailed plots for a city
    sidebarPanel(
        selectInput( inputId = 'City_dropdown',
                     labe='Cities',
                     choices = c('all',
                                 'Seoul',
                                 'New York',
                                 "Paris",
                                 'London',
                                 "Suzhou"
                                 )
      ),
      
        plotOutput('temp_line', width= 575, height  = 250),
        plotOutput('bike_line', click = 'plot_click',  width= 575, height  = 250),
        verbatimTextOutput('bike_date_output'),
        plotOutput('humidity_pred_chart', width= 575, height  = 250)
    ))
    ))
