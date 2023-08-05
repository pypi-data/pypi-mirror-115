import os
import json
from glob import glob
from shutil import rmtree
from typing import Union

from .base import BaseStylingLayerCache
from ...configs import StylingLayerConfig
from ..util import create_dir_name_from_config, create_file_name_from_path
from py_pdf_term.stylings import PDFStylingScoreList


class StylingLayerFileCache(BaseStylingLayerCache):
    def __init__(self, cache_dir: str) -> None:
        super().__init__(cache_dir)
        self._cache_dir = cache_dir

    def load(
        self, pdf_path: str, config: StylingLayerConfig
    ) -> Union[PDFStylingScoreList, None]:
        dir_name = create_dir_name_from_config(config)
        file_name = create_file_name_from_path(pdf_path, "json")
        cache_file_path = os.path.join(self._cache_dir, dir_name, file_name)

        if not os.path.isfile(cache_file_path):
            return None

        with open(cache_file_path, "r") as json_file:
            try:
                obj = json.load(json_file)
            except json.JSONDecodeError:
                return None

        return PDFStylingScoreList.from_dict(obj)

    def store(
        self, styling_scores: PDFStylingScoreList, config: StylingLayerConfig
    ) -> None:
        dir_name = create_dir_name_from_config(config)
        file_name = create_file_name_from_path(styling_scores.pdf_path, "json")
        cache_file_path = os.path.join(self._cache_dir, dir_name, file_name)

        os.makedirs(os.path.dirname(cache_file_path), exist_ok=True)

        with open(cache_file_path, "w") as json_file:
            json.dump(styling_scores.to_dict(), json_file, ensure_ascii=False, indent=2)

    def remove(self, pdf_path: str, config: StylingLayerConfig) -> None:
        dir_name = create_dir_name_from_config(config)
        file_name = create_file_name_from_path(pdf_path, "json")
        cache_dir_path = os.path.join(self._cache_dir, dir_name)
        cache_file_path = os.path.join(cache_dir_path, file_name)

        if not os.path.isfile(cache_file_path):
            return

        os.remove(cache_file_path)

        cache_file_paths = glob(os.path.join(cache_dir_path, "*.json"))
        if not cache_file_paths:
            rmtree(cache_dir_path)
