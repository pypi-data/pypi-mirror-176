from fenix_bot_api.util import get_output, get_users
from fenix_bot_api.constants import common_prefix
from fenix_bot_api.comm import commands, command

def rights_(name: str):
    output = get_output(["sacctmgr", "show", "user", "format=user,account,qos,admin", "-s", "-n", "-p"])
    for uaqa in output.split("\n"):
        if uaqa.find(name) != -1:
            return uaqa.replace("|", ", ")

def create_(name: str):
    return f"create {name}"

def load():
    jobs = command(["jobs", "squeue"])
    jobs.help = f"Usage: {common_prefix}{jobs.alias} name\nname is the name of the user to show"
    jobs.execute = lambda name=None: get_output(["squeue", "-u", name]) if name is not None else get_output(["squeue", "-l"])

    rights = command("rights")
    rights.help = f"Usage: {common_prefix}{rights.alias} name\nname is the name of the user to show"
    rights.execute = rights_

    disk = command(["disk", "du"])
    disk.help = f"Usage: {common_prefix}{disk.alias} name\nname is the name of the user to show"
    disk.execute = lambda name: get_output(["du", "-csh", f"/home/{name}"])

    names = command("names")
    names.execute = lambda extra: get_users()
    
    commands.append(jobs)
    commands.append(rights)
    commands.append(disk)
    commands.append(names)