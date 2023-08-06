"""
ssh.py - Part of SSHepherd

:author: George <drpresq@gmail.com>
:description: SSHepherd SSH module - Consists of objects that define communication with ssh hosts
:license: GPL3
:donation:
    BTC - 15wRP3NGm2zQwsC36gYAMf8ZaBNuDP6BiR
    LTC - LQANeFg6qhEUCftCGpXTdgCKnPkBMR5Ems
"""

import getpass
import subprocess
import time
from typing import Union, Optional
from pathlib import Path
from enum import IntEnum


class ArgIndex(IntEnum):
    key = 2
    target = 3
    command = 4
    source = 1
    destination = 2


class Communicator:
    ssh_user: str
    ssh_key: Path
    current_users: dict

    _args: list = ['ssh', '-i', '{ssh_key}', '{ssh_user}@{target_system}', '{ssh_command}']

    def __init__(self, ssh_user: Optional[str] = None, ssh_key: Optional[Union[str, Path]] = None) -> None:
        self.ssh_user = ssh_user if ssh_user else getpass.getuser()
        try:
            self.ssh_key = Path(ssh_key) if ssh_key is not None \
                and Path(ssh_key).exists() \
                else self.__validate_ssh_key(ssh_key)
        except FileNotFoundError as err:
            print(f'SSH Key file not found: {err}')
            exit(-1)

    @staticmethod
    def __validate_ssh_key(ssh_key: Optional[str] = None) -> Path:
        candidate_path: Path = Path(f'{Path.home()}/.ssh/{ssh_key}') if Path(f'{Path.home()}/.ssh/{ssh_key}').exists() \
            else Path(f'{Path.home()}/.ssh/id_rsa')
        if not candidate_path.exists():
            raise FileNotFoundError()
        return candidate_path

    @staticmethod
    def __communicate(arguments: [str]) -> str:
        return subprocess.check_output(arguments, stderr=subprocess.DEVNULL).decode()

    def get_users_by_system(self, target_group: Union[list, str]) -> dict:
        self._args[ArgIndex.command] = "$(which ls) /home/"
        current_users: dict = {}
        if not isinstance(target_group, list):
            target_group = [target_group]
        for system in target_group:
            self._args[ArgIndex.target] = f'{self.ssh_user}@{system}'
            current_users.update({system: self.__communicate(self._args).strip('\n').split('\n')})
        self.current_users = current_users
        return current_users

    def add_users(self, target_group: Union[list, str], new_users: dict) -> dict:
        scp_arguments = ['scp', '', '']
        new_users = {users: key for users, key in new_users.items() if Path(key).exists()}
        _ = self.get_users_by_system(target_group)
        if not isinstance(target_group, list):
            target_group = [target_group]
        for system in target_group:
            user_delta: list = [user for user in new_users.keys() if user not in self.current_users[system]]
            for user in user_delta:
                scp_arguments[ArgIndex.source] = new_users[user]
                scp_arguments[ArgIndex.destination] = f'{self.ssh_user}@{system}:~'
                self.__communicate(scp_arguments)
                self._args[ArgIndex.target] = f'{self.ssh_user}@{system}'
                self._args[ArgIndex.command] = f'sudo useradd -s /bin/bash {user};sudo mkdir /home/{user};sudo cp -r /etc/skel/. /home/{user};sudo mkdir /home/{user}/.ssh;sudo mv {user}_id_rsa.pub /home/{user}/.ssh/authorized_keys; sudo chown -R {user} /home/{user};sudo chgrp -R {user} /home/{user}/'
                self.__communicate(self._args)
                time.sleep(10)
        return self.get_users_by_system(target_group)

    def run_command(self, target_group: Union[list, str], command: str) -> None:
        if not isinstance(target_group, list):
            target_group = [target_group]
        self._args[ArgIndex.command] = command
        for system in target_group:
            self._args[ArgIndex.target] = f'{self.ssh_user}@{system}'
            ret = self.__communicate(self._args).strip('\n').split('\n')
            print(f'{system} output:\t{ret}')
