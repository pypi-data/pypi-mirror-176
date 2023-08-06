from fenix_bot_api.util import decode_time, defaultTime
from fenix_bot_api.constants import common_prefix, create_alias
from fenix_bot_api.comm import commands, command

# this should be different from what the srun or bin runs, to evade problems
param_prefix = "--"

# sbatch options
name = command(["name", "job-name"])
name.execute = lambda bash, name: bash.replace("0NAME", name)

qos = command("qos")
qos.execute = lambda bash, qos: bash.replace("0QOS", qos)

n = command(["n", "N"])
n.execute = lambda bash, n: bash.replace("0N", n)

ntasks = command(["ntasks", "ntasks-per-node"])
ntasks.execute = lambda bash, ntasks: bash.replace("0NTASKS", ntasks)

out = command(["output", "out", "o"])
out.execute = lambda bash, out: bash.replace("0OUT", getLog(out, ".out"))

err = command(["error", "err", "e"])
err.execute = lambda bash, err: bash.replace("0ERR", getLog(err, ".err"))

log = command(["log", "l"])
log.execute = lambda bash, log: bash.replace("0OUT", getLog(log, ".out")).replace("0ERR", getLog(log, ".err"))

time = command(["time", "t"])
time.execute = lambda bash, time: bash.replace("0TIME", decode_time(time))

modules = command(["modules", "mod", "m"])
modules.execute = lambda bash, modules: bash.replace("0MODULES", "0MODULES\n" + "\n".join([f"module load {module}" for module in modules.split(" ")]))

BIN = command(["bin", "b"])
BIN.execute = lambda bash, BIN: bash.replace("0COMMAND", BIN)

mail = command("mail")
mail_bash = "#SBATCH --mail-user={}\n#SBATCH --mail-type=ALL"
mail.execute = lambda bash, mail: bash.replace("0MAIL", mail_bash.format(mail))

# auto_modules declaration
mpi = command("mpi")
mpi.execute = lambda bash: "mpi/latest"
mkl = command("mkl")
mkl.execute = lambda bash: "mkl/latest"

# flags declaration
no_purge = command("no-purge")
no_purge.execute = lambda bash: bash.replace("module purge\n", "")
no_env = command("no-env")
no_env.execute = lambda bash: bash.replace("#SBATCH --get-user-env\n", "")

options = [name, qos, n, ntasks, out, err, log, time, modules, BIN, mail]
auto_modules = [mpi, mkl]
flags = [no_purge, no_env]

def run(commands: list):
    bash = open("base").read()
    current_command: command = None
    current_stash = []
    jobname = ""
    for comm in commands:
        if str(comm).startswith(param_prefix):
            if current_command is not None:
                bash = current_command.execute(bash, " ".join(current_stash))
                current_command = None
                current_stash.clear()
            comm = comm[2:]
            for option in options:
                if option.match(comm):
                    current_command = option
                    continue
            for auto_module in auto_modules:
                if auto_module.match(comm):
                    bash = bash.replace("0MODULES", "0MODULES\n" + f"module load {auto_module.execute(bash)}")
                    continue
            for flag in flags:
                if flag.match(comm):
                    bash = flag.execute(bash)
                    continue
            continue
        if current_command is not None:
            current_stash.append(comm)
    if len(current_stash) > 0:
        bash = current_command.execute(bash, " ".join(current_stash))
        current_command = None
        current_stash.clear()
    bash = bash.replace("0MODULES", "")
    bash = bash.replace("0QOS", "small-gaku")
    bash = bash.replace("0N", "1")
    bash = bash.replace("0NTASKS", "1")
    bash = bash.replace("0OUT", f"{jobname}_%j.out")
    bash = bash.replace("0ERR", f"{jobname}_%j.err")
    bash = bash.replace("0TIME", defaultTime)
    bash = bash.replace("0MAIL", "")
    return bash

def getLog(log: str, ext: str):
    return log if log.endswith(ext) else log + ext

def load():
    # Its here just to appear in the help command
    create = command(create_alias)
    create.help = f"""
Usage: {common_prefix}create [params]
params, * is required, in () are the default values:
    *{name} name
    {qos} qos (small-gaku)
    {n} N (1)
    {ntasks} ntasks (1)
    {out} out (name_%j.out)
    {err} error (name_%j.err)
    {log} log (shorthand for out and err at the same time)
    {time} time ({defaultTime})
    {modules} modules
    *{BIN} bin
    {auto_modules} shorcuts
    {flags} shorcuts
"""
    create.execute = lambda extra: None
    commands.append(create)