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

from argparse import ArgumentParser
from heapq import heapify, heappop, heappush, heappushpop
from itertools import groupby
from operator import itemgetter
import re
import sys
from typing import TextIO


def generate(
        num_groups: int,
        prefix_length: int,
        stream: TextIO,
        min_length: int = 0,
        min_count: int = 0,
        swap: bool = False) -> None:

    # Word and count index
    iw, ic = (1, 0) if swap else (0, 1)
    word_counts = (
        (t[iw].lower(), int(t[ic])) for t in
        (l.strip().split() for l in stream)
    )

    prefix_counts_dupes = (
        (w[:prefix_length], c) for w, c in word_counts
        if len(w) >= min_length and c >= min_count and
        re.fullmatch('[a-z]+', w)
    )

    # Count of each prefix followed by the prefix
    prefix_counts = [
        (sum(c for _, c in g), p) for p, g in
         groupby(sorted(prefix_counts_dupes), itemgetter(0))
    ]
    prefix_counts.sort()

    prefix_heap: list[tuple[int, list[str]]] = [
        (0, []) for _ in range(num_groups)
    ]
    heapify(prefix_heap)

    # Get the smallest count from the heap (they're all zero anyway)
    c0, ps = heappop(prefix_heap)

    for c, p in prefix_counts:
        ps.append(p)
        c0, ps = heappushpop(prefix_heap, (c0+c, ps))

    # Put the last one back in
    heappush(prefix_heap, (c0, ps))

    # Sort by largest count just so the order is independent of the
    # heapq implementation
    prefix_heap.sort(reverse=True)

    print(f'PREFIX_LENGTH = {prefix_length}')
    print(f'MIN_LENGTH = {min_length}')
    print(f'NUM_GROUPS = {num_groups}')
    print('PREFIXES = [')
    for _, prefixes in prefix_heap:
        print(f' {repr(" ".join(prefixes))},')

    print(']')


def main():
    p = ArgumentParser()
    p.add_argument('-m', '--min-length', type=int, default=3,
                   help="Minimum word length to use")
    p.add_argument('-g', '--num-groups', type=int, default=16,
                   help="Number of groups of prefixes")
    p.add_argument('-l', '--prefix-length', type=int, default=2,
                   help="Prefix length to use")
    p.add_argument('-c', '--min-count', type=int, default=2,
                   help="Minimum number of times a word must appear to be used")
    p.add_argument('-s', '--swap', action='store_true',
                   help="Swap order of count and word because count appears first")
    args = p.parse_args()
    generate(args.num_groups,
             args.prefix_length,
             sys.stdin,
             args.min_length,
             args.min_count,
             args.swap)


if __name__ == '__main__':
    main()
