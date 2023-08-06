# Game Core Replacement
# (C) 2009 Clint Banis.  All rights reserved.
#
from . import Heartbeat, Game
from .db import Database

from time import time as getSystemTime
from pdb import runcall, set_trace as enter_debugger
from os import getpid, getenv
from queue import Empty

# System Database.
class Local(Database):
    import sys

    def __init__(self, *args, **kwd):
        # Obselete, just configure packages.
        # try: libdata = kwd['libdata']
        # except KeyError: pass
        # else:
        #     del kwd['libdata']
        #     if libdata not in self.sys.path:
        #         self.sys.path.append(libdata)

        Database.__init__(self, *args, **kwd)

    def activate(self, engine):
        engine.db = self
        self.boot()

# Application.
def freeClient(network, port):
    print('Opening Loopback Connection:', port)
    network.openConnection(('localhost', port))

class Core(Heartbeat):
    class Pulse(Heartbeat.Task):
        # This could go in system.heartbeat
        from time import time as getTimeInSeconds, sleep
        getTimeInSeconds = staticmethod(getTimeInSeconds)
        sleep = staticmethod(sleep)

        OPT_MSEC = 100 # Milliseconds per timeslice.

        def getRemainingTimeslice(self, duration):
            return duration % self.OPT_MSEC # XXX what if duration > OPT_MSEC??
        def sleepForMilliseconds(self, duration):
            duration /= 1000
            # duration /= 10 # seems more accurate, but wtf?
            # print duration
            self.sleep(duration) # / 1000) # XXX don't divide by 1000!?
        def getTimeInMilliseconds(self):
            return self.getTimeInSeconds() * 1000

        def __init__(self, heartbeat):
            self.heartbeat = heartbeat

        def perform(self, engine):
            start = self.getTimeInMilliseconds()

            # import pdb; pdb.set_trace()
            # pdb.runcall(self.heartbeat.pulse, 0, 100)

            # import time, datetime
            # print datetime.datetime.fromtimestamp(time.time())

            try:
                self.heartbeat.pulse(0, 100, blocking = engine.blockingQueue)

                duration = self.getTimeInMilliseconds() - start
                remaining = self.getRemainingTimeslice(duration)
                if remaining:
                    self.sleepForMilliseconds(remaining)

            except Empty:
                # What are we catching if not an errant exception coming from
                # pulse.  This is able to clear the error which seems to not
                # be happening in the emulated machine.  It is unclear if this
                # catch will work if not for the sleep call that might raise
                # the pending Empty exception.
                pass

            except KeyboardInterrupt:
                @engine.event.call
                def done():
                    # debugOn()
                    engine.stop()
                    StuphMUD.ShutdownGame()
                    # gc.collect(); os.kill(signal.SIGTERM, os.getpid())

            except:
                from traceback import print_exc
                print_exc()

    def __init__(self, xxx_todo_changeme,
                 stuphlib, worldModule,
                 globalize = False,
                 initForCore = None,
                 consoleClass = None):

        # Configure for continuous metal.
        (options, args) = xxx_todo_changeme
        timeout = None if options.fast_vm else False

        Heartbeat.__init__(self)
        self.cmdln = dict(options = options, args = args)

        # Configure against options.
        try: import readline
        except ImportError: pass

        if options.debug > 3:
            enter_debugger()

        if options.runpid:
            with open(getenv('RUNPID_FILENAME', 'runpid'), 'w+b') as o:
                o.write(str(getpid()))

        self.headless = options.headless
        if not options.headless:
            if consoleClass is not None:
                console = consoleClass.create(debug = options.debug) # interactive = options.interactive
                self += console

                if options.supreme:
                    console.avatar.level = console.avatar.LVL_SUPREME

                    # Enable 'examine' command.
                    from world.player import EnableEMHW
                    EnableEMHW() # Emergency Mode Holographic Wizard

                if options.admin_name:
                    console.avatar.name = options.admin_name
                # if options.enter_game:
                #     from stuphos.system.api import world
                #     console.avatar.room = world.room(3001)

            else:
                console = None

        self += Game(timeout = timeout)

        if options.port:
            from stuphos.system.network import MotherSocket
            network = MotherSocket(options.port)
            self += network
            # self.event.call(freeClient, self.network, options.port)

            from world import player
            player.emergeInternalPeer = network.emergeInternalPeer

            if not options.headless:
                console.attachNetwork(network)

        if options.debug > 2:
            runcall(self.bootMudStart, options, stuphlib, worldModule)
        else:
            self.bootMudStart(options, stuphlib, worldModule)

        if not options.headless:
            def ehwm(console):
                StuphMUD.GreetPlayer(console)
                StuphMUD.NewIncomingPeer(console)
                enterGameInRoom(console, console.avatar)

            self.event.call(ehwm, console)

        if options.data_dir:
            from os import chdir
            print('Changing to data directory: %s' % options.data_dir)
            chdir(options.data_dir)

        if callable(initForCore):
            # Let calling context initialize, now that most of the
            # core is booted, before the main process is run.
            initForCore(self)

        if options.debug > 1:
            runcall(self.run)
        elif options.async:
            from _thread import start_new_thread as nth
            nth(self.run, ())
        else:
            # Move this above execution?
            if globalize:
                global instance
                import builtins as builtin
                instance = builtin.core = self

            try: self.run()
            except KeyboardInterrupt:
                print()

    @property
    def blockingQueue(self):
        return self.cmdln['options'].blocking

    def bootMudStart(self, options, stuphlib, worldModule):
        # Initialize MUD Package.
        import stuphos
        if options.config_file:
            stuphos.reloadConfigFile(options.config_file)

        stuphos.bootStart()

        # Complete MUD Boot Cycle.
        self.bootStartTime = getSystemTime()
        if not options.no_world:
            self.event.call(self.bootWorld, options, stuphlib, worldModule)

        self.event += self.worldResetStart
        self.event += self.worldResetComplete
        self.event += self.bootMudComplete

    def bootMudComplete(self):
        import stuphos
        elapsed = getSystemTime() - self.bootStartTime
        stuphos.bootComplete((elapsed / 1000, elapsed % 1000))

        if self.cmdln['options'].fast_vm:
            from ..metal import vm
            self.fastVM = vm()
            nth(self.fastVM)

        else:
            # Install timing driver.
            try: self += self.Pulse(stuphos.getHeartbeat())
            except AttributeError as e:
                print(str(e)) # No need to print the traceback.

            # If components.system.core.Core construction fails
            #     to bootStart because the components.runtime.core
            #     fails, then it doesn't not fail the system core
            #     construction, it just causes the runtime.bootStart
            #     to return None (so no bridge...) 

            #     This means that later functionality may fail to
            #     load, for example, the compartmental framework
            #     heartbeat driver activated at the end of the
            #     boot protocol.

            #     Really what this means is that the boot start
            #     shouldn't fail where the boot complete continues,
            #     except that as a discrete and specific failure,
            #     a non-existence bridge should indicate no heartbeat
            #     module, and thus an alternative pulse activation.

            #         But to do this means that the core logics need
            #         to recognize and apply state.


    # def initConsole(self, console):
    #     from stuphmud.server.player import interpret
    #     interpret(console)

    def bootWorld(self, options, stuphlib, worldModule):
        if options.world_dir:
            self += Local(stuphlib, worldModule,
                          options.world_dir, options.zone_index,
                          cascade = options.cascade, verbose = options.verbose)
                          # libdata = options.libdata)

    def worldResetStart(self):
        StuphMUD.StartWorldReset()
    def worldResetComplete(self):
        StuphMUD.CompleteWorldReset()

# Todo: these are player-specific things:
def getDefaultStartRoom(actor):
    return 3001
def getLoadRoom(actor):
    return getattr(actor, 'loadroom', None) # saveroom??

def getFirstValidRoom(*rooms):
    import world; table = world.room.table
    for vnum in rooms:
        try: return table[vnum]
        except KeyError:
            pass

def loadIntoRoom(peer, actor, room):
    if room is not None:
        actor.room = room
        from stuphos.system.game.namespace import lookAtRoom
        lookAtRoom(actor, peer, room)

def enterGameInRoom(peer, actor):
    StuphMUD.EnterGame(peer, actor)
    loadIntoRoom(peer, actor, getFirstValidRoom(getLoadRoom(actor), getDefaultStartRoom(actor)))


# System Core Bridged Events.
StuphMUD.ShutdownGame = 'shutdownGame'

StuphMUD.StartWorldReset = 'resetStart'
StuphMUD.CompleteWorldReset = 'resetComplete'

StuphMUD.StartZoneReset = 'startZoneReset'
StuphMUD.CompleteZoneReset = 'completeZoneReset'

StuphMUD.MobileFromRoom = 'removeMobileFromRoom'
StuphMUD.MobileToRoom = 'putMobileInRoom'

