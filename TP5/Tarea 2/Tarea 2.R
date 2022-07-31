############# TRABAJO PRÁCTICO 5 : DATA VISUALIZATION - tarea 2 #############
############# LEYRE SÁENZ GUILLÉN Y VALERIA ZOTTOS ###############

#Load Libraries
library("ggplot2")
library("tibble")
library("gridExtra")
library("dplyr")
library("Lock5Data")
library("ggthemes")
library("fun")
library("zoo")
library("corrplot")
library("maps")
library("mapproj")
library("ggpubr")
library("tidyverse")
library("shadowtext")
library("rgdal")
library("dplyr")
library("tmap")
library("broom")

#seteamos directorio 
setwd("/Volumes/GoogleDrive-112553083728584115268/My Drive/Herramientas computacionales/Clase 5/videos 2 y 3")

#cargamos shapefile de Londres
lnd <- readOGR(dsn = "data/london_sport.shp")

#download.file("http://data.london.gov.uk/datafiles/crime-community-safety/mps-recordedcrime-borough.csv", destfile = "mps-recordedcrime-borough.csv")
# UPDATE (but not the same...) https://data.london.gov.uk/dataset/recorded_crime_summary

crime_data <- read.csv("data/mps-recordedcrime-borough.csv",
                       stringsAsFactors = FALSE)

head(crime_data$CrimeType) # information about crime type

# Extract "Theft & Handling" crimes and save
crime_theft <- crime_data[crime_data$CrimeType == "Theft & Handling", ]

# Calculate the sum of the crime count for each district, save result
crime_ag <- aggregate(CrimeCount ~ Borough, FUN = sum, data = crime_theft)

# Compare the name column in lnd to Borough column in crime_ag to see which rows match.
lnd$name %in% crime_ag$Borough
# Return rows which do not match
lnd$name[!lnd$name %in% crime_ag$Borough]

# We use left_join because we want the length of the data frame to remain unchanged, with variables from new data appended in new columns (see ?left_join). The *join commands (including inner_join and anti_join) assume, by default, that matching variables have the same name. Here we will specify the association between variables in the two data sets:

head(lnd$name,100) # dataset to add to 
head(crime_ag$Borough,100) # the variables to join

lnd@data <- left_join(lnd@data, crime_ag, by = c('name' = 'Borough'))

# Mapa de thefts de Londres con ggplot

## ggmap requires spatial data to be supplied as data.frame, using tidy(). The generic plot() function can use Spatial objects directly; ggplot2 cannot. Therefore we need to extract them as a data frame. The tidy function was written specifically for this purpose. For this to work, broom package must be installed.
lnd_f <- broom::tidy(lnd)

# This step has lost the attribute information associated with the lnd object. We can add it back using the left_join function from the dplyr package (see ?left_join).
lnd$id <- row.names(lnd) # allocate an id variable to the sp data
lnd_f <- left_join(lnd_f, lnd@data) # join the data

# The new lnd_f object contains coordinates alongside the attribute information associated with each London Borough. It is now straightforward to produce a map with ggplot2. coord_equal() is the equivalent of asp = T in regular plots with R:

## ----"Mapa de Thefts in London"-------------------------------
mapggplot <- ggplot(lnd_f, aes(long, lat, group = group, fill = CrimeCount)) +
  geom_polygon(colour="darkgray") + coord_equal() +
  geom_path(colour="black", lwd=0.05) + 
  coord_equal() +
  labs(x = "", y = "",
       fill = "% of thefts") +
  ggtitle("London Thefts") + 
  geom_shadowtext (aes (label = name),
                   check_overlap = TRUE,
                   size = 3,
                   hjust = 0.5,                            
                   vjust = 0.5,                           
                   color = "black",                       
                   bg.color="white") + 
  scale_fill_distiller(palette = "Reds",
                       direction = +1, 
                       name = "Thefts by borough")

mapggplot

#we save the map

ggsave("mapggplot.png")

# What is wrong with this map is that the borough is duplicated due to an excess of data per borough. We ask classmates what they did with this problem and me decided to create one variable so we can have only one label. 
#We need less data, so first we check if the variables are in numeric format:  
lapply(lnd_f, class) #or
#sapply(lnd_f, class)

#In order to create new variables and not change the original file, we make a copy.
copylnd <- lnd_f

# We transform the variables in numeric expression 
copylnd$piece <- as.numeric(as.factor(copylnd$piece))
copylnd$group <- as.numeric(as.factor(copylnd$group))
copylnd$Pop_2001 <- as.numeric(as.character(copylnd$Pop_2001))
copylnd$id <- as.numeric(as.character(copylnd$id))
copylnd$ons_label <- as.numeric(as.character(copylnd$ons_label))

#Estimation of the mean of the variables in the df copylnd
vars_copylnd_mean <- copylnd %>%
  group_by(name)%>%
  summarise_all("mean")

#Use the same code as before but adding data=vars_copylnd_mean 
mapggplot1 <- ggplot(lnd_f, aes(long, lat, group = group, fill = CrimeCount)) +
  geom_polygon(colour="darkgray") + coord_equal() +
  geom_path(colour="black", lwd=0.05) + 
  coord_equal() +
  labs(x = "", y = "",
       fill = "% of thefts") +
  ggtitle("London Thefts") + 
  geom_shadowtext (aes (label = name),
                   check_overlap = TRUE,
                   data = vars_copylnd_mean, #this is what we add
                   size = 3,
                   hjust = 0.5,                            
                   vjust = 0.5,                           
                   color = "black",                       
                   bg.color="white") + 
  scale_fill_distiller(palette = "Reds",
                       direction = +1, 
                       name = "Thefts by borough")

mapggplot1

#we save the map

ggsave("mapggplot1.png")

###### TMAP ######
# tmap was created to overcome some of the limitations of base graphics and ggmap.
maptmap <- tm_shape(lnd) +
  tm_polygons("CrimeCount", 
              title = "Thefts by borough",
              palette = "Oranges") +
  tm_layout(main.title = "Thefts in London",
            main.title.color = "grey1",
            main.title.position = c("left", "top"),
            legend.outside = TRUE)+
  tm_text("name",
          shadow = TRUE,
          remove.overlap = TRUE)
  
maptmap

#save the map
tmap_save(maptmap, "maptmap.png")




