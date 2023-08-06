import os
from threading import Thread
from time import sleep
from infiniguard_api.lib.rest.common import http_code

from infiniguard_api.common import const, messages
from infiniguard_api.lib.hw.cli_handler import run_syscli
from infiniguard_api.lib.logging import iguard_logging
from infiniguard_api.lib.rest.common import error_handler
from infiniguard_api.lib.hw.output_parser import check_command_successful


log = iguard_logging.get_logger(__name__)


@error_handler
def reboot(**kwargs):
    wait_time = kwargs.pop('wait_time', const.REBOOT_WAIT_TIME_S)
    reboot_thread(wait_time)
    return dict(message=messages.DDE_REBOOTING_MSG.format(wait_time)), http_code.OK


def reboot_system(wait):
    sleep(wait)
    log.warn(messages.REBOOTING_SYSTEM)
    command_line = ['/opt/DXi/syscli', '--nodemanage', '--reboot', '--sure']
    infiniguard_reboot = os.environ.get('INFINIGUARD_REBOOT', "1") == "1"
    if infiniguard_reboot:
        run_syscli(command_line, check_command_successful, 'system')


def reboot_thread(wait_time):
    wait_time = const.REBOOT_WAIT_TIME_S if not wait_time else wait_time
    thread = Thread(target=reboot_system, args=(wait_time,))
    log.warn(messages.REBOOTING_TIME_WARNING.format(wait_time))
    thread.start()
