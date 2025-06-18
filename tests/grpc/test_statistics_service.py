import pytest
from unittest.mock import MagicMock
from statistics_service.server import StatisticsService
from proto import statistics_pb2


@pytest.fixture
def service():
    service = StatisticsService()
    service.ch_client = MagicMock()
    return service


def test_get_post_stats_returns_correct_data(service):
    # Мокаем ClickHouse ответ
    service.ch_client.execute.return_value = [(100, 25, 10)]

    request = statistics_pb2.PostIdRequest(post_id=1)
    response = service.GetPostStats(request, context=None)

    assert response.views == 100
    assert response.likes == 25
    assert response.comments == 10


def test_get_post_likes_dynamics_returns_correct_data(service):
    service.ch_client.execute.return_value = [
        ('2024-06-01', 5),
        ('2024-06-02', 10)
    ]

    request = statistics_pb2.PostDynamicsRequest(
        post_id=1,
        start_date='2024-06-01',
        end_date='2024-06-02'
    )

    response = service.GetPostLikesDynamics(request, context=None)

    assert len(response.data) == 2
    assert response.data[0].date == '2024-06-01'
    assert response.data[0].value == 5
    assert response.data[1].date == '2024-06-02'
    assert response.data[1].value == 10


def test_get_top_users_by_views(service):
    service.ch_client.execute.return_value = [
        (101, 300),
        (102, 250)
    ]

    request = statistics_pb2.TopRequest(metric='views')
    response = service.GetTopUsers(request, context=None)

    assert len(response.users) == 2
    assert response.users[0].user_id == 101
    assert response.users[0].value == 300
