#!/usr/bin/env python3
import os
import yaml
import click
import getpass
import subprocess
import urllib.request

from time import time


class GameManager:
    def __init__(self, name) -> None:
        with open(f"{os.path.dirname(__file__)}/servers.yaml") as f:
            serverObj = yaml.load(f, Loader=yaml.FullLoader)[name]
        f.close()

        self.name = serverObj["name"]
        self.installer = serverObj["installer"]
        self.backend = serverObj["backend"]
        self.appId = serverObj["appId"]
        self.params = serverObj["launchParams"]
        self.user = getpass.getuser()
        self.install_path = f'{os.path.expanduser("~")}/{self.name}-server'
        self.daemon_path = "/etc/systemd/system"
        self.launch_file = f"{self.install_path}/launch.sh"
        self.steamcmd_path = "/opt/steamcmd"
        os.makedirs(self.daemon_path, exist_ok=True)

    def install(self) -> None:
        os.makedirs(self.install_path, exist_ok=True)
        unit_file = f"{self.daemon_path}/{self.name}.service"

        if os.path.exists(self.launch_file):
            os.rename(self.launch_file, f"{self.launch_file}_{time()}.backup")

        with open(self.launch_file, "w+") as file:
            file.write(self.params)
        file.close()

        if os.path.exists(unit_file):
            os.rename(unit_file, f"{unit_file}_{time()}.backup")
        with open(unit_file, "w+") as file:
            file.write(
                f"[Unit]\nAfter=network.target\nDescription=Daemon for {self.name} dedicated server\n[Install]\nWantedBy=default.target\n[Service]\nType=simple\nWorkingDirectory={self.install_path}\nExecStart=/bin/bash {self.install_path}/launch.sh"
            )
        file.close()

        if self.installer == "steamcmd":
            subprocess.run(
                [
                    f"{self.steamcmd_path}/steamcmd.sh",
                    "+login",
                    "anonymous",
                    "+force_install_dir",
                    self.install_path,
                    "+app_update",
                    self.appId,
                    "validate",
                    "+quit",
                ],
                check=True,
                cwd=self.steamcmd_path,
            )

        if self.backend == "srcds":
            if os.path.exists(f"{self.install_path}/{self.name}/console.log"):
                os.rename(f"{self.install_path}/{self.name}/console.log", f"{self.install_path}/{self.name}/console.log_{time()}.backup")
            else:
                os.makedirs(f"{self.install_path}/{self.name}", exist_ok=True)
                subprocess.run(["touch", f"{self.install_path}/{self.name}/console.log"])

            with open(self.launch_file, "a") as file:
                file.write(f"\ntail -f {self.install_path}/{self.name}/console.log")
            file.close()


@click.group()
def gsdcli():
    pass


@gsdcli.command()
@click.argument("name")
def install(name):
    game_manager = GameManager(name)
    game_manager.install()


if __name__ == "__main__":
    gsdcli()
