#!/usr/bin/env python3

import sys
import json
import argparse
import requests


def setup(conf):

    url_create_user = conf.url + '/api/v1/user'
    url_enroll_user = conf.url + '/api/v1/user/%s/start_enrollment'

    headers = {
        'User-Agent': ('Mozilla/5.0 (X11; Linux x86_64; rv:125.0) '
                       'Gecko/20100101 Firefox/125.0'),
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json',
        'Origin': conf.url,
        'Connection': 'keep-alive',
        'Referer': conf.url + '/admin/users',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
    }

    cookies = {
        'defguard_session': conf.token,
    }

    return (
        url_create_user,
        url_enroll_user,
        headers,
        cookies
    )


def run(conf):
    url_create_user, url_enroll_user, headers, cookies = setup(conf)

    with open(conf.file, 'r') as fp:
        lines = fp.readlines()
        for user_entry in lines:

            user_entry = user_entry.strip()
            if user_entry == "":
                continue

            firstname, lastname, email = user_entry.split(";")
            print(f"f: {firstname}, l: {lastname}, e: {email}")

            username = email.split("@")[0]

            if conf.create:
                data = json.dumps({
                    "username": username,
                    "email": email,
                    "last_name": lastname,
                    "first_name": firstname,
                    "phone": "",
                    "groups": ["Users"],
                })
                # print("headers", headers, "cookies", cookies, "data", data)
                r = requests.post(
                    url_create_user,
                    headers=headers,
                    cookies=cookies,
                    data=data
                )
                print(r, r.text)
                if r.status_code == 201:
                    print((
                        f"User created: {username} - {email} - {firstname}"
                        f" - {lastname}"
                    ))
                elif r.status_code == 500:
                    print(f"User {username} already exists")
                else:
                    print((
                        "Unknown status code for "
                        f"{username}: {r.status_code}"
                    ))

            if conf.enroll:
                data = json.dumps({
                    "email": email,
                    "send_enrollment_notification": True,
                })
                url = url_enroll_user % username
                r = requests.post(
                    url,
                    headers=headers,
                    cookies=cookies,
                    data=data
                )
                print(r, r.text)
                print((
                    f"User {username} - {email} - {firstname}"
                    f" - {lastname}, enrolled"
                ))
                if r.status_code == 500:
                    print(f"User {username} already exists")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f", "--file",
        required=False,
        default="user_list.txt",
        help="file containing a list of firstname;lastname;email"
    )
    parser.add_argument(
        "-t", "--token",
        required=True,
        help="defguard admin session token"
    )
    parser.add_argument(
        "-u", "--url",
        help="defguard url, ex: https://defguard.example.com",
        required=True
    )
    parser.add_argument(
        "-d", "--dry-run",
        default=False,
        action="store_true"
    )
    parser.add_argument(
        "-c", "--create",
        default=False,
        action="store_true"
    )
    parser.add_argument(
        "-e", "--enroll",
        default=False,
        action="store_true"
    )
    args = parser.parse_args()

    run(conf=args)
    sys.exit(0)
