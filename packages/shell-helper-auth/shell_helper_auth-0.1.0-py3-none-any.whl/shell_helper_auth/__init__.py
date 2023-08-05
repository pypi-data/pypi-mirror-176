import subprocess

from requests.auth import AuthBase


class ShellHelperAuth(AuthBase):
    def __init__(self, command, prefix=''):
        self.command = command
        self.prefix = prefix

    def __call__(self, request):
        token = subprocess.run(
            self.command.split(), capture_output=True, encoding="utf-8", text=True
        ).stdout.rstrip()

        request.headers["Authorization"] = f"{self.prefix}{token}"
        return request
