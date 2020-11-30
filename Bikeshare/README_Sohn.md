Adam Sohn submission

# Project 1: Query Project

- In the Query Project, you will get practice with SQL while learning about
  Google Cloud Platform (GCP) and BiqQuery. You'll answer business-driven
  questions using public datasets housed in GCP. To give you experience with
  different ways to use those datasets, you will use the web UI (BiqQuery) and
  the command-line tools, and work with them in jupyter notebooks.

- We will be using the Bay Area Bike Share Trips Data
  (https://cloud.google.com/bigquery/public-data/bay-bike-share). 

#### Problem Statement

- You're a data scientist at Ford GoBike (https://www.fordgobike.com/), the
  company running Bay Area Bikeshare. You are trying to increase ridership, and
  you want to offer deals through the mobile app to do so. What deals do you
  offer though? Currently, your company has three options: a flat price for a
  single one-way trip, a day pass that allows unlimited 30-minute rides for 24
  hours and an annual membership. 

- Through this project, you will answer these questions: 
  * What are the 5 most popular trips that you would call "commuter trips"?
  * What are your recommendations for offers (justify based on your findings)?


---

## Part 1 - Querying Data with BigQuery

### What is Google Cloud?
- Read: https://cloud.google.com/docs/overview/

### Get Going

- Go to https://cloud.google.com/bigquery/
- Click on "Try it Free"
- It asks for credit card, but you get $300 free and it does not autorenew after the $300 credit is used, so go ahead (OR CHANGE THIS IF SOME SORT OF OTHER ACCESS INFO)
- Now you will see the console screen. This is where you can manage everything for GCP
- Go to the menus on the left and scroll down to BigQuery
- Now go to https://cloud.google.com/bigquery/public-data/bay-bike-share 
- Scroll down to "Go to Bay Area Bike Share Trips Dataset" (This will open a BQ working page.)


### Some initial queries
Paste your SQL query and answer the question in a sentence.

- What's the size of this dataset? (i.e., how many trips)
SELECT count(*) as Num_of_Trips FROM `bigquery-public-data.san_francisco.bikeshare_trips`
The size of the dataset is 983648 rows, with each row representing a trip.

- What is the earliest start time and latest end time for a trip?
SELECT MIN(start_date) as Earliest_Trip_Start, MAX(end_date) as Latest_Trip_End FROM `bigquery-public-data.san_francisco.bikeshare_trips`
The earliest start time for a trip is '2013-08-29 09:08:00 UTC' and the latest end time for a trip is '2016-08-31 23:48:00 UTC'.

- How many bikes are there?
SELECT count(distinct bike_number) as Count_of_Distinct_Bikes from `bigquery-public-data.san_francisco.bikeshare_trips`
There are 700 distinct bikes in the dataset.

### Questions of your own
- Make up 3 questions and answer them using the Bay Area Bike Share Trips Data.
- Use the SQL tutorial (https://www.w3schools.com/sql/default.asp) to help you with mechanics.

--------- commuter uses bike to get to work. different start/end trip except golden gate trip


--What is the mean trip count per day per bike for 2016?

- Question 1: What is the mean trip count per day per bike for 2016?
  * Answer: 1.42 trips per day per bike
  * SQL query:
SELECT COUNT(*) / (COUNT(DISTINCT EXTRACT(DAYOFYEAR from start_date)) * COUNT(DISTINCT bike_number)) as ride_per_bike_per_day_2016
FROM `bigquery-public-data.san_francisco.bikeshare_trips`
WHERE EXTRACT(year FROM start_date) = 2016


- Question 2: What is the percentage of trips in each of following duration buckets (minutes) over the entire time horizon: [0-30,31-45,46-60,61-120,121-1440,1441+]  
  * Answer: The percentage of trips in duration buckets [0-30,31-45,46-60,61-120,121-1440,1441+] is as shown in table below: 
0-30_min_trip 		99.9796%
121-1140_min_trip	0.0025%
61-120_min_trip		0.0068%
31-45_min_trip		0.0056%
46-60_min_trip		0.0054%
1441+				0.0001%

  * SQL query:
SELECT sub.duration_bucket, FORMAT("%.*f",4,CAST(100*COUNT(*) / (SELECT COUNT(*) FROM `bigquery-public-data.san_francisco.bikeshare_trips`) AS FLOAT64)) AS percentage_of_trips
FROM (
  SELECT CASE 
    WHEN duration_sec >= 1441*60*60 THEN '1441+'
    WHEN duration_sec >= 121*60*60 THEN '121-1140_min_trip'
    WHEN duration_sec >= 61*60*60 THEN '61-120_min_trip'
    WHEN duration_sec >= 46*60*60 THEN '46-60_min_trip'
    WHEN duration_sec >= 31*60*60 THEN '31-45_min_trip'
    WHEN duration_sec >= 0 THEN '0-30_min_trip'
    ELSE 'error' END AS duration_bucket, start_date
  FROM `bigquery-public-data.san_francisco.bikeshare_trips`
  ) as sub
GROUP BY sub.duration_bucket

- Question 3: What percentage of trips take place in each (Northern Meteorological) Season?
  * Answer: (Northern Meteorological) seasonal percentages for trips are shown below:
Summer 28.1%
Autumn 25.9%
Spring 25.7%
Winter 20.3%

  * SQL query:
SELECT CASE 
  WHEN EXTRACT(month FROM start_date) BETWEEN 3 AND 5 THEN 'Spring'
  WHEN EXTRACT(month FROM start_date) BETWEEN 6 AND 8 THEN 'Summer'
  WHEN EXTRACT(month FROM start_date) BETWEEN 9 AND 11 THEN 'Autumn'
  WHEN EXTRACT(month FROM start_date) = 12 THEN 'Winter'
  WHEN EXTRACT(month FROM start_date) BETWEEN 1 AND 2 THEN 'Winter'
  ELSE 'error' END AS season, FORMAT("%.*f",1,CAST(100 * count(*)/(SELECT COUNT(*) FROM `bigquery-public-data.san_francisco.bikeshare_trips`) AS FLOAT64)) AS percentage_of_trips
FROM `bigquery-public-data.san_francisco.bikeshare_trips`
GROUP BY season
ORDER BY percentage_of_trips DESC

---

## Part 2 - Querying data from the BigQuery CLI - set up 

### What is Google Cloud SDK?
- Read: https://cloud.google.com/sdk/docs/overview

- If you want to go further, https://cloud.google.com/sdk/docs/concepts has
  lots of good stuff.

### Get Going

- Install Google Cloud SDK: https://cloud.google.com/sdk/docs/

- Try BQ from the command line:

  * General query structure

    ```
    bq query --use_legacy_sql=false 
        'SELECT count(*)
        FROM
           `bigquery-public-data.san_francisco.bikeshare_trips`'
    ```

### Queries

1. Rerun last week's queries using bq command line tool (Paste your bq
   queries):

- What's the size of this dataset? (i.e., how many trips)
    bq query --use_legacy_sql=false 'SELECT count(*) as Num_of_Trips FROM `bigquery-public-data.san_francisco.bikeshare_trips`'
+--------------+
| Num_of_Trips |
+--------------+
|       983648 |
+--------------+
	The size of the dataset is 983648 rows, with each row representing a trip.

- What is the earliest start time and latest end time for a trip?
	bq query --use_legacy_sql=false 'SELECT MIN(start_date) as Earliest_Trip_Start, MAX(end_date) as Latest_Trip_End FROM `bigquery-public-data.san_francisco.bikeshare_trips`'
+---------------------+---------------------+
| Earliest_Trip_Start |   Latest_Trip_End   |
+---------------------+---------------------+
| 2013-08-29 09:08:00 | 2016-08-31 23:48:00 |
+---------------------+---------------------+
	The earliest start time for a trip is '2013-08-29 09:08:00 UTC' and the latest end time for a trip is '2016-08-31 23:48:00 UTC'.


- How many bikes are there?
	bq query --use_legacy_sql=false 'SELECT count(distinct bike_number) as Count_of_Distinct_Bikes from `bigquery-public-data.san_francisco.bikeshare_trips`'
+-------------------------+
| Count_of_Distinct_Bikes |
+-------------------------+
|                     700 |
+-------------------------+
	There are 700 distinct bikes in the dataset.


2. New Query (Paste your SQL query and answer the question in a sentence):

- How many trips are in the morning vs in the afternoon?
	bq query --use_legacy_sql=false 'SELECT CASE 
	WHEN EXTRACT(hour FROM start_date) BETWEEN 0 and 11 then "morning" 
	WHEN EXTRACT(hour FROM start_date) BETWEEN 12 and 23 then "afternoon" 
	ELSE "error" END AS time_of_day, count(*) as trip_count 
	FROM `bigquery-public-data.san_francisco.bikeshare_trips`
	group by time_of_day'

+-------------+------------+
| time_of_day | trip_count |
+-------------+------------+
| afternoon   |     571309 |
| morning     |     412339 |
+-------------+------------+
	412339 trips are in the morning (1200 - 2359) while 571309 trips are in the afternoon (0000-1159).


### Project Questions
Identify the main questions you'll need to answer to make recommendations (list
below, add as many questions as you need).

-----What are the 5 most popular trips (by count) that are during commuter times?
-----What are your recommendations for offers (justify based on your findings)?
 
- Question 1: Is there a morning/afternoon 'rush' time range suggested by ridership data?
- Motivation for Question 1: Assuming participation in 'rush' times is a defining factor of commuters, this query will help the researcher define 'rush' times for Ford GoBike customers. 

- Question 2: Does weekday (M-F) vs. weekend (Sa-Su) ridership help identify the commuting population?
- Motivation for Question 2: Validate assumption that 'rush' times is a weekday only phenomena.

- Question 3:  Does customer type of 'Subscriber' or 'Customer' (ie. not a 'Subscriber') help identify the commuting population?
- Motivation for Question 3: Assuming commuters would likely be subscribers and other rider types would be less likely to be subscribers (than commuters), true 'rush' should exhibit a higher percentage of subscribers than other times. 

- Question 4: Leveraging all learning from Research Question A, establish 5 most popular trips that could be called commuter trips.
- Motivation for Question 4: Culmination of examination of commuter habits

- Question 5: Characterize what days would be the bikes would have lowest utilization by Subscribers.
- Motivation for Question 5: These days are the best options for fare sale days, as subscribers are least likely to be disenfranchised by lack of bike availability.

- Question 6: Characterize seasonality of trip count (with trip count as a proxy for bike utilization).
- Motivation to Question 6: Running subscription promotions after the peak of ridership has subsided will help keep bike utilization high during the 'off season'.

- Question 7: Which are the high-volume (>10k trips) stations with the lowest percentages of their outgoing weekday trips coinciding with rush times?
- Motivation for Question 7: These stations are underperforming from a subscriber perspective and could benefit from a station-specific promotion.


### Answers

Answer at least 4 of the questions you identified above You can use either
BigQuery or the bq command line tool.  Paste your questions, queries and
answers below.

- Question 1: Is there a morning/afternoon 'rush' time range suggested by ridership data?
  * Answer: The most popular trip start times are in the 7-9 hrs & 16-18 hrs. This coincides with common understanding of 'rush' times.
  
+-------------+---------------------+
| hour_of_day | percentage_of_trips |
+-------------+---------------------+
|           8 |                13.5 |
|          17 |                12.8 |
|           9 |                 9.8 |
|          16 |                 9.0 |
|          18 |                 8.6 |
|           7 |                 6.9 |
|          12 |                 4.8 |
|          15 |                 4.8 |
|          13 |                 4.4 |
|          10 |                 4.3 |
|          19 |                 4.2 |
|          11 |                 4.1 |
|          14 |                 3.8 |
|          20 |                 2.3 |
|           6 |                 2.1 |
|          21 |                 1.6 |
|          22 |                 1.0 |
|          23 |                 0.6 |
|           5 |                 0.5 |
|           0 |                 0.3 |
|           1 |                 0.2 |
|           2 |                 0.1 |
|           4 |                 0.1 |
|           3 |                 0.1 |
+-------------+---------------------+
  * SQL query:

bq query --use_legacy_sql=false 'SELECT EXTRACT(hour FROM start_date) AS hour_of_day, ROUND(100 * count(*)/(SELECT COUNT(*) FROM `bigquery-public-data.san_francisco.bikeshare_trips`),1) AS percentage_of_trips
FROM `bigquery-public-data.san_francisco.bikeshare_trips`
GROUP BY hour_of_day
ORDER BY percentage_of_trips DESC'

- Question 2: Does weekday (M-F) vs. weekend (Sa-Su) ridership help identify the commuting population?
  * Answer:
  
For weekends, the most popular trip start times move from traditional 'rush' start times in the 7-9 hrs & 16-18 hrs to mid-day 11-16 hrs. Additionaly, the trips are less concentrated in any given hr. This reflects a high-level change in usage pattern between week and weekend which will be interpretted as weekend trips being primarily recreational, not commuting. 
  
+---------------------+---------------------+
| hour_of_weekend_day | percentage_of_trips |
+---------------------+---------------------+
|                  13 |                 9.6 |
|                  12 |                 9.5 |
|                  14 |                 9.2 |
|                  15 |                 9.1 |
|                  11 |                 8.7 |
|                  16 |                 8.7 |
|                  10 |                 7.1 |
|                  17 |                 7.1 |
|                  18 |                 5.7 |
|                   9 |                 5.2 |
|                  19 |                 4.0 |
|                   8 |                 3.1 |
|                  20 |                 2.9 |
|                  21 |                 2.2 |
|                  22 |                 1.7 |
|                   7 |                 1.5 |
|                  23 |                 1.3 |
|                   0 |                 1.1 |
|                   1 |                 0.7 |
|                   6 |                 0.6 |
|                   2 |                 0.4 |
|                   5 |                 0.3 |
|                   3 |                 0.2 |
|                   4 |                 0.1 |
+---------------------+---------------------+
  
+---------------------+---------------------+
| hour_of_weekday_day | percentage_of_trips |
+---------------------+---------------------+
|                   8 |                14.8 |
|                  17 |                13.6 |
|                   9 |                10.4 |
|                  16 |                 9.1 |
|                  18 |                 9.0 |
|                   7 |                 7.6 |
|                  15 |                 4.3 |
|                  12 |                 4.2 |
|                  19 |                 4.2 |
|                  10 |                 4.0 |
|                  13 |                 3.8 |
|                  11 |                 3.5 |
|                  14 |                 3.2 |
|                   6 |                 2.3 |
|                  20 |                 2.2 |
|                  21 |                 1.5 |
|                  22 |                 1.0 |
|                  23 |                 0.6 |
|                   5 |                 0.6 |
|                   0 |                 0.2 |
|                   4 |                 0.1 |
|                   1 |                 0.1 |
|                   2 |                 0.0 |
|                   3 |                 0.0 |
+---------------------+---------------------+  
    
  * SQL query:

-- FOR WEEKEND
bq query --use_legacy_sql=false 'SELECT EXTRACT(hour FROM start_date) AS hour_of_weekend_day, ROUND(100 * count(*)/(SELECT COUNT(*) FROM `bigquery-public-data.san_francisco.bikeshare_trips` WHERE EXTRACT(DAYOFWEEK FROM start_date) in (1,7)),1) AS percentage_of_trips
FROM `bigquery-public-data.san_francisco.bikeshare_trips`
WHERE EXTRACT(DAYOFWEEK FROM start_date) in (1,7)
GROUP BY hour_of_weekend_day
ORDER BY percentage_of_trips DESC'

-- FOR WEEKDAY
bq query --use_legacy_sql=false 'SELECT EXTRACT(hour FROM start_date) AS hour_of_weekday_day, ROUND(100 * count(*)/(SELECT COUNT(*) FROM `bigquery-public-data.san_francisco.bikeshare_trips` WHERE EXTRACT(DAYOFWEEK FROM start_date) in (2,3,4,5,6)),1) AS percentage_of_trips
FROM `bigquery-public-data.san_francisco.bikeshare_trips`
WHERE EXTRACT(DAYOFWEEK FROM start_date) in (2,3,4,5,6)
GROUP BY hour_of_weekday_day
ORDER BY percentage_of_trips DESC'

- Question 3:  Does customer type of 'Subscriber' or 'Customer' (ie. not a 'Subscriber') help identify the commuting population?

  * Answer: Yes! When viewing weekdays by hourly buckets of start_date, Customer (not Subscriber) trips only show 1 hour coincident (17) with the Subscriber trips. The subscriber trips more closely coincide with expectation. This finding was expected based on the expectation that habitual customers (ie. commuters) would require the convenience of a subscription.
  
+---------------------+------------------------------+
| hour_of_weekday_day | percentage_of_trips_customer |
+---------------------+------------------------------+
|                  17 |                          9.0 |
|                  16 |                          9.0 |
|                  15 |                          8.6 |
|                  12 |                          8.3 |
|                  14 |                          8.3 |
|                  13 |                          8.2 |
|                  11 |                          7.6 |
|                  18 |                          7.1 |
|                  10 |                          5.7 |
|                   9 |                          5.1 |
|                   8 |                          5.0 |
|                  19 |                          4.4 |
|                  20 |                          3.0 |
|                  21 |                          2.4 |
|                   7 |                          2.4 |
|                  22 |                          2.0 |
|                  23 |                          1.3 |
|                   6 |                          0.9 |
|                   0 |                          0.5 |
|                   1 |                          0.4 |
|                   2 |                          0.3 |
|                   5 |                          0.3 |
|                   3 |                          0.1 |
|                   4 |                          0.1 |
+---------------------+------------------------------+

+---------------------+--------------------------------+
| hour_of_weekday_day | percentage_of_trips_subscriber |
+---------------------+--------------------------------+
|                   8 |                           15.8 |
|                  17 |                           14.0 |
|                   9 |                           10.9 |
|                  18 |                            9.2 |
|                  16 |                            9.1 |
|                   7 |                            8.1 |
|                  19 |                            4.2 |
|                  15 |                            3.8 |
|                  10 |                            3.8 |
|                  12 |                            3.7 |
|                  13 |                            3.3 |
|                  11 |                            3.1 |
|                  14 |                            2.6 |
|                   6 |                            2.4 |
|                  20 |                            2.2 |
|                  21 |                            1.4 |
|                  22 |                            0.9 |
|                   5 |                            0.6 |
|                  23 |                            0.5 |
|                   0 |                            0.2 |
|                   4 |                            0.1 |
|                   1 |                            0.1 |
|                   3 |                            0.0 |
|                   2 |                            0.0 |
+---------------------+--------------------------------+
  
  * SQL query:
  
-- FOR CUSTOMER (non-subscriber)
bq query --use_legacy_sql=false 'SELECT EXTRACT(hour FROM start_date) AS hour_of_weekday_day, ROUND(100 * count(*)/(SELECT COUNT(*) FROM `bigquery-public-data.san_francisco.bikeshare_trips` WHERE subscriber_type != "Subscriber"
AND EXTRACT(DAYOFWEEK FROM start_date) in (2,3,4,5,6)),1) AS percentage_of_trips_customer
FROM `bigquery-public-data.san_francisco.bikeshare_trips`
WHERE subscriber_type != "Subscriber"
AND EXTRACT(DAYOFWEEK FROM start_date) in (2,3,4,5,6)
GROUP BY hour_of_weekday_day
ORDER BY percentage_of_trips_customer DESC'

-- FOR SUBSCRIBER
bq query --use_legacy_sql=false 'SELECT EXTRACT(hour FROM start_date) AS hour_of_weekday_day, ROUND(100 * count(*)/(SELECT COUNT(*) FROM `bigquery-public-data.san_francisco.bikeshare_trips` WHERE subscriber_type = "Subscriber"
AND EXTRACT(DAYOFWEEK FROM start_date) in (2,3,4,5,6)),1) AS percentage_of_trips_subscriber
FROM `bigquery-public-data.san_francisco.bikeshare_trips`
WHERE subscriber_type = "Subscriber"
AND EXTRACT(DAYOFWEEK FROM start_date) in (2,3,4,5,6)
GROUP BY hour_of_weekday_day
ORDER BY percentage_of_trips_subscriber DESC'
  
- Question 4: Leveraging all learning from Research Question A, establish 5 most popular trips that could be called commuter trips.
  * Answer: Using all learnings on isolating commuter trips (Subscibers only, start_date in one of the following hours: 7,8,9,16,17,18, weekdays only), the above combinations comprise the top 5 popular trips that could be called commuter trips.

+-----------------------------------------+------------------------------------------+-------------------+
|           start_station_name            |             end_station_name             | pct_of_rush_trips |
+-----------------------------------------+------------------------------------------+-------------------+
| 2nd at Townsend                         | Harry Bridges Plaza (Ferry Building)     |              0.95 |
| Harry Bridges Plaza (Ferry Building)    | 2nd at Townsend                          |              0.94 |
| San Francisco Caltrain 2 (330 Townsend) | Townsend at 7th                          |              0.94 |
| Embarcadero at Sansome                  | Steuart at Market                        |              0.88 |
| Embarcadero at Folsom                   | San Francisco Caltrain (Townsend at 4th) |              0.88 |
+-----------------------------------------+------------------------------------------+-------------------+ 
  
  * SQL Query: 
bq query --use_legacy_sql=false 'SELECT start_station_name, end_station_name, ROUND(100 * count(*)/(SELECT COUNT(*) FROM `bigquery-public-data.san_francisco.bikeshare_trips` WHERE subscriber_type = "Subscriber"
AND EXTRACT(DAYOFWEEK FROM start_date) in (2,3,4,5,6) AND EXTRACT(HOUR FROM start_date) in (7,8,9,16,17,18)),2) AS pct_of_rush_trips
FROM `bigquery-public-data.san_francisco.bikeshare_trips`
WHERE subscriber_type = "Subscriber"
AND EXTRACT(DAYOFWEEK FROM start_date) in (2,3,4,5,6)
AND EXTRACT(HOUR FROM start_date) in (7,8,9,16,17,18)
GROUP BY start_station_name, end_station_name
ORDER BY pct_of_rush_trips DESC
LIMIT 5'

- Question 5:  Characterize what days would be the bikes would have lowest utilization by Subscribers.

 * Answer
 The low ridership trend demonstrates the following attributes of a day to be detrimental to ridership: weekend, winter season, and being within 1 day (inclusive) of federal holidays.
+------------+-------+-------------+--------+----------------------------------+
|    date    | trips | day_of_week | season | federal_holiday_plus_minus_1_day |
+------------+-------+-------------+--------+----------------------------------+
| 2015-12-20 |    37 | Sunday      | Winter | No                               |
| 2016-01-01 |    44 | Friday      | Winter | Yes                              |
| 2015-12-25 |    45 | Friday      | Winter | Yes                              |
| 2014-12-25 |    45 | Thursday    | Winter | Yes                              |
| 2016-03-13 |    46 | Sunday      | Spring | No                               |
| 2016-03-05 |    54 | Saturday    | Spring | No                               |
| 2015-12-13 |    57 | Sunday      | Winter | No                               |
| 2015-12-27 |    58 | Sunday      | Winter | No                               |
| 2015-11-26 |    61 | Thursday    | Fall   | Yes                              |
| 2014-11-27 |    64 | Thursday    | Fall   | Yes                              |
| 2015-12-26 |    66 | Saturday    | Winter | Yes                              |
| 2014-02-02 |    67 | Sunday      | Winter | No                               |
| 2014-02-09 |    68 | Sunday      | Winter | No                               |
| 2016-01-17 |    70 | Sunday      | Winter | Yes                              |
| 2015-01-01 |    70 | Thursday    | Winter | Yes                              |
| 2016-01-03 |    71 | Sunday      | Winter | No                               |
| 2014-02-08 |    72 | Saturday    | Winter | No                               |
| 2016-01-10 |    78 | Sunday      | Winter | No                               |
| 2013-12-25 |    84 | Wednesday   | Winter | Yes                              |
| 2016-04-09 |    88 | Saturday    | Spring | No                               |
| 2015-12-06 |    90 | Sunday      | Winter | No                               |
| 2014-11-30 |    91 | Sunday      | Fall   | No                               |
| 2014-03-29 |    91 | Saturday    | Spring | No                               |
| 2015-02-08 |    92 | Sunday      | Winter | No                               |
| 2015-07-04 |    95 | Saturday    | Summer | Yes                              |
| 2016-03-20 |    95 | Sunday      | Spring | No                               |
| 2016-07-17 |    96 | Sunday      | Summer | No                               |
| 2016-03-06 |    97 | Sunday      | Spring | No                               |
| 2016-01-02 |   101 | Saturday    | Winter | Yes                              |
| 2014-12-11 |   102 | Thursday    | Winter | No                               |
| 2016-03-27 |   102 | Sunday      | Spring | No                               |
| 2016-01-16 |   104 | Saturday    | Winter | No                               |
| 2014-12-28 |   104 | Sunday      | Winter | No                               |
| 2016-01-09 |   105 | Saturday    | Winter | No                               |
| 2015-07-05 |   106 | Sunday      | Summer | No                               |
| 2015-12-24 |   107 | Thursday    | Winter | Yes                              |
| 2013-11-28 |   108 | Thursday    | Fall   | Yes                              |
| 2016-03-12 |   110 | Saturday    | Spring | No                               |
| 2016-07-03 |   110 | Sunday      | Summer | Yes                              |
| 2016-05-29 |   111 | Sunday      | Spring | Yes                              |
| 2014-12-27 |   113 | Saturday    | Winter | No                               |
| 2015-05-24 |   115 | Sunday      | Spring | Yes                              |
| 2015-11-27 |   115 | Friday      | Fall   | Yes                              |
| 2016-05-22 |   119 | Sunday      | Spring | No                               |
| 2016-04-10 |   119 | Sunday      | Spring | No                               |
| 2015-05-31 |   121 | Sunday      | Spring | No                               |
| 2013-09-01 |   122 | Sunday      | Fall   | Yes                              |
| 2015-11-29 |   123 | Sunday      | Fall   | No                               |
| 2014-01-01 |   124 | Wednesday   | Winter | Yes                              |
| 2016-02-14 |   125 | Sunday      | Winter | Yes                              |
| 2016-06-05 |   125 | Sunday      | Summer | No                               |
| 2015-01-04 |   125 | Sunday      | Winter | No                               |
| 2016-05-07 |   125 | Saturday    | Spring | No                               |
| 2015-09-06 |   125 | Sunday      | Fall   | Yes                              |
| 2015-11-28 |   128 | Saturday    | Fall   | No                               |
| 2014-07-04 |   131 | Friday      | Summer | Yes                              |
| 2016-04-30 |   131 | Saturday    | Spring | No                               |
| 2015-04-05 |   131 | Sunday      | Spring | No                               |
| 2016-04-03 |   132 | Sunday      | Spring | No                               |
| 2014-12-21 |   133 | Sunday      | Winter | No                               |
| 2016-07-23 |   133 | Saturday    | Summer | No                               |
| 2014-08-31 |   133 | Sunday      | Summer | Yes                              |
| 2015-11-08 |   134 | Sunday      | Fall   | No                               |
| 2015-05-10 |   134 | Sunday      | Spring | No                               |
| 2016-07-04 |   137 | Monday      | Summer | Yes                              |
| 2015-11-15 |   138 | Sunday      | Fall   | No                               |
| 2016-07-24 |   138 | Sunday      | Summer | No                               |
| 2016-01-31 |   138 | Sunday      | Winter | No                               |
| 2016-05-08 |   138 | Sunday      | Spring | No                               |
| 2016-08-07 |   138 | Sunday      | Summer | No                               |
| 2015-12-19 |   138 | Saturday    | Winter | No                               |
| 2016-07-02 |   139 | Saturday    | Summer | No                               |
| 2016-04-17 |   140 | Sunday      | Spring | No                               |
| 2014-03-02 |   141 | Sunday      | Spring | No                               |
| 2016-06-26 |   143 | Sunday      | Summer | No                               |
| 2015-06-07 |   143 | Sunday      | Summer | No                               |
| 2013-12-29 |   144 | Sunday      | Winter | No                               |
| 2016-07-31 |   144 | Sunday      | Summer | No                               |
| 2015-06-14 |   144 | Sunday      | Summer | No                               |
| 2015-10-18 |   144 | Sunday      | Fall   | No                               |
| 2015-01-25 |   146 | Sunday      | Winter | No                               |
| 2016-06-19 |   147 | Sunday      | Summer | No                               |
| 2015-11-22 |   147 | Sunday      | Fall   | No                               |
| 2015-02-22 |   147 | Sunday      | Winter | No                               |
| 2015-02-15 |   147 | Sunday      | Winter | Yes                              |
| 2016-01-24 |   148 | Sunday      | Winter | No                               |
| 2016-02-07 |   148 | Sunday      | Winter | No                               |
| 2016-08-06 |   149 | Saturday    | Summer | No                               |
| 2016-05-28 |   150 | Saturday    | Spring | No                               |
| 2015-01-18 |   150 | Sunday      | Winter | Yes                              |
| 2016-05-30 |   150 | Monday      | Spring | Yes                              |
| 2015-04-26 |   151 | Sunday      | Spring | No                               |
| 2016-02-28 |   151 | Sunday      | Winter | No                               |
| 2014-10-05 |   151 | Sunday      | Fall   | No                               |
| 2014-05-11 |   151 | Sunday      | Spring | No                               |
| 2016-08-27 |   151 | Saturday    | Summer | No                               |
| 2015-08-16 |   152 | Sunday      | Summer | No                               |
| 2016-08-21 |   152 | Sunday      | Summer | No                               |
| 2016-05-01 |   153 | Sunday      | Spring | No                               |
| 2015-12-05 |   153 | Saturday    | Winter | No                               |
+------------+-------+-------------+--------+----------------------------------+
 * SQL Query
 
bq query --use_legacy_sql=false '
SELECT DATE_TRUNC(DATE(start_date), DAY) as date, COUNT(DATE_TRUNC(DATE(start_date), DAY)) as trips,
CASE
  WHEN EXTRACT(DAYOFWEEK FROM start_date) = 1 THEN "Sunday"
  WHEN EXTRACT(DAYOFWEEK FROM start_date) = 2 THEN "Monday"
  WHEN EXTRACT(DAYOFWEEK FROM start_date) = 3 THEN "Tuesday"
  WHEN EXTRACT(DAYOFWEEK FROM start_date) = 4 THEN "Wednesday"
  WHEN EXTRACT(DAYOFWEEK FROM start_date) = 5 THEN "Thursday"
  WHEN EXTRACT(DAYOFWEEK FROM start_date) = 6 THEN "Friday"
  WHEN EXTRACT(DAYOFWEEK FROM start_date) = 7 THEN "Saturday"
  ELSE "error" END AS day_of_week,
CASE 
  WHEN EXTRACT(MONTH FROM start_date) BETWEEN 1 and 2 then "Winter"
  WHEN EXTRACT(MONTH FROM start_date) BETWEEN 3 and 5 then "Spring"
  WHEN EXTRACT(MONTH FROM start_date) BETWEEN 6 and 8 then "Summer"
  WHEN EXTRACT(MONTH FROM start_date) BETWEEN 9 and 11 then "Fall"
  WHEN EXTRACT(MONTH FROM start_date) = 12 then "Winter"
  ELSE "error" END AS season, 
CASE
  WHEN DATE_TRUNC(DATE(start_date), DAY) in ("2013-01-01","2013-01-21","2013-02-18","2013-05-27","2013-07-04","2013-09-02","2013-10-14","2013-11-11","2013-11-28","2013-12-25","2014-01-01","2014-01-20","2014-02-17","2014-05-26","2014-07-04","2014-09-01","2014-10-13","2014-11-11","2014-11-27","2014-12-25","2015-01-01","2015-01-19","2015-02-16","2015-05-25","2015-07-03","2015-09-07","2015-10-12","2015-11-11","2015-11-26","2015-12-25","2016-01-01","2016-01-18","2016-02-15","2016-05-30","2016-07-04","2016-09-05","2016-10-10","2016-11-11","2016-11-24","2016-12-26","2013-01-02","2013-01-22","2013-02-19","2013-05-28","2013-07-05","2013-09-03","2013-10-15","2013-11-12","2013-11-29","2013-12-26","2014-01-02","2014-01-21","2014-02-18","2014-05-27","2014-07-05","2014-09-02","2014-10-14","2014-11-12","2014-11-28","2014-12-26","2015-01-02","2015-01-20","2015-02-17","2015-05-26","2015-07-04","2015-09-08","2015-10-13","2015-11-12","2015-11-27","2015-12-26","2016-01-02","2016-01-19","2016-02-16","2016-05-31","2016-07-05","2016-09-06","2016-10-11","2016-11-12","2016-11-25","2016-12-27","2012-12-31","2013-01-20","2013-02-17","2013-05-26","2013-07-03","2013-09-01","2013-10-13","2013-11-10","2013-11-27","2013-12-24","2013-12-31","2014-01-19","2014-02-16","2014-05-25","2014-07-03","2014-08-31","2014-10-12","2014-11-10","2014-11-26","2014-12-24","2014-12-31","2015-01-18","2015-02-15","2015-05-24","2015-07-02","2015-09-06","2015-10-11","2015-11-10","2015-11-25","2015-12-24","2015-12-31","2016-01-17","2016-02-14","2016-05-29","2016-07-03","2016-09-04","2016-10-09","2016-11-10","2016-11-23","2016-12-25"
) then "Yes"
ELSE "No" END AS federal_holiday_plus_minus_1_day
FROM `bigquery-public-data.san_francisco.bikeshare_trips`
WHERE subscriber_type = "Subscriber"
GROUP BY date, day_of_week, season, federal_holiday_plus_minus_1_day
ORDER BY trips ASC
LIMIT 50'

- Question 6: Characterize seasonality of trip count (with trip count as a proxy for bike utilization).
 * Answer - As suspected, there are more trips in summer months than winter months, with fall and spring being transitional times. Winter (and December especially) are consistently low-ridership months. This information can be leveraged for timings of sales, as increased demand (on the aggregate) would not disenfranchise Subscribers from having an available bike.
 
Limiting output to 5 rows only
+------------+-------+--------+
| date_month | trips | season |
+------------+-------+--------+
| 2013-08-01 |  2102 | Summer |
| 2013-09-01 | 25243 | Fall   |
| 2013-10-01 | 29105 | Fall   |
| 2013-11-01 | 24219 | Fall   |
| 2013-12-01 | 19894 | Winter |
+------------+-------+--------+ 
  
 * SQL Query
 bq query --use_legacy_sql=false '
SELECT DATE_TRUNC(DATE(start_date), MONTH) as date_month, COUNT(DATE_TRUNC(DATE(start_date), DAY)) as trips,
CASE 
  WHEN EXTRACT(MONTH FROM start_date) BETWEEN 1 and 2 then "Winter"
  WHEN EXTRACT(MONTH FROM start_date) BETWEEN 3 and 5 then "Spring"
  WHEN EXTRACT(MONTH FROM start_date) BETWEEN 6 and 8 then "Summer"
  WHEN EXTRACT(MONTH FROM start_date) BETWEEN 9 and 11 then "Fall"
  WHEN EXTRACT(MONTH FROM start_date) = 12 then "Winter"
  ELSE "error" END AS season
FROM `bigquery-public-data.san_francisco.bikeshare_trips`
GROUP BY season, date_month
ORDER BY date_month ASC'

- Question 7: Which are the high-volume (>10k trips) stations with the lowest percentages of their outgoing weekday trips coinciding with rush times?
 * Answer

+-----------------------------------------------+---------------------------------+----------+------------+
|              start_station_name               | percentage_of_trips_during_rush | rsh_trip | wkday_trip |
+-----------------------------------------------+---------------------------------+----------+------------+
| Temporary Transbay Terminal (Howard at Beale) |                            76.5 |    28880 |      37764 |
| San Francisco Caltrain (Townsend at 4th)      |                            76.1 |    52441 |      68896 |
| San Francisco Caltrain 2 (330 Townsend)       |                            75.5 |    40264 |      53299 |
| Steuart at Market                             |                            71.5 |    25313 |      35389 |
| 2nd at Townsend                               |                            67.7 |    24103 |      35599 |
| Harry Bridges Plaza (Ferry Building)          |                            67.2 |    27298 |      40610 |
| South Van Ness at Market                      |                            66.6 |    10657 |      15995 |
| Embarcadero at Folsom                         |                            65.9 |    13037 |      19785 |
| Beale at Market                               |                            65.0 |    13841 |      21283 |
| Grant Avenue at Columbus Avenue               |                            64.0 |    12277 |      19186 |
+-----------------------------------------------+---------------------------------+----------+------------+
 
 * SQL Query
 
bq query --use_legacy_sql=false 'SELECT bk.start_station_name, ROUND(100 * count(bk.start_station_name)/(SUM(sub.stn_cnt)/COUNT(sub.stn_cnt)),1) AS percentage_of_trips_during_rush, count(bk.start_station_name) as rsh_trip, CAST(sum(sub.stn_cnt)/COUNT(sub.stn_cnt) as int64) as wkday_trip
FROM `bigquery-public-data.san_francisco.bikeshare_trips`as bk
JOIN 
  (SELECT start_station_name, COUNT(start_station_name) as stn_cnt 
  FROM `bigquery-public-data.san_francisco.bikeshare_trips`
  WHERE EXTRACT(DAYOFWEEK FROM start_date) in (2,3,4,5,6)
  GROUP BY start_station_name
  HAVING COUNT(start_station_name) > 10000) sub
ON bk.start_station_name = sub.start_station_name
WHERE EXTRACT(DAYOFWEEK FROM bk.start_date) in (2,3,4,5,6)
AND EXTRACT(hour FROM bk.start_date) in (7,8,9,16,17,18)
GROUP BY bk.start_station_name
HAVING COUNT(bk.start_station_name) > 10000
ORDER BY percentage_of_trips_during_rush ASC
LIMIT 10'


---

## Part 3 - Employ notebooks to synthesize query project results

### Get Going

Use JupyterHub on your midsw205 cloud instance to create a new python3 notebook. 


#### Run queries in the notebook 

```
! bq query --use_legacy_sql=FALSE '<your-query-here>'
```

- NOTE: 
- Queries that return over 16K rows will not run this way, 
- Run groupbys etc in the bq web interface and save that as a table in BQ. 
- Query those tables the same way as in `example.ipynb`


#### Report
- Short description of findings and recommendations 
- Add data visualizations to support recommendations 

### Resource: see example .ipynb file 

[Example Notebook](example.ipynb)




