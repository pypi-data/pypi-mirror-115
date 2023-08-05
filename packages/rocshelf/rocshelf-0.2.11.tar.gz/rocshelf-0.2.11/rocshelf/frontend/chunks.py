""" Модуль разделения фронтенда на чанки

"""


from __future__ import annotations

import typing as _T

import rlogging

logger = rlogging.get_logger('mainLogger')


class Chunk(object):
    """ Группа статики для группы страниц """

    __slots__ = ('routeKeys', 'shelfSlugs', 'isBase')

    routeKeys: list[str]
    shelfSlugs: list[str]
    isBase: bool

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return '<Chunk isBase:{0} {1}:{2}>'.format(
            self.isBase,
            self.routeKeys,
            self.shelfSlugs
        )

    def __init__(self,
                 routeKeys: _T.Optional[_T.Iterable[str]] = None,
                 shelfSlugs: _T.Optional[_T.Iterable[str]] = None,
                 isBase: bool = False
                 ) -> None:

        self.routeKeys = [] if routeKeys is None else list(routeKeys)
        self.shelfSlugs = [] if shelfSlugs is None else list(shelfSlugs)

        self.isBase = isBase


class MergeChunks(object):

    chunks: list[Chunk]

    def __init__(self, chunks: list[Chunk]) -> None:
        self.chunks = chunks

    def __no_duplicates(self, items: list[str]) -> list[str]:
        return list(set(items))

    def __merge_chunks_iterable(self, targetChunk: Chunk, callback: _T.Callable[[Chunk], None]) -> bool:
        if targetChunk.shelfSlugs is None or targetChunk.routeKeys is None:
            return False

        for subChunk in self.chunks:
            if id(targetChunk) == id(subChunk):
                continue

            callback(targetChunk, subChunk)

        return targetChunk

    def __merge_chunks_by_static(self, targetChunk: Chunk, subChunk: Chunk):
        if targetChunk.shelfSlugs == subChunk.shelfSlugs and targetChunk.isBase == subChunk.isBase:
            targetChunk.routeKeys += subChunk.routeKeys
            targetChunk.routeKeys = self.__no_duplicates(targetChunk.routeKeys)
            subChunk.shelfSlugs = None

    def __merge_chunks_by_routes(self, targetChunk: Chunk, subChunk: Chunk):
        if targetChunk.routeKeys == subChunk.routeKeys:
            targetChunk.shelfSlugs += subChunk.shelfSlugs
            targetChunk.shelfSlugs = self.__no_duplicates(targetChunk.shelfSlugs)
            if targetChunk.isBase or subChunk.isBase:
                targetChunk.isBase = True
            subChunk.routeKeys = None

    def merge_chunks_loop(self):
        """ Слияние групп

        В приоритете уменьшение до 0 скачивания ненужных файлов

        """

        while True:
            lastLen = len(self.chunks)

            self.chunks = list(filter(
                lambda x: x,

                map(
                    lambda x: self.__merge_chunks_iterable(x, self.__merge_chunks_by_static),
                    self.chunks
                )
            ))

            self.chunks = list(filter(
                lambda x: x,

                map(
                    lambda x: self.__merge_chunks_iterable(x, self.__merge_chunks_by_routes),
                    self.chunks
                )
            ))

            if len(self.chunks) == lastLen:
                break

    @classmethod
    def merge_chunks(cls, chunks: list[Chunk]) -> list[Chunk]:
        mergeChunksObject = cls(chunks)
        mergeChunksObject.merge_chunks_loop()
        return mergeChunksObject.chunks
