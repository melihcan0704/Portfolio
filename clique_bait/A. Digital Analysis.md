## Solutions to section A.

**How many users are there?**

```sql
SELECT 
COUNT(DISTINCT user_id) AS user_count
FROM clique_bait.users;
```

![image](https://user-images.githubusercontent.com/104590611/214282598-ac5a99b4-34ff-4d84-ae79-03e08ed14918.png)
