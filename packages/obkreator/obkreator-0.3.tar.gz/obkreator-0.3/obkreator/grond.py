from astropy import table
import argparse

from . import argparser
from . import types
from . import obkreator
from . import _config

STANDARD_OBs = table.Table(
    rows=[ 
        ( '4m4td',  10.0,     1,     1,    6,    6,  35.4,     4,   4),
        ( '8m4td',  10.0,     1,     2,    6,    6, 114.9,     4,   4),
        ('20m4td',  10.0,     1,     5,    6,    6, 369.0,     4,   4),
        ('40m4td',  10.0,     1,    10,    6,    6, 799.0,     4,   4),
        ( '6m6td',  10.0,     1,     1,    6,    6,  35.4,     6,   6),
        ('12m6td',  10.0,     1,     2,    6,    6, 114.9,     6,   6),
        ('30m6td',  10.0,     1,     5,    6,    6, 369.0,     6,   6),
        ('60m6td',  10.0,     1,    10,    6,    6, 799.0,     6,   6),
        ('2x6m6td', 10.0,     1,     1,    6,    6,  35.4,    12,   6),
        ('8x6m6td', 10.0,     1,     1,    6,    6,  35.4,    48,   6),
    ],
    names=[
         'tpltype', 'dit','ndit','nint','nmd','nmp','odit', 'ntd','ntp',
    ]
)

def grond_post_parser(args):
    
    # single templates and filtre set
    args.acq = 'acq'
    args.obs = 'obs'
    args.filter = 'grizJHK'
    
    if args.tpltype == 'stare':
        
        args.nmd = 1
        args.nmp = 1
        args.ntd = 1
        args.ntp = 1
        args.nint = 999
        args.obtime = 720
        args.obtime_s = 9999 
        args.acqtime_s = 300
        args.acqtime = args.acqtime_s / 60
        args.tpltime_s = 9999
        args.tpltime = 720
        args.nexp = 9999
        args.onint = 999
 
        if args.ag == 'auto':
            args.ag = 'T'
            args.combinedoffset = 'T'
    
        return

    # AG properties
   
    if args.ag == "auto":
        args.ag = 'F' if all(t == '4m4td' for t in args.tpltype) else 'T'
        args.combinedoffset = args.ag

    for name in STANDARD_OBs.colnames[1:]:
        setattr(args, name, [])
    
    # Template execution time and number of exposures
    args.onint = 1
    args.tpltime_s = []
    args.nexp = []
    for ot in args.tpltype:
       
        dits = STANDARD_OBs[STANDARD_OBs['tpltype'] == ot][0]
        rd_ov = 27.0 if args.omode == 'fast' else 57.6 
        
        for name in dits.colnames[1:]:
            value = dits[name]
            if name == 'odit' and args.omode == 'fast':
                value += 30.6
            getattr(args, name).append(value)
  
        ag_ov = 30 if args.combinedoffset == 'T' else 0.
        ov = rd_ov + ag_ov
        
        nexp = args.ntd[-1] * (1 + args.nmd[-1] * args.nint[-1])
        tpltime_s = (args.odit[-1] + ov) * args.ntd[-1]        

        args.tpltime_s.append(tpltime_s)
        args.nexp.append(nexp)

    args.acqtime_s = 300 if args.ag == 'T' else 240
    args.acqtime = args.acqtime_s / 60
    
    args.tpltime = [t / 60 for t in args.tpltime_s]
    args.obtime_s = sum(args.tpltime_s, start=args.acqtime_s)   
    args.obtime = args.obtime_s / 60


def grond_parser_check(parser, args):

    if args.tpltype == ['stare']:
        args.tpltype = 'stare'
    tpltype = args.tpltype
    
    stare_params = [n for n in ['dit', 'ndit', 'odit']  if getattr(args, n)]
 
    # if not reading from table, must specify OB type and give
    # consistent key word
    if args.table is None:
        if tpltype is None:
            parser.error('tpltype or stare not specified')
        if tpltype == 'stare' and len(stare_params) < 3:
            parser.error('stare must come with dit, ndit, and odit')
        if tpltype != 'stare' and len(stare_params):
            parser.error(f'{tpltype} is not compatible with dit, ndit, and odit')

    # check that stare observation is the unique template in OB
    if isinstance(tpltype, list) and len(tpltype) > 1 and 'stare' in tpltype:
        parser.error(f'stare template must be the sole template in OB')

def add_grond_arguments(parser):

    # instrumental setup
    settings = parser.add_argument_group(title='instrument-specific settings')

    typ = settings.add_mutually_exclusive_group()
    choices = list(STANDARD_OBs['tpltype']) + ['stare']
    typ.add_argument(
        '--tpltype', '--mnemonic', nargs="+", choices=choices,
        metavar='MNEMONIC_TPL1 ... MNEMONIC_TPLn',
        help=f'mnemonic describing the type of observing template'
    )
    for tpltype in choices[:-1]:
        typ.add_argument(
            '--'+tpltype, dest='tpltype', action='store_const', const=[tpltype],
            help=f'Use a single {tpltype} dithered sequence template'
        )
    typ.add_argument(
        '--stare', action='store_const', const='stare', dest='tpltype',
        help='continous observation in stare mode'
    )
    
    settings.add_argument(
        '--dit', type=types.range_type(float, 2, 43200),
        help='infrared detector integration time in stare mode'
    )
    settings.add_argument(
        '--odit', type=types.range_type(float, 0, 43200),
        help='optical detector integration time in stare mode'
    )
    settings.add_argument(
        '--ndit', type=types.range_type(int, 1, 999),
        help='number of stacked infrared integrations in stare mode'
    )
    
    settings.add_argument(
        '--omode', choices=['slow', 'fast'], default='slow',
        help='optical readout mode(s).'
    )

    settings.add_argument(
        '--focoffset', default=0.,
        type=types.range_type(float, -10000., 10000.),
        help='focus offset'
    )
    
    settings.add_argument(
        '--obstype', default='science', choices=['science', 'calib'],
        help='purpose of observation',
    )
    # autoguider   
    argparser.add_ag_parameters(parser)

   
GROND_TEMPLATES = dict(
    obd_acq = '''# Acquisition template 

TPL.ID                  "GROND_img_acq"
TPL.PRESEQ              "GROND_img_acq.seq"
TPL.TYPE                "acquisition"
TPL.RESOURCES           ""
TPL.NAME                "Preset and acquisition ({acqtime:.1f} min)"
TPL.DID                 "ESO-VLT-DIC.TPL-1.9"
TPL.EXPNO               "0"
TPL.INSTRUM             "GROND"
TPL.NEXP                "0"
TPL.EXECTIME            "{acqtime_s:.0f}" # predicted execution time (s)
TPL.MODE                ""
TPL.GUI                 ""
TPL.REFSUP              "GROND_img_acq.ref"
TPL.VERSION             "$Revision: 1.4 $"
TEL.AG.START            "{ag}" # start autoguider (T/F)
TEL.GS1.ALPHA           "0.000" # unused
TEL.GS1.DELTA           "0.000" # unused
TEL.GS1.MAG             "14" # unused
TEL.PRESET.NEW          "T" # preset telescope (T/F)
TEL.TARG.ADDVELALPHA    "0.0" # differential tracking in ra
TEL.TARG.ADDVELDELTA    "0.0" # differential tracking in delta
TEL.TARG.ALPHA          "{coo:r!obd}" # right ascension hhmmss.sss 
TEL.TARG.DELTA          "{coo:d!obd}" # declination ddmmss.sss
TEL.TARG.EQUINOX        "{equinox:.1f}" # equinox of equatorial frame
TEL.TARG.EPOCH          "{epoch:.1f}" # epoch of target coordinates
TEL.TARG.FOCOFFSET      "{focoffset}" # focus offset
TEL.TARG.NAME           "{target}" # target name
TEL.TARG.PMA            "{pm:r!arcsec/yr}" # ra proper motion in (arcsec/yr)
TEL.TARG.PMD            "{pm:d!arcsec/yr}" # de proper motion (arcsec/yr)

''', 
    obd_obs = '''# Science template

TPL.ID                  "GROND_img_obs_exp"
TPL.PRESEQ              "GROND_img_obs_exp.seq"
TPL.TYPE                "science"
TPL.RESOURCES           ""
TPL.NAME                "Dithered sequence ({ntd} * {odit:.0f} s -> {tpltime:.1f} min)" # prints in bob
TPL.DID                 "ESO-VLT-DIC.TPL-1.9"
TPL.EXPNO               "1"
TPL.INSTRUM             "GROND"
TPL.NEXP                "{nexp}" # total number of exposures
TPL.EXECTIME            "{tpltime_s:.0f}" # estimated execution time (s)
TPL.MODE                "IMAGING"
TPL.GUI                 ""
TPL.REFSUP              "GROND_img_obs_exp.ref"
TPL.VERSION             "$Revision: 1.4 $"
DET1.DIT                "{dit}" # IR integration time (s)
DET1.IMODE              "Double" # IR readout mode
DET1.NDIT               "{ndit}" # number of stacked IR integrations
DET1.NINT               "{nint}" # number of IR exposures
DET2.NGR                "{onint}" # number of optical g' r' exposures
DET2.NIZ                "{onint}" # number of optical i' z' exposures
DET2.OMODE              "{omode}" # optical readout speed
DET2.UITGR              "{odit}" # optical DIT in g' r' (s)
DET2.UITIZ              "{odit}" # optical DIT in i' z' (s)
INS.TARG.NMD            "{nmd}" # number of IR mirror ditherings
INS.TARG.NMP            "{nmp}" # number of IR mirror dither positions
TEL.COMBINED.OFFSET     "{combinedoffset}" # automatically reacquire AG after dither?
TEL.PRESET.AUTO         "T" # preset telescope?
TEL.TARG.FOCOFFSET      "{focoffset:.0f}" # focus offset 
TEL.TARG.MAXSTAGE       "9" # pipeline reduction request 
TEL.TARG.NTD            "{ntd}" # number of telescope ditherings
TEL.TARG.NTP            "{ntp}" # number of telescope dither positions
TEL.TARG.OBSEQNUM       "1" # OB number in observing run
TEL.TARG.OBSRUNID       "1" # observing run number
TEL.TARG.OBTYPEID       "{tpltype}" # short mnemonic for template type
TEL.TARG.TARGETID       "{target}" # target name without space
TEL.TARG.TYPE           "{obstype}" # purpose of observation

'''
)

_config.register_defaults(
    tel='2.2',
    ins='GROND',
    parser=add_grond_arguments,
    check=grond_parser_check,
    postparser=grond_post_parser,
    templates=GROND_TEMPLATES
)

def mkgrndobs(cmdline=None):

    obkreator.create_obs(tel='2.2', ins='GROND', cmdline=cmdline)

