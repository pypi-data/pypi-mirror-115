import logging

class Log(object):
    def __init__(self,filename=None, level='WARNING', format='%(asctime)s - %(levelname)s - %(funcName)s - %(lineno)d - %(message)s'):
        if level == 'debug':
            level = logging.DEBUG
        elif level == 'info':
            level = logging.INFO
        elif level == 'warning':
            level = logging.WARNING
        elif level == 'error':
            level = logging.ERROR
        elif level == 'critical':
            level = logging.CRITICAL
        else:
            level = logging.WARNING
        self.logger = logging.getLogger("")
        self.logger.setLevel(level)
        if filename is not None:
            fh = logging.FileHandler(filename, 'a', encoding='utf-8')
            fh.setLevel(level)
            fh.setFormatter(logging.Formatter(format))
            self.logger.addHandler(fh)
            fh.close()

        sh = logging.StreamHandler()
        sh.setLevel(level)
        sh.setFormatter(logging.Formatter(format))
        self.logger.addHandler(sh)
        sh.close()

    def getLogger(self):
        return self.logger


if __name__ == '__main__':
    a = Log(level='info').getLogger()
    a.info('123456789')