import sys
import argparse
import logging
import pprint

from .config import commandline

_LOGGER = logging.getLogger(__name__)



def main(argv=None):
    if argv is None:
        argv= sys.argv[1:]

    ap = argparse.ArgumentParser()
    pytehon 
    # adds options to load/print configuration file
    commandline.standard_argparse_options(
        ap.add_argument_group('configuration'),
        default_config='config.yaml')

    # more explicit actions
    ap.add_argument('--dry-run', action='store_true')
    
    options = ap.parse_args(argv)

    # load configuraiton from file
    config = commandline.config_from_options(options)

    return config
    


