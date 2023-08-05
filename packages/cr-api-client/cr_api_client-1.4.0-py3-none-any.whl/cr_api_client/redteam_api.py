# -*- coding: utf-8 -*-
#
# Copyright (c) 2016-2021 AMOSSYS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
import time
from typing import Any

import requests


# Configuration access to Cyber Range endpoint
REDTEAM_API_URL = "http://127.0.0.1:5004"
# Expect a path to CA certs (see:
# https://requests.readthedocs.io/en/master/user/advanced/)
CA_CERT_PATH = None
# Expect a path to client cert (see:
# https://requests.readthedocs.io/en/master/user/advanced/)
CLIENT_CERT_PATH = None
# Expect a path to client private key (see:
# https://requests.readthedocs.io/en/master/user/advanced/)
CLIENT_KEY_PATH = None

# Module variables
attack_list = {}


# -------------------------------------------------------------------------- #
# Internal helpers
# -------------------------------------------------------------------------- #


def _get(route: str, **kwargs: str) -> Any:
    return requests.get(
        f"{REDTEAM_API_URL}{route}",
        verify=CA_CERT_PATH,
        cert=(CLIENT_CERT_PATH, CLIENT_KEY_PATH),
        **kwargs,
    )


def _post(route: str, **kwargs: str) -> Any:
    return requests.post(
        f"{REDTEAM_API_URL}{route}",
        verify=CA_CERT_PATH,
        cert=(CLIENT_CERT_PATH, CLIENT_KEY_PATH),
        **kwargs,
    )


def _put(route: str, **kwargs: str) -> Any:
    return requests.put(
        f"{REDTEAM_API_URL}{route}",
        verify=CA_CERT_PATH,
        cert=(CLIENT_CERT_PATH, CLIENT_KEY_PATH),
        **kwargs,
    )


def _delete(route: str, **kwargs: str) -> Any:
    return requests.delete(
        f"{REDTEAM_API_URL}{route}",
        verify=CA_CERT_PATH,
        cert=(CLIENT_CERT_PATH, CLIENT_KEY_PATH),
        **kwargs,
    )


# -------------------------------------------------------------------------- #
# Redteam API
# -------------------------------------------------------------------------- #


def reset_redteam() -> None:
    result = _delete("/platform")
    result.raise_for_status()
    result = result.json()


def execute_attack(idAttack: int, name: str) -> None:
    url = "/attack/" + str(idAttack) + "?action=start"

    response = _get(url, headers={}, data={})

    idAttack = response.json().get("idAttack", None)

    print(
        "[SATAN] "
        + response.json().get("started_date", None)
        + " : "
        + name
        + " : Started"
    )

    if idAttack is not None:
        return waiting_attack(idAttack)


def waiting_attack(id_attack: str) -> None:
    url = "/attack/" + str(id_attack)
    payload = {}
    headers = {}

    response = _get(url, headers=headers, data=payload)
    status = response.json().get("status", None)
    while status != "success":
        time.sleep(1)
        response = _get(url, headers=headers, data=payload)
        status = response.json().get("status", None)
        if status == "waiting" or status == "failed":
            break

        time.sleep(1)

    print(
        "[SATAN] "
        + response.json().get("last_update", None)
        + " : "
        + response.json()["worker"]["name"]
        + " : "
        + status
    )

    return status


def stop_satan() -> None:
    url = "/platform"
    payload = {}
    headers = {}

    response = _delete(url, headers=headers, data=payload)
    if response:
        print("Done")
    else:
        print(" ERROR - " + str(response.text.encode("utf8")))


def attack_in_list(attack_name: str, workers: str) -> str:
    return next((x for x in workers if x["name"] == attack_name), None)


def attack_is_possible(attack_name: str) -> str:

    response = _get("/attack", headers={}, data={})
    attacks = response.json()

    return next(
        (x["idAttack"] for x in attacks if x["worker"]["name"] == attack_name), None
    )


def execute_scenario(attacks: list) -> bool:
    if attacks is not None:
        return scheduler(attacks)


def list_actions() -> str:
    response = _get("/attack", headers={}, data={})
    return response.json()


def list_workers() -> str:
    response = _get("/worker", headers={}, data={})
    return response.json()


def scheduler(attacks: list) -> bool:
    for attack in attacks:
        time.sleep(5)
        # Scenario language constraint not use currently
        if type(attack) == dict:
            name = list(attack.keys())[0]
            # requirements = attack[name]
        else:
            name = attack

        idAttack = attack_is_possible(name)
        while idAttack is None:
            print("[SATAN] Attack " + name + "not available : Waiting ...")
            time.sleep(5)
            idAttack = attack_is_possible(name)
        if idAttack is not None:
            print("[SATAN] execution : " + name)
            if execute_attack(idAttack, name) == "failed":
                print("[SATAN] Error : " + attack)
                return False
        else:
            print("[SATAN] Attack not available.")
            break
    return True
