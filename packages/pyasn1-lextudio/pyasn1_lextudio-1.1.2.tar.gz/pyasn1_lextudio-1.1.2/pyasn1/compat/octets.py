#
# This file is part of pyasn1 software.
#
# Copyright (c) 2005-2020, Ilya Etingof <etingof@gmail.com>
# License: https://www.pysnmp.com/pyasn1/license.html
#

# noinspection PyPep8
int2oct = lambda x: bytes((x,))
null = bytes()
# noinspection PyPep8
oct2int = lambda x: x
# noinspection PyPep8
octs2ints = lambda x: x
# noinspection PyPep8
str2octs = lambda x: x.encode("iso-8859-1")
# noinspection PyPep8
octs2str = lambda x: x.decode("iso-8859-1")
# noinspection PyPep8
isOctetsType = lambda s: isinstance(s, bytes)
# noinspection PyPep8
isStringType = lambda s: isinstance(s, str)
