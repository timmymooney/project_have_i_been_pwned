"""
Check whether one or more email addresses have appeared in known data breaches.

This module uses the Have I Been Pwned (HIBP) Breached Account API.
Unlike the password API, this endpoint requires a HIBP API key.
"""

import sys
import requests

from .config import HIBP_API_KEY, USER_AGENT

# base URL for the HIBP breached email account API
API_URL = "https://haveibeenpwned.com/api/v3/breachedaccount/"


def check_email_breaches(email):
    """
    Check whether an email address appears in known breaches.

    Args:
        email (str): The email address to check.

    Returns:
        list: Breach information if found.
        []: No breaches found.

    Raises:
        RuntimeError: If no API key is configured or another API error occurs.
    """

    # the email API cannot be used without a valid HIBP API key
    if not HIBP_API_KEY:
        raise RuntimeError(
            "HIBP_API_KEY is not configured. The HIBP email API requires a paid API key."
        )

    headers = {
        "hibp-api-key": HIBP_API_KEY,
        "User-Agent": USER_AGENT,
    }

    params = {
        # request full breach details rather than a truncated response
        "truncateResponse": "false"
    }

    response = requests.get(
        API_URL + email,
        headers=headers,
        params=params,
        timeout=10,
    )

    # successful request
    if response.status_code == 200:
        return response.json()

    # 404 means the account was not found in any known breach
    if response.status_code == 404:
        return []

    if response.status_code == 401:
        raise RuntimeError("Invalid HIBP API key.")

    if response.status_code == 429:
        raise RuntimeError("Rate limit exceeded.")

    raise RuntimeError(f"HIBP API error: {response.status_code}")


def main(args):
    """
    Command-line entry point.

    Args:
        args (list[str]): Email addresses supplied on the command line.

    Returns:
        int: Exit status code.
    """

    if not args:
        print("Usage: python -m src.check_email <email1> [<email2> ...]")
        return 1

    # check each supplied email address
    for email in args:
        try:
            breaches = check_email_breaches(email)

            if breaches:
                print(f"{email} was found in {len(breaches)} breach(es):")

                for breach in breaches:
                    print(f" - {breach['Name']} ({breach['BreachDate']})")
            else:
                print(f"{email} was not found in any known breaches.")

        except RuntimeError as error:
            print(error)
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))