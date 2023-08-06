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

"""Parse source text file into a book model."""

import argparse
import logging
from dataclasses import dataclass, field
from importlib import import_module
from typing import Any, List, Tuple, Union

import cjkwrap
import regex as re

from txt2ebook.models import Book, Chapter, Volume
from txt2ebook.tokenizer import Tokenizer

logger = logging.getLogger(__name__)


@dataclass
class Parser:
    """Parser class to massage and parse a text content."""

    raw_content: str = field()
    config: argparse.Namespace = field()

    def __init__(self, raw_content: str, config: argparse.Namespace) -> None:
        """Set the constructor for the Parser."""
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

        raise AttributeError(key)

    def parse(self) -> Book:
        """Parse the content into volumes (optional) and chapters.

        Returns:
          txt2ebook.models.Book: The Book model
        """
        massaged_content = self.massage()
        tokens = Tokenizer(massaged_content, self.config).parse()

        (book_title, authors, toc) = self.parse_tokens(tokens)

        return Book(
            title=book_title,
            language=self.language,
            authors=authors,
            cover=self.cover,
            raw_content=self.raw_content,
            massaged_content=massaged_content,
            toc=toc,
            structure_names=self.STRUCTURE_NAMES,
        )

    def parse_tokens(self, tokens: List) -> Tuple:
        """Parse the tokens and organize into book structure."""
        toc: List[Union[Volume, Chapter]] = []
        book_title = ""
        authors = []
        current_volume = Volume("")
        current_chapter = Chapter("")

        for (lineno, (token_type, token_value)) in enumerate(tokens):
            logger.debug(
                "%s %s %s", lineno, token_type, repr(token_value[0:10])
            )

            if token_type == "METADATA":
                [(_type, book_title), (_type, author)] = token_value
                authors.append(author)

            if token_type == "VOLUME_CHAPTER":
                [(_type, volume_title), (_type, chapter_title)] = token_value

                if current_volume.title != volume_title:
                    current_volume = Volume(title=volume_title)
                    toc.append(current_volume)

                if current_chapter.title != chapter_title:
                    current_chapter = Chapter(title=chapter_title)
                    if isinstance(toc[-1], Volume):
                        toc[-1].add_chapter(current_chapter)

            if token_type == "VOLUME":
                if current_volume.title != token_value:
                    current_volume = Volume(title=token_value)
                    toc.append(current_volume)

            if token_type == "CHAPTER":
                if current_chapter.title != token_value:
                    current_chapter = Chapter(title=token_value)

                    if toc and isinstance(toc[-1], Volume):
                        toc[-1].add_chapter(current_chapter)
                    else:
                        toc.append(current_chapter)

            if token_type == "PARAGRAPH":
                if toc and isinstance(toc[-1], Volume):
                    toc[-1].chapters[-1].add_paragraph(token_value)

                if toc and isinstance(toc[-1], Chapter):
                    toc[-1].add_paragraph(token_value)

        if book_title == "":
            logger.info("No book title found from file!")

        total_volume = sum(1 for s in toc if isinstance(s, Volume))
        total_chapter = sum(1 for s in toc if isinstance(s, Chapter))

        logger.info("Found volumes: %s", total_volume)
        logger.info("Found chapters: %s", total_chapter)

        # Use authors if set explicitly from command line.
        if self.config.author:
            authors = self.config.author

        if self.config.title:
            book_title = self.config.title

        return (book_title, authors, toc)

    def massage(self) -> str:
        """Massage the txt content.

        Returns:
          str: The book in parsed string
        """
        content = self.raw_content

        content = Parser.to_unix_newline(content)

        if self.re_delete:
            content = self.do_delete_regex(content)

        if self.re_replace:
            content = self.do_replace_regex(content)

        if self.re_delete_line:
            content = self.do_delete_line_regex(content)

        if self.width:
            content = self.do_wrapping(content)

        return content

    def get_regex(self, metadata: str) -> Union[List, str]:
        """Get the regex by the book metadata we want to parse and extract.

        Args:
          metadata(str): The type of the regex for each parser by language.

        Returns:
          str | list: The regex or list of regexs of the type.
        """
        regexs = getattr(self, f"re_{metadata}")
        if regexs:
            return regexs if metadata == "replace" else "|".join(regexs)

        return getattr(self, f"DEFAULT_RE_{metadata.upper()}")

    @staticmethod
    def to_unix_newline(content: str) -> str:
        """Convert all other line ends to Unix line end.

        Args:
          content(str): The book content

        Returns:
          str: The formatted book content
        """
        return content.replace("\r\n", "\n").replace("\r", "\n")

    def do_delete_regex(self, content: str) -> str:
        """Remove words/phrases based on regex.

        Args:
          content(str): The book content

        Returns:
          str: The formatted book content
        """
        for delete_regex in self.get_regex("delete"):
            content = re.sub(
                re.compile(rf"{delete_regex}", re.MULTILINE), "", content
            )
        return content

    def do_replace_regex(self, content: str) -> str:
        """Replace words/phrases based on regex.

        Args:
          content(str): The book content

        Returns:
          str: The formatted book content
        """
        regex = self.get_regex("replace")
        if isinstance(regex, list):
            for search, replace in regex:
                content = re.sub(
                    re.compile(rf"{search}", re.MULTILINE),
                    rf"{replace}",
                    content,
                )

        return content

    def do_delete_line_regex(self, content: str) -> str:
        """Delete whole line based on regex.

        Args:
          content(str): The book content

        Returns:
          str: The formatted book content
        """
        for delete_line_regex in self.get_regex("delete_line"):
            content = re.sub(
                re.compile(rf"^.*{delete_line_regex}.*$", re.MULTILINE),
                "",
                content,
            )
        return content

    def do_wrapping(self, content: str) -> str:
        """Wrap or fill CJK text.

        Args:
            content (str): Massage book content

        Returns:
            str: Massage book content
        """
        logger.info("Wrapping paragraph to width: %s", self.width)

        paragraphs = []
        # We don't remove empty line and keep all formatting as it.
        for paragraph in content.split("\n"):
            paragraph = paragraph.strip()

            lines = cjkwrap.wrap(paragraph, width=self.width)
            paragraph = "\n".join(lines)
            paragraphs.append(paragraph)

        wrapped_content = "\n".join(paragraphs)
        return wrapped_content
