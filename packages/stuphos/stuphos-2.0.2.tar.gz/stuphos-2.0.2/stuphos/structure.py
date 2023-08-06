# mud.management.structure

# XXX upgrade this to use lang.document.structural
# from op.runtime.structural.document import Submapping, Core
from stuphos.language.document.structural import Submapping, Core

from stuphos.runtime import Object
from stuphos.runtime.architecture.api import writeprotected, extension
from stuphos.etc.tools.strings import renderTemplate
from stuphos.etc.tools.logs import tracebackString, exceptionHeader
from stuphos.etc.tools import isYesValue
from stuphos.kernel import Subroutine, grammar, Girl, Script, executeGirl, newModuleTask
from stuphos.kernel import vmNewMapping, AutoMemoryMapping, AutoMemorySequence, Processor
from stuphos.kernel import vmNewSequence, vmCurrentTask, BypassReturn, MemorySequence
from stuphos.kernel import MemoryMapping, Instance, protectedMemoryCopy
from stuphos import getConfig

from queue import Queue
import json


class MarshalizedObject(writeprotected, extension):
    def __init__(self, object):
        extension.__init__(self, json.dumps(object))

    def __call__(self):
        return protectedMemoryCopy(vmCurrentTask(), json.loads(self._object))


def convertTaskValue(task, value):
    if isinstance(value, MemorySequence):
        return task.sequence(convertTaskValue(task, i) for i in value)
    if isinstance(value, Instance):
        return MarshalizedObject(value)

    return value


class Trigger(writeprotected, Object):
    # todo: get rid of synchronous attr, it has no meaning
    __public_members__ = ['code', 'environment']

    def __init__(self, code, synchronous = False, environment = None):
        self.code = code
        self._synchronous = synchronous
        self.environment = environment

        # todo: on-construct security check for synchronous allowed.

    @property
    def synchronous(self):
        return self._synchronous

    @property
    def preprocessedCode(self):
        # Always a module -- account for single-line yaml.
        return self.code + '\n' # return renderTemplate(self.code, trigger = self)

    @property
    def _module(self):
        # try: return self._m_module
        # except AttributeError:
        #   from mud.lang.girl import Girl
        #   mod = self._m_module = Girl(Girl.Module, self.preprocessedCode)
        #   return mod
        return Girl(Girl.Module, self.preprocessedCode)

    @property
    def _expression(self):
        # How will this work with newlines?
        return Girl(Girl.Expression, self.preprocessedCode)

    class _Emulation(Script):
        # todo: override exception-handling, storing exception on task.
        # Then, read flag on (rendering) task completion handler
        # to know what to do (push q reponse) with it.

        debugging = False # True
        if debugging:
            def tracing(self, frame, pos, instr, args):
              # import pdb; pdb.set_trace()
              name = getattr(instr, '__name__', '?')
              msg = '%04d: %s(%s)' % (pos, name, ', '.join(map(repr, args)))

              # print(frame.procedure)
              print(msg)

              # if name == 'call':
              #     print '    %r' % frame.task.stack[-1]
              #     if frame.task.name:
              #         print '    %s' % frame.task.name

    def _activate(self, procedure, *args, **kwd):
        kwd['synchronous'] = bool(self.synchronous)

        try: environ = kwd.pop('environ')
        except KeyError: environ = dict()

        environ.setdefault('trigger', self)
        environ.setdefault('environment', self.environment)
        environ.setdefault('doc', self.environment)

        task = self._Emulation.Load(environ = environ, user = kwd.pop('user', None))

        try: task.operator = kwd.pop('operator')
        except KeyError:
            pass

        progr = kwd.pop('programmer', None)

        try:
            if kwd.pop('audit') is True:
                task.tracing = task.auditInstruction
        except KeyError:
            try: task.tracing = kwd.pop('trace')
            except KeyError:
                pass

        # For billing API.
        try: account = kwd.pop('account')
        except KeyError: pass
        else:
            if account is not None:
                task.account = account

        procedure.setEnvironment(task.environ)

        try: locals = kwd.pop('locals')
        except KeyError:
            task.addFrameCall(procedure, arguments = args,
                              programmer = progr)
        else:
            task.addFrameCall(procedure, locals = locals,
                              arguments = args,
                              programmer = progr)

        finishingScript = kwd.pop('finishing', '')

        try: traceback = kwd.pop('traceback')
        except KeyError: pass
        else:
            try: runtime.call.System.Journal.waitLogs(task, traceback)
            except runtime.doesNotExist: pass

        try: init = kwd.pop('initialize')
        except KeyError: pass
        else: init(task) # A chance to construct memory-bound objects.

        # Todo: don't return this (it's a decorator).  Until a replacement
        # can be written, be aware that this is returned to the girl code.
        onComplete = executeGirl(task, **kwd)

        if finishingScript:
            @onComplete
            def done(task, exception = None):
                # Spawn new task.
                newModuleTask(finishingScript, trigger = self,
                              completedTask = task)

        # @onComplete
        # def debugViewTermination(task, exception = None):
        #     debugOn()
        #     locals

        # Returned to the protected girl environment.
        return self.Task(task, procedure)

    def _activateAsync(self, procedure, task):
        # Used by asynchronous tasks to schedule evaluation.
        procedure.setEnvironment(task.environ)

        locals = dict(environment = self.environment,
                      doc = self.environment,
                      trigger = self)

        return task.frameCall(procedure, locals = locals)

    def _activateCheck(self, *args, **kwd):
        assert 'programmer' not in kwd, KeyError('programmer')
        assert 'operator' not in kwd, KeyError('operator')
        assert 'audit' not in kwd, KeyError('audit')
        assert 'trace' not in kwd, KeyError('trace')
        assert 'context' not in kwd, KeyError('context')

        return self._activate(*args, **kwd)

    def __call__(self, *args, **kwd):
        progr = vmCurrentTask().findProgrammer()
        return self._activate(self._module, *args,
                              **dict(environ = kwd,
                                     programmer = progr))

    @property
    def _evaluation(self):
        'Synchronous activation: wait for new task/frame call to execute.'

        from stuphos.kernel import Machine

        try: task = Machine.GetContextObject().task
        except AttributeError:
            # Not running within virtual machine task -- synchronously evaluate.
            # Note: there's no authority associated with this activation method.
            task = self._Emulation()

        return self._activateAsync(self._expression, task)

    class Task(Object):
        def __init__(self, task, procedure):
            self._task = task
            self._procedure = procedure

        @property
        def _onComplete(self):
            return self._task.onComplete

        @property
        def _result(self):
            return self._task.stack.pop()[0]

        @property
        def result(self):
            c = vmCurrentTask()
            s = c.machine.suspendedTasks
            s.suspendTask(c)

            @self._onComplete
            def complete(task, exception = None):
                if not exception:
                    try: value = self._task.stack.pop()[0]
                    except: value = None

                    value = convertTaskValue(c, value)
                    s.resumeTask(c, c.machine, value = value)

            raise BypassReturn


Evaluation = Trigger

class Inline(Trigger):
    @property
    def _module(self):
        return self.code

    @classmethod
    def _Build(self, ast, *args, **kwd):
        return self(Girl(Girl.Built, ast), *args, **kwd)

inline = Inline._Build

class View(writeprotected, Object):
    def register(self): # What is this used for?
        raise NotImplementedError
    def _render(self, request = None):
        raise NotImplementedError
    def _debugging(self, task, etype, value, tb):
        # Specifically, there was a bug during execution of the context trigger,
        # so this is a good place to generate a report page with task traceback.

        raise etype(value).with_traceback(tb) # there was a python bug


class NodePath(writeprotected, list):
    # __init__ = list.__init__

    def __init__(self, items):
        # Todo: whatever's constructing NodePath/DeepView must do this encoding..!
        # But this object maintains internal consistancy as a native object.
        # debugOn()
        list.__init__(self, (s.decode('utf-8') if isinstance(s, bytes)
                             else s for s in items))

    @property
    def _controlObject(self):
        return self

    def __getitem__(self, item):
        # Q: Why am I overriding this?
        result = list.__getitem__(self, item)
        if isinstance(item, slice):
            result = classOf(self._controlObject)(result)

        return result

    # def getElementAt(self, index):
    #     return list.__getitem__(self, index)
    def getTrailingElements(self):
        return vmNewSequence(list.__getitem__(self, slice(1, None, None)))

    @property
    def string(self):
        return '/'.join(self)

# @runtime.available(runtime.System.Journal)
# def debugging(log, self, etype, value, tb):

def debugging500(self, task, etype, value, tb):
    # import pdb; pdb.set_trace()

    # todo: generate html-ready (FO) tracebacks

    if isinstance(value, Processor.UncaughtError):
        etype = value.etype
        tb = value.tb

        if self.debug:
            vtb = '\n'.join(task._task.formatTraceback(value.traceback))

        value = value.value
    else:
        vtb = ''

    if not self.debug:
        # The idea at this point is that, because this is web view error
        # handling, but it is generally uncaught, we need to communicate
        # to the initiator (and the programmer) the things that we need
        # to.  If the site debug page is disabled, then the initiator
        # will basicaly get a 'didn't work' message.

        raise value.with_traceback(tb)

    # task.formatTraceback()

    # But we're mostly interested in python exception.
    if isYesValue(getConfig('native-traceback', 'Interpreter')):
        tb = '%s:\n%s\n' % (exceptionHeader(etype, value),
                            tracebackString(tb))
    else:
        tb = exceptionHeader(etype, value)

    from django.template.loader import get_template
    from django.template import Context
    from django.template.exceptions import TemplateDoesNotExist

    try: t = get_template('wm/500.html')
    except TemplateDoesNotExist:
        return tb

    return t.render(Context(dict(traceback = tb, vtraceback = vtb,
                                 task = task._task)))

    # return 'Heres where we return a 500 template with traceback!'

class EmulatedView(View):
    __public_members__ = ['context', 'environment', 'source', 'debug', 'path']
    _debugging = debugging500

    def __init__(self, template, context, environment = None, source = None, debug = False, path = ''):
        self._template = template
        self.context = context
        self.environment = environment
        self.source = source
        self.debug = debug
        self.path = path.split('/')

    def renderTemplate(self, **kwd):
        if self._template is None:
            return '' # kwd.get('content', '')

        return renderTemplate(self._template, **kwd)

    class RequestAdapter(writeprotected, Object):
        def __init__(self, request):
            self.__request = request

        @property
        def method(self):
            return self.__request.method
        @property
        def GET(self):
            return vmNewMapping(*list(self.__request.GET.items()))
        @property
        def POST(self):
            return vmNewMapping(*list(self.__request.POST.items()))
        # @property
        # def META(self):
        #     return vmNewMapping(*self.__request.META.items())
        @property
        def FILES(self):
            return vmNewMapping(*list(self.__request.FILES.items()))

        class _User(writeprotected, Object):
            def __init__(self, request):
                self._request = request

            @property
            def username(self):
                return self._request.user.username
            name = username

            @property
            def is_authenticated(self):
                return self._request.user.is_authenticated

        @property
        def user(self):
            return self._User(self.__request)

        @property
        def session(self):
            return # :security:
            return self.__request.session

        @property
        def body(self):
            return self.__request.body

        # provide access to persistant storage.

    def _render(self, request = None, response = None, account = None,
                path = None, **ctxtdct):

        # *Call from an extra-heartbeat thread.
        q = Queue()

        # from phsite.network.models import DefaultPlayer
        from phsite.network.embedded.olc import WebProgrammer
        progr = None
        if request is not None and request.user is not None \
            and request.user.is_authenticated:
            for d in request.user.default_players.all():
                progr = WebProgrammer(d.player.player_name)
                break

        def report(logger, task, traceback):
            # XXX is this being called?!
            logger.systemLog(task, traceback)

        ctxtdct['source'] = self.source
        ctxtdct['view'] = self.path # Q: setdefault?
        contextObject = ctxtdct # todo: wrap to provide other services?

        # todo: could make environ point to self.environment
        environ = contextObject
        environ.update(dict(context = contextObject))

        locals = dict(environment = self.environment,
                      doc = self.environment,
                      request = self.RequestAdapter(request),
                      response = response)

        # locals['source'] = self.source
        locals['path'] = path

        protected = None # [None]
        def initializeTask(task):
            # Store memory-safe mapping for response local.
            # p = protected[0] = task.memory.Mapping(task.memory, **response)
            # task.frame.locals['response'] = p

            nonlocal protected
            protected = task.memory.Mapping(task.memory, **response)
            task.frame.locals['response'] = protected

        task = self.context._activate(self.context._module,
                                      locals = locals,
                                      environ = environ,
                                      programmer = progr,
                                      traceback = report,
                                      account = account,
                                      initialize = initializeTask,
                                      user = request is not None and request.user or None)

        @task._onComplete
        def completeViewRequest(task, exception = None):
            # import game
            # game.syslog('view-request-context: %r' % ctxtdct)

            # print 'view-request-context: %r' % (exception,)

            if response is not None:
                # response.update(protected[0])
                response.update(protected)

            if exception:
                # Introspect into the ph runtime with debugging view.
                q.put((False, exception))
            else:
                # Re-acquire unicode/basestring type for renderTemplate call.
                for (key, value) in list(ctxtdct.items()):
                    if isinstance(key, bytes):
                        del ctxtdct[key] # The bytes key.
                        ctxtdct[key.decode('ascii')] = value

                # task.stack.pop()

                try: q.put((True, self.renderTemplate(**ctxtdct)))
                except:
                    from sys import exc_info
                    q.put((False, exc_info()))

        (success, result) = q.get() # *
        if success:
            return result

        return self._debugging(task, *result) # response or raise


    class _DeepView(NodePath):
        def __init__(self, view, path):
            NodePath.__init__(self, path)
            self._view = view

        @property
        def _controlObject(self):
            return self._view

        def _render(self, request = None, response = None, **ctxtdct):
            ctxtdct['path'] = self # todo: pass to render as keyword argument.
            return self._view._render(request = request, response = response,
                                      **ctxtdct)

    def lookup(self, *names):
        return self._DeepView(self, names)

UserAdapter = EmulatedView.RequestAdapter._User


# from stuphos.kernel import LibraryView as libView
# from django.views.decorators.csrf import csrf_exempt

# class LibraryView(libView):
#     'CMS Library View bound to node configuration.'

#     @runtime.available(runtime.Agent.System)
#     @csrf_exempt
#     def render(core, self, request = None, response = None, **ctxtdct):
#         return libView.render(self(request, core), self.path)

#     def __init__(self, path):
#         self.path = path


class StaticView(View):
    __public_members__ = ['content']

    def __init__(self, content):
        self.content = content
    def _render(self, *args, **kwd): # request = None, response = None, account = None):
        return self.content

class HtmlView(View):
    '''
    (stuph$html):
      html:
        - head:
          - title: 'The webpage title'
          - style:
              type: 'text/css'
              .content::
                body { margin: 10px }

        - body:
          - div: 'This is the content'
          - button:
              .content: 'Ok?'
              onclick::
                alert('Ok');
    '''

    __public_members__ = ['document']

    def __init__(self, root, context):
        self.document = root
        self._context = context

    _blacklist_element = []
    _blacklist_attribute = {}
    _blacklist_attribute_star = []

    def _render(self, request = None, response = None):
        def buildMap(xxx_todo_changeme):
            (name, items) = xxx_todo_changeme
            if name in self._blacklist_element:
                return ''

            bla = self._blacklist_attribute.get(name, [])
            attrs = []

            if isinstance(items, dict):
                content = ''
                children = []

                for (k, v) in items.items():
                    if k == '.content':
                        content = v
                    elif k == '.children':
                        children = v
                    else:
                        if not k in bla and k not in self._blacklist_attribute_star:
                            # todo: render v structural item
                            v = repr(v).replace('\\n', '\n').replace('\\t', '\t')
                            attrs.append('%s=%s' % (k, v))

                def buildChildren():
                    for c in children:
                        yield build(c)
                    if content:
                        # todo: escape html entities in content
                        # or, render structural item
                        # or, transform other markup
                        yield content

                children = nls(buildChildren())

            elif isinstance(items, list):
                children = nls(mapi(build, items))
            else:
                children = str(items)

            attrs = ' '.join(attrs)

            return '<%s%s%s>\n%s\n</%s>\n' % (name, attrs and ' ' or '',
                                              attrs, indent(children), name)

        def build(node):
            if isinstance(node, dict):
                return ''.join(mapi(buildMap, iter(node.items())))

            elif isinstance(node, list):
                return nls(mapi(build, node))

            else:
                try: r = node.render
                except AttributeError: pass
                else:
                    return str(r())

            return ''

        return build(self.document)

    class _ScriptElement(writeprotected):
        __public_members__ = ['item']

        def __init__(self, item):
            self.item = item

        def render(self):
            return ''

class Template(writeprotected, Object):
    def __init__(self, template):
        pass

    def renderTemplate(self, *args, **kwd):
        for a in args:
            if isinstance(a, (list, tuple)):
                a = dict(a)
            if isinstance(a, dict):
                kwd.update(a)

        return renderTemplate(self.template, **kwd)

    render = __call__ = renderTemplate
    rendering = property(renderTemplate)


class Streaming(writeprotected, Object):
    __public_members__ = ['handler']

    def __init__(self, handler):
        self.handler = handler

    def __call__(self, request, *args, **kwd):
        # todo: setup new task environ with request, and execute handler.
        pass

class EqSet(writeprotected, AutoMemoryMapping):
    def equip(self, ch):
        # :security: native exposure.
        machine.checkAccess(['game:equip'])

        import world
        for (where, vnum) in self.items():
            i = world.item(vnum).instantiate(ch)
            try: ch.equip(i, where)
            except IndexError:
                pass # i.extract()

    __call__ = equip

class AuctionList(writeprotected, AutoMemorySequence):
    def __init__(self, sequence):
        AutoMemorySequence.__init__(self, sequence)
        # self.registerAll()

    def registerAll(self):
        for item in self:
            item.register()
        return self
    __call__ = registerAll

class Factory(Submapping):
    from .db.vardb import db, table

    def trigger(self, name, value, **kwd):
        if isinstance(value, str):
            code = value
            synchronous = False
        else:
            code = value['code']
            synchronous = value.get('synchronous', False)
            assert not synchronous # Keep this for now. :security:

        # Todo: kwd['container'] is a dict (not a Building.Item)
        return Trigger(code, synchronous, kwd['container'])

    task = let = evaluation = trigger

    def emulation(self, name, value, **kwd):
        return None

        # Todo: Pass a procedure/module and emulate a buffered version of those instructions.
        if isinstance(value, grammar.Node):
            pass # validated, but compile todo
        elif not isinstance(value, str):
            raise TypeError(type(value))

        # todo: compile the value?
        # value = Girl(Girl.Module, value)

        from stuphos.system.api import game
        task = game.emulateTask(value) # as module?
        return Trigger.Task(task, None)

    def view(self, name, value, **kwd):
        if isinstance(value, str):
            content = value
        else:
            try: content = value['content']
            except KeyError:
                # Build an emulator program for rendering data.
                template = value.get('template', None)
                context = value['context']

                return EmulatedView(template, context, kwd['container'],
                                    debug = value.get('debug', False),
                                    source = kwd.get('document'),
                                    path = name) # source is a positional keyword in mud.lang.structure.document

        return StaticView(content)

    # def libraryView(self, name, value, **kwd):
    #     return LibraryView(value)

    def template(self, name, value, **kwd):
        return Template(value)

    def streaming(self, name, value, **kwd):
        return Streaming(self.trigger(name, value, **kwd))

    def html(self, name, value, **kwd):
        return HtmlView(value, kwd)

    def encoded(self, name, value, **kwd):
        return value.decode('base64')
    def zencoded(self, name, value, **kwd):
        return value.decode('base64').decode('zlib')

    def configuration(self, name, value, **kwd):
        return # XXX Provide native-supported Configuration impl.

        from io import StringIO
        from configparser import ConfigParser
        from .management.config import Configuration

        cfg = ConfigParser()
        cfg.readfp(StringIO(value))

        return Configuration(cfg, name)

    # def pgAuth(self, name, value, **kwd):
    #     from .management.db import dbCore
    #     value['type'] = 'pg-auth'
    #     return dbCore.installConfiguration(name, **value)

    def planet(self, name, value, **kwd):
        return # XXX use spatial api

        from stuphmud.server.zones import Planet # , core
        p = Planet(value['vnum'], value['name'], value['object'])
        for c in value.get('continents', []):
            p.newContinent(c['vnum'], c['name'], c['object'])

        # p._enterSystem(mud.zones.core)
        return p

    def eqSet(self, name, value, **kwd):
        if isinstance(value, dict):
            return EqSet(value)

    def auctionItem(self, name, value, **kwd):
        return # XXX Use native-supported constraint for item.

        item = runtime[runtime.StuphMUD.Auction].Item \
               (-1, value['vnum'], name, value['minlevel'], value['minbid'], 0,
                description = value.get('description', ''),
                payload = value.get('payload', ''))
        return item

    def auction(self, name, value, **kwd):
        return AuctionList(iter(value.values()))

    from stuphmud.server.magic.structure import spell
    spell = staticmethod(spell)

    def rst(self, name, value, **kwd):
        from docutils.core import publish_parts
        return MemoryMapping(publish_parts(value, writer_name = 'html'))

    def quest(self, name, value, **kwd):
        # :security: internal load
        # return # todo: move into tool

        from ph.emulation.machine import vmCurrentTask
        try: task = vmCurrentTask()
        except AttributeError: return
        task.checkAccess(['zones:autoquest'], 'create')

        from stuphmud.server.zones.specials.autoquest import loadQuest

        VALID_QUEST_TYPES = ['$builtin.ProtectedSenario']

        assert value['quest-type'] in VALID_QUEST_TYPES
        return loadQuest(value, source = kwd.get('document', []) + [name])

    def value(self, name, value, **kwd):
        return value # identity

    # def synthetic(self, name, value, **kwd):
    #     return Synthetic(value)

    def url(self, name, value, **kwd):
        # :security: XXX unsafe load package
        raise NotImplementedError('Blocking unsafe operation')

        from phsite.network import url, importView, patterns, include_urlpatterns
        try:
            try: value = value['include']
            except KeyError:
                view = value['view'].split('.')
                viewModule = '.'.join(view[:-1])
                viewName = view[-1]

                view = importView(viewModule, viewName)
                try: view = view.view
                except AttributeError:
                    pass

                return url(value['pattern'], view)
            else:
                if isinstance(value, list):
                    return patterns('', value)

                from stuphmud.server.runtime import LookupObject
                include = LookupObject(value['package']).urlpatterns
                return include_urlpatterns(value['pattern'],
                                           include)

        except Exception as e:
            return e

        '''
        patterns:
          - (stuph$url):
            pattern: '^/html/format$'
            view: person.services.web.views.format_html
          - (stuph$url):
            include:
              pattern: '^game/'
              package: web.stuph.embedded.urls
          - (stuph$url):
            include:
            - (stuph$url):
              pattern: '^accounts/profile'
              view: web.stuph.accounts.profile
        '''

    def library(self, name, value, **kwd):
        # XXX This introduces a lowlevel object that has no memory management.
        raise NotImplementedError('Blocking unsafe operation')

        return LibraryCore(value.getSection('LibraryCore'),
                           LibraryCore.Node)

    class factory(Object, object):
        '''
        my/application:
            interfaces/interface::
                object($submapping):
                    classes:
                        object: my/components/object/kernel

                    document::
                        component($object): true


            documents/usage::
                structure('my/application/interface').object.component

                '''

        def __new__(self, name, value, **kwd):
            raise NotImplementedError

            core = runtime[runtime.Agent.System]
            if not core:
                raise NotImplementedError('%s not installed' % runtime.Agent.System)

            try: classes = value['classes']
            except NameError:
                classes = value
                document = None
            else:
                document = value['document']

            # Todo: merge parent-document 'value' structure into sub-document result object?

            f = object.__new__(self, core, name, classes, **kwd)
            f.__init__(core, name, classes, **kwd)

            if document is None:
                return f

            # Load sub-document.
            return f(document, **kwd) # kwd env?


        def __init__(self, core, name, classes, **kwd):
            self._classes = dict((n, self._lookupSubmapping(core, v))
                                 for (n, v) in classes.items())

        def _lookupSubmapping(self, core, n):
            s = n.split('/')

            for i in range(len(s), -1, -1):
                n = s[:i]

                try: n = core.lookup(*n) # XXX won't the Node.Tool just dereference its scope..?
                except KeyError:
                    continue

                if isinstance(n, core.Node.Tool):
                    n = n.scope

                    for o in s[i:]:
                        n = getattr(n, o) # todo: catch AttributeError and restart library search?


                    # An object was found, now decide what to do with it.

                    # if isinstance(n, Submapping):
                    #   return n


                    # SECURITY NOTE:  Because structures are intended to be loaded from the
                    # virtual machine, they are restricted to only loaded native tool library
                    # paths, which should only be producing object encapsulations.
                    #
                    # Additionally, native tool structural objects must be loaded from the
                    # tool's "_Factory" object, because structural item building methods do
                    # not take frame parameters.  Instead, the factory must detect the vm's
                    # task context instance if it needs to do frame-dependent actions.

                    return n._Factory


                if isinstance(n, core.Node.Module):
                    return self._activity(self, core, n, s)


        @property
        def _machine(self):
            from world import heartbeat as vm
            return vm
            return runtime[runtime.System.Engine]

        def __call__(self, source, **env):
            from stuphos.language.document.interface import load

            def coprocess():
                # XXX object-load/instantiation order is arbitrary!
                return load(source, self._classes, '', **env)

            try: task = self._machine.contextObject.task
            except AttributeError:
                return coprocess()
            else:
                # a parallel document-loading routine object that submaps to library activities
                # and when loading, evaluates the instantiations asynchronously

                # XXX it's not asynchronous, it's callAsynchronous, or some bullshit.
                task.callAsynchronous(coprocess)


        class _activity:
            def __init__(self, submapping, core, node, segments):
                self._submapping = submapping
                self._core = core
                self._node = node
                self._segments = segments

            def __call__(self, name, value, **kwd):
                from stuphos.kernel import LibraryNode, Script, findCurrentUser

                with Script.Loading(environ = kwd, user = findCurrentUser()) as task:
                    lib = LibraryNode._WithCore(self._core, self._node, self._segments)
                    instance = lib.instantiate(arguments = dict(value = value))

                    @task.onComplete
                    def buildComplete():
                        # Hack the stack to assert an exact task return value.
                        task.stack[:] = [instance]


                    # Wait for the virtual task to complete, and return the
                    # object result inserted from the activity instantation.
                    # Todo: errors.
                    return task.returnValue


    submapping = factory

    def structure(self, name, value, **kwd):
        # Well shit... isnt this factory?!
        # Duh, this was supposed to wrap a factory.
        raise NotImplementedError('Blocking unsafe operation')

        core = runtime[runtime.Agent.System]
        if core is not None:
            classes = value['classes']
            document = value['document']
            default = value.get('default', '') # 'stuph'

            if isinstance(classes, self.factory):
                classes = classes._classes
            else:
                def factory(path):
                    node = core[path]
                    if isinstance(node, core.Node.Module):
                        pass
                    elif isinstance(node, core.Node.Structure):
                        pass

                    elif isinstance(node, core.Node.Tool):
                        # XXX check permission.
                        return node.scope._Factory

                classes = dict((type, factory(path))
                                for (type, path) in classes)

            # from mud.lang.structure import Factory
            # classes['stuph'] = Factory

            from stuphos.language.document.interface import load
            return load(document, classes, default)


    class _MethodInterface(Subroutine.Interface):
        # As a Subroutine.Interface, this object is callable by the emulation
        # runtime by dereferencing the procedure.  This object generates new
        # subroutine instances on property dereference for individual frames.

        def __init__(self, module, name):
            self._module = module
            self._name = name

        @property
        def _subroutine(self):
            return self._module.getSubroutine(self._name)

    def method(self, name, value, **kwd):
        # Not really sure what the point of this is, to be part of
        # a synthetic (structural) class.  It could be wrapped by
        # something to mark it and get passed to the class constructor,
        # but, a method definition really has no use alone.
        module = buildMethodFromStructure(name, value, **kwd)

        from stuphos.kernel import Girl
        module = Girl(Girl.Module, module)

        return self._MethodInterface(module, name)

    from stuphos.language.shortate import shortate
    shortate = staticmethod(shortate)


    def command(self, name, value, **kwd):
        # XXX Provide a memory-sensitive implementation of actionable.command[.verb]
        raise NotImplementedError('Blocking unsafe operation')

        # Requires implementation.
        from spatial.architecture import actionable

        if isinstance(value, str):
            value = dict(implementation = value)

        parse = value.get('parse')

        if isinstance(parse, str):
            parse = buildMethodFromStructure(parse, **kwd)

        impl = value['implementation']

        if isinstance(impl, str):
            impl = buildMethodFromStructure(impl, **kwd)

        # if isinstance(parse, subroutine):
        #   parse = compileSubroutine(parse)
        # if isinstance(impl, subroutine):
        #   impl = compileSubroutine(impl)


        ns = dict(__call__ = impl)
        if parse is not None:
            ns['parseArgs'] = parse


        verbClass = newClassType('implementation', (actionable.command.verb,), ns)
        ns = dict(name = name, implementation = verbClass)

        return newClassType('%sCommand' % name, (actionable.command,), ns)


def buildMethodFromStructure(name, value, **kwd):
    if isinstance(value, str):
        parameters = []
        code = value
    else:
        parameters = value['parameters']
        code = value['code']

    parameters = ', '.join(parameters)
    return buildMethod(name, parameters, code)

def buildMethod(name, parameters, code = 'pass'):
    # from ph.lang.layer import grammar
    # ast = grammar.Grammar.AST

    # suite = ast.Suite([])
    # module = ast.Suite([ast.FunctionDefinition(name, parameters, suite)])

    return 'def %s(%s):\n%s\n' % (name, parameters, indent(code))


@staticmethod
def htmlScript(name, value, **kwd):
    # XXX value must be interned here, meaning a memory mapping or sequence,
    # otherwise, structural.Items won't be constrained by mental.objects code.
    raise NotImplementedError('Blocking unsafe operation')

    return HtmlView._ScriptElement(value)

#@staticmethod
def syntheticClass(name, value, **kwd):
    from stuphos.kernel import Girl, SyntheticClass

    # todo: $classInit$ trigger method for initializing
    # environment.  Also, pass kwd/document container
    # for connecting class impl to structure.

    attributes = []
    def checkMember(n, m):
        if isinstance(m, (dict, str)):
            return True

        attributes.append((n, m))
        return False

    methods = ((n, m) for (n, m) in value.items()
               if checkMember(n, m))

    synth = SyntheticClass \
            (name,
             Girl(Girl.Module,
                  nls(buildMethodFromStructure(defn, m, **kwd) for
                      (defn, m) in methods)),
             kwd.get('container'))

    for (n, m) in attributes:
        # todo: is this right?  Shouldn't it be set in environ?
        setattr(synth, n, m)

    # Note: classInit must be called by client.
    return synth


setattr(Factory, 'html.script', htmlScript)
setattr(Factory, 'class', syntheticClass)
Factory.object = Factory.formula = getattr(Factory, 'class')

from stuphos.kernel import GirlCore
class LibraryCore(GirlCore):
    def loadEntities(self, cfg, nodeClass):
        pass
    def saveNode(self, node, recurse = False):
        pass
    def destroyNode(self, node):
        pass


class SystemFactory(Submapping):
    def tool(self, path, sourceCode, **kwd):
        segments = path.split('/')
        assert isinstance(sourceCode, str)
        core = runtime[runtime.Agent.System]
        assert core is not None
        scope = Core.Python().module(path, sourceCode,
                                     container = kwd['container'])
        return core.addPythonTool(segments, scope) # Q: dictOf()?

    # def lock(self, name, value, **kwd):
    #   from threading import Lock
    #   return Lock()
