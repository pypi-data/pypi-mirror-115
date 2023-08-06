# -*- coding: utf-8 -*-
"""
Displays status of jenkins jobs.

This py3status module displays the status of desired jenkins jobs.
The desired jenkins jobs are defined by configuration. The current
status of each job is represented by the i3status colors. In default
configuration of the colors is as following:

Configuration parameters:
    cache_timeout: Renew of jenkins job status interval in seconds (default 60)
    jenkins_url: The base URL of jenkins server
    jenkins_pass_path: Path to jenkins credentials, if password-store is using.
    jenkins_username: Username for jenkins server, if unsecure credentials storage method is using.
    jenkins_password: Password for jenkins server, if unsecure credentials storage method is using.
    text_status: Text displayed for jenkins job status (default "S").
    text_not_connected: Text displayed if jenkins server is not reachable (default "-").
    text_common_error: Text displayed if an error occurred (default "E").
    text_job_separator: Separator between the Jenkins job status.
    jobs: List of jenkins jobs.

Configuration parameter for jobs entries:
    name: Jenkins job name.
    text_status: Text dispayls for this jenkins job status. If not set, the common text_status will be displayed.

Format placeholders:

    format: {jobs} dispay the configured jenkins jobs status
    format_job: {status} display the status of a jenkins job

Color options:
    color_good: job status "SUCCESS"
    color_degraded: job status "UNSTABIL"
    color_bad: job status "FAILURE"
    color_aborted: job status "ABORTED"
    color_bad: common error or jenkins server not reachable

Requires:
    pass: Recommended storage of jenkins credentials.

Example:
```
jenkins_status {
  jenkins_url = "https://myjenkins:1234"
  jenkins_pass_path = "Jenkins"
  jobs = [
    {
      "name": "job1",
      "text_status": "J1"
    },
    {
      "name": "job2",
      "text_status": "J2"
    }
  ]
}
```

@author Andreas Schmidt
@license MIT
"""

import logging
from jenkins import Jenkins
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from pypass import PasswordStore, EntryType
from py3status.composite import Composite

log = logging.getLogger("py3status-jenkins_status")


class Py3status:

    format = "JS: {jobs}"
    format_job = "{status}"
    jenkins_url = ""
    cache_timeout = 60
    jenkins_pass_path = None
    jenkins_username = None
    jenkins_password = None
    jobs = []
    text_status = "S"
    text_not_connected = "-"
    text_common_error = "E"
    text_job_separator = ""
    color_aborted = "#CCCCCC"

    def __init__(self):
        self._jenkins_server = None

    def jenkins_status(self):
        if not self._set_jenkins_server():
            return self._error_response(self.text_common_error)
        if not self._is_jenkins_available():
            return self._error_response(self.text_not_connected)
        if not isinstance(self.jobs, list):
            return self._error_response(self.text_common_error)

        jobs_status = []
        for job in self.jobs:
            job_response = {}
            if not isinstance(job, dict):
                return self._error_response(self.text_common_error)
            success, color = self._get_job_color(job)
            text_status = (
                job["text_status"] if "text_status" in job.keys() else self.text_status
            )
            if not success:
                full_text = self.py3.safe_format(self.format_job, {"status": self.text_common_error}, force_composite=True)
                job_response["color"] = self.py3.COLOR_BAD
            else:
                full_text = self.py3.safe_format(self.format_job, {"status": text_status}, force_composite=True)
                job_response["color"] = color
            if isinstance(full_text, Composite):
                job_response["full_text"] = full_text.text()
            else:
                job_response["full_text"] = str(full_text)
            jobs_status.append(job_response)
        job_separator = self.py3.safe_format(self.text_job_separator)
        composite = self.py3.composite_join(job_separator, jobs_status)
        return {
            "cached_until": self.py3.time_in(self.cache_timeout),
            "full_text": self.py3.safe_format(self.format, {"jobs": composite}),
        }

    def _error_response(self, error_text: str) -> dict:
        return {
            "full_text": self.py3.safe_format(self.format, {"status": error_text}),
            "color": self.py3.COLOR_BAD,
        }

    def _set_jenkins_server(self) -> bool:
        if self._jenkins_server:
            return True
        user, pw = self._get_credentials()
        if user is None or pw is None:
            return False
        try:
            self._jenkins_server = Jenkins(self.jenkins_url, username=user, password=pw)
            # TODO This is ugly but currently there are no other way to disable
            #      ssl verification. Fix it after
            #      https://review.opendev.org/c/jjb/python-jenkins/+/709118
            #      is completed.
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
            self._jenkins_server._session.verify = False
        except Exception as e:
            log.error("Jenkins init error: {}".format(e))
            return False
        return True

    def _is_jenkins_available(self) -> bool:
        try:
            self._jenkins_server.get_whoami()
        except Exception as e:
            log.error("Jenkins communication error: {}".format(e))
            return False
        return True

    def _get_job_color(self, job: dict):
        # TODO make colors configurable in depends of jenkins status
        try:
            job_info = self._jenkins_server.get_job_info(job["name"])
            last_build_number = job_info["lastCompletedBuild"]["number"]
            build_info = self._jenkins_server.get_build_info(
                job["name"], last_build_number
            )

            if build_info["result"] == "SUCCESS":
                return True, self.py3.COLOR_GOOD
            elif build_info["result"] == "UNSTABLE":
                return True, self.py3.COLOR_DEGRADED
            elif build_info["result"] == "ABORTED":
                if self.py3.COLOR_ABORTED:
                    return True, self.py3.COLOR_ABORTED
                else:
                    return True, self.color_aborted
            else:
                return True, self.py3.COLOR_BAD

        except Exception as e:
            log.error("Get jenkins job info failed: {}".format(e))
            return False, self.py3.COLOR_BAD

    def _get_credentials(self):
        if self.jenkins_pass_path:
            return self._get_pass_credentials()
        elif self.jenkins_username and self.jenkins_password:
            return self.jenkins_username, self.jenkins_password
        else:
            log.error("No credentials information found")
            return None, None

    def _get_pass_credentials(self):
        try:
            ps = PasswordStore()
        except Exception as e:
            log.error("Initialization of pypass failed: {}".format(e))
            return None, None
        credentials_list = ps.get_passwords_list()
        if self.jenkins_pass_path not in credentials_list:
            log.error(
                'No credentials under path "{}" found'.format(self.jenkins_pass_path)
            )
            return None, None
        user = ps.get_decrypted_password(self.jenkins_pass_path, EntryType.username)
        pw = ps.get_decrypted_password(self.jenkins_pass_path, EntryType.password)
        return user, pw


if __name__ == "__main__":  # pragma: no cover
    """
    Test this module by calling it directly.
    """
    from py3status.module_test import module_test

    logging.basicConfig()
    log.setLevel(logging.DEBUG)

    config = {
        # 'jenkins_pass_path': "",
        # 'jenkins_url': "",
        # 'format': 'xyz: {status}',
        # 'jobs': [
        #   {
        #     'name': "job1",
        #     'text_status': 'J1'
        #   },
        #   {
        #     'name': "job2"
        #   },
        #   {
        #     'name': "job3"
        #   }
        # ]
    }

    module_test(Py3status, config)
