#!/usr/bin/env python

import argparse
from typing import Optional

from .scripts.tg import TG
from .scripts.xrd import XRD

def main():

    parser = argparse.ArgumentParser(prog='tomodb', description='Tool for submitting data to TomoDB')

    required = parser.add_argument_group('required named arguments')
    required.add_argument('-a', '--analysis', choices=['tga', 'xrd', 'bet'], help='Type of analysis.')
    required.add_argument('-f', '--folder', type=str, help='The folder directory containing the data files.')

    # TGA SPECIFIC
    tga_specific = parser.add_argument_group('optional tga specific')
    tga_specific.add_argument('--coke', action='store_true', help='If sample contains coke.')

    # XRD SPECIFIC
    xrd_specific = parser.add_argument_group('optional xrd specific')
    xrd_specific.add_argument('--drysealed', action='store_true', help='If capillaries were sealed.')
    xrd_specific.add_argument('-drying_temp', type=int, help='Drying temperature.')

    # BET SPECIFIC




    args = parser.parse_args()
    args_dict = vars(args)


    # Commiting analysis.

    if args.analysis == 'tga':
        TG(folder_path=args.folder, coke=args.coke)

    elif args.analysis == 'xrd':
        XRD(folder_path=args.folder, dry_and_sealed=args.drysealed, drying_temp=args.drying_temp)

    elif args.analysis == 'bet':
        pass

    



