"""
File that consists of the HelloWorld Command Functionality
"""
from typing import List, Tuple
from syslog import LOG_ERR, syslog
from summit_rcm.at_interface.commands.command import Command
from summit_rcm_hello_world.services.hello_world_service import HelloWorldService


class HelloWorldCommand(Command):
    """
    AT Command to print 'Hello World'
    """

    NAME: str = "Print 'Hello World'"
    SIGNATURE: str = "at+hello"
    VALID_NUM_PARAMS: List[int] = [1]

    @staticmethod
    async def execute(params: str) -> Tuple[bool, str]:
        (valid, params_dict) = HelloWorldCommand.parse_params(params)
        if not valid:
            syslog(LOG_ERR, "Invalid Parameters")
            return (True, "ERROR")
        try:
            hello_world_str = HelloWorldService().get_hello_world()
            return (True, f"+HELLO: {hello_world_str}\r\nOK")
        except Exception as exception:
            syslog(LOG_ERR, f"Error printing 'Hello World': {str(exception)}")
            return (True, "ERROR")

    @staticmethod
    def parse_params(params: str) -> Tuple[bool, dict]:
        valid = True
        params_dict = {}
        params_list = params.split(",")
        valid &= len(params_list) in HelloWorldCommand.VALID_NUM_PARAMS
        for param in params_list:
            valid &= param == ""
        return (valid, params_dict)

    @staticmethod
    def usage() -> str:
        return "AT+HELLO"

    @staticmethod
    def signature() -> str:
        return HelloWorldCommand.SIGNATURE

    @staticmethod
    def name() -> str:
        return HelloWorldCommand.NAME
