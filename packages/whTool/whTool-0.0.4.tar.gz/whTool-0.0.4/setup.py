from setuptools import setup, find_packages

setup(
    name = 'whTool',
    version = '0.0.4',
    keywords='wh',
    description = 'a library for wh Developer',
    license = 'MIT License',
    url = 'https://gitlab.enncloud.cn/wenhaoc/whTool.git',
    author = 'wenhaoc',
    author_email = 'wenhaoc@enn.cn',
    packages = find_packages(),
    include_package_data = True,
    platforms = 'any',
    install_requires = [
        'python-dateutil',
        'requests',
        'pymysql',
        ],
)