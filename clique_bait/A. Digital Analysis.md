## Solutions to section A.

**How many users are there?**

```sql
SELECT 
COUNT(DISTINCT user_id) AS user_count
FROM clique_bait.users;
```
Result:

![image](https://user-images.githubusercontent.com/104590611/214282598-ac5a99b4-34ff-4d84-ae79-03e08ed14918.png)



**How many cookies does each user have on average?**

```sql
SELECT
	ROUND(AVG(cookie_count),2) AS avg_cookie
		FROM
			(SELECT 
				user_id, 
				COUNT(cookie_id) AS cookie_count
			FROM clique_bait.users
				GROUP BY 1) X
```
Result:

![image](https://user-images.githubusercontent.com/104590611/214284460-aad955fb-8ca1-44e6-ba0b-c7ef246a8cc2.png)



**What is the unique number of visits by all users per month?**

```sql
SELECT 
	TO_CHAR(TO_TIMESTAMP(DATE_PART('month', event_time)::text, 'MM'), 'Month') AS MONTH,
	COUNT(DISTINCT e.visit_id) AS visits_p_month
FROM clique_bait.events e
	GROUP BY 1
```

Result:


![image](https://user-images.githubusercontent.com/104590611/214289405-ddb70357-4382-4ba6-85e3-55d7d18074d2.png)



**What is the number of events for each event type?**



```sql
SELECT 
	event_name,
	e.event_type,
	COUNT(*)
FROM clique_bait.events e
	INNER JOIN clique_bait.event_identifier ei
		ON e.event_type = ei.event_type
GROUP BY 1,2
```

Result:


![image](https://user-images.githubusercontent.com/104590611/214290687-80ec446c-80d5-4d33-974a-e20e690663f8.png)


**What is the percentage of visits which have a purchase event?**

```sql
SELECT 
	ROUND(COUNT(*)*100.0
	/
	(SELECT COUNT(DISTINCT visit_id) FROM clique_bait.events),2) AS purchase_percentage
FROM clique_bait.events e
	INNER JOIN clique_bait.event_identifier ei
		ON e.event_type = ei.event_type
WHERE event_name = 'Purchase'
```

Result:

![image](https://user-images.githubusercontent.com/104590611/214293490-2f928d56-ffb8-457f-8668-9313f6d87f8b.png)




*to be continued.*
*underwork*
