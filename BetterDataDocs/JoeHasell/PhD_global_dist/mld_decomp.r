library(gpinter)
library(tidyverse)


url = "https://joeh.fra1.digitaloceanspaces.com/PIP/percentiles_filled.csv"


df<- read.csv(url)




# +
gpinter_deciles<- function(distribution){

#choose the lower bracket thresholds, begin from 0 
p <- c(seq(0,90,10))/100

# This calculates the upper brakect thresholds (up to 1)
p_1<- c(tail(p, length(p)-1),1)

average_in_bracket<- bracket_average(distribution, p, p_1)

q<- fitted_quantile(distribution, p)

#average_above<- top_average(distribution, p)

#share_above<- top_share(distribution, p)

# size of bracket (share of population)
#share_of_pop<- p_1 - p

#output <- data.frame(p, q, average_in_bracket, average_above, share_above, share_of_pop)
output <- data.frame(p, q, average_in_bracket)

return(output)

}
