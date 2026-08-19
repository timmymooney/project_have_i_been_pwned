"""
Unit tests for the email checker module.
"""

from src.check_email import check_email_breaches
from unittest.mock import Mock, patch

import pytest

# raise RuntimeError when no API key is configured.
def test_check_email_no_api_key():
    with patch("src.check_email.HIBP_API_KEY", None):
        with pytest.raises(RuntimeError, match="not configured"):
            check_email_breaches("nobody@badexample.com")


# return an empty list when the email is not found.
def test_check_email_not_found():
    mock_response = Mock()
    mock_response.status_code = 404

    with patch("src.check_email.HIBP_API_KEY", "fake-api-key"):
        with patch(
            "src.check_email.requests.get",
            return_value=mock_response
        ):
            result = check_email_breaches("nobody@badexample.com")

    assert result == []


# raise RuntimeError for an invalid API key.
def test_check_email_invalid_api_key():
    mock_response = Mock()
    mock_response.status_code = 401

    with patch("src.check_email.HIBP_API_KEY", "fake-api-key"):
        with patch(
            "src.check_email.requests.get",
            return_value=mock_response
        ):
            with pytest.raises(RuntimeError, match="Invalid HIBP API key"):
                check_email_breaches("nobody@badexample.com")