import re
from fenix_bot_api.util import get_length, get_nodes, get_output
from fenix_bot_api.constants import common_prefix
from fenix_bot_api.comm import commands, command

def show_(extra):
    ## Up Time
    pattern = re.compile("up ([0-9]+) [a-z]+, ( ?[0-9]{1,2}:[0-9]{2}|[0-9]{1,2} [a-z]{3})")
    days, hours = re.findall(pattern, get_output("uptime"))[0]
    ## Jobs Running
    running = str(get_length(["squeue", "-t", "RUNNING"]))
    ## Jobs in Q
    pending = str(get_length(["squeue", "-t", "PENDING"]))
    ## Nodes
    allNodes = get_nodes()
    responsives = get_nodes("-r")
    dead = get_nodes("-d")
    allocated = get_nodes(["-t", "allocated"])
    down = get_nodes(["-t", "down"])
    mixed = get_nodes(["-t", "mixed"])
    idle = get_nodes(["-t", "idle"])
    ## Connected Users
    users = str(get_length("w"))
    return f"""
Up Time: {days} d {hours}
Jobs Running: {running}
Jobs Pending: {pending}
Total Nodes: {allNodes}
Responsive Nodes: {responsives}
Dead Nodes: {dead}
Idle Nodes: {idle}
Midex Nodes: {mixed}
Allocated Nodes: {allocated}
Down Nodes: {down}
Connected Users: {users}
"""

def load():
    show = command("show")
    show.execute = show_

    status = command("status")
    status.execute = lambda extra: "Running"

    qos = command("qos")
    qos.execute = lambda extra: get_output(["sacctmgr", "show", "qos", "format=name,priority,maxWall"])

    nodes = command(["nodes", "node"])
    nodes.execute = lambda extra: get_output("sinfo")

    user = command(["usuario", "user", "u"])
    user.help = f"Usage: {common_prefix}{user.alias} name\nname is the name of the user to show"
    user.execute = lambda u: get_output(["squeue", "-l", "-u", u])

    commands.append(show)
    commands.append(status)
    commands.append(qos)
    commands.append(nodes)
    commands.append(user)