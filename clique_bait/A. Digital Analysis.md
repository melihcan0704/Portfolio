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




