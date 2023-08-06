#!/usr/bin/env python3
"""
Code to systematically find the most stable geometry for molecules on surfaces
"""
import os

import daemon

from config_arg import get_args
from config_log import config_log
from dos_input import read_input
from isolated import run_isolated
from screening import run_screening
from refinement import run_refinement


def dockonsurf():
    logger.info(f'DockOnSurf started on {os.getcwd()}.')
    logger.info(f'To kill DockOnSurf execution type: `$ kill {os.getpid()}`.')
    logger.info(f"Using '{args.input}' as input.")

    inp_vars = read_input(args.input)

    if inp_vars['isolated']:
        run_isolated(inp_vars)

    if inp_vars['screening']:
        run_screening(inp_vars)

    if inp_vars['refinement']:
        run_refinement(inp_vars)

    logger.info(f'DockOnSurf finished.')


args = get_args()
logger = config_log('DockOnSurf')

print("Running DockOnSurf.\n"
      f"To check DockOnSurf activity see '{logger.handlers[0].baseFilename}'.")

if args.foreground:
    dockonsurf()
else:
    with daemon.DaemonContext(working_directory=os.getcwd(), umask=0o002,
                              files_preserve=[
                                  logger.handlers[0].stream.fileno()]):
        # From here on, the execution is carried out by a separate process in
        # background
        dockonsurf()
