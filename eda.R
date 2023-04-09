library(ggplot2)

gasp <- read.csv("clean_data/clean_gasprice.csv")
relevstates <- names(gasp)[2:length(names(gasp))]
gasp$X <- as.Date(gasp$X)

gasp$Date <- as.Date(gasp$Date)

p <- ggplot(gasp) + geom_line(aes(x=Date,y=Colorado), group=1, color="red")
p
ggplot(gasp) + geom_line(data=gasp$Colorado, aes(x=Date, y="Value"))

colors = c("red", "blue", "green", "orange", "purple", "black", "magenta")
priceplot <- ggplot(gasp, aes(x=Date)) + xlab("Year") + ylab("Price") + ggtitle("Gas Prices") 
for (i in seq(1,length(relevstates))){
  state <- relevstates[i]
  print(state)
  this_color <- colors[i]
  priceplot <- priceplot + geom_line( aes(y = gasp[[state]]), 
                                     color=this_color)
}
priceplot
?scale_y_date
priceplot <- priceplot + scale_x_date(date_breaks = "1 year") + scale_y_date(breaks = 1)
priceplot <- priceplot + theme(axis.text.x=element_text(angle=50, hjust=1)) 
priceplot
list(gasp["Colorado"])
x <- seq(length(gasp$X))

Ys <- cbind(gasp$Florida, gasp$Colorado, gasp$Ohio)
plot(x, gasp$Colorado, type="l")
lines(x, gasp$Florida, type="l")

?ggplot
axis(1, at = x, labels = gasp$X, las=3)

?plot

p <- ggplot(gasp, aes(x=X,y=Colorado))
p



plot <- +
   +
  geom_line(aes(y = Florida, group = 1), color="blue") +
  geom_line(aes(y = New.York, group = 1), color="green")


?ggplot
