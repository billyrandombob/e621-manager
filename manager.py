#!/usr/bin/env python3
import argparse
import json
import src.post_manager as pm
import src.tag_manager as tm
import src.util_manager as um
from os import path
from pathlib import Path
import sys

ROOT_DIR = Path(path.dirname(path.abspath(__file__)))

def get_config(p):
    print(p.config)
    try:
        with open(p.config, 'r') as config_file:
            return json.load(config_file)
    except:
        print("Invalid config file!")
        exit(1)
        
def print_menu():
    print('Please make a selection:')
    print('1 - Manage Posts')
    print('2 - Manage Tags')
    print('3 - Manage Pools')
    print('4 - Utilities')
    print('0 - Quit')
    
def main():
    parser = argparse.ArgumentParser(description='Welcome to Szurubooru Manager')
    parser.add_argument('-c', '--config', help='Configuration file', type=Path,
                    default=path.join(ROOT_DIR, 'config/config.json'))
    p = parser.parse_args(sys.argv[1:])
    config = get_config(p)
    print()
    
    selection = -1
    while selection != '0':
        print_menu()
        selection = input('Selection: ')
        print()
        
        if selection == '1':
            pm.manage_posts(config)
        elif selection == '2':
            tm.manage_tags(config)
        elif selection == '3':
            print('not implemented yet')
        elif selection == '4':
            um.manage_utils()
        
main()
    