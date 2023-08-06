# Pick3letters

Pick3letters is a program to help inspire you to create poetry or
prose by taking a random string (hexadecimal strings and Torrent
magnet links are currently supported) and outputting lists of word
prefixes you can use. Just for fun, and for confirming that you used
the right prefixes, it also supports recovering the original hex
string or a working magnet link from the poetry or prose they came up
with.

# Usage

The output of pick3letters is a sequence of prefix lists, one per
line. For each line, choose a word of at least 4 letters that starts
with one of the prefixes. You may use capital letters and punctuation
at the end of a word, but any word that starts with punctuation or has
any punctuation mark within the prefix will be ignored during
decoding. Words shorter than 4 letters will also be ignored, making it
easy to insert articles, conjunctions, or fill words where needed
while still being able to check your work by "decoding" it.

To "encode", pass `-e`. To get back the original data, pass `-d`. If
your input or desired output is a hex string, pass `-x`, or if you
want to use a magnet link pass `-m`.

# The prefix list

The list of prefixes was generated with
`pick3letters/generate.py`. That takes a list of words and their
counts as input and generates a specified number of prefix lists as
output, such that the sum of counts of each prefix in a group is
approximately the same. It also allows filtering the list of words by
minimum count to avoid unusual prefixes or typoes. You can also change
the prefix length, the number of groups (which must be a power of 2),
and the minimum word length.

## Generating new prefix lists

You can run the generator with `python3 -m pick3letters.generate` for
usage information. For now, you'd need to replace prefixes.py with its
output, though at some point I'll probably add support for multiple
prefix lists.
