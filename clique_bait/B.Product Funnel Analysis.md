**Using a single SQL query - create a new output table which has the following details:

How many times was each product viewed?

How many times was each product added to cart?

How many times was each product added to a cart but not purchased (abandoned)?

How many times was each product purchased?**

```sql
WITH activity_count AS (
  SELECT 
    e.visit_id,
	ph.page_name,
    ph.product_id,
    ph.product_category,
    SUM(CASE WHEN e.event_type = 1 THEN 1 ELSE 0 END) AS page_views,
    SUM(CASE WHEN e.event_type = 2 THEN 1 ELSE 0 END) AS added_to_cart
  FROM clique_bait.events e
  	JOIN clique_bait.page_hierarchy ph
    	ON ph.page_id = e.page_id 
  WHERE product_id IS NOT NULL
  	GROUP BY 1,2,3,4
)
,
purchases AS ( 
  SELECT 
    DISTINCT visit_id
  FROM clique_bait.events
  WHERE event_type = 3
),
joint_report AS ( 
  SELECT 
    ac.visit_id, 
    ac.product_id, 
    ac.page_name, 
    ac.product_category, 
    ac.page_views, 
    ac.added_to_cart,
    CASE WHEN p.visit_id IS NOT NULL THEN 1 ELSE 0 END AS purchase
  FROM activity_count AS ac
  LEFT JOIN purchases AS p
    ON ac.visit_id = p.visit_id
),
final_report AS (
  SELECT 
    page_name, 
    product_category, 
    SUM(page_views) AS views,
    SUM(added_to_cart) AS cart_adds, 
    SUM(CASE WHEN added_to_cart = 1 AND purchase = 0 THEN 1 ELSE 0 END) AS abandoned,
    SUM(CASE WHEN added_to_cart = 1 AND purchase = 1 THEN 1 ELSE 0 END) AS purchases
  FROM joint_report
  GROUP BY product_id, page_name, product_category)

SELECT *
FROM final_report

```

final report result:

![image](https://user-images.githubusercontent.com/104590611/214571306-bbace09f-534b-4234-99f4-f4710d170d1a.png)
