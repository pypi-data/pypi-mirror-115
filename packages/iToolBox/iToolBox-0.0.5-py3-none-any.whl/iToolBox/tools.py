#!/usr/bin/env python

"""
A set of useful tools.
"""

import os
import shutil
import sys

from loguru import logger

LOG_FORMAT = '<light-green>[{time:HH:mm:ss}]</light-green> <level>{message}</level>'
LOG_LEVEL = 'TRACE'

logger.remove()
logger.add(sys.stderr, format=LOG_FORMAT, level=LOG_LEVEL)


def trace(s): logger.info(s) if s else ''
def debug(s): logger.debug(s) if s else ''
def info(s): logger.info(s) if s else ''
def success(s): logger.success(s) if s else ''
def warning(s): logger.warning(s) if s else ''
def error(s): logger.error(s) if s else ''
def critical(s): logger.critical(s) if s else ''


def error_and_exit(msg, code=1):
    """
    Logging an error message and exit with an exit code.
    
    :param msg: str, an error message.
    :param code: int, an exit code.
    """
    
    error(msg)
    sys.exit(code)


def mkdir(path):
    """
    Make a directory or exit on error.
    
    :param path: str, path to directory needs to be created.
    :return: str, path to a directory.
    """
    
    if not path:
        error_and_exit('Path for mkdir must be a non-empty string.')
    if not isinstance(path, str):
        error_and_exit(f'Path {path} for mkdir is not a string.')
    try:
        os.mkdir(path)
    except FileExistsError:
        debug(f'Directory {path} already exist.')
    except OSError as e:
        error_and_exit(f'{e}, create directory failed!')
    return path


def touch(path, overwrite=False):
    """
    Touch a empty file or exit on error.
    
    :param path: str, path to a file needs to be created.
    :param overwrite: bool, whether to overwrite an existing file.
    :return: str, path to a file.
    """
    
    if not path:
        error_and_exit('Path for touch must a be non-empty string.')
    if not isinstance(path, str):
        error_and_exit(f'Path {path} for touch is not a string.')
    if os.path.isfile(path):
        if overwrite:
            try:
                with open(path, 'w') as o:
                    o.write('')
            except OSError as e:
                error_and_exit(f'{e}, touch file (overwrite existing file) failed!')
        else:
            logger.debug(f'File {path} already exists and did not overwrite.')
    else:
        try:
            with open(path, 'w') as o:
                o.write('')
        except OSError as e:
            error_and_exit(f'{e}, touch file failed!')
    return path


def rm(path, exit_on_error=True):
    """
    Delete a path (to a file or directory).
    
    :param path: str, path to a file or directory needs to be deleted.
    :param exit_on_error: bool, whether to exit on error of deleting.
    :return: None
    """
    
    if not path:
        error_and_exit('Path for rm must be a non-empty string.')
    if not isinstance(path, str):
        error_and_exit(f'Path {path} for rm is not a string.')
    if os.path.exists(path):
        try:
            os.unlink(path)
        except IsADirectoryError:
            try:
                shutil.rmtree(path)
            except Exception as e:
                error(f'{e}, delete directory failed!')
                if exit_on_error:
                    sys.exit(1)
        except OSError as e:
            error(f'{e}, delete file failed!')
            if exit_on_error:
                sys.exit(1)
    else:
        debug(f"No such file or directory '{path}', delete file or directory aborted!")


def equal_len_lists(l1, l2, msg='', exit_if_unequal=True):
    """
    Check if two lists consist of same number of elements.
    
    :param l1: list, the first list.
    :param l2: list, the second list.
    :param msg: str, error message if two list consists of unequal number of elements.
    :param exit_if_unequal: bool, whether to exit on two list consists of unequal number of elements.
    :return: boo, True or False for equal or unequal number of elements, respectively.
    """
    
    equal = len(l1) == len(l2)
    if not equal:
        error(msg)
        if not exit_if_unequal:
            sys.exit(1)
    return equal


def exist(path, file=False, folder=False, exit_on_non_exist=True, messaging=True, prefix='Path'):
    def _exist(p):
        if os.path.exists(p):
            message = ''
            if file:
                message = '' if os.path.isfile(p) else f"{prefix} '{p}' does exist, but it is not a file."
            elif folder:
                message = '' if os.path.isfile(p) else f"{prefix} '{p}' does exist, but it is not a directory."
        else:
            message = f"{prefix} '{path}' does not exist"
        if message:
            p = ''
            if exit_on_non_exist:
                error_and_exit(message)
            else:
                if messaging:
                    error(messaging)
        return p
    
    if path:
        if isinstance(path, str):
            path = _exist(path)
        elif isinstance(path, (list, tuple)):
            path = [_exist(p) for p in path]
        else:
            error_and_exit(f'TypeError: {prefix} only can be string, list, or tuple.')
    else:
        error_and_exit(f'ValueError: {prefix} can not be any None values.')
    return path


def link(source, destine, return_basename=False):
    def _link(src, dst):
        src = exist(src, file=True, prefix='Link source')
        if exist(dst, exit_on_non_exist=False, messaging=False):
            if not os.path.islink(dst):
                error_and_exit(f"Link target '{dst}' already exist, but it is not a link.")
        else:
            try:
                os.symlink(src, dst)
            except OSError as e:
                error_and_exit(f'{e}, create link failed!')
        return os.path.basename(dst) if return_basename else dst
    
    if isinstance(source, str):
        if isinstance(destine, str):
            destine = _link(source, destine)
        else:
            error_and_exit(f'TypeError: link destine only can be string when the source is a string.')
    elif isinstance(source, (list, tuple)):
        if isinstance(destine, (list, tuple)):
            if len(source) == len(destine):
                destine = [_link(s, d) for s, d in zip(source, destine)]
            else:
                error_and_exit(f'ValueError: link source and destine have unequal number of elements.')
        else:
            error_and_exit(f'TypeError: link source only can be a list or tuple when the source is a list or tuple.')
    else:
        error_and_exit(f'TypeError: link source only can be string, list, or tuple.')
    return destine


def replace(s, pat='', repl='', patterns=None, start=False, end=False):
    d = {}
    if pat:
        if isinstance(pat, str) and isinstance(repl, str):
            d[pat] = repl
        else:
            error_and_exit('Argument pat and repl for function replace need to be strings.')
    elif patterns:
        if isinstance(patterns, dict):
            d = patterns
        else:
            error_and_exit('Argument patterns for function replace need to be a dictionary.')
    else:
        error_and_exit('ValueError: invalid arguments were passed to function replace, see doc for usage!')
    for k, v in d.items():
        if start:
            s = v.join(s.split(k, 1)) if s.startswith(k) else s
        elif end:
            s = v.join(s.rsplit(k, 1)) if s.endswith(k) else s
        else:
            s = s.replace(k, v)
    return s


def basename(path, prefix=None, suffix=None):
    if isinstance(path, str):
        path = os.path.basename(path)
        if isinstance(prefix, str):
            path = replace(path, prefix, '', start=True)
        elif isinstance(prefix, (list, tuple)):
            for x in prefix:
                path = replace(path, x, '', start=True)
        elif prefix is None:
            pass
        else:
            error_and_exit('Argument prefix for function basename must be a string, list, or tuple.')
        
        if isinstance(suffix, str):
            path = replace(path, suffix, '', start=True)
        elif isinstance(suffix, (list, tuple)):
            for x in suffix:
                path = replace(path, x, '', end=True)
        elif suffix is None:
            pass
        else:
            error_and_exit('Argument suffix for function basename must be a string, list, or tuple.')
    else:
        error_and_exit('Argument path for function basename must be a string.')
    return path


if __name__ == '__main__':
    pass
