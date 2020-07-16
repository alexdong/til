# To group data by day

Plot out the daily total for selected period of time. 

```sql
SELECT
  created_at as "time",
  sum(total) as "current"
FROM bi_orders
WHERE
  $__timeFilter(created_at) AND
  purchase_from_channels = "Repeat customer"
GROUP BY DATE_FORMAT(created_at, '%Y-%m-%d')
ORDER BY created_at
```

Then compare the above to previous period.

```sql
SELECT
  DATE_ADD(created_at, INTERVAL 1 YEAR) AS "time_sec",
  sum(total) AS "prev. year"
FROM bi_orders
WHERE
  created_at >= DATE_ADD($__timeFrom(), INTERVAL -1 YEAR) AND
  created_at <= DATE_ADD($__timeTo(), INTERVAL -1 YEAR) AND
  purchase_from_channels = "Repeat customer"
GROUP BY DATE_FORMAT(created_at, '%Y-%m-%d')
ORDER BY created_at
```
