from os import path
from os import walk
import sys

'''
    封装路径方法类
'''

class Path(object):

    # 获取当前文件路径
    def getCurrentFilePath(self):
        return sys.argv[0]

    # 获取当前文件所在文件夹路径
    def getCurrentDirPath(self):
        return path.dirname(sys.argv[0])

    # 获取传入文件/文件夹所在的文件夹路径（上一级文件夹路径）
    def getDirPath(self, file_path):
        return path.dirname(file_path)

    # 查找指定文件夹下，指定文件的路径，未找到返回None
    def getFilePathByName(self, dir_path, file_name):
        for root, dirs, files in walk(dir_path):
            for file in files:
                if file == file_name:
                    return path.join(root, file)
            for dir in dirs:
                self.getFilePathByName(path.join(root, dir), file_name)
        return None

    # 查找指定文件夹下，指定文件夹的路径，未找到返回None
    def getDirPathByName(self, dir_path, dir_name):
        for root, dirs, files in walk(dir_path):
            for dir in dirs:
                if dir == dir_name:
                    return path.join(root, dir)
                else:
                    self.getDirPathByName(path.join(root, dir), dir_name)
        return None




if __name__=='__main__':
    a = Path()
    b = a.getCurrentDirPath()
    c = a.getDirPath(b)
    print(c)
    d = a.getDirPathByName(c, 'test_dir')
    print(d)
    print(a.getFilePathByName(d, 'conf.ini'))