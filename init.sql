CREATE TABLE IF NOT EXISTS post_events (
    event_time DateTime,
    post_id UInt64,
    user_id UInt64,
    event_type Enum('view' = 1, 'like' = 2, 'comment' = 3)
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(event_time)
ORDER BY (post_id, event_time);

CREATE MATERIALIZED VIEW IF NOT EXISTS post_statistics_mv
ENGINE = SummingMergeTree()
PARTITION BY toYYYYMM(date)
ORDER BY (post_id, date)
POPULATE
AS SELECT
    post_id,
    toDate(event_time) AS date,
    countIf(event_type = 'view') AS views,
    countIf(event_type = 'like') AS likes,
    countIf(event_type = 'comment') AS comments
FROM post_events
GROUP BY post_id, date;