"""
Hard link items in dir A to dir B, with history cached.
"""
import os, shutil
import re
import json
import argparse
import logging

parser = argparse.ArgumentParser(description='Hard link files to another dir')
parser.add_argument('-i', '--input-path', metavar='input_path', dest='input_path', type=str, required=True, help='File or Folder which to be hardlinked')
parser.add_argument('-o', '--output-path', metavar='output_path', dest='output_path', type=str, required=True, help='Directory as hardlink destination')
parser.add_argument('-s', '--single-dir', dest='single_dir', action='store_true', help= 'Optional. Indicates whether to search for all the items inside the input directory' )
parser.add_argument('-c', '--clear-log', dest='clear_log', action='store_true', help= 'Optional. less ouput log message' )
ARGS = parser.parse_args()

ARGS.input_path = os.path.expanduser(ARGS.input_path)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '\n%(asctime)s - Module: %(module)s - Line: %(lineno)d - Message: %(message)s'
)
file_handler = logging.FileHandler('file_dup.log', encoding='utf8')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


class HistoryManager:
    def __init__(self):
        self.search_history_file_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'DupHistory.json')

    def open_history(self):
        try:
            with open(self.search_history_file_path, 'r',
                      encoding='utf8') as f:
                self.search_history = json.load(f)
            self.history_json_fd = open(self.search_history_file_path,
                                        'r+',
                                        encoding='utf8')
            return True
        except:
            self.search_history = {'path_dupped': [], 'basename': []}
            self.history_json_fd = open(self.search_history_file_path,
                                        'w',
                                        encoding='utf8')
            json.dump(self.search_history, self.history_json_fd, indent=4)
            # self.history_json_fd.close()
            return False

    def is_file_previously_dupped(self, file_path):
        for name in self.search_history['path_dupped']:
            if file_path == name:
                return True
        return False

    def append_to_dup_history(self, file_path):
        # append file_path to history
        if file_path not in self.search_history['path_dupped']:
            self.search_history['path_dupped'].append(file_path)

        json.dump(self.search_history, self.history_json_fd, indent=4)
        self.history_json_fd.seek(0)

    def close_history(self):
        self.history_json_fd.close()


def ensureDir(file_path):
    if os.path.isfile(file_path):
        file_path = os.path.dirname(file_path)
    if not os.path.exists(file_path):
        os.makedirs(file_path)


def hdlinkCopy(fromLoc, toDir):
    destDir = toDir
    ensureDir(destDir)
    if os.path.isfile(fromLoc):
        destFile = os.path.join(destDir, os.path.basename(fromLoc))
        if not os.path.exists(destFile):
            # print('ln ', fromLoc, destFile)
            os.link(fromLoc, destFile)
        else:
            print('\033[36mExisted: %s =>  %s \033[0m' % (fromLoc, destFile))
    else:
        destDir = os.path.join(destDir, os.path.basename(fromLoc))
        if not os.path.exists(destDir):
            # print('copytree ', fromLoc, destDir)
            shutil.copytree(fromLoc, destDir, copy_function=os.link)
        else:
            print('\033[36mExisted: %s =>  %s \033[0m' % (fromLoc, destDir))


def hdlinkLs(loc):
    destDir = os.path.join(ARGS.output_path, loc)
    ensureDir(destDir)
    return os.listdir(destDir)


def assert_settings():
    assert os.path.exists(
        ARGS.input_path), f'"{ARGS.input_path}" does not exist'
    # assert os.path.isdir(ARGS.output_path), f'"{ARGS.output_path}" directory does not exist'


def get_all_paths():
    paths = [ os.path.normpath(ARGS.input_path)] if ARGS.single_dir \
        else [os.path.join(ARGS.input_path, f) for f in os.listdir(ARGS.input_path) ]

    if os.name == 'nt':
        for i, _ in enumerate(paths):
            if os.path.isabs(paths[i]) and not paths[i].startswith('\\\\?\\'):
                paths[i] = '\\\\?\\' + paths[i]

    return paths


def main():
    assert_settings()

    hisman = HistoryManager()
    hisman.open_history()

    paths = get_all_paths()
    for i, path in enumerate(paths):
        search_name = os.path.basename(path)
        # search_name = path
        if hisman.is_file_previously_dupped(search_name):
            s = '\033[32mSkipping. File previously linked: %s \033[0m' % (
                search_name)
            if not ARGS.clear_log:
                print(s)
            logger.info(slice)
            continue
        info = 'Hardlink %d of %d : %s ' % (i + 1, len(paths),
                                                           search_name)
        print(info)
        logger.info(info)
        hisman.append_to_dup_history(search_name)

        hdlinkCopy(path, ARGS.output_path)

    hisman.close_history()


if __name__ == '__main__':
    main()
