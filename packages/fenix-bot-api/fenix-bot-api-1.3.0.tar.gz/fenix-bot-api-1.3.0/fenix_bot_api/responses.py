from fenix_bot_api.comm import run_command
from fenix_bot_api.command_create import run
from fenix_bot_api.util import to_code
from fenix_bot_api.constants import create_alias

def handle_response(content: str, md: bool = False) -> str:
    message: list[str] = content.lower().strip().split(" ")
    if len(message) == 0:
        return None
    elif len(message) == 1:
        resp = run_command(message[0], None)
        if resp is None:
            return None
        else:
            return resp if not md else to_code(resp, "scala")
    elif len(message) == 2:
        resp = run_command(message[0], message[1])
        if resp is None:
            return None
        else:
            return resp if not md else to_code(resp, "scala")
    
    if message[0] == create_alias:
        resp = run(message[1:])
        if resp is None:
            return None
        else:
            return resp if not md else to_code(resp, "sh")
