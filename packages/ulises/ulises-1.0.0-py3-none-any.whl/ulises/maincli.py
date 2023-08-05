import docker
from pprint import pprint as pp, pformat as pf
import rlcompleter
import readline

from ulises.subcli import SubCli
from ulises.imagescli import ImagesCli
from ulises.containerscli import ContainersCli
from ulises.volumescli import VolumesCli

readline.parse_and_bind("tab: complete")
readline.set_completer_delims(' \t')

class MainCli(SubCli):

    NOT_REMOVABLE_STATUS = ["restarting", "running", "paused"]

    def __init__(self):
        super().__init__()

        self.error=0
        self.docker = docker.from_env()

    def CMD_images(self):
        self.next_command = ImagesCli(self.docker).cmdloop()

    def CMD_containers(self):
        self.next_command = ContainersCli(self.docker).cmdloop()

    def CMD_volumes(self):
        self.next_command = VolumesCli(self.docker).cmdloop()

    def CMD_networks(self):
        self.next_command = NetworksCli(self.docker).cmdloop()

    CMD_images.__doc__=SubCli.CMD_images.__doc__
    CMD_containers.__doc__=SubCli.CMD_containers.__doc__
    CMD_volumes.__doc__=SubCli.CMD_volumes.__doc__
    CMD_networks.__doc__=SubCli.CMD_networks.__doc__
