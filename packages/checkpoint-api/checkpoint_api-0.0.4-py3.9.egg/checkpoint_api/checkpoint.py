import functools
import time
import logging
import logging.handlers
from urllib.parse import urljoin

import requests

requests.packages.urllib3.disable_warnings()

from .enumerations import DetailsLevel
from .exceptions import CheckpointMissingCredentialsException


class CheckpointSession(requests.Session):
    checkpoint_login_url = "login"
    checkpoint_logout_url = "logout"

    def __init__(
        self,
        mgmt_ip,
        checkpoint_user="",
        checkpoint_pass="",
        api_key="",
        domain="",
        read_only=True,
        verify=False,
        logfile="checkpoint.log",
    ):
        super().__init__()
        self.checkpoint_user = checkpoint_user
        self.checkpoint_pass = checkpoint_pass
        self.api_key = api_key
        if not (self.checkpoint_user and self.checkpoint_pass) and not self.api_key:
            raise CheckpointMissingCredentialsException(
                "Specify either checkpoint_user and checkpoint_pass or api_key!"
            )
        self.mgmt_ip = mgmt_ip
        self.base_url = f"https://{self.mgmt_ip}/web_api/"
        self.domain = domain
        self.read_only = read_only
        self.verify = verify
        self.logfile = logfile
        self._logging(self.logfile)
        self.headers.update({"content-type": "application/json"})

    def _logging(self, logfile):
        """Initialize logging"""
        self.logger = logging.getLogger("CHECKPOINT")
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        if logfile:
            fh = logging.handlers.RotatingFileHandler(
                logfile, encoding="utf-8", maxBytes=100000000, backupCount=5
            )
            fh.setLevel(logging.DEBUG)
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)

    def __enter__(self):
        """used by command 'with open()'"""
        self._login()
        return super().__enter__()

    def __exit__(self, *args):
        """always close connection"""
        self._logout()
        super().__exit__(*args)

    def request(self, method, url, *args, **kwargs):
        kwargs["verify"] = self.verify
        url = urljoin(self.base_url, url)
        self.logger.debug(f"Send: {url} {str(kwargs)}")

        response = super().request(method, url, *args, **kwargs)
        if not response.encoding:
            response.encoding = "utf-8"
        self.logger.debug(
            f"Received: {response.text} status_code: {str(response.status_code)}"
        )
        if response.status_code == 200:
            return response.json()
        else:
            try:
                code = response.json()["code"]
                message = response.json()["message"]
            except Exception as e:
                code = "err"
                message = str(e)
            raise Exception(f"{response.status_code}: {code} - {message}")

    def _login(self):
        """Login to Check Point API"""
        self.logger.debug(f"Logging in {self.checkpoint_user}")
        if self.api_key:
            login_data = {"api-key": self.api_key}
        else:
            login_data = {
                "user": self.checkpoint_user,
                "password": self.checkpoint_pass,
            }
        login_data["read-only"] = "true" if self.read_only else "false"

        if self.domain:
            login_data["domain"] = self.domain

        response_json = self.post(self.checkpoint_login_url, json=login_data)
        self.sid = response_json["sid"]
        self.headers.update({"X-chkp-sid": self.sid})
        self.logger.debug(f"SessionId: {self.sid}")

    def _logout(self):
        """Logout from Check Point API"""
        if not self.read_only:
            self.logger.debug(
                f"Discarding unpublished changes for {self.checkpoint_user}"
            )
            self.discard()
        self.logger.debug(f"Logging out {self.checkpoint_user}")
        try:
            self.post(self.checkpoint_logout_url, json={})
        except Exception as e:
            self.logger.debug(e)
            self.logger.debug(f"Logging out {self.checkpoint_user} - next attempt")
            self.post(self.checkpoint_logout_url, json={})

    def paginate(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            res = func(*args, **kwargs)
            check_attributes = ["objects", "rulebase", "objects-dictionary"]
            if not any([attr in res for attr in check_attributes]):
                return res
            result = {attr: res[attr] for attr in check_attributes if attr in res}
            if "to" in res and "from" in res:
                length = res["to"] - res["from"] + 1
            while length >= kwargs["json"]["limit"]:
                kwargs["json"]["offset"] += kwargs["json"]["limit"]
                res = func(*args, **kwargs)
                {
                    result[attr].extend(res[attr])
                    for attr in check_attributes
                    if attr in res
                }
                if "to" in res and "from" in res:
                    length = res["to"] - res["from"] + 1
            return result

        return wrapper

    def search_object_by_cidr(
        self, cidr, type=None, details_level=DetailsLevel.STANDARD, limit=10, offset=0
    ):
        data = {
            "filter": cidr,
            "ip-only": True,
            "limit": limit,
            "offset": offset,
            "details-level": details_level.value,
        }
        if type:
            data["type"] = type.value
        return self.post_paginate("show-objects", json=data)

    def get_groups(self, details_level=DetailsLevel.STANDARD, limit=10, offset=0):
        data = {"limit": limit, "offset": offset, "details-level": details_level.value}
        return self.post_paginate("show-groups", json=data)

    @paginate
    def post_paginate(self, url, json):
        if "limit" not in json:
            json["limit"] = 50
        if "offset" not in json:
            json["offset"] = 0
        return super().post(url, json=json)

    # TODO: Test!
    def publish(self):
        task = self.post("publish", json={})
        count = 0
        while True:
            time.sleep(2)
            task_status = self.post(
                "show-task",
                json={
                    "task-id": task["task-id"],
                },
            )
            if task_status["tasks"][0]["status"] != "in progress":
                break
            if count >= 100:
                raise Exception("Publishing taking too long")
        if task_status["tasks"][0]["status"] != "succeeded":
            raise Exception(f"Error publishing changes")

    # TODO: Test!
    def discard(self):
        return self.post("discard", json={})

    # TODO: Test!
    def policy_install(
        self,
        policy_package,
        targets,
        access=True,
        desktop_security=False,
        qos=False,
        threat_prevention=False,
    ):
        policy_install_data = {
            "policy-package": policy_package,
            "targets": targets,
            "access": access,
            "desktop-security": desktop_security,
            "qos": qos,
            "threat-prevention": threat_prevention,
        }
        return self.post("install-policy", json=policy_install_data)
