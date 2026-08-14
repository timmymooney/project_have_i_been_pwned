"""
Unit tests for the password checker module.
"""

from src.check_password import get_password_leaks_count, pwned_api_check, request_api_data
from unittest.mock import Mock, patch

import pytest

# create Mock HIBP password API response for testing
@pytest.fixture
def mock_password_response():

    response = Mock()
    response.text = "ABCDEF:5\n123456:10"
    return response


# return the breach count when the hash suffix exists
def test_get_password_leaks_count_match(mock_password_response):

    count = get_password_leaks_count(mock_password_response, "ABCDEF")
    assert count == 5

# return zero when the hash suffix is not present
def test_get_password_leaks_count_no_match(mock_password_response):

    count = get_password_leaks_count(mock_password_response, "ZZZZZZ")
    assert count == 0

# return the response object when the API request succeeds
@patch("src.check_password.requests.get")
def test_request_api_data_success(mock_get):

    mock_response = Mock(status_code=200)
    mock_get.return_value = mock_response

    response = request_api_data("ABCDE")

    assert response == mock_response
    mock_get.assert_called_once()

#  raise RuntimeError when the API request fails
@patch("src.check_password.requests.get")
def test_request_api_data_failure(mock_get):

    mock_get.return_value = Mock(status_code=500)

    with pytest.raises(RuntimeError):
        request_api_data("ABCDE")