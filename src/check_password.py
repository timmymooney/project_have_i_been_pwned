"""
Check whether one or more passwords have appeared in known data breaches.

This module uses the Have I Been Pwned (HIBP) Pwned Passwords API and
implements the k-anonymity model, meaning the full password is never
actually sent to the API.
"""

import hashlib
import sys
import requests

# base URL for the HIBP passwords API
API_URL = "https://api.pwnedpasswords.com/range/"


def request_api_data(query_char):
    """
    Request password hash suffixes matching the given SHA-1 prefix.

    Args:
        query_char (str): The first five characters of the SHA-1 hash.

    Returns:
        requests.Response: The API response containing hash suffixes.

    Raises:
        RuntimeError: If the API request fails.
    """

    response = requests.get(API_URL + query_char, timeout=10)

    if response.status_code != 200:
        raise RuntimeError(
            f"Error fetching: {response.status_code}. Check the API and try again."
        )

    return response


def get_password_leaks_count(response, hash_to_check):
    """
    Search the API response for the password hash suffix.

    Args:
        response (requests.Response): API response containing hash suffixes.
        hash_to_check (str): The SHA-1 hash suffix to search for.

    Returns:
        int: Number of times the password has appeared in breaches.
    """

    hashes = (line.split(":") for line in response.text.splitlines())

    for hash_suffix, count in hashes:
        if hash_suffix == hash_to_check:
            return int(count)

    return 0


def pwned_api_check(password):
    """
    Check whether a password has been exposed in a known data breach.

    Args:
        password (str): The plaintext password to check.

    Returns:
        int: Number of times the password has appeared in breaches.
    """

    # convert the password to an uppercase SHA-1 hash
    sha1_password = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()

    # split the hash for k-anonymity lookup
    first_five, tail = sha1_password[:5], sha1_password[5:]

    response = request_api_data(first_five)

    return get_password_leaks_count(response, tail)


def main(args):
    """
    Command-line entry point.

    Args:
        args (list[str]): Passwords supplied on the command line.

    Returns:
        int: Exit status code.
    """

    if not args:
        print("Usage: python -m src.check_password <password1> [<password2> ...]")
        return 1

    # check each supplied password individually
    for password in args:
        count = pwned_api_check(password)

        if count:
            print(
                f"'{password}' was found {count:,} times. You should change this password."
            )
        else:
            print(f"'{password}' was NOT found. Good news!")

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))