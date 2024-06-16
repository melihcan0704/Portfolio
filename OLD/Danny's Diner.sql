

## Case Study Source: https://8weeksqlchallenge.com/case-study-1/




--What is the total amount each customer spent at the restaurant?
SELECT 
	customer_id,
	SUM(price) total_sale
FROM dannys_diner.sales s
	JOIN dannys_diner.menu m 
		ON m.product_id = s.product_id
GROUP BY 1;

--How many days has each customer visited the restaurant?

SELECT 
	customer_id,
	COUNT(order_date)
FROM sales
GROUP BY 1;

--What was the first item from the menu purchased by each customer?

SELECT * FROM
(
	SELECT 
		DISTINCT customer_id,
		MIN(order_date) first_purchase_date
	FROM dannys_diner.sales s
		JOIN dannys_diner.menu m 
			ON m.product_id = s.product_id 
	GROUP BY 1
) X

	LEFT JOIN

(
	SELECT 
		DISTINCT customer_id,
		MIN(order_date) first_purchase_date,
		product_name
	FROM dannys_diner.sales s
		JOIN dannys_diner.menu m 
			ON m.product_id = s.product_id
	GROUP BY 1,3
) Y
	ON X.first_purchase_date = Y.first_purchase_date 
		AND X.customer_id = Y.customer_id
ORDER BY 1;
/* Customer_id 'A' has made 2 different purchases on the first day. 
Since there are no time stamps on the date we can't know which one was purchased first. */


--What is the most purchased item on the menu and how many times was it purchased by all customers?

SELECT 
	DISTINCT product_name,
	COUNT(*) times_purchased
	FROM dannys_diner.sales s
		JOIN dannys_diner.menu m 
			ON m.product_id = s.product_id 
GROUP BY 1
	ORDER BY 2 DESC;


--Which item was the most popular for each customer?
SELECT
	customer_id,
	MAX(times_purchased) most,
	product_name 
FROM
(
	SELECT 
		customer_id,
		COUNT(s.product_id) times_purchased,
		product_name
	FROM dannys_diner.sales s
		JOIN dannys_diner.menu m 
			ON m.product_id = s.product_id 
	GROUP BY 1,3
	ORDER BY 1
) A
GROUP BY 1,3
	ORDER BY most DESC
		LIMIT 3;
		
--Which item was purchased first by the customer after they became a member?
SELECT 
	customer_id,
	join_date,
	order_date,
	product_name
FROM 
(
	SELECT 
		m.customer_id,
		me.product_name,
		join_date,
		order_date,
		LAG(order_date) OVER(PARTITION BY m.customer_id) AS previous_purchase
	FROM dannys_diner.members m
		LEFT JOIN dannys_diner.sales s
			ON m. join_date <= s.order_date 
				AND m.customer_id = s.customer_id
		JOIN dannys_diner.menu me
			ON me.product_id = s.product_id

) B
WHERE previous_purchase IS NULL;


--Which item was purchased just before the customer became a member?
SELECT
	customer_id,
	product_name,
	join_date,
	order_date
FROM
(
	SELECT 
		m.customer_id,
		me.product_name,
		join_date,
		order_date,
		LAG(order_date) OVER(PARTITION BY m.customer_id ORDER BY order_date) AS first_just_before_member
	FROM dannys_diner.members m
		LEFT JOIN dannys_diner.sales s
			ON m. join_date >= s.order_date 
				AND m.customer_id = s.customer_id
		JOIN dannys_diner.menu me
			ON me.product_id = s.product_id
			) C
WHERE first_just_before_member IS NULL;


--What is the total items and amount spent for each member before they became a member?

SELECT 
	m.customer_id,
	COUNT(me.product_name) total_purchase_number,
	SUM(price) total_spent
FROM dannys_diner.members m
	LEFT JOIN dannys_diner.sales s
		ON m. join_date > s.order_date 
			AND m.customer_id = s.customer_id
	JOIN dannys_diner.menu me
		ON me.product_id = s.product_id
GROUP BY 1
	ORDER BY 1;
	
	
--If each $1 spent equates to 10 points and sushi has a 2x points multiplier - how many points would each customer have?

SELECT 
	s.customer_id,
		SUM(CASE WHEN m.product_id IN (2,3) THEN (price*10)
			ELSE (price*20)
				END) AS points
FROM dannys_diner.sales s
	JOIN dannys_diner.menu m 
		ON m.product_id = s.product_id
GROUP BY 1
ORDER BY 2 DESC;

--In the first week after a customer joins the program (including their join date) they earn 2x points on all items, 
--not just sushi - how many points do customer A and B have at the end of January?


SELECT 
	s.customer_id,
		SUM(CASE WHEN m.product_id IN (1,2,3) THEN (price*20)
			ELSE (price*20) END) AS points
FROM dannys_diner.sales s
	JOIN dannys_diner.menu m 
		ON m.product_id = s.product_id
	JOIN dannys_diner.members me
		ON me.customer_id = s.customer_id
			AND me.join_date <= s.order_date
WHERE s.order_date BETWEEN join_date AND '2021-02-01'
	GROUP BY 1
		ORDER BY 2 DESC;
