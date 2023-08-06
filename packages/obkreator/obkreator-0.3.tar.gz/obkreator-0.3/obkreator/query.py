import random
import bs4
import urllib
from astroquery.simbad import Simbad
import warnings
import numpy as np
from astropy.table import Column

from . import _config 

from astropy.table import Table, MaskedColumn

def query_simbad(tab):
            
    # lookup simbad and remove what's not found 

    simbad = Simbad()

    simbad.add_votable_fields('typed_id', 'ra', 'dec', 'pmra', 'pmdec')
    simbad.remove_votable_fields('main_id', 'coordinates')

    with warnings.catch_warnings() as w:

        warnings.simplefilter('ignore')
        res = simbad.query_objects(tab['target'])
        invalid = np.argwhere(res['RA'] == '')[:,0]
        
        if len(invalid):
            targets = ', '.join(tab['target'][invalid])
            warnings.warn("unrecognised targets skipped: {targets}", 
                    category=UserWarning)
        
        res.remove_rows(invalid)
        tab.remove_rows(invalid)
    
    # add coordinate info to table

    names = ['coo', 'pm', 'equinox', 'epoch']

    coo = [f"{a} {b}" for a, b in res['RA','DEC']]
    pm = [f"{a} {b}" for a, b in res['PMRA', 'PMDEC']]
    cols = [coo, pm, [2000.0] * len(tab), [2000.0] * len(tab)]

    tab.add_columns(cols, indexes=(1,)*len(names), names=names)
    old_names =  ['ra', 'dec', 'pmra', 'pmdec', 'equinox', 'epoch']
    tab.remove_columns([n for n in old_names if n in tab.colnames])

def lookup_pid(args, *, tel, ins):

    url = 'http://archive.eso.org/wdb/wdb/eso/sched_rep_arc/query'
    data = dict(
        progid=args.pid, wdbo='html/display', pi_coi_name='PI_only', 
        tel=tel, instrument=f"{ins}%", tab_progid='on', force_tabular_mode='on'
    )
    data = urllib.parse.urlencode(data)

    with urllib.request.urlopen(f"{url}?{data}") as response:
        html = response.read()
    soup = bs4.BeautifulSoup(html, features='html.parser')
    res = soup.find(id='1')
    if res is None:
        raise ValueError(f'{args.pid}: not a {tel}/{ins} programme ID')
    res = res.find_all('td')[5:8]
    ins, pid, pi = [r.contents[0] for r in res]

    if args.pid != pid:
        raise ValueError(f'{args.pid}: not a {tel}/{ins} programme ID')

    if args.pi and args.pi != pi:
        print(f'{pid}: {tel}/{ins} observations by {args.pi} under {pi} PID')
    else:
        args.pi = pi
        print(f'{pid}: {tel}/{ins} observations by {pi}')


