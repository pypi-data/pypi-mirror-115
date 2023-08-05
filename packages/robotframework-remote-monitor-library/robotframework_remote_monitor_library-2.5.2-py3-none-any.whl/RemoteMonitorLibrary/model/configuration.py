from threading import Event

from robot.utils import DotDict
from robot.utils.robottime import timestr_to_secs

from RemoteMonitorLibrary.utils.sys_utils import get_error_info

DEFAULT_INTERVAL = 1
DEFAULT_CONNECTION_INTERVAL = 60
DEFAULT_FAULT_TOLERANCE = 10


class Configuration:
    mandatory_fields = {
        'alias': (True, None, str, str),
        'host': (True, None, str, str),
        'username': (True, None, str, str),
        'password': (False, '', str, str),
        'port': (False, 22, int, int),
        'certificate': (False, None, str, str),
        'interval': (False, DEFAULT_INTERVAL, timestr_to_secs, (int, float)),
        'fault_tolerance': (False, DEFAULT_FAULT_TOLERANCE, int, int),
        'event': (False, Event(), Event, Event),
        'timeout': (True, DEFAULT_CONNECTION_INTERVAL, timestr_to_secs, (int, float))
    }

    def __init__(self, **kwargs):
        self._parameters = DotDict()
        err = []
        attr_list = set(list(kwargs.keys()) + list(self.mandatory_fields.keys()))
        for attr in attr_list:
            try:
                mandatory, _, _, _ = self.mandatory_fields.get(attr, (False, None, None, None))
                if mandatory:
                    assert attr in kwargs.keys(), f"Mandatory parameter '{attr}' missing"
                self._set_parameter(attr, kwargs.get(attr, None))
            except AssertionError as e:
                err.append(f"{e}")
            except Exception as e:
                f, l = get_error_info()
                err.append(f"Unexpected error occurred during handle parameter '{attr}'; File: {f}:{l} - Error: {e}")

        assert len(err) == 0, "Following fields errors occurred:\n\t{}".format('\n\t'.join(err))

    def _set_parameter(self, parameter, value):
        attr_template = self.mandatory_fields.get(parameter, None)
        assert attr_template, f"Unknown parameter '{parameter}' provided"
        _, default, formatter, type_ = attr_template
        if type_:
            if value:
                param_value = formatter(value) if not isinstance(value, type_) else value
            else:
                param_value = default
        else:
            param_value = value
        self._parameters[parameter] = param_value

    @property
    def parameters(self):
        return self._parameters

    @property
    def alias(self):
        return self.parameters.alias

    def update(self, dict_: dict = None, **kwargs):
        dict_ = dict_ or {}
        dict_.update(**kwargs)
        unexpected = {}
        for name, value in dict_.items():
            try:
                self._set_parameter(name, value)
            except AssertionError:
                unexpected.update({name: value})
        return unexpected

    def clone(self):
        return type(self)(**self.parameters)

