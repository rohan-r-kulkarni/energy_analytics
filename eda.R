# Example state: Texas
# STL decomposition shows that the generation/revenue data is non stationary
# Exponential smoothing, moving averages would work better than ARIMA (autoregressive)

library(ggplot2)
library(ggfortify)
library(xts)
library(lubridate)

# import generation datasets (X)
indus <- c("biomass", "coal", "hydroelectric", "naturalgas", "nuclear", "solar", "wind", "wood")

genlist <- list()
for (i in 1:length(indus)){
  filepath <- paste("clean_data/clean_", indus[i], "_gen.csv", sep="")
  this_df <- data.frame(read.csv(filepath))
  genlist[[i]] <- this_df
}

# import population dataset (normalizer)
pop <- read.csv("clean_data/clean_population.csv")
head(pop)

# import response variables
climatecols <- c("DSCI", "pH", "temp", "turbidity")
climatedata <- list()
for (i in 1:length(climatecols)){
  filepath <- paste("clean_data/resp/clean_", climatecols[i], ".csv", sep="")
  this_df <- data.frame(read.csv(filepath))
  climatedata[[i]] <- this_df
}
rev <- read.csv("clean_data/resp/clean_revenue.csv")
head(rev)

########

# Choose one state (we will make this a loop later)
state <- "Texas"
time <- seq(as.Date("2001-01-01"), as.Date("2022-12-01"), by="month")
shifted.time <- na.omit(shift(time, 1))

#building climate index
equal.weighting <- replicate(length(climatecols), 1/length(climatecols)) # user-defined

minmax.scaler <- function(x){(x-min(x))/(max(x)-min(x))}


get.state.climateindex <- function(state, weighting){
  index <- replicate(nrow(data.frame(climatedata[1])), 0) # 0-initialize
  for (i in 1:length(climatecols)){
    values <- c(data.frame(climatedata[i])[,state])    
    values <- minmax.scaler(values)*100 #scale each climate variable
    index <- index + values*weighting[i]
  }
  return (minmax.scaler(index)*100) #scale the whole index
}

state.climindex <- get.state.climateindex(state, equal.weighting)

# create response variable
careparam <- 0.7 #the "care" parameter
get.response <- function(state, climindex, param){
  sales <- minmax.scaler(rev[,state]/pop[,state])*100 
  #scaled revenue per capita from energy sales
  resp <- param*sales + (1-param)*climindex #scale the convex combo
  return (resp)
}
state.resp <- get.response(state, state.climindex, careparam)

# X vs. Y
shift <- function(x, n){
  c(x[-(seq(n))], rep(NA, n))
}
get.stateXY <- function(state, resp){
  X <- data.frame((matrix(nrow=length(time))))
  for (i in 1:length(indus)){
    col.name <- indus[i]
    cols.available <- c(names(genlist[[i]]))
    if (state %in% cols.available){
      # per capita generation by sector, then scaled up
      X[[col.name]] <- (data.frame(genlist[[i]])[,state]/pop[,state])*(10e4)
    }
  }
  out <- X[,2:length(names(X))]
  out[["RESP"]] <- resp
  out$RESP <- shift(out$RESP, 1) #shift to predict next month on this month
  
  return (na.omit(out)) # 263 observations
}
stateXY <- get.stateXY(state, state.resp)

## STL ##

plot.vs.time <- function(vals, this.time, ytitle="Value", maintitle=""){
  df <- data.frame(Time = this.time, yvar = vals)
  p <- ggplot(df, aes(x=Time, y=yvar)) + ylab(ytitle) + ggtitle(paste(maintitle, "Time Series")) + geom_line() + scale_x_date(date_labels = "%b %Y", date_breaks = "1 year") + theme(axis.text.x=element_text(angle=50, hjust=1)) 
  return (p)
}


plot.stl <- function(vals, this.time, freq=12, maintitle="Time Series"){
  start <- c(year(xts::first(this.time)), month(xts::first(this.time)))
  end <- c(year(xts::last(this.time)), month(xts::last(this.time)))
  tsobject <- ts(data = as.vector(coredata(vals)),
                 start = start,
                 end = end, frequency = freq)
  fit <- stl(tsobject, s.window = "periodic")
  p <- autoplot(fit, ts.colour = 'blue') + ggtitle(paste("STL Decomposition of", maintitle))
  return (p)
}

plot.vs.time(state.resp, time, "Response", "Response")
plot.stl(state.resp, time, freq=12, maintitle="Reponse")

# do for every generation in indus
indus <- c("biomass", "coal", "hydroelectric", "naturalgas", "nuclear", "solar", "wind", "wood")


