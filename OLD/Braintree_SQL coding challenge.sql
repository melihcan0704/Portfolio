
--This SQL challenge is from Braintree SQL coding challenge created by Alexander Connelly. 
--(Link: https://github.com/AlexanderConnelly/BrainTree_SQL_Coding_Challenge_Data_Analyst)

--I will only be copying the questions in there which will be followed by my submissions. For details & context you can visit the link provided above.


--Q1. Data Integrity Checking & Cleanup

--Alphabetically list all of the country codes in the continent_map table that appear more than once. 

SELECT DISTINCT 
country_code
,COUNT(continent_code)
FROM braintree.continent_map
GROUP BY 1
HAVING COUNT(continent_code) > 1
ORDER BY 1

Output:

"country_code"	"count"
"ARM"	              3
"AZE"             	2
"CYP"	              2
"GEO"	              2
"KAZ"	              2
"RUS"	              2
"TUR"	              2
"UMI"	              2
[null]              4

--Display any values where country_code is null as country_code = "FOO" and make this row appear first in the list, 
--even though it should alphabetically sort to the middle. Provide the results of this query as your answer.

SELECT DISTINCT 
COALESCE(country_code,'FOO') as country_code
,COUNT(continent_code)
FROM braintree.continent_map
GROUP BY 1
HAVING COUNT(continent_code) > 1
ORDER BY 1


Output:

"country_code"	"count"
"ARM"	             3
"AZE"	             2
"CYP"	             2
"FOO"	             4
"GEO"	             2
"KAZ"	             2
"RUS"	             2
"TUR"	             2
"UMI"	             2

--For all countries that have multiple rows in the continent_map table, delete all multiple records leaving only the 1 record per country. 
--The record that you keep should be the first one when sorted by the continent_code alphabetically ascending. 
--Provide the query/ies and explanation of step(s) that you follow to delete these records.


WITH this AS (
SELECT
country_code
,continent_code
,ROW_NUMBER() OVER(PARTITION BY country_code ORDER BY continent_code) as country_count
FROM braintree.continent_map
ORDER BY 1
)
,
this2 AS (
select 
country_code,
continent_code
FROM this
WHERE country_count > 1
)

DELETE FROM braintree.continent_map 
WHERE EXISTS (SELECT * FROM this2 WHERE this2.country_code=braintree.continent_map.country_code 
			  AND this2.continent_code=braintree.continent_map.continent_code)


--Now there are 254 rows in total after the duplicate removal. (9 duplicate rows removed except for the null values)


--Q2. List the countries ranked 10-12 in each continent by the percent of year-over-year growth descending from 2011 to 2012.
--The percent of growth should be calculated as: ((2012 gdp - 2011 gdp) / 2011 gdp)
--The list should include the columns:
--rank, continent_name, country_code, country_name, growth_percent


--Created a table with 2011 data only.
WITH data2011 AS (select 
country_code,
year,
MAX(gdp_per_capita) AS max_capita
from braintree.per_capita
WHERE year = 2011
GROUP BY 1,2
)

,
--Created a table with 2012 data only.
data2012 AS (select 
country_code,
year,
MAX(gdp_per_capita) AS max_capita
from braintree.per_capita
WHERE year = 2012
GROUP BY 1,2
)
,
--Joined above 2 tables together and added the required formula in line 118. Numerical restrictions set by the challenge will be done in the next queries.
changeover_data AS (select 
d11.country_code
,ROUND(CAST(((d12.max_capita - d11.max_capita) / d11.max_capita * 100.0) AS DECIMAL),2) AS capita_changeover
FROM data2011 d11
JOIN data2012 d12
ON d11.country_code = d12.country_code
WHERE ((d12.max_capita - d11.max_capita) / d11.max_capita * 100.0) IS NOT NULL)
,
--continent_name and country_name doesnt exist in above CTE's so created a placeholder CTE so we can join this to the final query.
remaining_locations AS (
SELECT
ct.continent_name,
cr.country_name,
cr.country_code
FROM braintree.continent_map cm
JOIN braintree.continents ct ON ct.continent_code = cm.continent_code
JOIN braintree.countries cr ON cr.country_code = cm.country_code
)
--Added continent_name and country_name, converted the numerical column (growth_percent) as per the restriction.
--Made the output so that results only display countries ranked 10-12
SELECT 
rl.continent_name,
rl.country_name,
cd.country_code,
CONCAT(cd.capita_changeover,'%') AS growth_percent,
RANK() OVER(ORDER BY capita_changeover DESC)
FROM changeover_data cd
JOIN remaining_locations rl ON rl.country_code = cd.country_code
OFFSET 9
LIMIT 3





--Q3. For the year 2012, create a 3 column, 1 row report showing the percent share of gdp_per_capita for the following regions:
--(i) Asia, (ii) Europe, (iii) the Rest of the World. Your result should look something like
--	Asia	Europe	Rest of World
--	25.0%	25.0%	50.0%


--First calculation to see the total world gdp for future calculations.
SELECT SUM(gdp) AS world_gdp FROM

Output: 2618124.49

--Below query results in gdp_per_capita grouped by continents.
WITH continent_gdp AS (
SELECT 
continent_name,
year,
ROUND(SUM(CAST(gdp_per_capita AS DECIMAL)),2) gdp
FROM braintree.per_capita pc
JOIN braintree.continent_map cm ON cm.country_code = pc.country_code
JOIN braintree.continents ct ON ct.continent_code = cm.continent_code
WHERE year = 2012
GROUP BY 1,2)
,
--Below query results in gdp share of asked continents.
continent_share AS (
SELECT 
continent_name,
ROUND(((gdp/2618124.49)*100),2) AS gdp_share
FROM continent_gdp)
,
final AS (
SELECT 
CASE WHEN continent_name IN ('Oceania','South America','Africa','North America')  THEN 'Rest of the world'
ELSE continent_name END,
CONCAT(SUM(gdp_share),'%') total_gdp_share
FROM continent_share
GROUP BY 1
ORDER BY 1
)	


Final Output:

"continent_name"	"total_gdp_share"
"Asia"			"28.33%"
"Europe"		"42.24%"
"Rest of the world"	"29.42%"


--I understand that the final output needs to be pivoted for the correct answer. But I'am using PostgreSQL and pivoting in PSQL is very difficult
--compared to MS SQL Server or Excel. It requires an additional Module and a very time consuming syntax.(Module:tablefunc Function: CROSSTAB().)
--At this point I would switch the final output to MS SQL Server, Bigquery or excel (Depending on the import size) for pivoting.



--Q4
--4a. What is the count of countries and sum of their related gdp_per_capita values for the year 2007 where the string 'an' 
--(case insensitive) appears anywhere in the country name?

SELECT 
COUNT(c.country_code) AS country,
CONCAT(ROUND(CAST(SUM(pc.gdp_per_capita) AS INT),2),'$') AS total_gdp
FROM braintree.countries c
JOIN braintree.per_capita pc ON pc.country_code = c.country_code
WHERE country_name ILIKE '%an%' AND year = 2007

--4b. Repeat question 4a, but this time make the query case sensitive.

SELECT 
COUNT(c.country_code) AS country,
CONCAT(ROUND(CAST(SUM(pc.gdp_per_capita) AS INT),2),'$') AS total_gdp
FROM braintree.countries c
JOIN braintree.per_capita pc ON pc.country_code = c.country_code
WHERE country_name LIKE '%an%' AND year = 2007;


/* Q5 Find the sum of gdp_per_capita by year and the count of countries for each year that have non-null gdp_per_capita where 
   the year is before 2012 and Your result should have the columns:
year
country_count
total */

SELECT 
pc.year,
COUNT(DISTINCT c.country_name) country_count,
CONCAT(ROUND(CAST(SUM(pc.gdp_per_capita) AS INT),2),'$') total_gdp
FROM braintree.per_capita pc
JOIN braintree.countries c ON c.country_code = pc.country_code 
WHERE year < 2012 AND gdp_per_capita IS NOT NULL 
GROUP BY 1










