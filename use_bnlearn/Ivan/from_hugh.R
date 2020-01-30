
library(readstata13)
ivan_data <- read.dta13("Statistics/hurricane/IvanKatrinaStudies/IvanExport.dta")
write.csv(ivan_data, file = "Statistics/hurricane/IvanKatrinaStudies/IvanExport.csv")

Ivankat_data <- read.dta13("Statistics/hurricane/IvanKatrinaStudies/IvanKat.dta")
write.csv(Ivankat_data, file = "Statistics/hurricane/IvanKatrinaStudies/IvanKat.csv")