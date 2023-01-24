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

**What is the percentage of visits which view the checkout page but do not have a purchase event?**


```sql
--Checkout Page_id = 12
--Confirmation Page_id = 13
--Purchase event_type = 3
--Page_view event_type = 1


WITH bounce AS (
SELECT 
	visit_id,
	MAX(CASE WHEN event_type = 1 AND page_id = 12 THEN 1 ELSE 0 END) AS checkouts,
	MAX(CASE WHEN event_type = 3 THEN 1 ELSE 0 END) AS purchases
FROM clique_bait.events
GROUP BY 1)

SELECT ROUND(100-(SUM(purchases)*100.0 / SUM(checkouts)),2) AS checkouts_without_purchase FROM bounce
```

Result: 

![image](https://user-images.githubusercontent.com/104590611/214401418-010a628a-6b6d-4645-b354-aad6e8fae770.png)


**What are the top 3 pages by number of views?**

```sql
SELECT 
	page_name,
	COUNT(*)
FROM clique_bait.events e
	JOIN clique_bait.page_hierarchy ph
		ON e.page_id = ph.page_id
WHERE e.event_type = 1
	GROUP BY 1
		ORDER BY 2 DESC
			LIMIT 3

```

Result:

![image](https://user-images.githubusercontent.com/104590611/214403715-95254434-01d7-4675-9894-632fc509699d.png)


**What is the number of views and cart adds for each product category?**
```sql
--Event_type "Add to Cart" = 2
--Event_type "Page View" = 1
SELECT 
	product_category,
	SUM(CASE WHEN event_type = 1 THEN 1 ELSE 0 END) AS Page_views,
	SUM(CASE WHEN event_type = 2 THEN 1 ELSE 0 END) AS Add_to_cart
FROM clique_bait.events e
	JOIN clique_bait.page_hierarchy ph
		ON e.page_id = ph.page_id
WHERE ph.page_id BETWEEN 3 AND 11
	GROUP BY 1
		ORDER BY 2 DESC,3 DESC
```

Result:


![image](https://user-images.githubusercontent.com/104590611/214407406-a0eb4792-ce71-4d51-b714-02655f77c748.png)

*to be continued.*
*underwork*
