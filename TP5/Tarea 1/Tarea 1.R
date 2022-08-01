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
setwd("/Volumes/GoogleDrive-112553083728584115268/My Drive/Herramientas computacionales/Clase 5/Applied-Data-Visualization-with-R-and-ggplot2-master")

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

##Gráfico 1 öriginal"- Grammar of graphics and visual components
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
  
  

#Gráfico 3 "original"
  dfn <- df3[,c("home_ownership","loan_amnt","grade")]
  dfn <- na.omit(dfn) #remove NA y NONE
  dfn <- subset(dfn, !dfn$home_ownership %in% c("NONE"))
  #People with higher credit grades take smaller loans
  #People with lower credit grades take small loans if they don't have a mortgage.
  
  #Finer labelling in y 
  ggplot(dfn,aes(x=home_ownership,y=loan_amnt))+geom_boxplot(aes(fill=grade))+
    scale_y_continuous(breaks=seq(0,40000,2000))
  
#Gráfico 3 "modificado"
  # Me quedo con las columnas que me interesan y limpio los null
  loan = df3[,c("home_ownership","loan_amnt","grade")] 
  loan = na.omit(loan)
  
  # Divido por situación de hogar
  df3 = subset(loan, !loan$home_ownership %in% c("NONE")) #esto lo saco de lo que hicimos en el gráfico de películas de cine.
  loan_prom = loan %>% group_by(grade, home_ownership) %>% mutate(prom = mean(loan_amnt)) #consulté con compañeros para esta línea del código.
  
  p1 = ggplot(loan_prom %>% group_by(grade, home_ownership) %>% summarise(prom = mean(prom)), aes(x=grade,y=prom,fill=grade))
  p2 = p1 + geom_col(stat="identity")
  p3 = p2 + facet_wrap(~home_ownership)
  p4 = p3 + labs(x="",
                 y="",
                 title="Promedio de préstamos en dólares según el crédito otorgado dada la situación del hogar" )
  p5 = p4 +theme(text=element_text(size=8))
  p6 = p5 + guides(fill="none")
  p6 + scale_fill_brewer(palette="Viridis")
  
  
  
  
  