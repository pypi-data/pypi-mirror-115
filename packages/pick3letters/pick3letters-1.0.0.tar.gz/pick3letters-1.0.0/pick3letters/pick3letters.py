__copyright__ = """
Copyright 2021 Sean Richard Lynch <seanl@literati.org>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU Affero General Public
License along with this program.  If not, see
<https://www.gnu.org/licenses/>.
"""

__license__ = "AGPLv3"

from math import log2
from random import choice
import sys
from typing import Any, BinaryIO, Dict, Iterable, List

from .magnet import magnet2infohash, infohash2magnet
from .prefixes import NUM_GROUPS, PREFIXES, MIN_LENGTH, PREFIX_LENGTH

def make_rev_prefixes():
    global REV_PREFIXES

    REV_PREFIXES = {}
    for i, pl in enumerate(PREFIXES):
        for p in pl.split():
            REV_PREFIXES[p] = i

make_rev_prefixes()

def bytegen(stream: BinaryIO):
    while True:
        buf = stream.read(4096)
        if not buf:
            return
        for b in buf:
            yield b


def baseconv(inp: Iterable[int],
             inbits: int,
             outbits: int,
             partial: bool = True):
    x = 0
    n = 0
    for b in inp:
        x = (x << inbits) | b
        n += inbits
        while n >= outbits:
            # Yield the first 'bits' bits
            yield x >> (n - outbits)
            n -= outbits
            # Cut off the bits we yielded
            x &= (1 << n) - 1

    # Emit one more even if we are short on bits
    if partial and n > 0:
        # Treat any trailing bits as 0
        yield x << (outbits - n)
        if outbits - n >= inbits:
            yield None


def lastflag(seq: Iterable[Any]):
    it = iter(seq)
    prev = next(it)
    for x in it:
        yield prev, False
        prev = x

    yield prev, True


def encode(inp: Iterable[int],
           prefixes: List[str],
           inbits: int = 8):
    n = len(prefixes)

    # This used to be a Facebook interview question
    if n & (n - 1) != 0:
        raise ValueError("Number of prefixes must be a power of two!")

    outbits = int(log2(len(prefixes)))
    for x, is_last in lastflag(baseconv(inp, inbits, outbits)):
        if x is None:
            yield True
        else:
            yield prefixes[x]
            if is_last and (x & ((1 << inbits) - 1)) == 0:
                yield False


def words2ints(words: Iterable[str],
               rev_prefixes: Dict[str, int],
               prefix_length: int,
               min_length: int):
    for word in words:
        if len(word) < min_length:
            continue
        x = rev_prefixes.get(word[:prefix_length].lower())
        if x is not None:
            yield x


def hex2ints(hx: str):
    for h in hx:
        yield int(h, 16)


def decode(words: List[str],
           rev_prefixes: Dict[str, int],
           num_groups: int,
           prefix_length: int,
           outbits: int = 8) -> Iterable[int]:
    inbits = int(log2(num_groups))
    # We drop a trailing zero if the words end in a period
    drop_trailing_zero = words[-1][-1] == '.'
    prev = None
    for x in baseconv(words2ints(
        words, rev_prefixes, prefix_length, MIN_LENGTH
    ), inbits, outbits, False):
        if prev is not None:
            yield prev

        prev = x

    # Emit the last item only if it's not zero if we care
    if prev is not None and (prev != 0 or not drop_trailing_zero):
        yield prev


def do_encode(args):
    if args.hex:
        inp = hex2ints(''.join(args.input))
        inbits = 4
    elif args.magnet:
        url = ' '.join(args.input)
        inp = hex2ints(magnet2infohash(url))
        inbits = 4
    else:
        sys.exit('No type provided')

    if args.test:
        for ps in encode(inp, PREFIXES, inbits):
            if ps == True:
                print('.')
            elif ps == False:
                pass
            else:
                w = choice(ps.split())
                w += 'o' * (MIN_LENGTH - len(w))
                print(w, end=' ')
    else:
        for ps in encode(inp, PREFIXES, inbits):
            if ps == True:
                print('Must end in period.')
            elif ps == False:
                print('Must NOT end in period.')
            else:
                print(ps)

def do_decode(args):
    if args.input:
        words = ' '.join(args.input).split()
    else:
        words = [word.strip() for word in sys.stdin.read().split()]

    if args.hex or args.magnet:
        r = []
        for x in decode(words, REV_PREFIXES, NUM_GROUPS, PREFIX_LENGTH, 4):
            r.append('0123456789abcdef'[x])

        hx = ''.join(r)

        if args.hex:
            print(hx)
        elif args.magnet:
            print(infohash2magnet(hx))


def main():
    from argparse import ArgumentParser

    p = ArgumentParser()
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument('-e', '--encode', action='store_true')
    g.add_argument('-d', '--decode', action='store_true')
    g.add_argument('-t', '--test', action='store_true')
    g = p.add_mutually_exclusive_group()
    g.add_argument('-x', '--hex', action='store_true')
    g.add_argument('-m', '--magnet', action='store_true')
    p.add_argument('input', nargs='*')
    args = p.parse_args()

    if args.encode or args.test:
        do_encode(args)
    elif args.decode:
        do_decode(args)
    else:
        p.print_help()


if __name__ == '__main__':
    main()
