# Defguard create users

Create users without proper API

## Requirements

The input file is a CSV file in the format:

```
firstname;lastname;email
```

The `defguard_session` cookie value is needed for the `--token` option.

The defguard url is needed for the `--url` option.

## Example

Create users without enrollment:
```
./create_users.py --create --file users.csv --url https://defguard.example.com --token oodai0izahjae6Waedeith9of
```

Enroll previously created users:
```
./create_users.py --enroll --file users.csv --url https://defguard.example.com --token oodai0izahjae6Waedeith9of
```

## Options

```
usage: create_user.py [-h] [-f FILE] -t TOKEN -u URL [-d] [-c] [-e]

options:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  file containing a list of firstname;lastname;email
  -t TOKEN, --token TOKEN
                        defguard admin session token
  -u URL, --url URL     defguard url, ex: https://defguard.example.com
  -d, --dry-run
  -c, --create
  -e, --enroll
```
