# Copyright (C) 2021,2022 Kian-Meng Ang
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Parse source text file into tokens."""

import argparse
import logging
import re
from dataclasses import dataclass, field
from importlib import import_module
from typing import Any, List

logger = logging.getLogger(__name__)


@dataclass
class Tokenizer:
    """Tokenizer class to parse text content."""

    raw_content: str = field(repr=False)
    config: argparse.Namespace = field(repr=False)

    def __init__(self, raw_content: str, config: argparse.Namespace) -> None:
        """Set the constructor for the Tokenizer."""
        self.raw_content = raw_content
        self.config = config

        config_lang = config.language.replace("-", "_")
        self.langconf = import_module(f"txt2ebook.languages.{config_lang}")

    def __getattr__(self, key: str) -> Any:
        """Get a value of the config based on key name.

        Args:
            key(str): The key name of the config.

        Returns:
            Any: The value of a key, if found. Otherwise raise AttributeError
            exception.
        """
        if hasattr(self.config, key):
            return getattr(self.config, key)

        if hasattr(self.langconf, key):
            return getattr(self.langconf, key)

        raise AttributeError(f"invalid config key: '{key}'!")

    def parse(self) -> List:
        """Parse the content into tokens.

        Returns:
          List: The list of tokens.
        """
        # Remove the trailing separator at end of file.
        content = self.raw_content.rstrip(self.paragraph_separator)
        lines = content.split(self.paragraph_separator)
        return [self._tokenize_line(line) for line in lines]

    def _tokenize_line(self, line):
        tokenized_line = (
            self._tokenize_metadata(line)
            or self._tokenize_header(line)
            or self._tokenize_paragraph(line)
            or line
        )
        return tokenized_line

    def _tokenize_metadata(self, line):
        tokens = []
        match = re.search(self.DEFAULT_RE_TITLE, line)
        if match:
            title = match.group(1).strip()
            tokens.append(("TITLE", title))

        match = re.search(rf"\n{self.DEFAULT_RE_AUTHOR}", line)
        if match:
            author = match.group(1).strip()
            tokens.append(("AUTHOR", author))

        return ("METADATA", tokens) if tokens else False

    def _tokenize_header(self, line):
        return (
            self._tokenize_volume_chapter(line)
            or self._tokenize_volume(line)
            or self._tokenize_chapter(line)
        )

    def _tokenize_volume_chapter(self, line):
        token = ()
        regex = rf"^{self.DEFAULT_RE_VOLUME}\s*{self.DEFAULT_RE_CHAPTER}"
        match = re.search(regex, line)
        if match:
            volume = match.group(1).strip()
            chapter = match.group(2).strip()
            token = (
                "VOLUME_CHAPTER",
                [("VOLUME", volume), ("CHAPTER", chapter)],
            )
        return token if token else False

    def _tokenize_volume(self, line):
        token = ()
        regex = rf"^{self.DEFAULT_RE_VOLUME}$"
        match = re.search(regex, line)
        if match:
            volume = match.group(1).strip()
            token = ("VOLUME", volume)

        return token if token else False

    def _tokenize_chapter(self, line):
        token = ()
        regex = rf"^{self.DEFAULT_RE_CHAPTER}$"
        match = re.search(regex, line)
        if match:
            chapter = match.group(1).strip()
            token = ("CHAPTER", chapter)

        return token if token else False

    def _tokenize_paragraph(self, line):
        return ("PARAGRAPH", line)
