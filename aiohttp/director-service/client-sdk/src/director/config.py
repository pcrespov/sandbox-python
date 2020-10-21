import functools

import trafaret as _t

import trafaret_config
import trafaret_config.commandline


OPTIONS_SCHEMA = _t.Dict({
    _t.Key("postgres"):
    _t.Dict({
        "database": _t.String(),
        "user": _t.String(),
        "password": _t.String(),
        "host": _t.String(),
        "port": _t.Int(),
        _t.Key("minsize", default=1 ,optional=True): _t.Int(),
        _t.Key("maxsize", default=4, optional=True): _t.Int(),
    }),
    _t.Key("host"): _t.IP,
    _t.Key("port"): _t.Int(),
})


# TODO: override function sfrom trafaret_config and bind schema

commandline = trafaret_config.commandline
commandline.config_from_options = functools.partial(trafaret_config.commandline.config_from_options, trafaret=OPTIONS_SCHEMA)
read_and_validate = functools.partial(trafaret_config.read_and_validate, trafaret=OPTIONS_SCHEMA)
parse_and_validate = functools.partial(trafaret_config.parse_and_validate, trafaret=OPTIONS_SCHEMA)