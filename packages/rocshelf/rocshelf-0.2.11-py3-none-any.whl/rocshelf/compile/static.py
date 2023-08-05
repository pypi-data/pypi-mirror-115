""" Модуль работы со статикой

"""

from __future__ import annotations
from rocshelf.components.files import GetFileInfo

import typing as _T

import rlogging
import sass
from rcore import sync
from rcore.rpath import rPath
from rocshelf import template
from rocshelf.compile.params import StaticCompilationMetaData
from rocshelf.components import shelves
from rocshelf.components.relations import Relation
from rocshelf.config import pcf
from rocshelf.frontend.chunks import Chunk

logger = rlogging.get_logger('mainLogger')


def static_file_types() -> list[tuple[str, str]]:
    """ Формирует список из под типов каждого файла

    Returns:
        list[tuple[str, str]]: Список

    """

    return [(i, d) for d in ['prep', 'final'] for i in ['style', 'script']]


def cache_folder(subFolder: _T.Optional[str] = None) -> rPath:
    if subFolder is None:
        return rPath('static', fromPath='cache')

    return rPath('static', fromPath='cache').merge(subFolder)


def get_basic_static_file(staticType: str) -> rPath:
    """ Формирование пути до файла с базовой статикой

    Args:
        staticType (str): Тип статики

    Returns:
        rPath: Путь до файла

    """

    userStaticFolder = pcf.path('import', 'static')

    return userStaticFolder.merge('{0}.{1}'.format(
        staticType,
        GetFileInfo.expansion(staticType)
    ))


class CompileStaticCode(object):
    """ Группировка функций для компиляции разных видов кода """

    @staticmethod
    def sass(inputFile: rPath, exportFile: rPath):
        """ Компиляция sass кода

        Args:
            inputFile (rPath): Входной файл
            exportFile (rPath): Результат сохранить в файл

        """

        if not exportFile.check():
            exportFile.create()

        try:
            compiledText = sass.compile(filename=str(inputFile), output_style=pcf.setting('compression'))

        except sass.CompileError as error:
            logger.error('При компиляции sass кода, произошла ошибка: {0}'.format(
                error
            ))
            compiledText = inputFile.read()

        exportFile.write(compiledText, 'w')


class CompileChunkType(sync.process.OnProcessMixin):
    """ Компиляция конкретного файла группы статики """

    relation: Relation
    localizationName: str

    staticType: str
    loadTime: str
    chunk: Chunk

    staticFileName: str

    def __init__(self, localizationName: str, staticType: str, loadTime: str, chunk: Chunk) -> None:
        self.relation = Relation(None, localizationName)
        self.localizationName = localizationName

        self.staticType = staticType
        self.loadTime = loadTime
        self.chunk = chunk

        self.staticFileName = self.relation.static_filename(staticType, loadTime, chunk.shelfSlugs)

    def __compile_file(self, targetFile: rPath) -> str:
        """ Обработка и компиляция файла статики

        Args:
            targetFile (rPath): Исходный файл

        Returns:
            str: Скомпилированный код

        """

        logger.debug('Обработка и компиляция файла статики "{0}"'.format(
            targetFile
        ))

        # None - localizationName
        processingParams = StaticCompilationMetaData.processing_params(
            self.localizationName, self.staticType, self.loadTime, self.chunk, self.staticFileName
        )

        shelfFileNode = template.nodes.FileNode(targetFile)
        processingNode = shelfFileNode.processing(processingParams)
        return processingNode.compile(processingParams)

    def add_comment(self, commentKey: str, *args):
        """ Добавление в файл статики комментария

        Args:
            commentKey (str): Тип комментария
            args (tuple): Доп параметры

        """

        logger.debug('Добавление коментария "{0}" в raw файл статики "{1}"'.format(
            commentKey,
            self.staticFileName
        ))

        cacheFolder = cache_folder('raw')
        staticFile = cacheFolder.merge(self.staticFileName)

        if commentKey == 'welcome':
            textComment = '/* Rocshelf processing static file ({0}): {1} - {2} */\n'.format(
                self.staticFileName,
                self.staticType,
                self.loadTime
            )
            textComment += '/* For routes: {0} */\n'.format(
                ', '.join(self.chunk.routeKeys)
            )
            textComment += '/* On shelves: {0} */\n'.format(
                ', '.join(self.chunk.shelfSlugs)
            )
            if self.chunk.isBase:
                textComment += '/* And base code */\n'
            staticFile.write(textComment, 'w')

        elif commentKey == 'br':
            textComment = '\n\n/* -- {0} -- */\n\n'.format(
                args[0]
            )
            staticFile.write(textComment, 'a')

    def parse_base_code(self):
        """ Чтение основных файлов статики и сохранение в промежуточной папке """

        if not self.chunk.isBase:
            logger.debug('Добавление базовой статики в чанк {0} пропускается: Чанк не должен содержать базовую статику'.format(
                self.chunk
            ))
            return

        basicStaticFile = get_basic_static_file(self.staticType)

        if not basicStaticFile.check():
            logger.warning('Добавление базовой статики в чанк {0} пропускается: Файл базовой статики "{1}" не существует'.format(
                self.chunk,
                basicStaticFile
            ))
            return

        logger.info('Добавление базовой статики в чанк "{0}"'.format(
            self.chunk
        ))

        self.add_comment('br', 'basic code')

        cacheFolder = cache_folder('raw')
        cacheStaticFile = cacheFolder.merge(self.staticFileName)

        cacheStaticFile.write(self.__compile_file(basicStaticFile), 'a')

    def parse_shelves(self):
        """ Чтение файлов статики шелфов и сохранение в промежуточной папке """

        logger.info('Чтение файлов статики шелфов и добавление в файл чанка "{0}"'.format(
            self.chunk
        ))

        cacheStaticFile = cache_folder('raw').merge(self.staticFileName)

        for shelfSlug in self.chunk.shelfSlugs:
            shelf = shelves.GetShelf.slug(shelfSlug)
            shelfStaticFile = shelf.paths.type(self.staticType)

            if shelfStaticFile is None:
                logger.debug('Добавление файла статики "{0}" шелфа "{1}" в чанк "{2}": исходный файл не существует'.format(
                    self.staticType, shelf, self.chunk
                ))
                continue

            logger.debug('Добавление файла статики "{0}" шелфа "{1}" в чанк "{2}": успешно'.format(
                self.staticType, shelf, self.chunk
            ))

            self.add_comment('br', str(shelf))

            cacheStaticFile.write(self.__compile_file(shelfStaticFile), 'a')

    def compile(self):
        fromStaticFile = cache_folder('raw').merge(self.staticFileName)
        targetStaticFile = cache_folder('compiled').merge(self.staticFileName)

        if self.staticType == 'style':
            CompileStaticCode.sass(fromStaticFile, targetStaticFile)

        else:
            fromStaticFile.copy_file(targetStaticFile)

    def filter(self):
        """ Фильтрация импорта

        Добавление параметра ignoreDowload для файлов статики, которые:
        * Не содержат кода

        """

        staticFile = cache_folder('compiled').merge(self.staticFileName)

        noCommentString = template.nodes.FileNode(staticFile).processing().compile().strip()

        if noCommentString == '':
            logger.warning('Файл статики "{0}" чанка {1} с временем загрузки "{2}" пустой'.format(
                self.staticType, self.chunk, self.loadTime
            ))
            staticFile.delete()

    def move(self):
        """ Перемещение скомпилированных группы """

        fromStaticFile = cache_folder('compiled').merge(self.staticFileName)
        targetStaticFile = self.relation.static_path(self.staticFileName)

        # Если новый файл статики не существует, то нужно удалить и тот, который должен скачиваться.
        # Далее в логике, если targetStaticFile, то ссылка на него формироваться не будет.
        if fromStaticFile.check():
            fromStaticFile.copy_file(targetStaticFile)

        else:
            targetStaticFile.delete()

    def on_process(self):
        self.add_comment('welcome')
        self.parse_base_code()
        self.parse_shelves()
        self.compile()
        self.filter()
        self.move()


class CompileChunk(sync.process.OnProcessMixin):
    """ Компиляция группы статики """

    chunk: Chunk
    localizationName: str

    def __init__(self, localizationName: str, chunk: Chunk) -> None:
        super().__init__()
        self.localizationName = localizationName
        self.chunk = chunk

    def on_process(self):
        processesPool = sync.process.NoDeamonProcessesPoolController(CompileChunkType)

        for staticType, loadTime in static_file_types():
            processesPool.add_process(self.localizationName, staticType, loadTime, self.chunk)

        processesPool.map()


def start_compile(localizationName: str, chunks: list[Chunk]):
    """ Компиляция и сохранение статики

    Args:
        localizationName (str): Компилируемая локализация
        chunks (list[Chunk]): Проанализированные группы статики

    """

    if not len(chunks):
        return

    processesPool = sync.process.NoDeamonProcessesPoolController(CompileChunk)

    for chunk in chunks:
        processesPool.add_process(localizationName, chunk)

    processesPool.map()
