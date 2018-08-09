#Returns top N% of the patches by d-norm contrast
#Input: filename, N%
topN <- function(filename, N) {
  patches <- read.csv(filename, header = F)
  t <- subset(patches, V10 > quantile(V10, probs = 1 - N/100))
  #write.table(t[,-10], paste(filename, ".input", sep = ""), row.names = F, col.names = F)
  return(t)
}

#Reduced dim (subtract mean divide by contrast) for top 20% pixels with dnorm contrast
top20_dnorm <- topN("patches_sample1.txt", 20)
res <- data.frame()
for (i in 1:nrow(top20_dnorm)) {
  pixels <- top20_dnorm[i,][,-10]
  contrast <- as.numeric(top20_dnorm[i,][10])
  pixels <- pixels - mean(as.numeric(pixels))
  pixels <- as.numeric(pixels)/contrast
  #print(pixels)
  res <- rbind(res, pixels)
}
write.table(res, "patches_top20", row.names = F, col.names = F)
