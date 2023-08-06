# Connects Girl interpreter to player shell/command experience.
# import new

from stuphos.kernel import Girl, Script, Volume, Undefined, Programmer
from stuphos.kernel import GirlSystemModule, Machine as VM, GrammaticalError
from stuphos.kernel import findUserByName
from stuphos.runtime import Object
from stuphos import getConfig
from stuphmud.server.player import getPlayerScope, events, HandleCommandError
from stuphmud.server.player.interfaces.code import ShellFactoryBase
from stuphmud.server.adapters import PeerAdapter, MobileAdapter, TriggerAdapter
from stuphos.etc.tools import getKeyword, Option, isYesValue
from . import ProgrammeManager, EvaluationShell, Programme, isFromSecureHost

# Permission level for non-authenticated command users.
DEFAULT_PROGRAMMER = Programmer.NONE

COMMAND_TASK = "call('player/interpreter/command', me, command, subcommand, arguments)"
# COMMAND_TASK = "'player/interpreter/command'(me, command, subcommand, arguments)"

VERB_TASK = "return call('player/interpreter/verb', me, command, arguments)"
# VERB_TASK = "return 'player/interpreter/verb'(me, command, arguments)"

# Implementation of VM.Task.
class PlayerScript(Script):
    def __init__(self, peer, shell, tracing, *args, **kwd):
        self.peer = peer
        self.shell = shell
        Script.__init__(self, *args, **kwd)
        self.uncaughtError = self.handleError
        if tracing:
            # debugOn()
            self.tracing = self.traceToPeer

    def frameOneForPeer(self, peer, *args, **kwd):
        return Script.frameOne(self, *args, **kwd)

    def frameOne0(self, *args, **kwd):
        # if 0:
        #     # :console: :debugging:
        #     import sys
        #     print >> sys.stderr, 'Frames:', len(self.frames)
        #     # print >> sys.stderr, '\n'.join(str(f.procedure) for f in self.frames)
        #     p = self.frame.procedure
        #     if hasattr(p, 'position'):
        #         o = p.position(0)
        #         print >> sys.stderr, p.instructionsString(o, o+1)

        # Swap in peer for console.
        # try: return self.shell.withPeerHeadAndException(self.peer, (self.Done, VM.Yield),
        #                                                 self.frameOneForPeer,
        #                                                 *args, **kwd)
        # # except Script.Yield:
        # #     import sys
        # #     (etype, value, tb) = sys.exc_info()
        # #     raise (etype, value, tb)

        # except Script.Done, e:
        #     # This is not necessary in all cases of Script.Done at this level.
        #     # This is because Done is also raised on exception, in which case
        #     # the stack is not REPL-integrated.
        #     # try: result = self.stack.pop()[0]
        #     # except IndexError: pass
        #     # else:
        #     #     if result is not None:
        #     #         print >> self.peer, repr(result)

        #     raise e

        return self.shell.withPeerHeadAndException \
                    (self.peer, (self.Done, VM.Yield),
                     self.frameOneForPeer,
                     *args, **kwd)

    def handleError(self, task, frame, exc, traceback):
        # XXX Emitting no error for some things but still raising Done.
        (etype, value, tb) = exc
        if isinstance(value, VM.Yield):
            return # This may not be right since it might need to be propogated.
            raise etype(value).with_traceback(tb)

        if isYesValue(getConfig('native-traceback', 'Interpreter')):
            HandleCommandError(self.peer, exc, frame_skip = 0)

        # todo: make actual printing of girl tb to peer a method on peer. :traceback:
        print('\n'.join(self.formatTraceback(traceback)), file=self.peer)
        print('%s: %s' % (exc[0].__name__, exc[1]), file=self.peer)

        # Eventually this will go away in favor of traceback logging.
        from traceback import print_exception as pe
        print('player error:')
        pe(*exc)

        self.logTraceback(task, traceback)
        raise self.Done

    def traceToPeer(self, frame, pos, instr, args):
        # Set up breakpoints for this:
        # debugOn()
        msg = '%04d %s(%s)' % (pos, getattr(instr, '__name__', '?'),
                               ', '.join(map(str, args)))
        #print >> self.peer, msg

        print(msg)
        print('    ' + '\n    '.join(map(str, frame.task.stack)))

    def handleVerbOutcome(self, outcome, command, argstr):
        # Override this in a new script class for custom command recognition.
        if not outcome:
            print('Unknown command: %r' % command, file=self.peer)


    # Invocation Methods:
    @classmethod
    def evaluateCode(self, peer, shell, program, scope, tracing = False, **environ):
        if isFromSecureHost(peer):
            # from stuphos.etc import isYesValue
            # from stuphos import getConfig

            if peer.avatar is None:
                progr = DEFAULT_PROGRAMMER
                user = None
            else:
                name = peer.avatar.name
                progr = Programmer(name)
                user = findUserByName(name)

            from stuphos.kernel import checkActiveTasks
            checkActiveTasks(user)

            task = self(peer, shell, tracing, user = user)
            task.environ.update(**environ)

            # This is for a persistance concept that doesn't yet exist so it should be removed.
            # task.environ['book'] = Volume(getattr(peer, 'environ', task.environ), program) # or scope

            # if isYesValue(getConfig('system-module', 'AgentSystem')):
            #     task.environ['system'] = GirlSystemModule.Get()

            program.setEnvironment(task.environ)

            vm = getVirtualMachine()
            new = task.addFrameCall(program, programmer = progr)
            new.locals = scope
            if user is not None:
                # Note: scope must be a managed memory object.
                # Todo: make it vm.Task...?
                scope._connectMemory(VM.Task.Memory.Connect(task, user))

            @new.onComplete
            def completion(frame, *error):
                if task.stack and error[1] is None:
                    value = task.stack.pop()[0]
                    if value is not None:
                        # todo: move actual printing to method on peer.
                        # print(f'task return value: {repr(value)}')

                        # XXX Not being sent by SessionManager to session page.
                        print(repr(value), file=peer)

                        # try: print >> peer, repr(value)
                        # except:
                        #     from pdb import post_mortem as pm
                        #     pm()
                    # else:
                    #     print('Task stack is None')

                # elif isinstance(error[1], task.frames.ForeignFrameError):
                #     frame = error[1].frame
                #     print >> peer, 'foreign:', frame #.procedure

            vm += task
            return task

    @classmethod
    def evaluateStatement(self, peer, statement, tracing = False, shell = None):
        scope = getGirlPlayerScope(peer) # target of @dir()
        program = Girl(Girl.Statement, statement)

        if shell is None:
            shell = peer.interpreter

        self.evaluateCode(peer, shell, program, scope,
                          tracing = tracing,
                          this = PeerAdapter(peer), # todo: persist these
                          me = MobileAdapter(peer.avatar))

        return True


    # Command/Verb invocation: the interpreter is a running task that is stored
    # as a weakref on the peer object, started by this class if it is not already
    # running (evaluates as non-None).  Commands and verbs are merely objects
    # passed to this running task using a synchronization queue.  The interpreter
    # program is responsible for sequencing the synchronicity of each command,
    # as well as (re)drawing the prompt.

    @classmethod
    def evaluateCommand(self, actor, name, subcmd, argstr):
        peer = actor.peer
        if peer is not None:
            scope = getGirlPlayerScope(peer) # target of @dir()

            try: program = Girl(Girl.Module, COMMAND_TASK+'\n')
            except GrammaticalError as e:
                print(e.report())
            else:
                self.evaluateCode(peer, peer.interpreter, program, scope,
                                  subcommand = subcmd, command = name,
                                  arguments = argstr,
                                  this = PeerAdapter(peer),
                                  me = MobileAdapter(actor))

    @classmethod
    def evaluateVerb(self, peer, actor, command, argstr):
        scope = getGirlPlayerScope(peer) # target of @dir()

        try: program = Girl(Girl.Module, VERB_TASK+'\n')
        except GrammaticalError as e:
            print(e.report())
        else:
            task = self.evaluateCode(peer, peer.interpreter, program, scope,
                                     command = command,
                                     arguments = argstr,
                                     this = PeerAdapter(peer),
                                     me = MobileAdapter(actor))

            if task is not None:
                @task.onComplete
                def completion(_, exception = None):
                    if exception is None:
                        try: outcome = task.stack.pop()[0]
                        except IndexError: pass # Shouldn't happen
                        else: task.handleVerbOutcome(outcome, command, argstr)

    @classmethod
    def evaluateMethodCall(self, request, path, name, *args):
        # todo: finish:
        #   instantiate self for task class
        #   interface with isFromSecureHost and request/peer
        #   integrate with SessionManager
        #   this came from mental.library.model.GirlCore.rpcCallMethod
        from stuphos.kernel import checkActiveTasks, Programmer, nullproc, getLibraryCore

        name = path[-1]
        path = path[:-1]

        # Acquire programmer and task state.
        if request.user is not None:
            checkActiveTasks(request.user)

        for player in request.user.default_players.all():
            progr = Programmer(player.player.player_name)
        else:
            progr = Programmer.NONE

        task = Script.Load(user = request.user)
        core = getLibraryCore(task)

        vm = runtime[runtime.System.Engine]

        task += dict(procedure = nullproc(), programmer = progr)
        vm += task

        return callGirlMethod(core, task, path, name, *args) () # block.


    @classmethod
    def invokeTrigger(self, peer, program, tracing = False):
        scope = getGirlPlayerScope(peer)
        self.evaluateCode(peer, peer.interpreter, program, scope,
                          tracing = tracing,
                          player = MobileAdapter(peer.avatar),
                          trigger = TriggerAdapter(self))

AgentScript = PlayerScript

class GirlPlayerProgrammeTrigger(Programme, events.Trigger):
    # Dual function: as stored programme, and also as triggerable player event.
    class _Meta(Programme._Meta):
        Attributes = Programme._Meta.Attributes + ['tracing']

    def __init__(self, *args, **kwd):
        tracing = getKeyword(kwd, 'tracing')
        Programme.__init__(self, *args, **kwd)
        self.tracing = tracing

    def __getstate__(self):
        state = Programme.__getstate__(self)
        state['tracing'] = self.tracing
        return state

    def getCompiledCode(self):
        if isinstance(self.sourceCode, str):
            # Compile as module.
            return Girl(Girl.Module, self.sourceCode) # self.source.replace('\r', '')

    getTriggerCode = getCompiledCode

    def invokeProgramme(self, shell, peer):
        code = self.getCompiledCode()
        scope = getGirlPlayerScope(peer)
        PlayerScript.evaluateCode(peer, shell, code, scope,
                                  tracing = self.tracing,
                                  player = peer.avatar,
                                  this = peer, me = peer.avatar)

    def invokeTrigger(self, player):
        PlayerScript.invokeTrigger(player.peer, self.getTriggerCode(),
                                   self.tracing)

class GirlCodeManager(ProgrammeManager):
    # ProgrammeManager:
    ProgrammeClass = GirlPlayerProgrammeTrigger

    def getManagerName(self):
        return 'Girl'
    def getManagerId(self):
        return '%s.%s.Instance' % (self.__class__.__module__, self.__class__.__name__)

class GirlCodeShell(EvaluationShell):
    # EvaluationShell:
    def executeGirl(self, shell, peer, argstr):
        return self.executeSourceCode(shell, peer, argstr)

    __call__ = executeGirl

    def executeCode(self, shell, peer, program):
        scope = self.getScope(peer)
        PlayerScript.evaluateCode(peer, shell, program, scope,
                                  tracing = self.tracing,
                                  player = peer.avatar,
                                  this = peer, me = peer.avatar)

    def compileSourceCodeBlock(self, peer, sourceCode):
        if isinstance(sourceCode, str):
            # Currently always is -- Compile as module.
            return Girl(Girl.Module, self.manager.formatSourceCode(sourceCode))

    def compileSingleStatement(self, peer, sourceCode):
        return Girl(Girl.Statement, self.manager.formatSourceCode(sourceCode))

    # Implementation.
    def __init__(self, manager, tracing = False):
        EvaluationShell.__init__(self, manager)
        self.tracing = tracing

    def getScope(self, peer):
        return getGirlPlayerScope(peer)

# Infrastructure.
def getVirtualMachine():
    from world import heartbeat as vm
    return vm

def getGirlScope(scope, name = None):
    # Basically return a persistant, shared namespace associated with,
    # wrapping, and being wrapped by the standard player scope.

    try: return scope.namespace
    except AttributeError: pass

    try: memory = scope.memory
    except AttributeError:
        memory = scope.memory = VM.Task.Memory.Connect(None) # XXX user = findUserByPrincipalName(name)

    ns = scope.namespace = VM.Task.Environment(memory)
    return ns

    # girl = getattr(scope, 'girl', Undefined)
    # if girl is Undefined:
    #     girl = new.module('%s.namespace' % Girl.__module__)

    #     # XXX UNSAFE.
    #     girl.shared = scope
    #     scope.girl = girl

    #     # Presumably, the girl-core facility is loaded before this is initialized.
    #     # XXX UNSAFE, because it exposes the core object to all player scripts.
    #     girl.core = runtime[runtime.Girl.System]

    # return girl.__dict__

# Singleton.
GirlCodeManager.Instance = GirlCodeManager()

def getGirlPlayerScope(peer):
    name = peer.avatar.name if peer.avatar else None
    return getGirlScope(getPlayerScope(peer), name = name)
def getGirlCodeEvaluator(*args, **kwd):
    return GirlCodeShell(GirlCodeManager.Instance, *args, **kwd)

class GirlCodeEvaluatorFactory(ShellFactoryBase):
    OPTIONS = [Option('-t', '--tracing', action = 'store_true')]

    def __new__(self, peer, tracing = False):
        print(EvaluationShell.PROGRAMMING_HEADER % 'Girl', file=peer)
        return getGirlCodeEvaluator(tracing)

def doGirlStatement(peer, cmd, argstr):
    # Execute single statement now.
    # todo: security policy
    if peer.avatar and peer.avatar.implementor:
        if argstr:
            # todo: delete_doubledollar(argstr)
            PlayerScript.evaluateStatement(peer, argstr, shell = peer.interpreter)
            return True

# Command Line.
def initCommands():
    try: from stuphmud.server.player import getSharedCommands # ...plain ACMD still being initialized.
    except ImportError: pass
    else: getSharedCommands().insertOverridingAll('@', doGirlStatement)

def createCommand(verb, path, commandName):
    def performGirlCommand(peer, cmd, argstr):
        from world import heartbeat as vm
        from stuphos.kernel import Script

        core = runtime[runtime.Agent.System]
        path = path.split('/')
        node = core.root.lookup(*path)
        task = Script() # Todo: PlayerScript import

        # Open subroutine and schedule.
        try: pos = node.module.symbols[commandName]
        except KeyError:
            raise NameError(commandName)

        # Todo: use string-name overload
        method = node.module.getSubroutine(pos)

        # todo: use executeGirl for synchronous option.
        task.addFrameCall(method, arguments = [cmd, argstr])
        vm += task
        return True

    from stuphmud.server.player import ACMD
    return ACMD(verb)(performGirlCommand)
