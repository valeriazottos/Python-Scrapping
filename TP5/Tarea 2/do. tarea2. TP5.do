//// HERRAMIENTAS COMPUTACIONALES DE INVESTIGACIÓN TP5 ////
//////// LEYRE SÁENZ GUILLÉN & VALERIA ZOTTOS ////////////


*Instalamos los paquetes que necesitamos

ssc install spmap
ssc install shp2dta
*net install sg162, from(http://www.stata.com/stb/stb60)
*net install st0292, from(http://www.stata-journal.com/software/sj13-2)
net install spwmatrix, from(http://fmwww.bc.edu/RePEc/bocode/s)
*net install splagvar, from(http://fmwww.bc.edu/RePEc/bocode/s)
*ssc install xsmle.pkg
*ssc install xtcsd
*net install st0446.pkg

*Seteamos el directorio 
global DATA = "/Volumes/GoogleDrive-112553083728584115268/My Drive/Herramientas computacionales/Clase 5/videos 2 y 3/data"
cd "$DATA"


* Leer la información shape en Stata

shp2dta using london_sport.shp, database(ls) coord(coord_ls) genc(c) genid(id) replace

* Importamos y transformamos los datos de Excel a formato Stata 
import delimited "$DATA/mps-recordedcrime-borough.csv", clear 
* En Stata necesitamos que la variable tenga el mismo nombre en ambas bases para juntarlas
keep if crimetype== "Theft & Handling" 
rename borough name
* preserve
collapse (sum) crimecount, by(name)
save "crime_.dta", replace

describe

* Uniremos ambas bases: london_sport y crime. Su usa la función merge con la variable name que se encuentra en ambas bases 

use ls, clear
merge 1:1 name using crime_.dta
*merge 1:1 name using crime.dta, keep(3) nogen
*keep if _m==3
drop _m

save london_crime_shp_1.dta, replace


*Cragamos el shapefile de london crime 
use london_crime_shp_1.dta, clear

*Nos quedamos con las variables que necesitamos y las guardamos 
keep x_c y_c name
save "vars_theft.dta", replace



*Cargamos la base
use london_crime_shp_1.dta, clear

*Creamos el mapa 
spmap crimecount using coord_ls, id(id) line(data("coord_ls.dta") color(gs10) size(vthin)) ///
    clmethod(q) cln(6) ///
    title("Number of thefts by borough") ///
    label(data("vars_theft.dta") x(x_c) y(y_c) label(name) size(tiny)) ///
    legend(size(vsmall) position(5) xoffset(1)) ///
    fcolor(Reds) plotregion(margin(b+15)) ndfcolor(gray) name(gtarea2,replace) 




