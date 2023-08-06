from fenix_bot_api.constants import common_prefix

# List of all commands
commands = []

class command:
    # alias: list[str] | str
    def __init__(self, alias) -> None:
        self.alias = alias
        self.help = f"Usage {common_prefix}{self.alias}"
        pass

    def execute(self, extra=None) -> str:
        raise NotImplementedError

    def match(self, other_alias):
        if isinstance(self.alias, str):
            return self.alias == other_alias
        elif isinstance(self.alias, list): 
            return other_alias in self.alias
        else:
            return False

    def __str__(self) -> str:
        return f"{self.alias}"

def help_execute(extra=None):
    if extra == None or extra == "":
        return f"Prefix: {common_prefix}\nCommands: {get_commands()}"
    else:
        for command in commands:
            if command.match(extra):
                return command.help

def run_command(comm: str, extra=None, commands=commands):
    for command in commands:
        if command.match(comm):
            return command.execute(extra)

def load():
    help_command = command("help")
    help_command.help = f"Usage {common_prefix}{help_command.alias} [args]\nargs is any other command.\n{get_commands()}"
    help_command.execute = help_execute

    commands.append(help_command)

def get_commands(jont: str=",\n"):
    return jont.join([str(c) for c in commands])