HEADER = dict(
    obd = '''# Observing Block description (.obd) written by {prog}

# Standard parameter file header

PAF.HDR.START           ; # Marks start of header
PAF.TYPE                "OB Description"; # Type of parfile
PAF.ID                  ""; # Unused
PAF.NAME                ""; # Unused
PAF.DESC                ""; # Unused
PAF.CRTE.NAME           "BOB"; # Broker for OBs
PAF.CRTE.DAYTIM         "{date}"; # Date+time of creation
PAF.LCHG.NAME           ""; # Unused
PAF.LCHG.DAYTIM         "{date}"; # Date+time of last change
PAF.CHCK.NAME           ""; # Unused
PAF.CHCK.DAYTIM         ""; # Unused
PAF.CHCK.CHECKSUM       ""; # Unused
PAF.HDR.END             ; # Marks end of header

# Observing Block 

OBS.ID                  "{obid}" # observing block ID
OBS.NAME                "{obname}" # observing block name
OBS.GRP                 "0" # Unused
OBS.PROG.ID             "{pid}" # ESO programme ID
OBS.PI-COI.ID           "0" # User ID 
OBS.PI-COI.NAME         "{pi}" # lead researcher (Surname, I.)
OBS.EXECTIME            "{obtime_s:.0f}" # expected execution time (s)
OBS.OBSERVER            "{observer}" # observer
OBS.TARG.NAME           "{target}" # target designation

''',
    obx = '''name                            "{name}"
userComments                    ""
InstrumentComments              ""
userPriority                    "{priority}"
type                            "O"

TARGET.NAME                     "{target}"
propRA                          "{pm:r!arcsec/yr}"
propDec                         "{pm:d!arcsec/yr}"
diffRA                          "0.0"
diffDec                         "0.0"
equinox                         "J{equinox:.1f}"
epoch                           "{epoch:.1f}"
ra                              "{coo:r!obx}"
dec                             "{coo:d!obx}"

CONSTRAINT.SET.NAME             "No Name"
seeing                          "{seeing:.1f}"
sky_transparency                "{transparency}"
air_mass                        "{airmass:.1f}"
fractional_lunar_illumination   "{fli:.1f}"
moon_angular_distance           "{moondist:.1f}"
strehlratio                     "0.0"
twilight                        "0"
watervapour                     "0.0"
atm                             "no constraint"
contrast                        "0.0"
description                     ""

OBSERVATION.DESCRIPTION.NAME    "{obdesc}"
instrument                      "{ins}"

''')
