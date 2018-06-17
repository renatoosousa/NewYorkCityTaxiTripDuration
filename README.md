# New York City Taxi Trip Duration
This repository contains the analysis and visualizations I have created in my first Tableau project.

#### About
This project contains the entire study on the chosen database, the reason for each graphical representation and also what conclusion was obtained.

Topics covered:
* Feature engineering
* Data cleaning
* Feature relations

#### Dataset

#### Feature Engineering
##### Distance
To calculate the distance (in Km) between trip pickup and dropoff points (latitude and longitude), a [python script](/preprocessing/preprocessing.py) was run on the raw database. The calculated distance is an approximation, since here the Euclidean distance is calculated and not the real way through the streets.
##### Average Speed
The average speed for each trip was calculated from `trip_durationMinute` and `Distance`, as follows:
```
[Distance] / ([trip_durationMinute] / 60)
```
##### Categories
Categories have been created to make it easier to create iterative filters. An example is `DropoffLatCategory`:
```
IF [dropoff_lat] > 41.4
THEN "Out"
ELSEIF [dropoff_lat] < 40,630
THEN "Out"
ELSE "In"
END
```
In the next section, I will explain better the choice of each threshold.

#### Data Cleaning
In this section, I explain how I filtered data that did not look right. After analyzing outliers, global filters are defined (for everyone who uses this database).
##### Trip Duration
when analyzing the distribution of trips by duration, we can find trips with more than 600 minutes (10 hours) and others with 0 minutes. To delete this unusual data, a category has been created `TripDurationCategory`:
```
IF [trip_durationMinute] > 180
THEN 'Invalid Trip'
ELSEIF [trip_durationMinute] < 1
THEN "Invalid Trip"
ELSE "Valid Trip"
END
```
*Obs: 180 minutes in a taxi trip sounds like a lot, but we need to find a value to limit superiorly*
And from this new category, a new filter was created.
##### Passenger
When we visualize the distribution of passenger numbers, we can observe trips with no passengers until traveling with 8 passengers (possibly an error).
In [New York City Taxi & Limousine Commission](http://www.nyc.gov/html/tlc/html/faq/faq_pass.shtml) I could find the rules that define the maximum amount of passengers in a taxi in New York:
> The maximum amount of passengers allowed in a yellow taxicab by law is four (4) in a four (4) passenger taxicab or five (5) passengers in a five (5) passenger taxicab, except that an additional passenger must be accepted if such passenger is under the age of seven (7) and is held on the lap of an adult passenger seated in the rear.

So the maximum of passengers on a taxi ride is 6 passengers. Obviously, the minimum is 1 passenger. A filter was created with these values.

##### Distance
To check if the calculated distance is correct, the best way to analyze was to visualize the Trip Duration by Distance graph. As expected, we can see a linear proportion between the two variables (the greater the distance covered, the longer the time spent). A certain noise is also observed, as well as unexpected values, but I believe it is due to the approximation of the calculation of the distance and the traffic in more agitated moments.

We can also see trips with 0km and more than 300km. A filter was created to only take trips with more than 1km and less than 60km

##### Latitude and Longitude
Based on the latitude and longitude distribution (for pickup and dropoff), a filter was created.
First, new Categories like PickupLatCategory, PickupLongCategory, DropoffLatCategory and DropoffLongCategory
Without this filter, we can see points outside of New York (even in the ocean)

#### Pickup points VS Dropoff points

#### Dynamics of the City
##### Average Speed
##### Average Speed per Weekday and Hour
##### Frequency of Trips per Weekday and Hour

#### Increasing Vendor Trips
##### Vendor Study
##### Best Trips Map
