from .argparser import get_parser, parse_cmdline, post_parser, iter_targets
from . import query 
from . import feros
from . import grond
from . import _config
from . import obheader


import sys
import os
import shlex
import numpy as np

#DEBUG
import argparse

def create_ob(tel, ins, args):

    # tune DITs, AG settings, and other tunings that command line cannot offer
    # so freely
    args.target = args.target[0]
    post_parser(args, tel=tel, ins=ins)    
    
    fmt = args.obformat
    filename = os.path.join(args.obdir, f'{args.obname}.{fmt}')
    
    # use a dictionary now
    args = vars(args)

    # determine templates for OB
    header = obheader.HEADER
    templates = _config.get_ins_templates(tel=tel, ins=ins)
   
    # OB header and acquisition 
    fmt = args['obformat']
    acq_name = f'{fmt}_{args["acq"]}'
    ob = header[fmt].format(**args) 
    ob += templates[acq_name].format(**args)

    # If any argument is an array, loop on arrays to produce more than one 
    # template

    try:
        values = np.broadcast_arrays(*args.values())
    except Exception as e:
        msg = 'number of arguments to options do not conform with each other'
        raise type(e)(msg)
        
    values = [np.atleast_1d(v) for v in values]
    nargs = len(values[0])
    args = {n: v for n, v in zip(args, values)}

    for i in range(nargs):
        args_i = {n: v[i] for n, v in args.items()}
        obs_name = f'{fmt}_{args_i["obs"]}'
        ob += templates[obs_name].format(**args_i)

    with open(filename, 'w') as out:
        out.write(ob)

    return filename

def create_obs(tel, ins, cmdline=None):
    
    if isinstance(cmdline, str):
        progname, *cmdline = shlex.split(cmdline)
    else:
        progname = os.path.basename(sys.argv[0])

    parser = get_parser(progname, tel=tel, ins=ins)
    args = parse_cmdline(parser, cmdline, tel=tel, ins=ins)
    
    # check run ID (gives instrument & PI) and load target list 

    try:

        query.lookup_pid(args, tel=tel, ins=ins)

    except Exception as e:

        print(f"{progname}: {e}")
        sys.exit()

    # run the command for each target

    cmdline0 = {n: v for n, v in vars(args).items() if v is not None
                    and n not in ['table', 'tableformat']}

    targets = iter_targets(parser, args)
    for i, target in enumerate(targets, start=1):
   
        # command line arguments are overridden by what is read from
        # target file
        cmdline = cmdline0 | target

        # parse command line made from arguments
        cmdline = [str(e) for n, v in cmdline.items() 
                                    for e in ['--'+n, *np.atleast_1d(v)]]   
        # print(f"#{i}", shlex.join([progname, *cmdline]))
        try:
            args = parse_cmdline(parser, cmdline, tel=tel, ins=ins)
            args.prog = progname
        except (SystemExit, Exception) as e:
            cmdline = shlex.join(cmdline)
            print(f'Error processing target #{i}: {e}')
            raise e
 
        # create the OB
        filename = create_ob(tel, ins, args)
        print(f'OB #{i} created: {filename}')
