#!/usr/bin/env python3

from datetime import datetime
import toml
import argparse
import os
from os import system
from os.path import exists, expanduser, join
import sys

def createDirIfNotExists(path):
    if os.path.exists(str(path)) == False:
        os.mkdir(str(path))
    else:
        pass

def createFileIfNotExists(path):
    if os.path.exists(str(path)) == False:
        with open(str(path), "x") as y:
            pass
    else:
        pass

def response(question):
    answer = input('[?] {}: [y/n] '.format(question))
    if not answer or answer[0].lower() != 'y':
        return False
    return True


def main():
    createDirIfNotExists(join(expanduser("~"), ".config"))
    if not exists(join(expanduser("~"), ".config", "journalwriter.toml")):
        createFileIfNotExists(join(expanduser("~"), ".config", "journalwriter.toml"))
        new_config_dict = {"directory": join(expanduser("~"), "journalwriter")}
        if sys.platform == "win32":
            new_config_dict["editor"] = "notepad"
        else:
            new_config_dict["editor"] = "nano"
        with open(join(expanduser("~"), ".config", "journalwriter.toml"), "w") as f:
            toml.dump(new_config_dict, f)

    config = toml.load(join(expanduser("~"), ".config", "journalwriter.toml"))
    try:
        datadir = config["directory"]
    except:
        datadir = join(expanduser("~"), "journalwriter")

    parser = argparse.ArgumentParser()
    parser.add_argument('task', help='Task to do', type=str, choices=['write', 'view'])
    parser.add_argument('name', help='The name of the journal', type=str)

    args = parser.parse_args()
    name = args.name

    journal_path = os.path.join(datadir, name)
    if not os.path.exists(journal_path):
        print('[!] The journal {} does not exist!'.format(name))
        res = response('Do you want to create journal {}'.format(name))
        if res:
            os.makedirs(journal_path)
        else:
            sys.exit()

    if args.task=='write':
        date = datetime.now()
        filename = date.strftime('%Y-%m-%d-%a') + '.md'
        curdir = os.path.join(datadir, name, date.strftime('%Y'), date.strftime('%m'))
        if not os.path.exists(curdir):
            os.makedirs(curdir)

        filepath = os.path.join(curdir, filename)
        try:
            editor_defined = config["editor"]
        except:
            if sys.platform == "win32":
                editor_defined = "notepad"
            else:
                editor_defined = "nano"
        system(str(editor_defined)+" "+filepath)
    else:
        print("Coming soon...")


if __name__=='__main__':
    main()