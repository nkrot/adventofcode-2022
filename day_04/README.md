
## Solutions from the forum

### A

First, convert the ranges to sets S and T.
For part 1, check whether S is a subset of T, or T is a subset of S.
For Part 2, check whether the intersection of S and T is not empty.

```
def f(line):
    a,b,c,d = map(int, re.findall(r'\d+', line))
    s,t = set(range(a, b+1)), set(range(c, d+1))
    return complex(s <= t or t <= s, any(s & t))

print(sum(map(f, open('input.txt'))))
```

New to me
* a `set` can be initialized from `range`
* set comparison operation `<=` to test intersection
* using `complex` to combine two solutions into one number

### B

https://github.com/mebeim/aoc/tree/master/2022#day-4---camp-cleanup

compute possible overlap segment and the compare it to given segments
