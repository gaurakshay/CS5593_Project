df = read.csv("coins_predicted.csv")
head(df)
df$predicted = ifelse(df$predicted >= .5, 1, 0)
results = df$predicted == df$viable
sum(results) / length(results)
sum(df$viable) / length(results)
