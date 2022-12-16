how to emulate sorted(..., cmp=function) from Python 2
https://learnpython.com/blog/python-custom-sort-function/


https://vaclavkosar.com/software/Python-functools.cmp_to_key-explained

## Part 1
input is similar to https://adventofcode.com/2021/day/18 (Snailfish numbers)

for parsing, use eval or json.loads().

safe eval():
https://docs.python.org/3/library/ast.html#ast.literal_eval

## In part 2
No need to sort all packets. It is sufficient to compare each of
divider packets to each of other packets and count how many of
the latter sort before the divider packet.
if you start by rearranging divider packets, the above can be
optimized: what sorts before the 1st of the divider packets, also
sorts before the other divider packet.

## Other solutions

https://gist.github.com/betaveros/81cd511b4bd53ef13a74043c1c0b4210
