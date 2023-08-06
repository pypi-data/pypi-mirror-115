# MUD Runtime -- Object Entities.
#
from .. import Concretion, declareEventController, EventController

# from types import DictionaryType
DictionaryType = dict
# from new import classobj as newClassObject
from types import new_class

def populateNamespace(data):
    def doNamespacePopulate(ns):
        ns.update(data)
    return doNamespacePopulate

def newClassObject(name, bases, values):
    return new_class(name, bases, exec_body = populateNamespace(values))

# Overall identity constant.
class Undefined(object):
    def __repr__(self):
        return self.__class__.__name__
    __str__ = __unicode__ = __repr__

Undefined = Undefined()

# Design Pattern.
class Singleton(object):
    # This should be further specialized into 'Event' for runtime constructs.
    class Meta(type):
        def __new__(self, name, bases, values):
            cls = type.__new__(self, name, bases, values)
            if Singleton in bases:
                return cls

            ##    postvalues = {}
            ##    for name in values.keys():
            ##        if name in ['__module__', '__doc__']:
            ##            postvalues[name] = values[name]
            ##            del values[name]
            ##
            ##    inst = cls(name, **values)
            ##    inst.__dict__.update(postvalues)
            ##    return inst

            return cls(name, **values)

# Identity.
class Object(object):
    class _Meta:
        Attributes = []

        def __init__(self, *attributes, **kwd):
            self.Attributes = list(attributes) + list(kwd.items())

        @staticmethod
        def formatAttribute(instance, a, default = Undefined):
            def getAttribute(name):
                if callable(name):
                    return name(instance)

                if name.endswith('()'):
                    v = getattr(instance._Meta, name[:-2], default)
                    if callable(v):
                        return v(instance)
                else:
                    return getattr(instance, name, default)

                return Undefined

            if type(a) in (list, tuple):
                if len(a) == 2:
                    return '%s = %r' % (a[0], getAttribute(a[1]))
                if len(a) == 3:
                    return '%s = %r' % (a[0], getAttribute(a[1], a[2]))

            elif type(a) is str:
                return '%s = %r' % (a, getAttribute(a))

        @staticmethod
        def className(instance):
            return instance.__object_name__()

        @classmethod
        def instanceRepr(self, instance):
            meta = instance._Meta
            attribs = ', '.join(meta.formatAttribute(instance, a) for \
                                a in meta.Attributes)
            if attribs:
                return '<%s %s>' % (meta.className(instance), attribs)

            return '<%s>' % meta.className(instance)

    def __init__(self, name = Undefined):
        if name is not Undefined:
            self.__name = name

    def __repr__(self):
        return self._Meta.instanceRepr(self)
    def __str__(self):
        return self.__repr__()

    # This should go in the Meta.
    def __object_name__(self):
        try: return self.__name
        except AttributeError:
            return self.__class__.__name__

    @classmethod
    def instanceOf(self, other):
        return isinstance(other, self)

        ##    try: return issubclass(other.__class__, self)
        ##    except AttributeError:
        ##        return False

from .lookup import LookupObject
LookupClassObject = LookupObject

class Synthetic(Object, dict): # todo: determine if adding dict base type is stable
    class _Meta(Object._Meta):
        Attributes = Object._Meta.Attributes + ['members()']

        @staticmethod
        def members(instance):
            return ', '.join(map(str, list(instance.__dict__.keys())))

    def __init__(self, dict = None, **values):
        if not isinstance(dict, DictionaryType):
            assert dict is None
            dict = values
        else:
            dict.update(values)

        self.__dict__ = dict

    # todo: FromStructure and ToStructure methods like in WRLC

class Namespace(Synthetic):
    # XXX namespace traditionally has a dict pointing to self.
    pass

namespace = Namespace


# Component Event Model.
# todo: rename to `Instrument'
# todo: make Singleton behavior part of new, AutoInstrument class.
class Component(Singleton, Concretion, metaclass=Singleton.Meta):
    # Todo: Rename to Instrument?
    Module = 'bridge'

    def __init__(self, name, Module = None, **others):
        # Register this component class instance with bridge module.
        self.Target = others.get('Target', self)

        if Module is None:
            Module = self.Module

        self.bindToRuntime(Module) # system-dependent

        try: init = self.__instance_init__
        except AttributeError: pass
        else: init() # others['__init_args__']

    def __call__(self, ctlr, *args, **kwd):
        method = self.getTriggerFunction(ctlr.event_name)
        if callable(method):
            return method(ctlr, *args, **kwd)

    def __eq__(self, other):
        if self.sameClass(other):
            try:
                return self.__class__.__module__ == \
                         other.__class__.__module__ and \
                       self.__class__.__name__ == \
                         other.__class__.__name__

            except AttributeError:
                return False

    def getTriggerFunction(self, event_name):
        return getattr(self.Target, self.getTriggerName(event_name), None)
    def getTriggerName(self, event_name):
        return getTriggerName(event_name)

    def getEventNames(self, module):
        from ..events import getEventNames
        return getEventNames(module)


    DYNAMIC_TRIGGERS = False
    def bindToRuntime(self, Module = None):
        # separate EVENT_NAMES from Component
        # system-dependent
        # Module: ExtensionPoint

        from ..events import Binding

        if Module is 'bridge':
            from stuphos import getBridgeModule
            Module = getBridgeModule()

        binding = Binding(Module)
        self.boundControllers = []

        # XXX This makes only one spectrum of component to be built.
        # (that is, use of Component is only ever for interned-core
        # events and never for some secondary set of events)
        for event in self.getEventNames(Module):
            # What this is saying is that it won't bind to events that don't exist.
            if self.DYNAMIC_TRIGGERS or callable(self.getTriggerFunction(event)):
                ctlr = binding.getController(event)
                ctlr.registerHandler(self)
                self.boundControllers.append(ctlr)

    def __repr__(self):
        return '%s.%s (Component)' % (self.__module__, self.__class__.__name__)

    def __registry_delete__(self):
        for ctlr in self.boundControllers:
            ctlr.unregisterHandler(self)


def getTriggerName(event_name):
    return 'on%s%s' % (event_name[0].upper(), event_name[1:])

def newComponent(cls, name = None, **values):
    if name is None:
        # Unfortunately, it ends up taking up the module name that calls newClassObject.
        name = '%s.%s' % (cls.__module__, cls.__name__)

    # values['__instance_init__'] = cls.__init__
    # values['__init_args__'] = (args, kwd)
    return newClassObject(name, (Component, cls), values)

# This should be in events, but it relies on Singleton.
class DeclareEvent(Singleton, metaclass=Singleton.Meta):
    def __new__(self, *args, **kwd):
        return declareEventController(*args, **kwd)


# Memory management.
class writable(object):
    # Base class for emulated object attribute sets.
    def _setAttribute(self, name, value):
        return object.__setattr__(self, name, value)

class writeprotected(writable):
    # The preferred native object base class for constraining memory sets.

    def __setattr__(self, name, value):
        # Note: allowing all private sets (preceeding undescore) simplifies Pythonic
        # private variables becoming writable.  Now this becomes unsuitable for any-
        # thing other than expressing objects into the virtual environment (where private
        # members are already protected).
        if name.startswith('_') or name in getattr(self, '__public_members__', []):
            return self._setAttribute(name, value)

        raise AttributeError('Unwritable: %s' % name)

blockSetAttr = writeprotected

class representable:
    def __repr__(self):
        return '<%s>' % self.__class__.__name__

class extension:
    def __init__(self, object):
        self._object = object

wrapper = extension

def reprWrapper(self):
    return '<%s: type %s>' % (self.__class__.__name__,
                              type(self._object).__name__)

class Transparent(Object, wrapper):
    __init__ = extension.__init__
    __repr__ = reprWrapper

_transparent = Transparent

class ExceptionType(Object, wrapper):
    # More opaque than a transparent object.
    __repr__ = reprWrapper


# Execution Primitives.
class Procedure(Object):
    class Done(Exception, Object):
        pass

    # Note: This should probably define __call__ -> run(),
    # since that what a procedure does, which would simplify
    # heartbeat/engine code.

    class Interface(Object):
        # Revealed to the GIRL object runtime, proxies the local subroutine def
        # through the vm invocation instruction.
        def __init__(self, procedure):
            self._procedure = procedure


class Computer:
    # Instruction set.
    pass

class Source:
    pass


# Game-Level Objects.
class UnknownFlag(NameError):
    pass

class Bitvector(Object):
    # A pure implementation of the bitvector type in game module.
    class _Meta(Object._Meta):
        Attributes = Object._Meta.Attributes + ['set']

    def __init_subclass__(self, **kwd):
        pass

    def __init__(self, __bitv = 0, **bits):
        # This is an abstract base class.
        assert self.__class__ is not Bitvector

        self.__bitv = int(__bitv)
        for (name, value) in bits.items():
            setattr(self, name, bool(value))

        self.getUpperBitvNames()

    @classmethod
    def getUpperBitvNames(self):
        try: return self.__UPPER_BITVECTOR_NAMES
        except AttributeError:
            names = self.__UPPER_BITVECTOR_NAMES = \
                [n.upper() for n in self.BITVECTOR_NAMES]

        return names

    BITVECTOR_NAMES = []

    def isBitSet(self, bit):
        return bool(self.__bitv & bit)
    def getFlagBit(self, name):
        try: return (1 << self.getUpperBitvNames().index(name.upper()))
        except ValueError:
            raise UnknownFlag

    def isFlagSet(self, name):
        return self.isBitSet(self.getFlagBit(name))

    @property
    def names(self):
        return self.BITVECTOR_NAMES

    @property
    def set(self):
        return [name for name in self.names if self.isFlagSet(name)]

    @property
    def notset(self):
        return [name for name in self.names if not self.isFlagSet(name)]

    unset = nonset = notset

    def __getattr__(self, name):
        try: return self.isFlagSet(name)
        except UnknownFlag:
            return object.__getattribute__(self, name)

    def __setattr__(self, name, value):
        try: bit = self.getFlagBit(name)
        except UnknownFlag: return object.__setattr__(self, name, value)
        else: self.__bitv |= bit if value else ~bit

    def __int__(self):
        return int(self.__bitv)
    def __str__(self):
        return ', '.join(map(str, self.set))
    def __iter__(self):
        return iter(self.set)

class PromptPreferences(Bitvector):
    BITVECTOR_NAMES = ['Mail', 'DataRate']
