import logging
import traceback
from logging.handlers import TimedRotatingFileHandler

from basic.os.path import create_dir_if_not_exist
from basic.os.file import get_file_folder

def init_log(file_path: str, log_level: int, log_interval: int=1, log_backup: int=30, log_time_fmt: str='[%Y-%m-%d %H:%M:%S]'):
    file_folder = get_file_folder(file_path)
    if create_dir_if_not_exist(file_folder) is True:
        handler = TimedRotatingFileHandler(filename=file_path, when="D", interval=log_interval, backupCount=log_backup)
        handler.suffix = "%Y-%m-%d_%H-%M.log"
        handler.setLevel(log_level)

        return logging.basicConfig(level=log_level, format='levelname:%(levelname)s filename: %(filename)s '
                                                'outputNumber: [%(lineno)d] output msg: %(message)s - %(asctime)s',
                                   datefmt='[%d/%b/%Y %H:%M:%S]', handlers=[handler])

def _get_normalized_locals_text(locals_dict) -> str:
    var_text_list = []
    for var_name, var_value in locals_dict.items():
        if var_name.startswith('__') or var_name == 'self':
            continue
        var_text_list.append(f"{var_name}={str(var_value)[:200]}")
    return ', '.join(var_text_list)


def log_unhandled_error(**kwargs):
    stacks = traceback.StackSummary.extract(traceback.walk_stack(None), limit=2, capture_locals=True)
    stack_len = len(stacks)
    if stack_len == 0:
        locals_text = "NO_STACK"
    elif stack_len == 1:
        locals_text = _get_normalized_locals_text(stacks[0].locals)
    else:
        locals_text = _get_normalized_locals_text(stacks[1].locals)
    logging.error(f"Unhandled exception! Locals: {locals_text}.", exc_info=True, stack_info=True)