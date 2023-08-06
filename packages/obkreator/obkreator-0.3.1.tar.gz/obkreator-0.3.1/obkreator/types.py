from astropy import coordinates 
import re
import argparse
import numpy as np
import os

def dir_type(dir):
    try:
       os.makedirs(dir, exist_ok=True)
    except:
        raise argparse.ArgumentTypeError(f'not a valid directory: {dir}')
    return dir

def range_type(type, min, max, precision=None):
    def converter(x, min=min, max=max, precision=precision):
        value = type(x)
        if value < min or value > max:
            raise argparse.ArgumentTypeError(f'value not in range {min}:{max}')
        if value != round(value, precision):
            msg = f'value too precise (at most {precision} decimal digits)'
            raise argparse.ArgumentTypeError(msg)
        return value
    return converter

class MultiargType:

    def __init_subclass__(cls):

        def init(self, option_strings, dest, nargs=None, **kwargs):

            if nargs is None:
                raise ValueError('nargs must be specified')

            argparse.Action.__init__(self, option_strings, dest, 
                nargs=nargs, **kwargs)

        def call(self, parser, namespace, values, option_string=None):

            value = cls(*values)
            setattr(namespace, self.dest, value)
            setattr(namespace, f'_{self.dest}_given', True)

        members = dict(__call__ = call, __init__ = init)
        
        actionname = f'Store{cls.__name__}'
        cls.action = type(actionname, (argparse.Action,), members)

    def __bool__(self):

        return True

class OffsetList(MultiargType):

    max = 9999 

    def __init__(self, *xy):

        xy = np.hstack([re.split('(\s*,\s*| )', str(c)) for c in xy])

        lst = ' '.join([str(z) for z in xy])
        if len(xy) % 2:
            raise ValueError(f'not a list of pair of offsets: {lst}')
        
        try:
            self.ra = [float(x) for x in xy[::2]]
            self.dec = [float(y) for y in xy[1::2]]
        except:
            raise ValueError(f'not a a list of floats: {lst}')

        if any(abs(o) > self.max for o in self.ra):
            raise ValueError(f'ra offset greater than 1800')   
        if any(abs(o) > self.max for o in self.dec):
            raise ValueError(f'dec. offset greater than 1800')   
            
    def __format__(self, fmt):

        # print(f'format {repr(self)} with {repr(fmt)}')

        if fmt in ['alpha', 'r', 'ra']:
            return ' '.join(format(r, '.3f') for r in self.ra)
        elif fmt in ['delta', 'd', 'dec']:
            return ' '.join(format(r, '.3f') for r in self.dec)
        else:
            off = [f"'{a},{b}'" for a, b in zip(self.ra, self.dec)]
            return ', '.join(off)
       
    def __repr__(self):

        off = [f"'{a},{b}'" for a, b in zip(self.ra, self.dec)]
        return f'{type(self).__name__}({", ".join(off)})'
 
class Pixel(MultiargType):

    def __init__(self, *coo):

        name = type(self).__name__
        val = f'{" ".join([str(c) for c in coo])}'

        if len(coo) == 1:
            coo = re.split('\s*,\s*| ', coo[0])
        if len(coo) != 2:
            raise ValueError(f'bad format for {name}: {val}')

        try:
            self.ra = float(coo[0])
            self.dec = float(coo[1])
        except:
            raise ValueError(f'{name}: not a pair of floats: {val}')

        bounds = f" {self.minx}..{self.maxx} {self.miny}..{self.maxy}"
        if (self.ra < self.minx or self.dec > self.maxx or 
            self.dec < self.miny or self.dec > self.maxy):
            raise ValueError(f'{name} out of {bounds}')

    def __format__(self, fmt='.1f'):

        if fmt in ['obd', 'obx']:
            return f'{self.ra:.3f} {self.dec:.3f}'
        if fmt in ['ra', 'alpha', 'r']:
            return format(self.ra, '.3f') 
        if fmt in ['de', 'dec', 'delta', 'd']:
            return format(self.dec, '.3f') 
         
        return f'{format(self.ra,fmt)},{format(self.dec,fmt)}'

    def __str__(self):

        return f'{self.ra:+.3f},{self.dec:+.3f}'

    def __repr__(self):
        
        return f'{type(self).__name__}({self.ra},{self.dec})'

class Offset(Pixel):

    minx = -9999
    maxx = 9999
    miny = -9999
    maxy = 9999

class ProperMotions(Pixel):

    minx = -3000
    maxx =  3000
    miny = -3000
    maxy =  3000

    def __format__(self, fmt):

        if fmt == '':
            fmt = 'c!mas/yr'
        invalid = f'invalid proper motion format: {fmt}'

        if '!' in fmt:
            coo, fmt = fmt.split('!')
        else:
            coo, fmt = fmt, 'mas/yr'

        if fmt in ['as/yr', 'arcsec/yr']:
            fmt = 1e-3
        elif fmt in ['mas/yr', 'milliarcsec/yr']:
            fmt = 1
        else:
            raise ValueError(invalid)

        if coo == 'c':
            return f'{self.ra * fmt},{self.dec * fmt}'
        if coo in ['r', 'ra', 'alpha']:
            return f'{self.ra * fmt:.5f}'
        if coo in ['d', 'dec', 'delta']: 
            return f'{self.dec * fmt:.5f}'
        raise ValueError(invalid)

    def __str__(self):
        
        return format(self)

class Coordinates(coordinates.SkyCoord, MultiargType):
           
    def __init__(self, *coo):

        unit = 'hour,deg'
 
        # if decimal format is given for RA, then it's assumed to be
        # degrees

        len_ = len(coo)

        if (len_ == 2 and ' ' not in coo[0] and ':' not in coo[0] or
            len_ == 1 and '.' in re.split('[ :+-]', coo[0])[0]):
            unit = 'deg,deg'

        if len_ % 2 == 0:
            coo = [':'.join(coo[:len_//2]), ':'.join(coo[len_//2:])]

        coo = ' '.join(coo)

        super().__init__(coo, unit=unit, frame='icrs')

    def __repr__(self):

        return f"{type(self).__name__}('{self}')"

    def __str__(self):

        return format(self)

    def __format__(self, fmt):

        if fmt == '':
            fmt = 'c!obx'

        if '!' in fmt:
            coo, fmt, *unused = fmt.split('!')
        else:
            coo = fmt
            fmt = 'obd'

        coord = self.to_string('hmsdms').split(' ')
        coord = [re.sub('[dhms]', ':', c)[0:12] for c in coord] 
        
        # OBD uses a numeric format hhmmss.sss and ddmmss.sss with
        # heading noughts and plus sign removed
        if fmt in ['obd', 'hmmss.sss dmmss.ss']:
            coord = [re.sub(':', '', c) for c in coord]
            coord = [re.sub('^\+?0{0,5}', '', c) for c in coord]
            jchar = ' '
        # Default target name from coordinates
        elif fmt in ['s', 'hhmm+ddmm']:
            coord = [re.sub(':', '', c) for c in coord]
            coord = [coord[0][0:4], coord[1][0:5]]
            jchar = ''
        elif fmt in ['J', 'Jhhmmss.sss+ddmmss.ss']:
            coord = [re.sub(':', '', c) for c in coord]
            coord[0] = 'J' + coord[0]
            jchar = '' 
        elif fmt in ['obx', 'hh:mm:ss.sss +dd:mm:ss.ss']:
            jchar = ' '
        
        if coo == 'c':
            return jchar.join(coord)
        elif coo == 'r':
            return coord[0]
        elif coo == 'd':
            return coord[1]

