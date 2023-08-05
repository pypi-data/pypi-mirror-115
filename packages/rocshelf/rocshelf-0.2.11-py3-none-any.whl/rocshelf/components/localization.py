""" Модуль для поддержки локализации при компиляции

Файл конфигурации локализации.
  Настраивает паттерн для файлов локализации, тип данных в этих файлах (json, yaml)

"""

import os
import re
import typing as _T
from glob import glob

import rlogging
import yaml
from rcore.rpath import rPath
from rocshelf.config import pcf

logger = rlogging.get_logger('mainLogger')

localFileDefaultExtension = '.lang'

re_local_name = re.compile(r'^[\w\_\-\.]*$')
re_local_field = re.compile(r'^[^{}\(\)\[\]]*$')


class LocalizationData(object):
    """ Интерфейс для работы с инициализированными данными модуля """

    inited: bool
    localizationData: dict
    defaultLocalizationName: str

    def __init__(self):
        self.inited = False
        self.localizationData = {}
        self.defaultLocalizationName = '_'

    def init(self, localizationData: _T.Optional[dict] = None, defaultLocalizationName: _T.Optional[str] = None):
        self.inited = True

        self.localizationData = {
            '_': {}
        }
        if localizationData:
            self.localizationData = localizationData

        self.defaultLocalizationName = '_'
        if defaultLocalizationName:
            self.defaultLocalizationName = defaultLocalizationName


class localDataization(LocalizationData):
    """ Выборка локализации """

    def check_params(self, localizationName: _T.Optional[str] = None, stringKey: _T.Optional[str] = None):
        if localizationName is not None and localizationName not in self.localizationData:
            raise KeyError('Локализация "{0}" не зарегистрирована'.format(
                localizationName
            ))

        if stringKey is not None and stringKey not in self.localizationData[localizationName]:
            raise KeyError('Ключа {0} в локализации "{1}" нет'.format(
                stringKey,
                localizationName
            ))

    def value(self, localizationName: str, stringKey: str):
        """ Выборка строки локализации

        Args:
            localizationName (str): Имя локализации
            stringKey (str): Ключ строки

        Returns:
            str: Значение по ключу

        """

        self.check_params(localizationName, stringKey)

        return self.localizationData[localizationName][stringKey]

    def all(self) -> dict[str, dict[str, str]]:
        """ Выборка всех локализаций """

        if self.localizationData:
            return self.localizationData

        return {
            '_': {}
        }

    def walk(self) -> _T.Generator[tuple[str, dict[str, str]], None, None]:
        """ Выборка всех локализаций """

        if self.localizationData:
            for localizationName, localizationFields in self.localizationData.items():
                yield (localizationName, localizationFields)

        else:
            yield ('_', {})

    def list(self) -> list[str]:
        """ Выборка всех локализаций """

        if self.localizationData:
            return list(self.localizationData.keys())

        return ['_']


localData = localDataization()


def check_valid_local_name(key: str):
    """ Проверка валидности ключа в файле локализации """

    if re_local_name.match(key) is None:
        raise ValueError('"{0}" - novalid localization name'.format(
            key
        ))


def check_valid_local_field(key: str):
    """ Проверка валидности ключа в файле локализации """

    if re_local_field.match(key) is None:
        raise ValueError('"{0}" - novalid field in localization'.format(
            key
        ))


class InitComponentCore(object):
    """ Класс с основными функциями для инициализации компонента локализации """

    localizationData: dict[str, dict[str, str]]
    localFieldsStatistics: dict[str, list]
    defaultLocalizationName: str

    def __init__(self) -> None:
        logger.info('Инициализация класса инициализации компонента локализации')

        self.localizationData = {}
        self.localFieldsStatistics = {}

    def save_localization_data(self, localizationName: str, localizationData: dict[str, str]):
        """ Сохранение результата парсинга парсинга файла локализации

        Args:
            localizationName (str): Имя локализации
            localizationData (dict[str, str]): Поля локализации

        """

        logger.debug('Сохранение результата парсинга парсинга файла локализации "{0}" : {1}'.format(
            localizationName, list(localizationData.keys())
        ))

        if localizationName not in self.localizationData:
            self.localizationData[localizationName] = {}

        self.localizationData[localizationName].update(localizationData)

        for localizationField in localizationData:
            if localizationField not in self.localFieldsStatistics:
                self.localFieldsStatistics[localizationField] = []

            self.localFieldsStatistics[localizationField].append(localizationName)

    def parse_file(self, localizationFile: str):
        """ Парсинг файла локализации

        Args:
            localizationFile (str): Файл локализации

        Raises:
            TypeError: Файл локализации хранит данные не в формате словаря

        """

        _, localizationName = os.path.split(os.path.splitext(localizationFile)[0])

        logger.debug('Парсинг значений локализации "{0}" из файла "{1}"'.format(
            localizationName,
            localizationFile
        ))

        with open(localizationFile, 'r') as localYaml:
            localizationData = yaml.safe_load(localYaml)

        if not isinstance(localizationData, dict):
            raise TypeError('Файл локализации "{0}" должен хранить данные в виде словара'.format(
                localizationFile
            ))

        self.save_localization_data(localizationName, localizationData)

    def parse_folder(self, folderPath: rPath):
        """ Парсинг папки с локализацией

        Args:
            folderPath (rPath): Папка с локализациями

        """

        logger.info('Поиск файлов локализации в папка "{0}"'.format(
            folderPath
        ))

        globFiles = glob('{0}/*{1}'.format(
            folderPath, localFileDefaultExtension
        ))

        for localizationFile in globFiles:
            self.parse_file(localizationFile)

    def default_localization(self):
        """ Определение локализации по умолчанию """

        self.defaultLocalizationName = '_'

        defaultLocalizationLen = 0
        for localizationName, localizationData in self.localizationData.items():
            logger.error(localizationName)
            if defaultLocalizationLen < len(localizationData):
                self.defaultLocalizationName = localizationName
                defaultLocalizationLen = len(localizationData)

        logger.info('Локализация по умолчанию - "{0}"'.format(
            self.defaultLocalizationName
        ))


class InitComponent(InitComponentCore):
    """ Класс инициализации компонента локализации """

    def parse(self):
        """ Сборка локализации """

        localPath = pcf.path('import', 'localization')

        if localPath.check():
            self.parse_folder(localPath)

        self.default_localization()

    def normalize(self):
        """ Дополнение неполных локализаций полями из локализации по умолчанию.

        Raises:
            ValueError: В локализации по умолчанию нет какого-то поля.

        """

        logger.info('Нормализация собраных данных локализации')

        localizationNames = set(self.localizationData.keys())

        for localizationField, nLocalizationNames in self.localFieldsStatistics.items():
            deffLocalizationNames = localizationNames - set(nLocalizationNames)

            if deffLocalizationNames:
                if self.defaultLocalizationName in deffLocalizationNames:
                    raise ValueError('В локализации по умолчанию "{0}" не найдено поле "{1}"'.format(
                        self.defaultLocalizationName,
                        localizationField
                    ))

                logger.warning('У локализаций "{0}" нет поля {1}. Он будет взят из локализации по умолчанию'.format(
                    deffLocalizationNames, localizationField
                ))

                for localizationName in deffLocalizationNames:
                    self.localizationData[localizationName][localizationField] = \
                        self.localizationData[self.defaultLocalizationName][localizationField]

    def check(self):
        """ Проверка валидности варианта локализации, основываясь на других вариантах """

        for localizationName, localizationData in self.localizationData.items():
            check_valid_local_name(localizationName)
            for localizationField in localizationData:
                check_valid_local_field(localizationField)

    @classmethod
    def all_stages(cls):
        initObject = cls()

        initObject.parse()
        initObject.check()
        initObject.normalize()

        logger.info('Инициализованы следующие варианты локализации: [{0}]'.format(
            {', '.join(initObject.localizationData.keys())}
        ))
        logger.info('В которых {0} полей локализации'.format(
            len(initObject.localFieldsStatistics)
        ))

        localData.init(initObject.localizationData, initObject.defaultLocalizationName)
