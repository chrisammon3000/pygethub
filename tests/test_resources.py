import pytest
import time
from unittest.mock import Mock, patch
from requests.models import Response
from pygethub.resources import (
    calculate_delay,
    fetch
)

def test_calculate_delay():
    # Create a mock response with specific 'X-RateLimit-Remaining' and 'X-RateLimit-Reset' headers
    response = Mock(headers={'X-RateLimit-Remaining': '50', 'X-RateLimit-Reset': '1629459260'})
    
    # Mock time.time to return a specific current time
    with patch('time.time', return_value=1629459200):
        # Call the function with the mock response
        delay = calculate_delay(response)

    # Check that the delay is calculated correctly
    assert delay == 1.2

def test_calculate_delay_no_remaining():
    # Create a mock response with 'X-RateLimit-Remaining' header set to '0'
    response = Mock(headers={'X-RateLimit-Remaining': '0', 'X-RateLimit-Reset': '1629459260'})
    
    # Mock time.time to return a specific current time
    with patch('time.time', return_value=1629459200):
        # Call the function with the mock response
        delay = calculate_delay(response)

    # Check that the delay is equal to the window
    assert delay == 60

def test_calculate_delay_reset_in_past():
    # Create a mock response with 'X-RateLimit-Remaining' header set to '0' and 'X-RateLimit-Reset' header set to a time in the past
    response = Mock(headers={'X-RateLimit-Remaining': '0', 'X-RateLimit-Reset': '1629459140'})
    
    # Mock time.time to return a specific current time
    with patch('time.time', return_value=1629459200):
        # Call the function with the mock response
        delay = calculate_delay(response)

    # Check that the delay is equal to 1
    assert delay == 1

@patch('requests.Session.get', autospec=True)
def test_fetch_success(mock_get):
    # Create a mock response
    mock_response = Mock(spec=Response)
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"key": "value"}
    mock_response.headers = {"X-RateLimit-Remaining": "100", "X-RateLimit-Reset": str(int(time.time() + 100))}

    # Configure the mock get to return the mock response
    mock_get.return_value = mock_response

    # Call the function with the mock response
    result = fetch('https://api.github.com/users', 'token')
    
    # Assert the function returned the expected result
    assert result == {"success": True, "data": {"key": "value"}, "link": None}


@patch('requests.Session.get', autospec=True)
def test_fetch_respects_rate_limit(mock_get):
    # Create a mock response
    mock_response = Mock(spec=Response)
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"key": "value"}
    mock_response.headers = {"X-RateLimit-Remaining": "1", "X-RateLimit-Reset": str(int(time.time() + 1))}

    # Configure the mock get to return the mock response
    mock_get.return_value = mock_response

    # Call the function with the mock response
    start_time = time.time()
    result = fetch('https://api.github.com/users', 'token')
    end_time = time.time()

    # Assert the function returned the expected result and respected the rate limit
    assert result == {"success": True, "data": {"key": "value"}, "link": None}
    assert end_time - start_time >= 1  # Ensure delay was at least 1 second
