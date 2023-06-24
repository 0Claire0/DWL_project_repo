install.packages("ggcorrplot")
library("ggcorrplot")
library("dplyr")

regression_data <- read.csv("~/Documents/Mon dossier Tableau Prep/Sources de données/Output_DWL_regression.csv", sep=";", comment.char="#")
summary(regression_data)

# change data type to numerical for all emotions, precip_24h and temp24h
regression_data$joy <- scan(text=regression_data$joy, dec=",", sep=".")
regression_data$joy <- as.numeric(regression_data$joy)

regression_data$sadness <- scan(text=regression_data$sadness, dec=",", sep=".")
regression_data$sadness <- as.numeric(regression_data$sadness)

regression_data$anger <- scan(text=regression_data$anger, dec=",", sep=".")
regression_data$anger <- as.numeric(regression_data$anger)

regression_data$optimism <- scan(text=regression_data$optimism, dec=",", sep=".")
regression_data$optimism <- as.numeric(regression_data$optimism)

regression_data$precip_24h <- scan(text=regression_data$precip_24h, dec=",", sep=".")
regression_data$precip_24h <- as.numeric(regression_data$precip_24h)

regression_data$temp_24h <- scan(text=regression_data$temp_24h, dec=",", sep=".")
regression_data$temp_24h <- as.numeric(regression_data$temp_24h)

# transform weekday variable into factors
regression_data$extraction_weekday <- as.factor(regression_data$extraction_weekday)

# correlation matrix between all variables of interest
df = data.frame(regression_data)
df <- df[c("anger", "joy", "sadness", "optimism", "extraction_weekday", "explicit_bool", "temp_24h", "precip_24h")]
df$extraction_weekday <- as.factor(df$extraction_weekday)

model.matrix(~0+., data=df) %>% 
  cor(use="pairwise.complete.obs") %>% 
  ggcorrplot(show.diag=FALSE, type="lower", lab=TRUE, lab_size=2, colors = c("red", "white", "blue"))

# linear model for joy, including weekdays, temperature and precipitation
model_test1_joy <- lm(joy ~ extraction_weekday + temp_24h + precip_24h, data = regression_data)
print(summary(model_test1_joy))

# testing significance of categorical variables (F-test)
drop1(model_test1_joy, test = "F")

# linear model for sadness, including weekdays, temperature and precipitation
model_test2_sadness <- lm(sadness ~ extraction_weekday + temp_24h + precip_24h, data = regression_data)
print(summary(model_test2_sadness))

# testing significance of categorical variables (F-test)
drop1(model_test2_sadness, test = "F")

# linear model for anger, including weekdays, temperature and precipitation
model_test3_anger <- lm(anger ~ extraction_weekday + temp_24h + precip_24h, data = regression_data)
print(summary(model_test3_anger))

# testing significance of categorical variables (F-test)
drop1(model_test3_anger, test = "F")

# linear model for optimism, including weekdays, temperature and precipitation
model_test4_optimism <- lm(optimism ~ extraction_weekday + temp_24h + precip_24h, data = regression_data)
print(summary(model_test4_optimism))

# testing significance of categorical variables (F-test)
drop1(model_test4_optimism, test = "F")
