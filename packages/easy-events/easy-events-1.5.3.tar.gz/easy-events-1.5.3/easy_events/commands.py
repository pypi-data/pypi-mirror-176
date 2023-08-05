from inspect import getfullargspec
from ast import literal_eval

# import json
# from types import SimpleNamespace
# x = json.loads(data, object_hook=lambda _d: SimpleNamespace(**_d))


class Parameters:
    def __init__(self, data, prefix: str = "", lock: bool = False):
        self._prefix = prefix
        self._called = True
        self.command = data
        self.parameters = ""

        if not lock:
            self.revert()
        else:
            self.convert()

    def convert(self):
        check = False
        blank_prefix = False
        com = self.command

        if isinstance(self._prefix, str):
            check = str(self.command).startswith(self._prefix)
            blank_prefix = False if self._prefix else True

        elif isinstance(self._prefix, list):
            for pre in self._prefix:
                if str(self.command).startswith(pre):
                    check = True

                if check and pre == "":
                    blank_prefix = True

        if check and not blank_prefix:
            try:
                self.command = com.lower().split()[0][1:]
                self.parameters = " ".join(com.split()[1:])
            except Exception:
                self.command = com.lower()
                self.parameters = ""

        elif check and blank_prefix:
            self.command = com.lower().split()[0]
            self.parameters = " ".join(com.split()[1:])

        self._called = check

    def revert(self):
        done = False
        try:
            data = {"command": "", "parameters": ""}

            if isinstance(self.command, str) or isinstance(self.command, bytes):
                data = literal_eval(self.command)

            elif isinstance(self.command, list):
                if self.command:
                    data["command"] = self.command[0]

                if len(self.command) > 1:
                    data["parameters"] = self.command[1:]

            else:
                data = self.command

            self.command = data.get("command")
            self.parameters = data.get("parameters")

            done = True

            for key, value in data.items():
                if key not in ["command", "parameters"]:
                    setattr(self, key, value)

        except Exception:
            if not done:
                self.convert()

    def transform(self):
        return self.__dict__

    def clear(self):
        keys = [k for k in self.__dict__.keys()]
        for key in keys:
            delattr(self, key)

    def clean(self):
        del(self.command)
        del(self.parameters)
        del(self._prefix)
        del(self._called)

    def build_str(self):
        res = ""
        for key, value in self.__dict__.items():
            res += f"{key} : {value}\n"

        return res

    def __str__(self):
        return self.build_str()

    def setattr(self, key, value):
        setattr(self, key, value)

    def delattr(self, key):
        delattr(self, key)


class Event:
    def __init__(self, names: list, event: str, condition: callable = None, event_type: str = None):
        self.names = names
        self.event = event
        self.condition = condition
        self.type = event_type


class Decorator:
    def __init__(self):
        self.events = []
        self.command = self.event

    def command_exist(self, name: str):
        return name in self.get_events_names()

    def get_events_names(self, event_type: str = None):
        liste = []
        for ev in self.events:
            for name in ev.names:
                if not event_type:
                    liste.append(name)

                elif ev.type == event_type:
                    liste.append(name)

        return liste

    def get_types(self):
        liste = []
        for ev in self.events:
            liste.append(ev.type)

        liste = list(dict.fromkeys(liste))
        
        if None in liste:
            liste.remove(None)
        
        return  liste

    def get_events(self, event_type: str):
        liste = []
        for event in self.events:
            if not event_type:
                liste.append(event)

            elif event_type == event.type:
                liste.append(event)

        return liste

    def get_event(self, name: str):
        for event in self.events:
            if name in event.names:
                return event

    def event(self, aliases: list = None, condition: callable = None, type: str = None):
        if isinstance(aliases, str):
            aliases = [aliases]

        elif not aliases:
            aliases = []

        if not callable(condition):
            condition = None

        def add_command(command_funct):
            aliases.append(command_funct.__name__)
            al = list(dict.fromkeys(aliases))
            self.events.append(Event(al, command_funct, condition, type))
            return command_funct

        return add_command


class Commands(Parameters, Decorator):
    def __init__(self, prefix: str = "", lock: bool = False):
        Decorator.__init__(self)
        self.prefix = prefix
        self._lock = lock

    def build_arguments(self, function, arguments):
        values = getfullargspec(function)

        arg = values.args
        arg.pop(0)

        default = values.defaults
        ext_default = values.kwonlydefaults

        para = {}

        if default:
            default = list(default)
            for i in range(-1, -len(default)-1, -1):
                para[arg[i]] = default[i]

        ext = None

        if values.kwonlyargs:
            ext = values.kwonlyargs[0]
            arg.extend(values.kwonlyargs)

        s = len(arg)
        dico = {}

        if ext:
            if not (isinstance(arguments, list) or isinstance(arguments, dict)):
                arguments = arguments.split()

            sep = len(arguments) - s + 1

            if not sep:
                sep = 1

            for i in range(s):
                key = arg[i]

                if key != ext:
                    if isinstance(arguments, list):
                        try:
                            dico[key] = arguments.pop(0)
                        except IndexError:
                            if key in para.keys():
                                dico[key] = para[key]

                    elif isinstance(arguments, dict):
                        try:
                            dico[key] = arguments[key]
                        except KeyError:
                            if key in para.keys():
                                dico[key] = para[key]

                else:
                    li = []
                    if isinstance(arguments, list):
                        for _ in range(sep):
                            try:
                                li.append(arguments.pop(0))
                            except IndexError:
                                pass

                    elif isinstance(arguments, dict):
                        try:
                            li.append(arguments[key])
                        except KeyError:
                            pass

                    if not li and ext_default and ext_default.get(key):
                        li = [ext_default[key]]

                    dico[key] = li

        elif s:
            if isinstance(arguments, list):
                dico = {key: value for key, value in zip(arg, arguments[0:s])}

            elif isinstance(arguments, dict):
                for key in arg:
                    try:
                        dico[key] = arguments[key]
                    except KeyError:
                        if key in para.keys():
                            dico[key] = para[key]
            else:
                dico = {key: value for key, value in zip(arg, arguments.split()[0:s])}

        return dico

    def execute(self, data: Parameters):
        event = self.get_event(data.command)
        com = event.event
        con = event.condition

        dico = self.build_arguments(com, data.parameters)
        data.clean()

        if (con and con(data)) or not con:
            return com(data, **dico)

    def process_data(self, data, lock: bool = None):
        none = type(None)

        if isinstance(lock, none):
            lock = self._lock

        args = data

        if isinstance(data, Parameters):
            pass
        elif not str(type(data)) == "<class 'easy_events.async_commands.Parameters'>":
            args = Parameters(data, self.prefix, lock)

        if isinstance(args.command, str) and self.command_exist(args.command) and args._called:
            try:
                val = self.execute(args)
            except Exception as e:
                raise e
                return f"{type(e)}: {e}"

            if isinstance(val, Parameters):
                return val.transform()

            return val

        if isinstance(data, bytes):
            return data.decode()

        return data


if __name__ == "__main__":
    client = Commands()

    @client.event("event_name", type="event")
    def event_name(data):
        print("test1")
        print("data", data)

    @client.event("second_event")
    def test2(data, arg1, arg2, *, arg3):
        print("test2", arg1, arg2, arg3)
        print("data", data)

    client.process_data("event_name")
    client.process_data({"command": "second_event", "parameters": ["arg1", "arg2", "arg3", "arg4"]})
    client.process_data(Parameters("test1"))
    print(client.get_events_names("event"))
    print(client.get_types())

    data = Parameters("test1")
    data.client = "hello"
    client.process_data(data)
