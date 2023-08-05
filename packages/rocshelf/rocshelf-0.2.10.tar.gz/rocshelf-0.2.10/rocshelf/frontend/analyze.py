from __future__ import annotations

import typing as _T

from rocshelf.frontend.chunks import Chunk, MergeChunks


class StaticAnalyze(object):
    """ Анализ статики. Разбиение на чанки """

    routesKeys: _T.KeysView[str]
    staticData: dict[str, _T.Any]

    chunks: list[Chunk]

    def __init__(self, staticData: dict[str, _T.Any]) -> None:
        super().__init__()

        self.routesKeys = staticData['shelves'].keys()
        self.staticData = staticData
        self.chunks = []

    def add_base_static(self):
        """ Добавление групп с базывыми статик файлами """

        for routeKey in self.routesKeys:
            self.chunks.append(
                Chunk([routeKey], None, True)
            )

    def add_shelves(self):
        """ Добавление шелфов в группы """

        for routeKey in self.routesKeys:
            for shelfName in self.staticData['shelves'][routeKey]:
                self.chunks.append(
                    Chunk([routeKey], [shelfName], False)
                )

    def sort(self):
        """ Сортировка шелфов

        Статика в файлах сортируется по причастности к шелфу:
        `Tag` -> `Block` -> `Page` -> `Wrapper` - где Tag будет в начале файла, а Wrapper в конце

        """

        countTable = {
            'tag': 4,
            'block': 3,
            'page': 2,
            'wrapper': 1
        }

        def __sort(value: str):
            shelfType = value.split('/')[0]
            return countTable[shelfType]

        for chunk in self.chunks:
            shelfSlugsList = list(chunk.shelfSlugs)
            shelfSlugsList.sort(key=__sort)
            chunk.shelfSlugs = shelfSlugsList

    @classmethod
    def all_stages(cls, staticData: dict[str, _T.Any]) -> StaticAnalyze:
        analyzeObject = cls(staticData)

        analyzeObject.add_base_static()
        analyzeObject.add_shelves()

        analyzeObject.chunks = MergeChunks.merge_chunks(analyzeObject.chunks)

        analyzeObject.sort()

        return analyzeObject
