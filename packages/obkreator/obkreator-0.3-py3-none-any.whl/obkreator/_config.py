INSTRUMENT_CONFIG = {}

def register_defaults(*, tel, ins, parser, templates,
        check=None, postparser=None): 

    global INSTRUMENT_CONFIG

    INSTRUMENT_CONFIG[tel, ins] = dict(
        parser=parser, postparser=postparser, check=check, templates=templates
    )

def get_ins_parser_func(*, tel, ins):
    return INSTRUMENT_CONFIG[tel, ins]['parser']

def get_ins_post_parser_func(*, tel, ins):
    return INSTRUMENT_CONFIG[tel, ins]['postparser']

def get_ins_parser_check_func(*, tel, ins):
    return INSTRUMENT_CONFIG[tel, ins]['check']

def get_ins_templates(*, tel, ins):
    return INSTRUMENT_CONFIG[tel, ins]['templates']
