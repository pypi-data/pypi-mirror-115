import argparse
import re
import numpy as np

from . import types
from . import argparser
from . import _config
from . import obkreator

class WfiPixel(types.Pixel):

    minx = 1
    maxx = 8568
    miny = 1
    maxy = 8256


FILTERS = [
'White', 'BB#U/50_ESO877', 'BB#B/123_ESO878', 'BB#V/89_ESO843',
'BB#Rc/162_ESO844', 'BB#I/203_ESO879', 'BB#Z+/61_ESO846', 'BB#U/38_ESO841',
'BB#B/99_ESO842', 'BB#Ic/Iwp_ESO845', 'NB#396/12_ESO865', 'MB#416/29_ESO872',
'MB#445/18_ESO873', 'MB#461/13_ESO874', 'MB#485/31_ESO860', 'NB#OIII/2',
'NB#OIII/8_ESO859', 'NB#504/10_ESO861', 'MB#518/16_ESO862', 'MB#531/17_ESO875',
'Gieren_501_2/2.7', 'Washington_M', '513/15', 'MB#549/16', 'MB#571/25_ESO863',
'MB#604/21_ESO864', 'MB#620/17_ESO866', 'MB#646/27_ESO867',
'NB#Halpha/7_ESO856', 'NB#665/12_ESO858', 'NB#SIIr/8_ESO857',
'MB#679/19_ESO868', 'MB#696/20_ESO869', 'MB#721/25_ESO847', 'MB#753/18_ESO848',
'MB#770/19_ESO849', 'MB#790/25_ESO850', 'MB#815/20_ESO851', 'MB#837/20_ESO852',
'MB#856/14_ESO853', 'MB#884/39_ESO870', 'MB#914/27_ESO854', 'NB#810/6',
'NB#817/7', 'NB#824/7', 'MB#516/16_ESO871']

FILTER_RE = '(.*)#((.*)/([0-9]+))_(.*)'

FILTER_ALIASES = {
    m.groups()[1 if re.match('[0-9]+', m.groups()[1]) else 2]: f
        for f in FILTERS if (m := re.search(FILTER_RE, f))
}
FILTER_NAMES = list(FILTER_ALIASES.keys()) + FILTERS    

def shorten_filter(name):
    
    m = re.match(FILTER_RE, name)
    if not m:
        return name 
    return m.groups()[1]
 

def wfi_check_parser(parser, args):
   
    # if reading from table, some command line options may be missing
    # and replaced by table values, don't check about their presence.
 
    if args.table is None:
        for opt in ['dit', 'nint']:
            if getattr(args, opt, None) is None:
                parser.error(f'{opt} is not specified')

def wfi_exectime(args):

    acqtime = 240 + 60 * (args.ag == 'T')
    if args.acq != 'preset':
        acqtime += 120 + args.acqdit

    tpltime = []
    oldfilter = args.filter[0]
    
    arrays = np.broadcast(args.filter, args.dit, args.nint, args.bin)
    
    for filter, dit, nint, bin in arrays:
        ov = 60 / int(bin[-1]) # not squared, WFI electronics bug
        ag_ov = 15 if args.combinedoffset else 60 # AG reacquisition
        f_ov = 120 * (filter != oldfilter) # filter change 
        noffsets = nint - (getattr(args, 'origin') == 'F')
        time = (dit + ov) * nint + ag_ov * noffsets + f_ov
        tpltime.append(time)
        oldfilter = filter

    args.acqtime_s = acqtime
    args.acqtime = acqtime / 60
    args.tpltime_s = tpltime
    args.tpltime = [t / 60 for t in tpltime]
    args.obtime_s = acqtime + sum(tpltime) 
    args.obtime = args.obtime_s / 60


def wfi_post_parser(args):

    args.obs = 'obs' # unique observing template

    if args.offsets is None:
        args.offsets = types.OffsetList(0, 0)
        args.autodither = 'T'
    else:
        args.autodither = 'F'
  
    if args.ag == "auto":
    
        if max(args.dit) > 45:

            # absolute offsets to determine if combineoffset holds (1/4 chip max) 

            ra = np.cumsum([args.initoffset.ra, *args.offsets.ra])
            dec = np.cumsum([arg.initoffset.dec, *args.offsets.dec])

            args.ag = 'T'
            args.combinedoffsets = 'T' if max(dec) < 240 and max(ra) < 120 else 'F'

        else:

            args.ag = 'F'
            args.combinedoffsets = 'F'
    
    args.filter = [FILTER_ALIASES.get(f, f) for f in args.filter]
    args.filt = [shorten_filter(f) for f in args.filter] # short filter name

    wfi_exectime(args)

def add_wfi_arguments(parser):


    det = parser.add_argument_group(title='detector and instrument settings')

    det.add_argument(
        '--dit', nargs="+", metavar="(DIT | DIT_TPL1 ... DIT_TPLn)",
        type=types.range_type(float, 0, 43200), 
        help='exposure time (s)')
    det.add_argument(
        '--nint', nargs="+", metavar="(NINT | NINT_TPL1 ... NINT_TPLn)",
        type=types.range_type(int, 1, 20), 
        help='number of exposures')

    det.add_argument(
        '--filter', nargs="+", choices=FILTER_NAMES, metavar='(FILTER | FILTER_TPL1 ... FILTER_TPLn)',
        help=f'filter(s)')

    bin = det.add_mutually_exclusive_group()
    bin.add_argument(
        '--bin', nargs="+", default='1x1', 
        choices=['1x1', '2x2', '3x3', '1x2', '1x3'], 
        metavar='(BIN | BIN_TPL1 ... BIN_TPLn)',
        help='binning mode')
    bin.add_argument(
        '--1x1', action='store_const', const=['1x1'], dest='bin',
        help='use 1x1 binning mode')
    bin.add_argument(
        '--2x2', action='store_const', const=['1x1'], dest='bin',
        help='use 2x2 binning mode')
    bin.add_argument(
        '--3x3', action='store_const', const=['1x1'], dest='bin',
        help='use 3x3 binning mode')
    
    det.add_argument(
        '--obstype', metavar='TYPE', default='OBJECT',
        choices=['OBJECT', 'SKY', 'FLUX,STD', 'ASTROMETRY', 'OTHER'],
        help='Purpose of the observation.')
    
    settings = parser.add_argument_group(title='acquisition and offsets')

    tpl = settings.add_mutually_exclusive_group()
    tpl.add_argument(
        '--acq', default='preset',
        choices=['preset', 'movetopixel', 'movetogap'],
        help='Acquisition template'
    )
    tpl.add_argument(
        '--move-to-gap', action='store_const', const='movetogap', dest='acq',
        help='preset and centre target on a gap'
    )
    tpl.add_argument(
        '--move-to-pixel', action='store_const', const='movetopixel', dest='acq',
        help='preset and centre target on a pixel'
    )
    tpl.add_argument(
        '--preset', action='store_const', const='preset', dest='acq',
        help='preset blindly'
    )

    settings.add_argument(
        '--pixel', nargs="+", action=WfiPixel.action, 
        default=WfiPixel(4150, 3950), metavar="XPIX,YPIX",
        help='detector pixel to centre on in the move-topixel preset'
    )
    settings.add_argument(
        '--acqdit', default=10., type=types.range_type(float, 0, 43200), 
        metavar="DIT",
        help='acquisition DIT in seconds.'
    )
    
    settings.add_argument(
        '--initoffset', nargs="+", action=types.Offset.action,
        default=types.Offset(0, 0), metavar="RA,DEC",
        help='Initial offset before dithering pattern'
    )
    settings.add_argument(
        '--offsets', action=types.OffsetList.action, nargs="+",
        metavar='RA_EXP2,DEC_EXP2 ... RA_EXPn,DEC_EXPn',
        help='list of offsets in arcseconds. Default: automatic dithering adapted to sky position.'
    )
    
    settings.add_argument(
        '--origin', choices=['T', 'F'], default='T', metavar='T/F', 
        help='whether to return to origin after dithering pattern'
    )

    argparser.add_ag_parameters(parser)

WFI_TEMPLATES = dict(
    obd_preset = '''# Blind acquisition template

TPL.ID                      "WFI_img_acq_Preset"
TPL.NAME                    "Preset blindly ({acqtime:.1f} min)" # name in bob
TPL.MODE                    "" # unused
TEL.TARG.ALPHA              "{coo:r!obd}" # r.a. in [hmms]s.sss format 
TEL.TARG.DELTA              "{coo:d!obd}"  # dec in [dmms]s.sss format
TEL.TARG.EQUINOX            "{equinox:.1f}" # equinox of equatorial frame
TEL.TARG.EPOCH              "{epoch:.1f}" # epoch of target coordinates
TEL.TARG.ADDVELALPHA        "0.0" # differential tracking in r.a.
TEL.TARG.ADDVELDELTA        "0.0" # differential tracking in declination
TEL.TARG.PMA                "{pm:r!arcsec/yr}" # proper motion in r.a. ("/yr)
TEL.TARG.PMD                "{pm:d!arcsec/yr}"  # proper motion in dec ("/yr)
TEL.TARG.NAME               "{target}"  # target designation
TEL.AG.START                "{ag}" # use autoguiding?
TEL.PRESET.NEW              "T" # preset telescope?
INS.FILT1.NAME              "{filter[0]}" # filtre

''',
    obd_movetopixel = '''# Preset and centre target on a pixel

TPL.ID                      "WFI_img_acq_MoveToPixel"
TPL.NAME                    "Preset and centre on pixel ({acqtime:.1f} min)"
TPL.MODE                    ""
DET.WIN1.UIT1               "{acqdit}" # DIT of acquisition image (s)
DET.PIXELCOORD              "{pixel:obd}" # det. pixel to centre on target
TEL.TARG.ALPHA              "{coo:r!obd}" # r.a. in [hhmms]s.sss format
TEL.TARG.DELTA              "{coo:d!obd}" # declination in [dmms]s.sss format
TEL.TARG.EQUINOX            "{equinox:.1f}" # equinox of equatorial frame
TEL.TARG.EPOCH              "{epoch:.1f}" # epoch of target coordinates
TEL.TARG.ADDVELALPHA        "0.0" # differential tracking in r.a.
TEL.TARG.ADDVELDELTA        "0.0" # differential tracking in declination
TEL.TARG.PMA                "{pm:r!arcsec/yr}" # proper motion in r.a. ("/yr)
TEL.TARG.PMD                "{pm:d!arcsec/yr}" # proper motion in dec ("/yr)
TEL.TARG.NAME               "{target}" # target designation
TEL.AG.START                "{ag}" # use autoguiding?
TEL.PRESET.NEW              "T" # preset telescope?
INS.FILT1.NAME              "{filter[0]}" # filtre

''',
    obd_movetogap = '''# Preset and centre target on a gap

TPL.ID                      "WFI_img_acq_MoveToGap"
TPL.NAME                    "Preset and centre on gap ({acqtime:.1f} min)"
TPL.MODE                    ""
DET.WIN1.UIT1               "{acqdit}" # DIT of acquisition image (s)
TEL.TARG.ALPHA              "{coo:r!obd}" # r.a. in [hhmms]s.sss format
TEL.TARG.DELTA              "{coo:d!obd}" # declination in [dmms]s.sss format
TEL.TARG.EQUINOX            "{equinox:.1f}" # equinox of equatorial frame
TEL.TARG.EPOCH              "{epoch:.1f}" # epoch of target coordinates
TEL.TARG.ADDVELALPHA        "0.0" # differential tracking in r.a.
TEL.TARG.ADDVELDELTA        "0.0" # differential tracking in declination
TEL.TARG.PMA                "{pm:r!arcsec/yr}" # proper motion in r.a. ("/yr)
TEL.TARG.PMD                "{pm:d!arcsec/yr}" # proper motion in dec ("/yr)
TEL.TARG.NAME               "{target}" # target designation
TEL.AG.START                "{ag}" # use autoguiding?
TEL.PRESET.NEW              "T" # preset telescope?
INS.FILT1.NAME              "{filter[0]}" # filtre

''',
    obd_obs = '''# science template WFI_img_obs_Dither

TPL.ID                      "WFI_img_obs_Dither"
TPL.NAME                    "Dither with {filt} ({nint} x {dit:.0f} s -> {tpltime:.1f} min)" 
TPL.MODE                    "IMAGING"  
TPL.NEXP                    "{nint}" # number of exposures
DET.WIN1.UIT1               "{dit:.3f}" # integration time
DET.READ.CLKIND             "{bin}" # binning mode
SEQ.NEXPO                   "{nint}" # number of integrations
TEL.TARG.OFFSETALPHA        "{offsets:r}" # dither relative offsets in ra
TEL.TARG.OFFSETDELTA        "{offsets:d}" # dither relative offsets in dec
TEL.TARG.AUTODITHER         "{autodither}" # use predetermined dither pattern
TEL.TARG.INITOFFSETALPHA    "{initoffset:r}" # ra offset before dither pattern
TEL.TARG.INITOFFSETDELTA    "{initoffset:d}" # dec offset before dither pattern
TEL.COMBINED.OFFSET         "{combinedoffset}" # reacquire AG automatically after offset?
TEL.RETURN                  "{origin}" # offset to origin after last exposure
INS.FILT1.NAME              "{filter}" # filter name
DPR.TYPE                    "{obstype}" # purpose of observation

''')

_config.register_defaults(
    tel='2.2',
    ins='WFI',
    parser=add_wfi_arguments,
    check=wfi_check_parser,
    postparser=wfi_post_parser,
    templates=WFI_TEMPLATES,
)

def mkwfobs(cmdline=None):
    
    obkreator.create_obs(tel='2.2', ins='WFI', cmdline=cmdline)

