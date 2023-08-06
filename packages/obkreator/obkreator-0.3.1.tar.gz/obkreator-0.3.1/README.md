## Brief intro

### Purpose

Create ESO observing blocks from a list of targets. Instrument supported: WFI, FEROS, GROND at 2.2m telescope.


### Installation

It is packaged as [obkreator](https://pypi.org/project/obkreator/).

Site-wide installation will be performed with `sudo -H pip3 install obkreator` on unix-like systems. At a user level, within a [virtual environment](https://docs.python.org/3/library/venv.html "venv package"), `pip3 install obkreator`. 

### Short examples

Create FEROS OBs with 2 × 10 min integrations for a few SIMBAD targets.

```sh

> mkfrsob --target "HD 10" "HD 20" "HD 30" --objcal --dit 600 --nint 2 --pid '0107.A-9032(A)'
0107.A-9032(A): 2.2/FEROS observations by GREDEL, R
Coordinates have been queried from SIMBAD
OB #1 created: OB/FEROS-2.2/HD10.obd
OB #2 created: OB/FEROS-2.2/HD20.obd
OB #3 created: OB/FEROS-2.2/HD30.obd
 
```

Create GROND OBs with several templates

```sh
> mkgrndob --target 'HD 1' 'HD 2' 'HD 3' --tpltype 4m4td 8m4td 20m4td --pid '0107.A-9033(A)' --pi 'Doe, J.'
0107.A-9033(A): 2.2/GROND observations by Doe, J. under GREDEL, R PID
Coordinates have been queried from SIMBAD
OB #1 created: OB/GROND-2.2/HD1.obd
OB #2 created: OB/GROND-2.2/HD2.obd
OB #3 created: OB/GROND-2.2/HD3.obd
```

Create WFI OBs from information in a table
```sh

> cat <<EOF >WFI.dat
heredoc> target   ag    dit             nint filter       acq       acqdit offsets
heredoc> ------ ------  --------------- ---- ---------- ----------- ------ -------------       
heredoc> HD 1   auto    100,50,50,20,10    4 U,B,V,Rc,I movetopixel    200
heredoc> HD 2           50 300          10 2 V,Halpha
heredoc> HD 3   manual  20              2    Rc                            10,20 900,900
heredoc> EOF
> mkwfob --pid '0107.A-9031(A)' --table WFI.dat
0107.A-9031(A): 2.2/WFI observations by GREDEL, R
Coordinates have been queried from SIMBAD
3 OBs to be generated using table
Columns are: target, coo, pm, ag, dit, nint, filter, acq, acqdit, offsets
OB #1 created: OB/WFI-2.2/HD1.obd
OB #2 created: OB/WFI-2.2/HD2.obd
OB #3 created: OB/WFI-2.2/HD3.obd
>
```
