# Have I Been Pwned checker

A Python project that checks whether passwords have appeared in known data breaches using the **Have I Been Pwned (HIBP) Pwned Passwords API**.

The password checker uses the **k-anonymity model**, meaning the full password is never transmitted to the API.

## Features

* Secure password checking using SHA-1 hash prefix matching
* Command-line interface
* Modular Python package structure
* Unit test scaffold (WIP)
* Email breach checker implementation (requires a HIBP Account and API key)

## Project Directory Tree

```text
project_have_i_been_pwned/
├── src/
│   ├── __init__.py
│   ├── check_email.py
│   ├── check_password.py
|   └── config.py
├── tests/
│   ├── test_check_email.py
│   └── test_check_password.py
├── .env.example
├── .gitignore
├── LICENSE
├── pytest.ini
├── README.md
└── requirements.txt
```

## Installation

Clone the repository:

```bash
git clone https://github.com/timmymooney/project_have_i_been_pwned.git
cd project_have_i_been_pwned
```

Create a virtual environment (only do once):

```bash
python -m venv .venv
```

Activate it (do each time loading your session):

Windows:

```powershell
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Password checking

Run:

```bash
python -m src.check_password Password321
```

Example output:

```text
'Password321' was found X number of times. You should change this password.
```

## Email checking

The email breach API requires a **HIBP API key**.

Set:

```text
HIBP_API_KEY=your_api_key_here
```

Then run:

```bash
python -m src.check_email nobody@badexample.com
```

## Security

Passwords are converted to SHA-1 locally.

Only the first five characters of the hash are sent to HIBP.

The plaintext password is never transmitted.

## Testing

Respective test files for the check password and check email scripts are located in the `tests/` directory, using pytest functions. 

To run test suite, run the following in the base root of the project directory:
```bash
pytest -v
```

## Future improvements

* Unit testing with Pytest (WIP)
* More verbose terminal output