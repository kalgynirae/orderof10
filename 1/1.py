#!/usr/bin/env python3
from collections import namedtuple
import glob
import itertools
import operator


frame = """\
      ####     
   #########   
  ###########  
 ############# 
 ############# 
############## 
######   ######
######   ######
######   ######
 ##############
 ############# 
 ############# 
  ###########  
   #########   
     ####      
"""


def main():
    # Print a number spiral
    #for row in spiral(range(1, 15 * 14 + 1)):
    #    print(' '.join('{:3}'.format(i.value) for i in row))

    paths = sorted(glob.glob('images/*.png'))
    print('<table>')
    for row in spiral(paths):
        print('<tr>')
        for item in row:
            if item.is_prime:
                pass
            else:
                print('<td style="padding: 0;"><img src="{}"></td>'.format(item.value))
        print('</tr>')
    print('</table>')


def spiral(seq):
    """Arrange the items of seq in a spiral and return them one row at a time

    Each yielded row is a list of ValueWithPrimeness objects.
    """
    length = len(seq)
    values = enumerate(seq, start=1)

    primelist = list(primes(length))
    directions = itertools.cycle([Vector(1, 0), Vector(0, -1), Vector(-1, 0), Vector(0, 1)])
    items = {}

    position = Vector(0, 0)
    try:
        for repetitions in repeat_each(itertools.count(1)):
            direction = next(directions)
            for _ in range(repetitions):
                i, value = next(values)
                items[position] = ValueWithPrimeness(value, i in primelist)
                position += direction
    except StopIteration:
        pass

    def row(item):
        return item[0].y
    def col(item):
        return item[0].x

    for _, row in itertools.groupby(sorted(items.items(), key=row), key=row):
        yield [item[1] for item in sorted(row, key=col)]


class Vector(namedtuple('Vector', 'x y')):
    def __add__(self, other):
        return self.__class__(self.x + other.x, self.y + other.y)


ValueWithPrimeness = namedtuple('ValueWithPrimeness', 'value is_prime')


def repeat_each(seq):
    for item in seq:
        yield item
        yield item


def primes(max=None):
    """Generate prime numbers

    See http://code.activestate.com/recipes/117119-sieve-of-eratosthenes/

    >>> list(primes(5))
    [2, 3, 5]

    """
    yield 2
    D = {}
    for q in itertools.count(3, 2):
        if max and q > max:
            return
        p = D.pop(q, None)
        if p is None:
            yield q
            D[q * q] = 2 * q
        else:
            x = p + q
            while x in D:
                x += p
            D[x] = p


if __name__ == '__main__':
    main()
