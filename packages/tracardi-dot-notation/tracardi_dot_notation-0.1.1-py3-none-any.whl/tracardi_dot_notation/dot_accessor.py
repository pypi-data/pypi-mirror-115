from dotty_dict import dotty


class DotAccessor:

    def __init__(self, profile=None, session=None, payload=None, event=None, flow=None):
        if flow is None:
            self.flow = {}
        else:
            self.flow = dotty(flow.dict())

        if event is None:
            self.event = {}
        else:
            self.event = dotty(event.dict())

        if payload is None:
            self.payload = {}
        else:
            self.payload = dotty(payload)

        if session is None:
            self.session = {}
        else:
            self.session = dotty(session.dict())

        if profile is None:
            self.profile = {}
        else:
            self.profile = dotty(profile.dict())

    def __delitem__(self, key):
        if key.startswith('profile@'):
            key = key[len('profile@'):]
            del self.profile[key]
        elif key.startswith('session@'):
            raise KeyError("Could not set session, session is read only")
        elif key.startswith('flow@'):
            raise KeyError("Could not set flow, flow is read only")
        elif key.startswith('payload@'):
            key = key[len('payload@'):]
            del self.payload[key]
        elif key.startswith('event@'):
            raise KeyError("Could not delete event, event is read only")
        else:
            raise ValueError(
                "Invalid dot notation. Accessor not available. " +
                "Please start dotted path with one of the accessors: [profile@, session@, payload@, event@] ")

    def __setitem__(self, key, value):
        if key.startswith('profile@'):
            key = key[len('profile@'):]
            self.profile[key] = self.__getitem__(value) if not isinstance(value, dict) else value
        elif key.startswith('session@'):
            raise KeyError("Could not set session, session is read only")
        elif key.startswith('flow@'):
            raise KeyError("Could not set flow, flow is read only")
        elif key.startswith('payload@'):
            key = key[len('payload@'):]
            self.payload[key] = self.__getitem__(value) if not isinstance(value, dict) else value
        elif key.startswith('event@'):
            raise KeyError("Could not set event, event is read only")
        else:
            raise ValueError(
                "Invalid dot notation. Accessor not available. " +
                "Please start dotted path with one of the accessors: [profile@, session@, payload@, event@] ")

    def __getitem__(self, dot_notation):
        if isinstance(dot_notation, str):
            if dot_notation.startswith('flow@'):
                value = dot_notation[len('flow@'):]
                try:
                    return self.flow[value]
                except KeyError:
                    raise KeyError("Invalid dot notation. Could not find value for `{}` in flow.".format(value))
            elif dot_notation.startswith('profile@'):
                value = dot_notation[len('profile@'):]
                try:
                    return self.profile[value]
                except KeyError:
                    raise KeyError("Invalid dot notation. Could not find value for `{}` in profile.".format(value))
            elif dot_notation.startswith('session@'):
                value = dot_notation[len('session@'):]
                try:
                    return self.session[value]
                except KeyError:
                    raise KeyError("Invalid dot notation. Could not find value for `{}` in session.".format(value))
            elif dot_notation.startswith('payload@'):
                value = dot_notation[len('payload@'):]
                try:
                    return self.payload[value]
                except KeyError:
                    raise KeyError("Invalid dot notation. Could not find value for `{}` in payload.".format(value))
            elif dot_notation.startswith('event@'):
                value = dot_notation[len('event@'):]
                try:
                    return self.event[value]
                except KeyError:
                    raise KeyError("Invalid dot notation. Could not find value for `{}` in event.".format(value))
        return dot_notation

    def __contains__(self, item):
        try:
            self.__getitem__(item)
            return True
        except (KeyError, TypeError):
            return False

    @staticmethod
    def get(dot_notation, payload, prefix):
        value = dot_notation[len(prefix + '@'):]
        try:
            return payload[value]
        except KeyError:
            raise KeyError("Could not find value for `{}` in {}".format(value, prefix))

    @staticmethod
    def set(key, value, payload, prefix):
        key = key[len(prefix + '@'):]
        payload[key] = value
