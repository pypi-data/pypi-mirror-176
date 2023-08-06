"""
Fenix Bot API Library
"""

__name__ = "fenix-bot-api"
__version__ = "1.3.0"
__author__ = "Carlettos"
__license__ = "GNU GPL v3"

from fenix_bot_api.comm import command, load as load0
from fenix_bot_api.command_create import load as load1
from fenix_bot_api.commands_system import load as load2
from fenix_bot_api.commands_user import load as load3

load0()
load1()
load2()
load3()