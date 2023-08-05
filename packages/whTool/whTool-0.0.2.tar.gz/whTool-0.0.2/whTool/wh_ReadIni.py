import configparser


class ReadIni(object):
    def __init__(self, ini_file_path):
        self.cf = configparser.RawConfigParser()
        self.cf.read(ini_file_path, encoding='utf-8')

    # 获取ini文件下的所有section，list返回，若无返回[]
    def getSections(self):
        return self.cf.sections()

    # 获取ini文件下，指定section的所有options，list返回，若无返回[]，若section不存在，返回None
    def getOptionsBySection(self, section):
        if self.cf.has_section(section):
            return self.cf.options(section)
        else:
            return None

    # 获取ini文件下，指定section的指定option的值value，返回字符串，若section/option不存在，则返回None
    def getValue(self, section, option):
        if self.cf.has_option(section, option):
            return self.cf.get(section, option)
        else:
            return None

    # 获取ini文件下，指定section的所有items（options与values的键值对，元组形式），list返回[(option1, value1), (option2, value2)]，若无返回[]，若section不存在，返回None
    def getItemsBySection(self, section):
        if self.cf.has_section(section):
            return self.cf.items(section)
        else:
            return None