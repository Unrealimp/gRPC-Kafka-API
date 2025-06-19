import json
from unittest.mock import MagicMock, patch
from statistics_service import kafka_consumer


@patch('statistics_service.kafka_consumer.get_consumer')
def test_kafka_consumer_receives_message(mock_get_consumer):
    mock_message = MagicMock()
    mock_message.value = {'post_id': 42, 'event_type': 'view'}

    mock_consumer = MagicMock()
    mock_consumer.__iter__.return_value = [mock_message]
    mock_get_consumer.return_value = mock_consumer

    with patch('builtins.print') as mock_print:
        kafka_consumer.start_kafka_consumer()
        mock_print.assert_called_with("[Kafka] Received: {'post_id': 42, 'event_type': 'view'}")

def test_kafka_event_structure():
    raw_message = json.dumps({
        "post_id": 100,
        "event_type": "comment"
    }).encode("utf-8")

    decoded = json.loads(raw_message.decode("utf-8"))

    assert isinstance(decoded["post_id"], int)
    assert decoded["event_type"] in ("view", "like", "comment")
