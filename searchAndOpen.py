# -*- coding: utf-8 -*-
"""
@author: Skibbe.N
"""
import mmap
import sys
import re
import time
import os
import subprocess


def defInput():
    if sys.version_info[:2] < (3, 0):
        return getattr(__builtins__, 'raw_input')
    else:
        return getattr(__builtins__, 'input')


def searchFileForString(filename, string):
    if sys.version_info[:2] < (3, 0):  # python version < 3.0
        try:
            with open(filename, 'r', 0) as infile:
                s = mmap.mmap(infile.fileno(), 0, access=mmap.ACCESS_READ)
                if re.search(r'{}'.format(string), s):
                    return filename
        except ValueError:
            return None

    else:  # python version > 3.0
        try:
            with open(filename, 'rb', 0) as infile, \
                    mmap.mmap(infile.fileno(),
                              0, access=mmap.ACCESS_READ) as s:
                if re.search(br'%b' % (string.encode()), s):
                    return filename
        except ValueError:
            return None


def open_algorithm(found, programm):
    _input = defInput()  # py 2/3 hack
    yn = _input('open files? [y/n] to open [all/none]\n'
                'alternatively enter [number] to open specific file\n')
    if yn == 'y':
        if len(found) > 3:
            if not _input('Really sure to open {} files [y/n]\n'
                          .format(len(found))) == 'y':
                return

        call = [r'{}'.format(programm)]
        for script in found:
            if script != __file__:
                call.append(r'{}'.format(script))
        subprocess.call(call)

    elif yn == 'n':
        pass

    else:
        try:
            index = int(yn)
            print('opening "{}"'.format(found[index]))
            subprocess.call([r'{}'.format(programm),
                             r'{}'.format(found[index])])
        except (ValueError, IndexError):
            print('"{}" is not a valid index.'.format(yn))

        open_algorithm(found, programm)


def searchDirectoryForString(directory, string, extension='.py'):
    t = time.time()
    searched = 0
    found_in = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                found = searchFileForString(os.path.join(root, file), string)
                if found is not None:
                    if not found[0].endswith('searchAndOpen.py'):
                        found_in.append(found)
                searched += 1
    print('Searched {} files for "{}", found {} matches in {:2.2f} seconds.'
          .format(searched, string, len(found_in), time.time() - t))
    return found_in


def findAndOpen(directory, string, extension='.py', open_with='spyder'):
    found = searchDirectoryForString(directory, string, extension=extension)

    for i, script in enumerate(found):
        print('({}) {}'.format(i, script))

    if len(found) == 0:
        return
    open_algorithm(found, open_with)


def main():
#    findAndOpen('/home61/skibbe/comet', 'config', open_with='spyder')
    findAndOpen('/home61/skibbe/custEM/samples', 'solve_main_problem',
                open_with='spyder3')
    # findAndOpen('C://', 'shuffle')  # > 10 min
#    findAndOpen('C://Skibbe.N/src/empymod_src_testing', 'bipole', open_with='C:/Software/WinPython-64bit-3.6.1.0Qt5/spyder.exe')

if __name__ == '__main__':
    main()
# The End
