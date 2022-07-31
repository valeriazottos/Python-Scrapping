############# TRABAJO PRÁCTICO 5 : DATA VISUALIZATION - tarea 1#############
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

#Set pathname for the directory where you have data
setwd("C:/Users/Merced/Desktop/Applied-Data-Visualization-with-R-and-ggplot2-master/Applied-Data-Visualization-with-R-and-ggplot2-master")

#Check working directory
getwd()

#Note: Working directory should be "Beginning-Data-Visualization-with-ggplot2-and-R"

#Load the data files
df <- read.csv("data/gapminder-data.csv")
df2 <- read.csv("data/xAPI-Edu-Data.csv")
df3 <- read.csv("data/LoanStats.csv")

#Summary of the three datasets
str(df)
str(df2)
str(df3)

##Grammar of graphics and visual components
#Subtopic - Layers
p1 <- ggplot(df,aes(x=Electricity_consumption_per_capita))
p2 <- p1+geom_histogram()
p2
p3 <- p1+geom_histogram(bins=15)
p3

#Exercise-Layers
p4 <- p3+xlab("Electricity consumption per capita")
p4


#Gráfico 1 "cambiado"
 p1 <- ggplot(df,aes(x=Electricity_consumption_per_capita)) +
 geom_histogram(color = "goldenrod3", fill = "goldenrod1") +
 labs(title = "Histogram of electricity consumption per capita",
  main.title.position = c("left","top"), x= "values", y = "count of values")
 p1
#Gráfico 2 "original"
   ### Exercise: Creating density plots
   df3s <- subset(df3,grade %in% c("A","B","C","D","E","F","G"))
   ggplot(df3s,aes(x=loan_amnt)) + geom_density() + facet_wrap(~grade)
  
#Gráfico 2 "modificado"
  ### Exercise: Creating density plots
  df3s <- subset(df3,grade %in% c("A","B","C","D","E","F","G"))
  ggplot(df3,aes(x=loan_amnt)) + geom_density(aes(fill=grade),alpha=0.8) +
    scale_fill_brewer(palette="Oranges") + xlab("Loan Amount") + theme_classic() +
    labs (title = "Loan Amount density plot") 