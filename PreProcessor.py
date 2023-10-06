# Version 2.2.2
import re
import pickle
import copy
import io
import requests
import yaml


class NoAliasDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True


class FUNC:
    def __init__(self, function, container):
        self.__function__ = function
        self.__container__ = container

    def __call__(self, **kwargs):
        for i in range(len(self.__container__) - 1, -1, -1):
            self.__container__[i].__getattribute__(self.__function__)(**kwargs)


class SELECT_ALL(list):
    def __init__(self, list: list):
        super().__init__(list)

    def __getattr__(self, item):
        return FUNC(item, self)


class SELECT_EMPTY:
    def __init__(self):
        def empty_function(*args, **kwargs):
            pass

        self.empty_function = empty_function

    def __len__(self):
        return 0

    def __getattr__(self, item):
        return self.empty_function


class LIST(list):
    def __init__(self, container=None, __iterable=None):
        list.__init__([])
        if not container == None:
            self.__container__ = container
        if not __iterable == None:
            self.extend(__iterable)

    def append(self, __object):
        __object.__setattr__("__container__", self.__container__)
        return super().append(__object)

    def insert(self, __index, __object):
        __object.__setattr__("__container__", self.__container__)
        return super().insert(__index, __object)

    def extend(self, __iterable):
        for i in __iterable:
            i.__setattr__("__container__", self.__container__)
        return super().extend(__iterable)

    def __setitem__(self, index, value):
        if isinstance(index, slice):
            for i in value:
                i.__setattr__("__container__", self.__container__)
        else:
            value.__setattr__("__container__", self.__container__)
        super().__setitem__(index, value)


def select_all(obj, reverse=False, **kwargs):
    result = []
    for i in obj:
        tmp = True
        for j in kwargs.keys():
            if j.startswith("re_"):
                if not re.search(kwargs[j], getattr(i, j[3:])):
                    tmp = False
                    break
            else:
                if not kwargs[j] == getattr(i, j):
                    tmp = False
                    break
        if tmp and not reverse:
            result.append(i)
        elif not tmp and reverse:
            result.append(i)
    return SELECT_ALL(result)


def select(obj, reverse=False, **kwargs):
    for i in obj:
        tmp = True
        for j in kwargs.keys():
            if j.startswith("re_"):
                if not re.search(kwargs[j], getattr(i, j[3:])):
                    tmp = False
                    break
            else:
                if not kwargs[j] == getattr(i, j):
                    tmp = False
                    break
        if tmp and not reverse:
            return i
        elif not tmp and reverse:
            return i
    return SELECT_EMPTY()


def pop_front(obj, item):
    obj.insert(0, item)


def pop_back(obj, item):
    obj.append(item)


def extend_back(obj, iterable):
    if not isinstance(iterable, list):
        raise ValueError("YAML List Expected")
    obj.extend(iterable)


def extend_front(obj, iterable):
    if not isinstance(iterable, list):
        raise ValueError("YAML List Expected")
    obj[0:0] = iterable


class Rule:
    def __init__(self, YAML: str = None, type: str = None, argument: str = None, policy: str = None, no_resolve: bool = False):
        if (type == None or argument == None or policy == None) and YAML == None:
            raise ValueError
        elif YAML == None:
            self.type = type
            self.argument = argument
            self.policy = policy
            self.no_resolve = no_resolve
        else:
            soup = yaml.load(YAML.encode("utf-8"), Loader=yaml.Loader)
            if isinstance(soup, list):
                soup = soup[0]
            self.YAML = soup

    @property
    def no_resolve(self):
        return self.no_resolve

    @no_resolve.setter
    def no_resolve(self, no_resolve: bool):
        if no_resolve:
            self._no_resolve = "no-resolve"
        else:
            self._no_resolve = ""

    @property
    def YAML(self):
        return ",".join(filter(bool, [self.type, self.argument, self.policy, self._no_resolve]))

    @YAML.setter
    def YAML(self, YAML: str):
        tmp = YAML.split(",")
        if "no-resolve" in tmp:
            self.no_resolve = True
            tmp.remove("no-resolve")
        else:
            self.no_resolve = False

        if len(tmp) == 3:
            self.type = tmp[0]
            self.argument = tmp[1]
            self.policy = tmp[2]
        else:
            self.type = None
            self.argument = tmp[0]
            self.policy = tmp[1]

    def delete(self):
        try:
            self.__container__.Rules.remove(self)
        except:
            pass

    def __repr__(self):
        return f"<PreProcessor.Rule object {self.YAML} at {hex(id(self))}>"

    def BATCH(YAML: str) -> list:
        soup = yaml.load(YAML.encode("utf-8"), Loader=yaml.Loader)
        if isinstance(soup, list):
            return [Rule(i) for i in soup]
        else:
            raise ValueError("YAML List Expected")


class Proxy:
    def __init__(self, DICT: dict = None, YAML: str = None):
        if DICT:
            self.DICT = DICT
        elif YAML:
            soup = yaml.load(YAML.encode("utf-8"), Loader=yaml.Loader)
            if isinstance(soup, list):
                soup = soup[0]
            self.DICT = soup
        else:
            raise ValueError

    @property
    def name(self):
        return self.DICT["name"]

    @name.setter
    def name(self, name: str):
        if isinstance(self.__container__, ProxyGroup):
            __container__ = self.__container__.__container__
        elif isinstance(self.__container__, Config):
            __container__ = self.__container__
        foregone = self.DICT["name"]
        if not foregone == name:
            self.DICT["name"] = name
            for i in range(len(__container__.ProxyGroups) - 1, -1, -1):
                for j in __container__.ProxyGroups[i].proxies:
                    if j.name == foregone:
                        j.name = name

    def delete(self, globally: bool = False):
        try:
            if isinstance(self.__container__, ProxyGroup):
                self.__container__.proxies.remove(self)
            elif isinstance(self.__container__, Config):
                globally = True
        except:
            pass
        if globally:
            try:
                if isinstance(self.__container__, ProxyGroup):
                    __container__ = self.__container__.__container__
                elif isinstance(self.__container__, Config):
                    __container__ = self.__container__
                for i in range(len(__container__.ProxyGroups) - 1, -1, -1):
                    for j in range(len(__container__.ProxyGroups[i].proxies) - 1, -1, -1):
                        if __container__.ProxyGroups[i].proxies[j].name == self.name:
                            __container__.ProxyGroups[i].proxies.pop(j)
                for i in range(len(__container__.Proxies) - 1, -1, -1):
                    if __container__.Proxies[i].name == self.name:
                        __container__.Proxies.pop(i)
            except:
                pass

    def __repr__(self):
        return f"<PreProcessor.Proxy object {self.name} at {hex(id(self))}>"

    def BATCH(YAML) -> list:
        soup = yaml.load(YAML.encode("utf-8"), Loader=yaml.Loader)
        if isinstance(soup, list):
            return [Proxy(i) for i in soup]
        else:
            raise ValueError("YAML List Expected")


class Embedded:
    DIRECT = Proxy(DICT={"name": "DIRECT"})
    REJECT = Proxy(DICT={"name": "REJECT"})


class Config:
    def __init__(self, Url: str = None, YAML: str = None, File: io.TextIOWrapper = None, DICT: dict = None, UA="Clash/1.11.0"):
        self._bypass = ("DICT", "Proxies", "ProxyGroups", "Rules", "YAML", "_DICT",
                        "_Proxies", "_ProxyGroups", "_Rules", "_meta", "__container__")
        self._meta = {}
        self._Rules = LIST(self)
        self._ProxyGroups = LIST(self)
        self._Proxies = LIST(self)
        self._DICT = {}
        self._meta["headers"] = {}
        if DICT:
            self.DICT = DICT
        elif Url:
            res = requests.get(Url, headers={"user-agent": UA})
            try:
                self._meta["headers"]["subscription-userinfo"] = res.headers["subscription-userinfo"]
            except:
                pass
            try:
                self._meta["headers"]["profile-update-interval"] = res.headers["profile-update-interval"]
            except:
                pass
            try:
                self._meta["headers"]["profile-web-page-url"] = res.headers["profile-web-page-url"]
            except:
                pass
            self.YAML = res.text
        elif YAML:
            self.YAML = YAML
        elif File:
            self.YAML = File.read()
        else:
            raise ValueError

    def __setattr__(self, __name: str, __value):
        if __name == "_bypass" or __name in self._bypass:
            object.__setattr__(self, __name, __value)
        else:
            self._meta[__name] = __value

    def __getattr__(self, __name: str):
        if __name == "_bypass" or __name in self._bypass:
            return object.__getattribute__(self, __name)
        else:
            return self._meta[__name]

    @property
    def Proxies(self):
        return self._Proxies

    @Proxies.setter
    def Proxies(self, Proxies: list):
        self._Proxies = LIST(self, Proxies)

    @property
    def ProxyGroups(self):
        return self._ProxyGroups

    @ProxyGroups.setter
    def ProxyGroups(self, ProxyGroups: list):
        self._ProxyGroups = LIST(self, ProxyGroups)

    @property
    def Rules(self):
        return self._Rules

    @Rules.setter
    def Rules(self, Rules: list):
        self._Rules = LIST(self, Rules)

    def getProxies(self, groups: bool = False, embedded: bool = False):
        result = self.Proxies
        if groups:
            result += [
                Proxy(DICT={"name": i.name})
                for i in self.ProxyGroups
            ]
        if embedded:
            result += [
                Embedded.DIRECT,
                Embedded.REJECT
            ]
        return result

    def mixin(self, YAML: str = None, DICT: dict = None):
        if DICT:
            YAML = yaml.dump(self.DICT, Dumper=NoAliasDumper)
        elif YAML:
            pass
        else:
            raise ValueError()
        self.YAML = self.YAML + "\n" + YAML

    @property
    def DICT(self):
        self._DICT["proxies"] = [i.DICT for i in self.Proxies]
        self._DICT["proxy-groups"] = [i.DICT for i in self.ProxyGroups]
        self._DICT["rules"] = [i.YAML for i in self.Rules]
        return self._DICT

    @DICT.setter
    def DICT(self, DICT: dict):
        self._DICT = DICT
        for i in self._DICT["proxy-groups"]:
            self.ProxyGroups.append(ProxyGroup(DICT=i))
        for i in self._DICT["proxies"]:
            self.Proxies.append(Proxy(DICT=i))
        for i in self._DICT["rules"]:
            self.Rules.append(Rule(YAML=i))

    @property
    def YAML(self):
        return yaml.dump(self.DICT, Dumper=NoAliasDumper)

    @YAML.setter
    def YAML(self, YAML: str):
        self.DICT = yaml.load(YAML.encode("utf-8"), Loader=yaml.Loader)

    def strip(self):
        for i in self.ProxyGroups:
            if len(i.proxies) == 0:
                i.delete()


class ProxyGroup:
    def __init__(self, DICT: dict = None, YAML: str = None):
        if DICT:
            self.DICT = DICT
        elif YAML:
            soup = yaml.load(YAML.encode("utf-8"), Loader=yaml.Loader)
            if isinstance(soup, list):
                soup = soup[0]
            self.DICT = soup
        else:
            raise ValueError

    @property
    def proxies(self):
        return self._proxies

    @proxies.setter
    def proxies(self, proxies: list[Proxy]):
        self._proxies = LIST(self, proxies)

    @property
    def DICT(self):
        self._DICT["proxies"] = [i.name for i in self._proxies]
        return self._DICT

    @DICT.setter
    def DICT(self, DICT: dict):
        self._DICT = DICT
        self.proxies = [Proxy(DICT={"name": i.name}) if isinstance(
            i, Proxy) else Proxy(DICT={"name": i}) for i in self._DICT["proxies"]]

    @property
    def name(self):
        return self._DICT["name"]

    @name.setter
    def name(self, name: str):
        foregone = self._DICT["name"]
        if not foregone == name:
            self._DICT["name"] = name
            try:
                for i in range(len(self.__container__.ProxyGroups) - 1, -1, -1):
                    for j in self.__container__.ProxyGroups[i].proxies:
                        if j.name == foregone:
                            j.name = name
                for i in self.__container__.Rules:
                    if i.policy == foregone:
                        i.policy = name
            except:
                pass

    def delete(self, policy: str = None):
        if policy == None:
            try:
                for i in range(len(self.__container__.Rules) - 1, -1, -1):
                    if self.__container__.Rules[i].policy == self.name:
                        self.__container__.Rules[i].delete()
            except:
                pass
        else:
            try:
                for i in range(len(self.__container__.Rules)):
                    if self.__container__.Rules[i].policy == self.name:
                        self.__container__.Rules[i].policy = policy
            except:
                pass
        try:
            self.__container__.ProxyGroups.remove(self)
        except:
            pass
        try:
            for i in range(len(self.__container__.ProxyGroups) - 1, -1, -1):
                select(
                    self.__container__.ProxyGroups[i].proxies, False, name=self.name).delete()
        except:
            pass

    def __repr__(self):
        return f"<PreProcessor.ProxyGroup object {self.name} at {hex(id(self))}>"

    def BATCH(YAML: str) -> list:
        soup = yaml.load(YAML.encode("utf-8"), Loader=yaml.Loader)
        if isinstance(soup, list):
            return [ProxyGroup(i) for i in soup]
        else:
            raise ValueError("YAML List Expected")


def loadsConfig(bytes: bytes) -> Config:
    obj = pickle.loads(bytes)
    r = Config(DICT=obj[0])
    r._meta = obj[1]
    return r


def dumpsConfig(config: Config) -> bytes:
    return pickle.dumps((config.DICT, config._meta))


def deepcopy(config: Config) -> Config:
    r = Config(DICT=copy.deepcopy(config.DICT))
    r._meta = copy.deepcopy(config._meta)
    return r
