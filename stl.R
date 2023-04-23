# Example state: Texas
# STL decomposition shows that the generation/revenue data is non stationary
# Exponential smoothing, moving averages would work better than ARIMA (autoregressive)

library(ggplot2)
library(ggfortify)
library(xts)
library(lubridate)
library(stringr)


# import generation datasets (X)
indus <- c("biomass", "coal", "hydroelectric", "naturalgas", "nuclear", "wind", "wood")

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

shift <- function(x, n){
  c(x[-(seq(n))], rep(NA, n))
}

state <- "Texas"
careparam <- 0.9 #the "care" parameter

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
  p <- autoplot(fit, ts.colour = 'blue') + ggtitle(paste("STL Decomposition of", maintitle)) + scale_x_date(date_labels = "%b %Y", date_breaks = "1 year") + theme(axis.text.x=element_text(angle=50, hjust=1)) 
  return (p)
}

plot.vs.time(state.resp, time, "Response", "Response")
resp.plot <- plot.stl(state.resp, time, freq=12, maintitle="Reponse, Care Parameter=0.9")
filepath <- paste0(getwd(),"/plots/stl/")
save.filetitle <- paste0(tolower(state), "_stl_", "response")
ggsave(paste0(filepath, save.filetitle, ".png"), resp.plot,"png")


# do for every generation in indus
indus <- c("biomass", "coal", "hydroelectric", "naturalgas", "nuclear", "wind", "wood")
genlist[1]
for (i in seq(length(indus))){
  filepath <- paste0(getwd(),"/plots/stl/")
  save.filetitle <- paste0(tolower(state), "_stl_", indus[i])
  
  gen <- data.frame(genlist[i])[,state]
  gen.time <- data.frame(genlist[i])[,"X"]
  gen.title <- paste(str_to_title(indus[i]), "Generation -", state)
  this.stlplot <- plot.stl(gen, gen.time, freq=12, maintitle=gen.title)
  print(this.stlplot)
  ggsave(paste0(filepath, save.filetitle, ".png"), this.stlplot,"png")
}




