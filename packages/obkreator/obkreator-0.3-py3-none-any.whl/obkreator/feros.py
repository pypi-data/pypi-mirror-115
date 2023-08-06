import numpy as np

from . import _config
from .types import range_type
from . import obkreator

READOUT_MODES = dict(
    normal='225kHz,1,low', 
    slow='60kHz,1,high', 
    fast='625kHz,1,med'
)

def feros_parser_check(parser, args, strict_option_check=True):

    # ADC cannot be IN with objcal

    adc_ref = np.broadcast_arrays(args.adc, args.reference)
    for i, (adc, ref) in enumerate(zip(*adc_ref), start=1):
        if ref != 'sky' and 'adc' == 'IN':
            msg = f'observing template #{i}: ADC cannot be IN with objcal'
            parser.error(msg)

    # If no table is specified, a reference must be set (sky, lamp, etc.)
    # and a DIT given

    if args.table is None:
        if args.reference is None:
            msg = 'reference must be set in filename or via options --reference --objsky/--sky --objcal/--cal/--lamp/--ThAr+Ne --wlc/--ThArNe'
            parser.error(msg)
        if args.dit is None:
            parser.error('option --dit or column dit in table is missing')

def feros_exectime(args):

    # find readout time 

    speed = float(args.readout.split('k')[0]) * 1e3
    bin = [int(b) for b in args.bin.split('x')]
    rdtime = 42. * (225e3 / speed) / np.prod(bin)

    # template time
    acqtime_s = 240 + 60 * (args.ag == 'T') 
    tpltime_s = []
    bc = np.broadcast_arrays(args.adc, args.dit, args.nint)

    for adc, dit, nint in zip(*bc):
        adc_ov = 30 if adc == 'IN' else 0
        time = (dit + rdtime) * nint + adc_ov
        tpltime_s.append(time)

    args.tpltime_s = tpltime_s
    args.tpltime = [t / 60 for t in tpltime_s]
    args.acqtime_s = acqtime_s
    args.acqtime = acqtime_s / 60
    args.obtime_s = sum(tpltime_s, start=acqtime_s)
    args.obtime = args.obtime_s / 60

def feros_post_parser(args):

    args.readout = READOUT_MODES[args.readout]
    args.bin = args.bin[0] # 1x1 -> 1, 2x2 -> 2
    
    # templates
    args.acq = 'acq' # a single acquisition template
    args.obs = ['objsky' if r == 'sky' else 'objcal' for r in args.reference]
 
    feros_exectime(args)

def add_feros_arguments(parser):

    det = parser.add_argument_group(title='detector settings')
        
    det.add_argument(
        '--dit', nargs="+", type=range_type(float, 0, 43200), 
        metavar="(DIT | DIT_TPL1 ... DIT_TPLn)",
        help='default exposure time (s)')
    det.add_argument(
        '--nint', default=1, nargs="+", type=range_type(int, 1, 100), 
        metavar="(NINT | NINT_TPL1 ... NINT_TPLn)",
        help='default number of exposures')

    # readout modes
    speed = det.add_mutually_exclusive_group()
    speed.add_argument(
        '--readout', default='normal', choices=['normal', 'slow', 'fast'],
        help='readout speed') 
    speed.add_argument(
        '--normal', action='store_const', dest='readout', const='normal', 
        help='Normal, low gain readout mode')
    speed.add_argument(
        '--slow', action='store_const', dest='readout', const='slow',
        help='Slow, high gain readout mode')
    speed.add_argument(
        '--fast', action='store_const', dest='readout', const='fast',
        help='Fast, medium gain readout mode')

    bin = det.add_mutually_exclusive_group()
    bin.add_argument(
        '--bin', action='store', default='1x1', choices=['1x1', '2x2'], 
        nargs="+",
        metavar="(BIN | BIN_TPL1 ... BIN_TPLn)",
        help='binning mode (default 1)')
    bin.add_argument(
        '--1x1', action='store_const', dest='bin', const=['1x1'], 
        help='1x1 binning in all templates'
    )
    bin.add_argument(
        '--2x2', action='store_const', dest='bin', const=['2x2'], 
        help='2x2 binning in all templates')
   
    settings = parser.add_argument_group(title='instrumental settings')
 
    # science template

    tpl = settings.add_mutually_exclusive_group()
    tpl.add_argument(
        '--reference', default='ThAr+Ne', nargs="+",
        metavar="REF | REF_TPL1 ... REF_TPLn", 
        choices=['sky', 'ThAr+Ne', 'WLC', 'FF'],
        help='object in the reference fibre'
    ) 
    tpl.add_argument(
        '--objsky', '--sky', action='store_const', const=['sky'], 
        dest='reference',
        help='sky in the reference fibre for all templates')
    tpl.add_argument(
        '--objcal', '--cal', '--lamp', '--ThAr+Ne',
        action='store_const', const=['ThAr+Ne'], dest='reference',
        help='ThAr+Ne lamp in the reference fibre in all templates')
    tpl.add_argument(
        '--wlc', '--ThArNe',
        action='store_const', const=['WLC'], dest='reference',
        help='ThArNe lamp in the reference fibre in all templates')

    # instrument-specific stuff

    adc = settings.add_mutually_exclusive_group() 
    adc.add_argument(
        '--adc', default=['OUT'], choices=['IN', 'OUT'], nargs="+", 
        metavar="(POS | POS_TPL1 ... POS_TPLn)",
        help='atmospheric dispersion corrector position(s), by default, OUT')
    adc.add_argument(
        '--adc-in', action='store_const', const=['IN'], dest='adc',
        help='use the  atmospheric dispersion corrector in all templates')
    adc.add_argument(
        '--adc-out', action='store_const', const=['OUT'], dest='adc',
        help='do not use the  atmospheric dispersion corrector')
    
    settings.add_argument(
        '--lamptime', default=15., type=float,
        help='Equivalent lamp time in seconds')
  
    settings.add_argument(
        '--ag', default='on', choices=['on', 'off'],
        help='Autoguiding mode'
    )
 
    settings.add_argument(
        '--obstype', default='SCIENCE', 
        choices=['STANDARD', 'SCIENCE', 'FLUX_STD', 'RV_STD', 'TELLURIC_STD',
                 'SKY'],
        help='Purpose of the observation.')
 
    return parser

FEROS_TEMPLATES = dict(
    obd_acq = '''

#  Telescope preset and acquistion

TPL.ID                  "FEROS_ech_acq" # sequencer name
TPL.NAME                "Preset and centre on fibre ({acqtime:.1f} min)" 
TPL.MODE                "" # unused
TEL.TARG.ALPHA          "{coo:r!obd}" # right ascencion in [hhmms]s.xxx format
TEL.TARG.DELTA          "{coo:d!obd}" # declination in [ddmms]s.xxx format
TEL.TARG.EQUINOX        "{equinox:.1f}" # equinox of equatorial frmae
TEL.TARG.OFFSETALPHA    "0.0" # RA offset after acquisiton
TEL.TARG.OFFSETDELTA    "0.0" # DEC offset after acquisition
TEL.ROT.OFFANGLE        "0" # used?
TEL.TARG.ADDVELALPHA    "0.0" # differential tracking in r.a.
TEL.TARG.ADDVELDELTA    "0.0" # differential tracking in declination
TEL.TARG.PMA            "{pm:r!arcsec/yr}" # proper motion in r.a. ("/yr)
TEL.TARG.PMD            "{pm:d!arcsec/yr}" # proper motion in dec. (arcsec/yr)
TEL.AG.FIBSELEC         "OBJFIB" # fibre to centre target on
TEL.AG.START            "{ag}" # whether start guiding (T/F)
TEL.PRESET.NEW          "T" # whether preset the telescope (T/F)
''',
    obx_acq = '''

ACQUISITION.TEMPLATE.NAME       "FEROS_ech_acq"
TEL.TARG.OFFSETALPHA            "0.0"
TEL.TARG.OFFSETDELTA            "0.0"
TEL.ROT.OFFANGLE                "0.0"
TEL.AG.FIBSELEC                 "OBJFIB"
TEL.AG.START                    "{ag}"
TEL.PRESET.NEW                  "T"
''',
    obd_objsky = '''

# Simultaneous target & sky observation

TPL.ID                  "FEROS_ech_obs_objsky" 
TPL.NAME                "Simultaneous target-sky observation ({nint} x {dit:.0f} s -> {tpltime:.1f} min)" 
TPL.NEXP                "{nint}" # number of exposures 
TPL.MODE                "SKY" # what is this?
DET1.READ.SPEED         "{readout}" # readout speed and gain 
DET1.WIN1.UIT1          "{dit:.1f}" # integration time
DET1.WIN1.BIN           "{bin}" # binning
SEQ.NEXPO               "{nint}" # number of exposures
SEQ.TYPE                "SCIENCE" # purpose of observations
INS.ADCA                "{adc}" # atmospheric dispersion corrector position
''',
    obx_objsky = '''

TEMPLATE.NAME           "FEROS_ech_obs_objsky"
TPL.MODE                "SKY" # what is this?
DET1.READ.SPEED         "{readout}" # readout speed and gain
DET1.WIN1.UIT1          "{dit:.1f}" # integration time (s)
DET1.WIN1.BIN           "{bin}" # binning
SEQ.NEXPO               "{nint}" # number of exposures
SEQ.TYPE                "SCIENCE" # purpose of observation
INS.ADCA                "{adc}" # atmospheric dispersion corrector position


''',
    obd_objcal = '''

# Simultaneous target & lamp observation

TPL.ID                  "FEROS_ech_obs_objcal" 
TPL.NAME                "Simultaneous target & lamp observation ({nint} x {dit:.0f} s -> {tpltime:.1f} min)"
TPL.MODE                "SKY" # what is this
TPL.NEXP                "{nint}" # number of exposures
DET1.READ.SPEED         "{readout}" # readout speed and gain
DET1.WIN1.UIT1          "{dit:.1f}"  # integration time
DET1.WIN1.BIN           "{bin}"  # binning
SEQ.CALTIME             "{lamptime:.1f}" # equivalent lamp exposure time
SEQ.DFL                 "0" # unused 
SEQ.DFLTESTDIT          "0" # unused
SEQ.DFLUSEDB            "F" # unused
SEQ.LAMPWAIT            "0" # wait time for lamp to warm up
SEQ.LEAVELAMPON         "T" # whether to leave lamp on
SEQ.NEXPO               "{nint}" # number of exposures
SEQ.TYPE                "{obstype}" # type of exposure
INS.OCLAMP              "{reference}" # calibration lamp used
''',
    obx_objcal = '''

TEMPLATE.NAME           "FEROS_ech_obs_objcal"
DET1.READ.SPEED         "{readout}"
DET1.WIN1.UIT1          "{dit:.1f}" 
DET1.WIN1.BIN           "{bin}" 
SEQ.CALTIME             "{lamptime:.1f}"
SEQ.DFL                 "0"
SEQ.DFLTESTDIT          "0"
SEQ.DFLUSEDB            "F"
SEQ.LAMPWAIT            "0"
SEQ.LEAVELAMPON         "T"
SEQ.NEXPO               "{nint}"
SEQ.TYPE                "{obstype}"
INS.OCLAMP              "{reference}"
'''
)

_config.register_defaults(
    tel='2.2',
    ins='FEROS',
    check=feros_parser_check,
    parser=add_feros_arguments, 
    postparser=feros_post_parser,
    templates=FEROS_TEMPLATES,
)

def mkfrsobs(cmdline=None):

    obkreator.create_obs(tel='2.2', ins='FEROS', cmdline=cmdline)

