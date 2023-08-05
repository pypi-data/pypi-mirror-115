from setuptools import setup, find_packages

setup(
    name             = 'OsEasyControl',
    version          = '1.0',
    description      = 'Easy to use cmd in py',
    author           = '자색치즈고구마',
    author_email     = 's.potato0530@gmail.com',
    url              = 'https://github.com/sweetpotato0530/OsEasyControl-Python-',
    install_requires = [ ],
    packages         = find_packages(exclude = ['docs', 'tests*']),
    keywords         = ['OsEasyControl'],
    python_requires  = '>=3',
    package_data     =  {
        'pyquibase' : [
            'db-connectors/sqlite-jdbc-3.18.0.jar',
            'db-connectors/mysql-connector-java-5.1.42-bin.jar',
            'liquibase/liquibase.jar'
    ]},
    zip_safe=False,
    classifiers      = [
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ]
)