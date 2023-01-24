CREATE SCHEMA clique_bait;

CREATE TABLE clique_bait.event_identifier (
  "event_type" INTEGER,
  "event_name" VARCHAR(13)
);

INSERT INTO clique_bait.event_identifier
  ("event_type", "event_name")
VALUES
  ('1', 'Page View'),
  ('2', 'Add to Cart'),
  ('3', 'Purchase'),
  ('4', 'Ad Impression'),
  ('5', 'Ad Click');

CREATE TABLE clique_bait.campaign_identifier (
  "campaign_id" INTEGER,
  "products" VARCHAR(3),
  "campaign_name" VARCHAR(33),
  "start_date" TIMESTAMP,
  "end_date" TIMESTAMP
);

INSERT INTO clique_bait.campaign_identifier
  ("campaign_id", "products", "campaign_name", "start_date", "end_date")
VALUES
  ('1', '1-3', 'BOGOF - Fishing For Compliments', '2020-01-01', '2020-01-14'),
  ('2', '4-5', '25% Off - Living The Lux Life', '2020-01-15', '2020-01-28'),
  ('3', '6-8', 'Half Off - Treat Your Shellf(ish)', '2020-02-01', '2020-03-31');

CREATE TABLE clique_bait.page_hierarchy (
  "page_id" INTEGER,
  "page_name" VARCHAR(14),
  "product_category" VARCHAR(9),
  "product_id" INTEGER
);

INSERT INTO clique_bait.page_hierarchy
  ("page_id", "page_name", "product_category", "product_id")
VALUES
  ('1', 'Home Page', null, null),
  ('2', 'All Products', null, null),
  ('3', 'Salmon', 'Fish', '1'),
  ('4', 'Kingfish', 'Fish', '2'),
  ('5', 'Tuna', 'Fish', '3'),
  ('6', 'Russian Caviar', 'Luxury', '4'),
  ('7', 'Black Truffle', 'Luxury', '5'),
  ('8', 'Abalone', 'Shellfish', '6'),
  ('9', 'Lobster', 'Shellfish', '7'),
  ('10', 'Crab', 'Shellfish', '8'),
  ('11', 'Oyster', 'Shellfish', '9'),
  ('12', 'Checkout', null, null),
  ('13', 'Confirmation', null, null);

CREATE TABLE clique_bait.users (
  "user_id" INTEGER,
  "cookie_id" VARCHAR(6),
  "start_date" TIMESTAMP
);

INSERT INTO clique_bait.users
  ("user_id", "cookie_id", "start_date")
VALUES
  ('1', 'c4ca42', '2020-02-04'),
  ('2', 'c81e72', '2020-01-18'),
  ('3', 'eccbc8', '2020-02-21'),
  ('4', 'a87ff6', '2020-02-22'),
  ('5', 'e4da3b', '2020-02-01'),
  ('6', '167909', '2020-01-25'),
  ('7', '8f14e4', '2020-02-09'),
  ('8', 'c9f0f8', '2020-02-12'),
  ('9', '45c48c', '2020-02-07'),
  ('10', 'd3d944', '2020-01-23'),
                .
                .
                .
                .
                .
                .
                .
                .
   
  ('64', '87a4ba', '2020-03-18');

CREATE TABLE clique_bait.events (
  "visit_id" VARCHAR(6),
  "cookie_id" VARCHAR(6),
  "page_id" INTEGER,
  "event_type" INTEGER,
  "sequence_number" INTEGER,
  "event_time" TIMESTAMP
);

INSERT INTO clique_bait.events
  ("visit_id", "cookie_id", "page_id", "event_type", "sequence_number", "event_time")
VALUES
  ('ccf365', 'c4ca42', '1', '1', '1', '2020-02-04 19:16:09.182546'),
  ('ccf365', 'c4ca42', '2', '1', '2', '2020-02-04 19:16:17.358191'),
  ('ccf365', 'c4ca42', '6', '1', '3', '2020-02-04 19:16:58.454669'),
  ('ccf365', 'c4ca42', '9', '1', '4', '2020-02-04 19:16:58.609142'),
  ('ccf365', 'c4ca42', '9', '2', '5', '2020-02-04 19:17:51.72942'),
  ('ccf365', 'c4ca42', '10', '1', '6', '2020-02-04 19:18:11.605815'),
  ('ccf365', 'c4ca42', '10', '2', '7', '2020-02-04 19:19:10.570786'),
  ('ccf365', 'c4ca42', '11', '1', '8', '2020-02-04 19:19:46.911728'),
  ('ccf365', 'c4ca42', '11', '2', '9', '2020-02-04 19:20:45.27469'),
  ('ccf365', 'c4ca42', '12', '1', '10', '2020-02-04 19:20:52.307244'),
  ('ccf365', 'c4ca42', '13', '3', '11', '2020-02-04 19:21:26.242563'),
                              .
                              .
                              .
                              .
                              .
                              .
                              .
                              .
  ('355a6a', '87a4ba', '10', '1', '15', '2020-03-18 22:44:16.541396'),
  ('355a6a', '87a4ba', '11', '1', '16', '2020-03-18 22:44:18.90083'),
  ('355a6a', '87a4ba', '11', '2', '17', '2020-03-18 22:45:12.670472'),
  ('355a6a', '87a4ba', '12', '1', '18', '2020-03-18 22:45:54.081818'),
  ('355a6a', '87a4ba', '13', '3', '19', '2020-03-18 22:45:54.984666');
