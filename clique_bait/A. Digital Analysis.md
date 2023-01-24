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
