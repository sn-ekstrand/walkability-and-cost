# Apartment Walkability and Cost per Square Foot

Maybe it's a Sunday morning and you want to go for a walk and grab a coffee from your local cafe. Or maybe it's a Wednesday night and you need a few ingredients for dinner so you want to walk to a store. Or maybe it's a Saturday night and you're going out with friends, but you don't want to worry about finding a designated driver. Do you have the option to walk to these places? Or are you looking to get a new apartment that enables you to walk to places like these? Are you prepared to pay the increased rent or live with the small unit? 

This study asks the question is the Walkscore of an apartment positively correlated with the cost per square foot of that apartment?  

## ... 
![](https://github.com/sn-ekstrand/walkability-and-cost/blob/master/images/austin_walkscore.png)  
[Walkscore.com](https://www.walkscore.com/) provides a rating for any address based on how many places are nearby. These are places like cafes, resturants, banks, schools, or grocery stores. 


## Hypotheses
Common knowledge tells you that urban environments are more expensive than sub-urban and rural ones, and apartments are not viewed as exception.  

H0: The mean rent/SqFt is the same for high Walkscore locations and low Walkscore locations.  
Ha: The mean rent/Sqft for high Walkscore locations is higher than low Walkscore locations.  
This analysis defines a high Walkscore as anything at or above 70, a "Walker's Paradise" or "Very Walkable". "Somewhat Walkable" and "Car-dependent" are considered low Walkscores.  
Significance alpha is set at 5%.

## Data
Data for this project was scraped from Apartments.com, which includes cost of rent, unit area, and a widget with [Walkscore](https://www.walkscore.com/) information. 489 apartment pages were collected. For each location, a mean rent and a mean unit area was calculated. 7 outliers based on the high rent/SqFt field were removed. 

## Statistical Test
A t-test is used because we want to compare the means of two groups. The resulting p-value is 1.728e-08 and we reject the null hypothesis that the mean rent/SqFt is the same for both Walkscore groups. 

![box plot]()

## Future Steps
- This study only used 482 apartments from Austin, TX. I would like to look at more cities and to gain more data from each city in general. With this we can start to compare cities and have more confidence in our analysis.  
- Aside from a Walkscore, each location has a transit score and a bike score. I would like to run an analysis for each one. 
- This test only looks at apartments but I would like to also look at houses and commercial property. 

![walkscore table]()
