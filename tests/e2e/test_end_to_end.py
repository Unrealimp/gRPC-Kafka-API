import requests
import time
from clickhouse_driver import Client

BASE_URL = "http://localhost:8000"


def test_post_view_stats_end_to_end():
    ch = Client(
        host="localhost",
        user="default",
        password="",
        database="default"
    )
    post_id = 555

    # Эмулируем просмотр поста — вставляем напрямую
    ch.execute("""
        INSERT INTO post_events (event_time, post_id, user_id, event_type)
        VALUES (now(), %(post_id)s, 777, 'view')
    """, {'post_id': post_id})

    time.sleep(1)  # Дать ClickHouse чуть времени (если Materialized View)

    # Проверяем через REST
    resp = requests.get(f"{BASE_URL}/posts/{post_id}/stats")
    assert resp.status_code == 200
    stats = resp.json()
    assert stats["views"] >= 1


def test_top_users_end_to_end():
    ch = Client(
        host="localhost",
        user="default",
        password="",
        database="default"
    )

    ch.execute("""
        INSERT INTO post_events (event_time, post_id, user_id, event_type)
        VALUES (now(), 123, 888, 'like')
    """)

    time.sleep(1)

    resp = requests.get(f"{BASE_URL}/top/users?metric=likes")
    assert resp.status_code == 200
    users = resp.json()
    assert any(user["user_id"] == 888 for user in users)


def test_invalid_metric_handling():
    resp = requests.get(f"{BASE_URL}/top/posts?metric=not_a_metric")
    assert resp.status_code == 400
    assert "Invalid metric" in resp.json()["detail"]
