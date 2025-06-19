from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from rest_api.main import app, stub
from rest_api.proto import statistics_pb2

client = TestClient(app)

def test_get_post_stats_success():
    stub.GetPostStats = MagicMock(return_value=statistics_pb2.PostStatsResponse(
        views=150, likes=30, comments=8
    ))

    response = client.get("/posts/42/stats")
    assert response.status_code == 200
    assert response.json() == {
        "views": 150,
        "likes": 30,
        "comments": 8
    }

def test_get_top_users_success():
    stub.GetTopUsers = MagicMock(return_value=statistics_pb2.TopUsersResponse(users=[
        statistics_pb2.TopUsersResponse.Item(user_id=1, value=100),
        statistics_pb2.TopUsersResponse.Item(user_id=2, value=80),
    ]))

    response = client.get("/top/users?metric=views")
    assert response.status_code == 200
    assert response.json() == [
        {"user_id": 1, "value": 100},
        {"user_id": 2, "value": 80}
    ]

def test_get_top_posts_invalid_metric():
    response = client.get("/top/posts?metric=invalid")
    assert response.status_code == 400
    assert "Invalid metric" in response.json()["detail"]
