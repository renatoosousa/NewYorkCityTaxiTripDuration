# New York City Taxi Trip Duration
This repository contains the analysis and visualizations I have created in my first Tableau project.

If you feel better, you can view the [project here](https://public.tableau.com/profile/renato.sousa#!/vizhome/NewYorkCityTaxiTripDuration/NewYorkTaxiTrip).

The project is also present in this repository in `NYTaxiTrip.twb`.

#### About
This project contains the entire study on the chosen database, the reason for each graphical representation and also what conclusion was obtained.

Topics covered:
* Feature engineering
* Data cleaning
* Feature relations

#### Dataset
The database was taken from the [New York City Taxi Trip Duration](https://www.kaggle.com/c/nyc-taxi-trip-duration/data) competition at Kaggle.
> In this competition, Kaggle is challenging you to build a model that predicts the total ride duration of taxi trips in New York City. Your primary dataset is one released by the NYC Taxi and Limousine Commission, which includes pickup time, geo-coordinates, number of passengers, and several other variables.

The base chosen was the training base (`train.csv`) containing 1458644 trip records.

The base contains the following attributes:

* id - a unique identifier for each trip
vendor_id - a code indicating the provider associated with the trip record
* pickup_datetime - date and time when the meter was engaged
dropoff_datetime - date and time when the meter was disengaged
* passenger_count - the number of passengers in the vehicle (driver entered value)
* pickup_longitude - the longitude where the meter was engaged
* pickup_latitude - the latitude where the meter was engaged
* dropoff_longitude - the longitude where the meter was disengaged
* dropoff_latitude - the latitude where the meter was disengaged
* store_and_fwd_flag - This flag indicates whether the trip record was held in vehicle memory before sending to the vendor because the vehicle did not have a connection to the server - Y=store and forward; N=not a store and forward trip
* trip_duration - duration of the trip in seconds

You can do the raw base download, save in `/data`, and then in `/preprocessing` run the `preprocessing.py` script; or unrar the file `train.rar` in `/data`

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
ELSEIF [dropoff_lat] < 40.630
THEN "Out"
ELSE "In"
END
```
In the next section, I will explain better the choice of each threshold.

#### Data Cleaning
In this section, I explain how I filtered data that did not look right. After analyzing outliers, global filters are defined (for everyone who uses this database).

![dataClean](/imgs/DataCleaning.png)
##### Trip Duration
when analyzing the distribution of trips by duration, we can find trips with more than `600 minutes` (`10 hours`) and others with `0 minutes`. To delete this unusual data, a category has been created `TripDurationCategory`:
```
IF [trip_durationMinute] > 180
THEN 'Invalid Trip'
ELSEIF [trip_durationMinute] < 1
THEN "Invalid Trip"
ELSE "Valid Trip"
END
```
*Obs: `180 minutes` in a taxi trip sounds like a lot, but we need to find a value to limit superiorly*
And from this new category, a new filter was created.
##### Passenger
When we visualize the distribution of passenger numbers, we can observe trips with no passengers until traveling with 8 passengers (possibly an error).
In [New York City Taxi & Limousine Commission](http://www.nyc.gov/html/tlc/html/faq/faq_pass.shtml) I could find the rules that define the maximum amount of passengers in a taxi in New York:
> The maximum amount of passengers allowed in a yellow taxicab by law is four (4) in a four (4) passenger taxicab or five (5) passengers in a five (5) passenger taxicab, except that an additional passenger must be accepted if such passenger is under the age of seven (7) and is held on the lap of an adult passenger seated in the rear.

So the maximum of passengers on a taxi ride is 6 passengers. Obviously, the minimum is 1 passenger. A filter was created with these values.

##### Distance
To check if the calculated distance is correct, the best way to analyze was to visualize the Trip Duration by Distance graph. As expected, we can see a linear proportion between the two variables (the greater the distance covered, the longer the time spent). A certain noise is also observed, as well as unexpected values, but I believe it is due to the approximation of the calculation of the distance and the traffic in more agitated moments.

We can also see trips with `0km` and more than `300km`. A filter was created to only take trips with more than `1km` and less than `60km`.

##### Average Speed
Here we can observe the distribution of average speeds (most less or equal to `20km/h`). Here we can also observe, trips with average speed over `200km/h` so it is clear that we need to filter trips with values so unexpected.
By visualizing the distribution it is possible to conclude that journeys with an average speed of up to `75km/h` are acceptable.

##### Latitude and Longitude
Based on the latitude and longitude distribution (for pickup and dropoff), a filter was created.
First, new Categories like `PickupLatCategory`, `PickupLongCategory`, `DropoffLatCategory` and `DropoffLongCategory`.
Without this filter, we can see points outside of New York (even in the ocean).

![MapFilterViz](/imgs/MapFilterViz.png)

#### Pickup points VS Dropoff points
![PickupDropoff](/imgs/PickupDropoff.png)

Here we can see pickup points (top map) and dropoff points (bottom map).
In both maps, Manhattan seems to have the same density of points (by the way, a high density). There are two other dots with high densities. When investigating important locations near this large cluster of points, we find *John F. Kennedy International Airport* and *LaGuardia Airport*.

Another issue that we can observe is that the dropoff points are more distributed throughout the city than the points of the pickup points. This may be because people are looking for easier places to get a taxi.

#### Dynamics of the City
In this section we can infer how New Yorkers behave during the days of the week and at different hours, based on the average speed and the amount of taxi trips per day of the week.

![AverageSpeed](/imgs/AverageSpeed.png)
##### Average Speed per Weekday and Hour
Here we can visualize traffic behavior on several days of the week and at different times. We can see that on weekdays, during business hours the average speed is very low. But before starting and at the end of business hours, we can observe higher average speeds (at these times, most people are at home).
On weekends, low average speed times occur later, as people wake up later on these days. And even at times with lower speeds, they are still higher than on weekdays, because on those days the traffic is less congested due to the fact that most people prefer to rest at home.
weekday and weekend.
##### Frequency of Trips per Weekday and Hour
Here, for each day of the week we can see the amount of taxi trips made for each time of day. **Weekdays** behave very similarly: they start the day by decreasing the amount of travel, it grows with the beginning of business hours, it keeps up during the day, it increases a little with the end of business hours and it falls at the end of the night. One notable exception is the friday, which at the end of the day behaves like saturday, since for most people the next day is not working day.
**Weekends** behave as described in the previous subsection: They start the day by decreasing the amount of travel (but they start with values ​​much larger than the weekdays and take longer descending), the time that they begin to grow is later (the people sleep a little more on those days), during the rest of the day the saturday continues to grow and sunday has a drop at the end of the day (the next day is a working day).

#### Increasing Vendor Trips
From `vendor_id` we will study the distribution of travel by company.

![dataClean](/imgs/Increase.png)
##### Number of Vendor Trip per Month and Hour of Day
Here, we have two graphs.

In the first graph (left graphic) we can see that the vendor of `id=2` has more trips in every month than the vendor of `id=1`. Does this imply that one supplier has more cars than the other?

In the second graph (right graph) we can see that the vendor of `id=2` also has more trips or is the same as the provider of `id=1` at almost all times of the day.
Here I begin to believe that the `id=2` vendor has more cars than the second vendor.

##### Best Trips Map
So far we do not know for sure why one supplier always has more trips than another. But now we will show an iterative map that helps the supplier who always makes fewer trips to find the best trips.

Here, according to the day and time, it is possible to choose the locations most likely for each setting. For example, if the vendor wants to enjoy trips with intermediate distances and that it spends little time, just mark the desired options.

In addition to time and day, the following options are available:

Distance:
* Intermediate Distance (`>20km`)
* Long Distance (`>10km` and `<=20km`)
* Short Distance (`<=10km`)

Time:
* Long Trip (`>15 min`)
* Short Trip (`<=15min`)
