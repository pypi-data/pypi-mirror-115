import os

RESULT_PATH_NEWS = r'..\dataset\news'  # 결과 저장할 경로
RESULT_PATH_TWEET = r'..\dataset\tweets'  # 결과 저장할 경로
RESULT_PATH_MODEL = r'..\dataset\models'  # 결과 저장된 경로


class path:
    def __init__(self, directory):
        self.directory = directory

    def createFolder(self):
        try:
            if not os.path.exists(self.directory):
                os.makedirs(self.directory)
                return True
        except OSError:
            print('Error: Creating directory. ' + self.directory)
            return False

    def getFolderList(self):
        self.fileList = os.listdir(self.directory)
        return self.fileList


def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
            return True
    except OSError:
        print('Error: Creating directory. ' + directory)
        return False


def getFolderList(directory):
    fileList = os.listdir(directory)
    return fileList
