import os
import argparse
from .dedup_utils import filter_images


def exc(_method, _root):
    filter_images(_method, _root)


def main():
    parser = argparse.ArgumentParser(description='dedup-img tools', prog='dedup')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-P', action='store_const', const='PHash', help='dedup by PHash')
    group.add_argument('-A', action='store_const', const='AHash', help='dedup by AHash')
    group.add_argument('-D', action='store_const', const='DHash', help='dedup by DHash')
    group.add_argument('-W', action='store_const', const='WHash', help='dedup by WHash')
    parser.add_argument('-d', '--directory', metavar='directory', action='store', required=True, help='images folder')
    args = parser.parse_args()

    if args.P:
        method = args.P
    elif args.A:
        method = args.A
    elif args.D:
        method = args.D
    else:
        method = args.W
    root = args.directory

    if not os.path.exists(root):
        print('image dir is not exist')
    elif not os.path.isdir(root):
        print('the input image dir is not a dir')
    else:
        exc(method, root)
