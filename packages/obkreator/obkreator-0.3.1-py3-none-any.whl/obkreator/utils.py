import random
import bs4
import urllib
from astroquery.simbad import Simbad
import warnings
import numpy as np

from . import _config 

from astropy.table import Table, MaskedColumn

def add_exectime(tab, args, *, tel, ins):

    func = _config.get_ins_exectime_func(tel=tel, ins=ins)
    func(tab, args)

def add_obid(tab):

    if 'obid' not in tab.colnames:    
        obid = [random.randint(3000000000, 4000000000)
                        for i in range(len(tab))]
        tab.add_column(obid, name='obid')

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

    names = ['ra', 'dec', 'pmra', 'pmdec', 'equinox', 'epoch']
    cols = [res[name.upper()] for name in names[0:4]]
    cols += [[2000.0] * len(tab), [2000.0] * len(tab)]
    tab.remove_columns([n for n in names if n in tab.colnames])
    tab.add_columns(cols, indexes=(1,)*len(names), names=names)

def lookup_pid(pid, *, tel, ins):

    print(f'Lookup for programme ID {pid}')

    url = 'http://archive.eso.org/wdb/wdb/eso/sched_rep_arc/query'
    data = dict(progid=pid, wdbo='html/display', pi_coi_name='PI_only', 
        tel=tel, instrument=f"{ins}%",force_tabular_mode='on')
    data = urllib.parse.urlencode(data)

    with urllib.request.urlopen(f"{url}?{data}") as response:
        html = response.read()
    soup = bs4.BeautifulSoup(html, 'lxml')

    res = soup.find(id='1')
    if res is None:
        raise RuntimeError(f'{pid}: not a {tel}/{ins} programme ID')
    res = res.find_all('td')[5:7]
    ins, pi = [r.contents[0] for r in res]

    print(f'{pid}: {tel}/{ins} observations by {pi}')

    return ins, pi


