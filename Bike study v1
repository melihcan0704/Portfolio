--We have 12 months of bike data as a csv file.
--To prepare the data for analysis we need to combine these files into one. Since total row count of all files are higher than 5 million therefore
--doing this in excel wouldn't be possible.
--I added all 12 csv files as different tables to Postgresql and then did the following UNION to create a one table that holds all values for the entire year.

CREATE TABLE year_2022 (
ride_id VARCHAR(50) PRIMARY KEY,
rideable_type VARCHAR(200),
started_at TIMESTAMP,
ended_at TIMESTAMP,
start_station_name VARCHAR(200),
start_station_id VARCHAR(50),
end_station_name VARCHAR(200),
end_station_id VARCHAR(50),
start_lat FLOAT,
start_lng FLOAT,
end_lat FLOAT,
end_lng FLOAT,
member_casual VARCHAR(200)
);

## Below tables have the same columns as above year_2022 table but contains monthly data only.

INSERT INTO year_2022
select * from january_2022
UNION
select * from february_2022
UNION
select * from march_2022
UNION
select * from april_2022
UNION
select * from may_2022
UNION
select * from june_2022
UNION
select * from july_2022
UNION
select * from august_2022
UNION
select * from september_2022
UNION
select * from october_2022
UNION
select * from november_2022
UNION
select * from december_2022


#At this point we have one table that contains every data in year 2022 which is year_2022 table.


