WITH snapshot AS (
    SELECT queue,
           CASE WHEN resolved <= :cutoff THEN 1 ELSE 0 END AS closed,
           (unixepoch(resolved) - unixepoch(opened)) / 3600.0 AS resolution_hours,
           (unixepoch(:cutoff) - unixepoch(opened)) / 3600.0 AS age_hours
    FROM tickets
    WHERE opened <= :cutoff
)
SELECT queue,
       COUNT(*) AS received,
       SUM(1 - closed) AS open_count,
       ROUND(MAX(CASE WHEN closed = 0 THEN age_hours END), 1) AS oldest_open_hours,
       ROUND(AVG(CASE WHEN closed = 1 THEN resolution_hours END), 1) AS avg_closed_hours
FROM snapshot
GROUP BY queue
ORDER BY oldest_open_hours DESC, queue;
