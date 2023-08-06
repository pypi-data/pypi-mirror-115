from datetime import datetime
import argparse
import re
import numpy as np
from astropy.table import Table
from astropy.coordinates import SkyCoord
from astropy.io.registry import get_formats
import random

from . import query 
from . import _config 
from . import types


def get_table_formats():
     return [f for c, f, d, r 
                in get_formats()['Data class', 'Format','Deprecated','Read']
                if not d and r and c == 'Table']

def _get_options(parser, ignore, nargs_cond):

    actions = parser._actions
    names = [a.option_strings[0] for a in actions if nargs_cond(a.nargs)]
    names = [o for n in names if (o := n.removeprefix('--')) not in ignore]

    return names

def get_table_colnames(parser):

    ignore = ['pid', 'pi', 'targetfile', 'obformat', 'tableformat', 'obdir']
    condition = lambda nargs: nargs != 0
    return _get_options(parser, ignore, condition)

    
def get_table_vector_colnames(parser):
    
    ignore = ['target']
    condition = lambda nargs: nargs not in [0, 1, None]
    return _get_options(parser, ignore, condition)

class CustomHelpFormatter(
    argparse.RawDescriptionHelpFormatter,
):

    # let user specify metavar if nargs > 1
    
    def _format_args(self, action, default_metavar):
        
        get_metavar = self._metavar_formatter(action, default_metavar)
        if getattr(action, 'nargs', None) == argparse.ONE_OR_MORE:
            return f'{get_metavar(1)[0]}'
        
        return super()._format_args(action, default_metavar)
    
    # do not list choices as metavar
    
    def _metavar_formatter(self, action, default_metavar):

        if action.metavar is not None:
            result = action.metavar
        else:
            result = default_metavar  

        def format(tuple_size):
            if isinstance(result, tuple):
                return result
            else:
                return (result, ) * tuple_size
        return format

    # list choices in help

    def _get_help_string(self, action):

        help = super()._get_help_string(action)
        if help[-1] not in '.!?':
            help += '.'
        help = help[0].upper() + help[1:]
        if action.nargs != 0 and action.default is not None:
            help += f" Default: {action.default}."
        if isinstance(action.choices, list):
            help += f" List of values: {', '.join(action.choices)}"

        return help


def parse_ag(args):

    if args.ag == "on":
        args.ag = 'T'
        args.combinedoffset = 'T'
    elif args.ag == "manual":
        args.ag = 'T'
        args.combinedoffset = 'F'
    else:
        args.ag = 'F'
        args.combinedoffset = 'F'

def parse_transparency(args):

    t = args.transparency
    if t in ['thn', 'thin']:
        t = 'Variable, thin cirrus'
    elif t in ['thk', 'thick']:
        t = 'Variable, thick cirrus'
    elif t in ['clear', 'clr']:
        t = 'Clear'
    else:
        t = 'Photometric'

    args.transparency = t

def parser_check(parser, args, *, tel, ins):

    # --coo and --pm only for a single target
    opts = [c for c in ['coo', 'pm'] if getattr(args, f'_{c}_given', False)]
    if len(opts):
        msg = None
        if args.table:
            msg = f"--table and --{opts[0]} are not compatible"
        if args.target is not None and len(args.target) > 1:
            msg = f"--{opts[0]} can only specified for a single target"
        if msg:
            parser.error(msg)

    ins_parser_check = _config.get_ins_parser_check_func(tel=tel, ins=ins)
    if ins_parser_check is not None:
        ins_parser_check(parser, args)

def post_parser(args, *, tel, ins):

    # missing information
    if not args.target:
        args.target = f'{args.coo:c!J}'
    if not args.obdesc:
        args.obdesc = f'{args.coo:c!hhmm+ddmm}_P{args.priority}'
    if not args.obname:
        args.obname = args.target
    if not args.obid:
        args.obid = random.randint(10000000, 20000000)
  
    # remove spaces
    args.target = re.sub('\s+', '', args.target)
    args.obname = re.sub('\s+', '', args.obname)
 
    # AG 
    parse_ag(args)

    # instrument-specific things such as setting DITs, etc. 
    ins_post_parser = _config.get_ins_post_parser_func(tel=tel, ins=ins)
    if ins_post_parser is not None:
        ins_post_parser(args)
   
    # sky transparency 
    parse_transparency(args)
   
    # date 
    args.date = datetime.now().isoformat()[0:19]

def iter_targets(parser, args):
    
    # read from file or commandline

    if args.table is not None:
        tab = Table.read(args.table, format=args.tableformat)
        src = 'table'
        del args.table
        del args.tableformat
    else:
        src = 'cmd'
        names = ['target', 'coo', 'pm', 'equinox', 'epoch']
        cols = {n: v for n in names if isinstance(v := getattr(args, n), list)}
        tab = Table(cols)

    # valid column names in table correspond to options with arguments 
    # excluding a few forbidden ones
    colnames = get_table_colnames(parser)
    for name in tab.colnames:
        if name not in colnames:
            raise parser.error(f"target table cannot have column '{name}'")

    # if coordinates are missing, query simbad
    if 'coo' not in tab.colnames:
        query.query_simbad(tab)
        print('Coordinates have been queried from SIMBAD')

    # split cells into lists if parser expects several arguments
    # (except for target)
    colnames = get_table_vector_colnames(parser)
 
    for name in tab.colnames:

        if name not in colnames:
            continue

        col = tab[name]
        if col.dtype.char != 'U':
            continue
            
        col = [re.split('\s+|\s*[;,]\s*', t) if not np.ma.is_masked(t) else t 
                    for t in col]
        tab.replace_column(name, np.array(col, dtype=object))

    if src == 'table':
        colnames = ", ".join(tab.colnames)
        print(f'{len(tab)} OBs to be generated using table')
        print(f'Columns are: {colnames}')

    # iter over lines
    for row in tab:
        target = {n: v for n, v in dict(row).items() if not np.ma.is_masked(v)}
        yield target

def add_ag_parameters(parser, choices=["on", "manual", "off", "auto"]):
    
    HELP = {
        'on': 'AG is used, acquired automatically from second offset',
        'manual': 'AG is used, acquired manually at each offset',
        'off': 'AG is not used',
        'auto': 'AG mode is automatically selected depending on exposure time and offset size'
    }

    ag0 = parser.add_argument_group(title='autoguiding')

    ag = ag0.add_mutually_exclusive_group()
    ag.add_argument(
        '--ag',
        choices=choices, default='on',
        help='Autoguider mode.'
    )
    for choice in choices:
        name = f'--ag-{choice}'
        ag.add_argument(
            name, action='store_const', const='on', dest='ag',
            help=HELP[choice]
        )


def add_sky_parameters(parser):
    
    sky = parser.add_argument_group(title='requested sky conditions')
    sky.add_argument(
        '--seeing', default=2.0,
        type=types.range_type(float, 0.2, 2, precision=1), metavar="[0.2..2]",
        help='Maxiumum seeing in arcsec.')
    sky.add_argument(
        '--fli', default=1.0,
        type=types.range_type(float, 0, 1, precision=1), metavar="[0..1]",
        help='Maximum fractional lunar illumination.')
    sky.add_argument(
        '--moondist', default=30,
        type=types.range_type(int, 0, 180), metavar="[0..180]",
        help='Minimum angular distance in degrees.')
    sky.add_argument(
        '--airmass', default=2.0, 
        type=types.range_type(float, 1, 5, precision=1), metavar="[1..5]",
        help='Maximum airmass.'
    )
    trans = sky.add_mutually_exclusive_group()
    trans.add_argument(
        '--transparency', default='clear', type=str.lower, 
        choices=['photometric', 'clear', 'thin', 'thick'],
        help='Worst acceptable sky transparency.'
    )
    trans.add_argument(
        '--clear', dest='transparency', action='store_const', const='clear',
        help='At worst, clear conditions.'
    )
    trans.add_argument(
        '--photometric', dest='transparency', action='store_const', 
        const='photometric',
        help='Photometric conditions required.'
    )
    trans.add_argument(
        '--thin', dest='transparency', action='store_const', const='thin',
        help='At worst, thin cirrus.'
    )
    trans.add_argument(
        '--thick', dest='transparency', action='store_const',  const='thick',
        help='Any conditions.'
    )
    
def add_ob_parameters(parser):

    format = parser.add_argument_group(title='observing block information')
    fmt = format.add_mutually_exclusive_group()
    fmt.add_argument(
        '--obformat', default='obd', choices=['obd', 'obx'],
        help='Format for saved OBs.'
    )
    fmt.add_argument(
        '--obd', '--bob', action='store_const', dest='obformat', const='obd', 
        help='Save in obd format for execution from bob.'
    )
    fmt.add_argument(
        '--obx', '--p2', action='store_const', dest='obformat', const='obx',
        help='Save in obx format for execution from p2.'
    )
    format.add_argument(
        '--obid', type=int, 
        help='OB ID number. Default: random.',
    )    
    format.add_argument(
        '--obname', type=str, 
        help='Name of OB. Default: target name.'
    )
    format.add_argument(
        '--obdesc', type=str, 
        help='OB description.'
    )
    format.add_argument(
        '--priority', type=types.range_type(int, 1,9), default=1,
        metavar="[1..9]",
        help='Execution priority.'
    )

def get_parser(progname, *, tel='2.2', ins='FEROS'):

    HELP = f"""\
Create {ins} observing blocks at the {tel} telescope for a list of targets.  

If specified, the file containing the target information may take any column
overriding the corresponding command line option, provided  it is an option 
taking one or more arguments. Columns pi, pid, targetfile, obformat, and
tableformat are not allowed. The file must contain either a target column 
(SIMBAD IDs) and/or a coo (equatorial coordinates) one.

The programme ensures that the programme ID is valid. Some care has been
taken to produce valid OBs, but extensive testing hasn't been done.
"""
    formatter = lambda prog: CustomHelpFormatter(prog, max_help_position=8)

    parser = argparse.ArgumentParser(
                prog=progname, formatter_class=formatter, description=HELP,
             )

    parser.add_argument('--obdir', metavar='DIR', default=f'OB/{ins}-{tel}',
        type=types.dir_type,
        help='Directory where OBs will be created'
    )

    prog = parser.add_argument_group(title='observing programme')
    prog.add_argument('--pid',type=str, required=True,
        help='ESO programme ID (mandatory).')
    prog.add_argument('--pi', type=str, 
        help='Principal investigator. Default: obtained from PID.')
    prog.add_argument('--observer', default='UNKNOWN', 
        help='Observer.')

    obsinfo = parser.add_argument_group(title='astronomical objects') 
    
    formats = get_table_formats()

    targets = obsinfo.add_mutually_exclusive_group()
    targetfile_action = targets.add_argument(
        '--table', type=argparse.FileType('rb'),
        metavar='FILENAME',
        help=f'Table with target and observation information.'
    )
    targets.add_argument(
        '--target', type=str, nargs="+", metavar="ID1 ... IDn",
        help='Target name(s) recognised by SIMBAD. Default: deduced from coordinates following format Jhhmmss.sss+ddmmss.sss.', 
    )

    obsinfo.add_argument(
        '--tableformat', default='ascii.fixed_width_two_line',
        choices=format, metavar='FMT',
        help=f'Table format.'
    )
    obsinfo.add_argument(
        '--coo', nargs="+", metavar="RA DEC", 
        action=types.Coordinates.action, 
        help='Target coordinates in the equatorial system if a single target is specified. Sexagesimal coordinates are understood as hours and degrees (hh:mm:ss +dd:mm:ss with spaces or colons), decimal in degrees and degrees (dd.ddd +dd.dddd). When coordinates are not specified, they are retrieved by simbad.'
    )
    obsinfo.add_argument(
        '--pm', nargs="+", metavar="PMRA,PMDEC",
        action=types.ProperMotions.action, default=types.ProperMotions(0., 0.),
        help='Proper motions in mas/yr if a single target is specified. If coordinates are retrieved by SIMBAD any specified or default value is overridden.'
    )
    obsinfo.add_argument(
        '--equinox', default=2000., 
        type=types.range_type(float, 0, 9999.9, precision=1), 
        help='Equinox for coordinates.'
    )
    obsinfo.add_argument(
        '--epoch', default=2000., 
        type=types.range_type(float, 0, 9999.9, precision=1), 
        help='Epoch for coordinates.'
    )

    add_ob_parameters(parser)
    add_sky_parameters(parser)

    add_ins_args = _config.get_ins_parser_func(tel=tel, ins=ins)
    add_ins_args(parser)
 
    # indicate table columns. 
    colnames = get_table_colnames(parser)
    targetfile_action.help += f' Allowed table columns: {", ".join(colnames)}.'
 
    return parser

def parse_cmdline(parser, cmdline, *, tel, ins):

    args = parser.parse_args(cmdline)
    
    parser_check(parser, args, tel=tel, ins=ins) 

    return args
