#!/usr/bin/env python3

import os
import sys
import time
import logging

from src.prober_kernel import ProberKernel
from src.args.ProberArgs import ProberArgsParser, ProberArgs


def main():
    arg_parser = ProberArgsParser()
    args = arg_parser.parse()

    _configure_logging(args)

    kernel = ProberKernel(args)
    kernel.run()
    logging.info('Exitting.')
# end def


def _configure_logging(prober_args : ProberArgs):
    log_fpath = os.path.join(
        prober_args.output_dirpath,
        'barapost-prober_{}.log'.format(
            time.strftime('%Y%m%d_%H%M%S', time.localtime())
        )
    )
    logging.basicConfig(
        encoding='utf-8',
        level = logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_fpath),
            logging.StreamHandler(sys.stderr)
        ]
    )
    logging.info('Starting.')
    logging.info('Logging to `{}`'.format(log_fpath))
    logging.info('Run parameters:')
    logging.info(str(prober_args))
# end def


if __name__ == '__main__':
    main()
# end def

sys.exit(0)
