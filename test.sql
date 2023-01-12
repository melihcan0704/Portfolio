
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


WITH data2011 AS (select 
country_code,
year,
MAX(gdp_per_capita) AS max_capita
from braintree.per_capita
WHERE year = 2011
GROUP BY 1,2
)
,
data2012 AS (select 
country_code,
year,
MAX(gdp_per_capita) AS max_capita
from braintree.per_capita
WHERE year = 2012
GROUP BY 1,2
)
,
changeover_data AS (select 
d11.country_code
,ROUND(CAST(((d12.max_capita - d11.max_capita) / d11.max_capita * 100.0) AS DECIMAL),2) AS capita_changeover
FROM data2011 d11
JOIN data2012 d12
ON d11.country_code = d12.country_code
WHERE ((d12.max_capita - d11.max_capita) / d11.max_capita * 100.0) IS NOT NULL)

SELECT 
country_code,
CONCAT(capita_changeover,'%'),
RANK() OVER(ORDER BY capita_changeover DESC)
FROM changeover_data









