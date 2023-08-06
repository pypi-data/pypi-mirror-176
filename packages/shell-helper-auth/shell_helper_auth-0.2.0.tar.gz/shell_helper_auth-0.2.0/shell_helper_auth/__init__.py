import subprocess

from requests.auth import AuthBase


class ShellHelperAuth(AuthBase):
    def __init__(self, command, remove_prefix='', add_prefix=''):
        self.command = command
        self.prefix_to_remove = remove_prefix
        self.prefix_to_add = add_prefix

    def __call__(self, request):
        command_stdout = subprocess.run(
            self.command.split(), capture_output=True, encoding="utf-8", text=True
        ).stdout

        request.headers["Authorization"] = self._build_header_value(command_stdout)
        return request

    def _build_header_value(self, command_stdout):
        token = _remove_prefix(command_stdout.rstrip(), self.prefix_to_remove)
        return f'{self.prefix_to_add}{token}'


def _remove_prefix(string, prefix):
    try:
        return string.removeprefix(prefix)
    except AttributeError:
        # Python <3.9
        return string[len(prefix):] if string.startswith(prefix) else string
