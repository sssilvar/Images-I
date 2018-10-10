library(ADNIMERGE)
library(ggplot2)
library(dplyr)
library(tibble)
library(zoo)

get_diagnoses <- function(id, tb, visualize = FALSE) {
  # Returns all the diagnoses related to an specific ID
  subject <- tb[which( tb$RID == id ), ]
  dxs <- subject$DX
  dx_grad <- sum(diff(as.integer( na.locf(dxs) )))
  
  if (dx_grad == 1){
    label <- "MCI to Dementia"
  } else if (dx_grad == 0) {
    label <- "MCI Stable"
  } else if (dx_grad == -1) {
    label <- "Regression"
  } else {
    label <- "NA"
  }
  
  if (visualize) {
    print(dxs)  # DEBUG
  }
  return(label)
}

# Get sex and diagnose
baseline <- adnimerge %>%
  filter(Month == 0 & !is.na(AGE) & DX == 'MCI')

# Iterate over all the MCIs and evaluate who converted and who did not
for (id in baseline$RID) {
  dx <- get_diagnoses(id, adnimerge)
  baseline$label[which(baseline$RID == id)] <- dx
  # cat("[  INFO  ] Subject", id, "label:", dx, "\n\n")  # DEBUG
}

# Get just conversions and stable
mcis <- baseline %>%
  filter(label != "Regression" & label != "NA")

# ggplot(baseline, aes(x=RID)) + geom_histogram(binwidth = 1)  # Check RID is unique

# Plot age and diagnosis
ggplot(mcis, aes(x = label , y = AGE, color = PTGENDER)) + geom_boxplot() + facet_wrap(~ COLPROT)

# Print participants

table(mcis$label, mcis$COLPROT)
cat("\n\n[  INFO  ] Number of participants:\n")
table(mcis$label, mcis$PTGENDER)
