# txt2ebook

Console tool to convert txt file to different ebook format.

## Installation

Stable version From PyPI:

```console
python3 -m pip install txt2ebook
```

Latest development version from GitHub:

```console
python3 -m pip install -e git+https://github.com/kianmeng/txt2ebook.git
```

## Usage

Showing help message of command-line options:

```console
txt2ebook --help
```

```console
usage: txt2ebook [-f {epub,txt}] [-t TITLE] [-l LANGUAGE] [-a AUTHOR]
                 [-c IMAGE_FILENAME] [-w WIDTH] [-ps SEPARATOR] [-rd REGEX]
                 [-rvc REGEX] [-rv REGEX] [-rc REGEX] [-rt REGEX] [-ra REGEX]
                 [-rl REGEX] [-rr REGEX REGEX] [-et TEMPLATE] [-vp] [-tp]
                 [-nb] [-d] [-h] [-v]
                 TXT_FILENAME [EBOOK_FILENAME]

txt2ebook/tte is a cli tool to convert txt file to ebook format.

  website: https://github.com/kianmeng/txt2ebook
  issues: https://github.com/kianmeng/txt2ebook/issues

positional arguments:
  TXT_FILENAME         source text filename
  EBOOK_FILENAME       converted ebook filename (default: 'TXT_FILENAME.{epub,txt}')

optional arguments:
  -f {epub,txt}        ebook format (default: 'epub')
  -t TITLE             title of the ebook (default: 'None')
  -l LANGUAGE          language of the ebook (default: 'None')
  -a AUTHOR            author of the ebook (default: '[]')
  -c IMAGE_FILENAME    cover of the ebook
  -w WIDTH             width for line wrapping
  -ps SEPARATOR        paragraph separator (default: '\n\n')
  -rd REGEX            regex to delete word or phrase (default: '[]')
  -rvc REGEX           regex to parse volume and chapter header (default: by LANGUAGE)
  -rv REGEX            regex to parse volume header (default: by LANGUAGE)
  -rc REGEX            regex to parse chapter header (default: by LANGUAGE)
  -rt REGEX            regex to parse title of the book (default: by LANGUAGE)
  -ra REGEX            regex to parse author of the book (default: by LANGUAGE)
  -rl REGEX            regex to delete whole line (default: '[]')
  -rr REGEX REGEX      regex to search and replace (default: '[]')
  -et TEMPLATE         CSS template for epub ebook (default: 'clean')
  -vp, --volume-page   generate each volume as separate page
  -tp, --test-parsing  test parsing for volume/chapter header
  -nb, --no-backup     disable backup source TXT_FILENAME
  -d, --debug          show debugging log and stacktrace
  -h, --help           show this help message and exit
  -v, --version        show program's version number and exit
```

Convert a txt file into epub:

```console
txt2book ebook.txt
```

## Copyright and License

Copyright (c) 2021,2022 Kian-Meng Ang

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU Affero General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option) any
later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along
with this program. If not, see <https://www.gnu.org/licenses/>.
