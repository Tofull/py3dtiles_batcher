#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import argparse
import base64
import glob
import itertools
import os
import pathlib
import shlex
import subprocess
import sys


def command_line():
    parser = argparse.ArgumentParser(
        description='Convert .las file to 3dtiles in batch.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        epilog='''Working example (remove --dryrun when you want to generate tiles) : py3dtiles_batcher.exe "D:\\data_py3dtiles\\output" "D:\\data_py3dtiles\\raw" --dryrun -v''')
    parser.add_argument('--dryrun', help="Active dryrun mode. No tile will be generated in this mode.", action='store_true')
    parser.add_argument('--incremental', help="Active incremental mode. Skip tile if <output_folder>/<tile>/tileset.json exists.", action='store_true')
    parser.add_argument('--srs_in', help="Srs in.", type=int, default=2959)
    parser.add_argument('--srs_out', help="Srs out.", type=int, default=4978)
    parser.add_argument('--cache_size', help="Cache size in MB.", type=int, default=3135)
    parser.add_argument('--docker_image', help="py3dtiles docker image to use.", type=str, default="py3dtiles")
    parser.add_argument('--verbose', '-v', action='count', help="Verbosity (-v simple info, -vv more info, -vvv spawn info)", default=0)
    parser.add_argument('output_folder', help='Directory to save tiles.')
    parser.add_argument('input_folder', nargs="*", default=".", help='Directory to watch.')
    args = parser.parse_args()

    if args.verbose > 2:
        print("Command line args : \n\t{}".format(vars(args)))
    parse_args(**vars(args))


def parse_args(dryrun=None, srs_in=None, srs_out=None, cache_size=None, docker_image=None, verbose=None, output_folder=None, input_folder=None, incremental=None, **kwargs):
    main(input_folder, output_folder, dryrun=dryrun, srs_in=srs_in, srs_out=srs_out, cache_size=cache_size, docker_image=docker_image, verbose=verbose, incremental=incremental, **kwargs)


def get_las(folder_to_watch):
    iterators = []
    for path in folder_to_watch:
        if os.path.exists(path):
            if os.path.isdir(path):
                iterator_to_add = glob.iglob(path + '/**/*.las', recursive=True)
            else:
                iterator_to_add = glob.iglob(path, recursive=True)

        iterators = itertools.chain(iterators, iterator_to_add)

    return iterators


def main(input_folder, output_folder, dryrun=None, srs_in=None, srs_out=None, cache_size=None, docker_image=None, verbose=None, incremental=None, **kwargs):

    liste_las_to_process_iterator = set(get_las(input_folder))
    detected_files = len(liste_las_to_process_iterator)

    folder_tiles_path = pathlib.PurePath(output_folder).as_posix()

    for index, filename in enumerate(liste_las_to_process_iterator):
        path = pathlib.PurePath(os.path.dirname(filename)).as_posix()
        basename = os.path.basename(filename)
        name, extension = os.path.splitext(basename)
        name_base64 = base64.b64encode(name.encode()).decode('utf-8')

        print("\nProcessing file {}/{}".format(index + 1, detected_files))
        if verbose > 1:
            print("File information : \
                \n\t filename : {}\
                \n\t path : {}\
                \n\t basename : {}\
                \n\t name : {}\
                \n\t name (base64): {}\
                \n\t extension : {}\
                \n".format(
                filename,
                path,
                basename,
                name,
                name_base64,
                extension))

        commandline = 'docker run --rm -v {}:/data_in -v {}:/data_out {} py3dtiles --overwrite True --srs_in {} --srs_out {} --out /data_out/{} --cache_size {} \"/data_in/{}\"'.format(
            path,
            folder_tiles_path,
            docker_image,
            srs_in,
            srs_out,
            name_base64,
            cache_size,
            basename)

        must_be_processed = True
        if incremental:
            if os.path.isfile(os.path.join(folder_tiles_path, name_base64, 'tileset.json')):
                must_be_processed = False

        if dryrun:
            print("DryRun : \n{}\n".format(commandline))
            print("Nothing to do in dryRun mode{}".format(" (This file will be skipped because of incremental mode)." if not must_be_processed else '.'))
            print("Done")
            pass
        else:
            if not must_be_processed:
                if verbose > 0:
                    print("Skipped because of incremental mode. File {} already exists".format(os.path.join(folder_tiles_path, name_base64, 'tileset.json')))
                continue
            if verbose > 0:
                print("Executing : \n{}\n".format(commandline))
            args = shlex.split(commandline)
            proc = subprocess.Popen(args, stdout=sys.stdout, stderr=sys.stderr, shell=True)
            proc.communicate()
            proc.wait()
            proc.kill()  # Ensure the process is killed to avoid docker: Error response from daemon: error while creating mount source path '/host_mnt/...': mkdir /host_mnt/...: file exists.
            print("\nDone")
    print("\nFinish")


if __name__ == "__main__":
    command_line()
