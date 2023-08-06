# Installation of Computation Core.

from stuphos.xmlrpc import getHost
from stuphos.xmlrpc import host

from stuphos.xmlrpc.config import NotConfigured


from stuphos import getConfig
from stuphos.etc import isYesValue

if isYesValue(getConfig('metal', 'VM')):
	from ph.emulation.metal import Machine
	from ph.emulation.metal import MachineCore
	from ph.emulation.metal import Native
	from ph.emulation.metal import TaskControl

	from ph.emulation.metal import Heartbeat

	from ph.emulation.metal import Processor
	from ph.emulation.metal import Subroutine

else:
	from ph.emulation.machine.virtual import Machine
	from ph.emulation.machine.virtual import MachineCore
	from ph.emulation.machine.virtual import Native
	from ph.emulation.machine.virtual import TaskControl
	# from ph.emulation.machine.virtual import startTask

	from ph.emulation.machine.virtual import machine
	from ph.emulation.machine.virtual import checkActiveTasks
	from ph.emulation.machine.virtual import BypassReturn
	from ph.emulation.machine.virtual import OuterFrame
	from ph.emulation.machine.virtual import Continuation

	from ph.emulation.machine import currentVMTask
	from ph.emulation.machine import vmCurrentTask
	from ph.emulation.machine import vmCheckAccess
	from ph.emulation.machine import vmNewMapping
	from ph.emulation.machine import vmNewSequence
	from ph.emulation.machine import nativeObject
	from ph.emulation.machine import nativeMemoryObject
	from ph.emulation.machine import deletable

	from ph.emulation.machine.memory import AutoMemoryObject
	from ph.emulation.machine.memory import AutoMemoryMapping
	from ph.emulation.machine.memory import AutoMemorySequence
	from ph.emulation.machine.memory import AutoMemoryNamespace
	from ph.emulation.machine.memory import protectedMemoryCopy
	from ph.emulation.machine.memory import MemoryMapping
	from ph.emulation.machine.memory import MemorySequence


	from ph.emulation.machine.heartbeat import Heartbeat

	from ph.emulation.operation.application import Processor
	from ph.emulation.operation.application import Subroutine


from ph.emulation.security import RelationNetwork


try:
	from ph.interpreter import mental as interpreter

	# from stuphos.runtime import Undefined
	from ph.interpreter.mental import Undefined

	from ph.interpreter.mental import Assembly
	from ph.interpreter.mental import CallMethodError
	from ph.interpreter.mental import Girl
	from ph.interpreter.mental import Ella # New symbology.
	from ph.interpreter.mental import Agent
	from ph.interpreter.mental import ParallelTask
	from ph.interpreter.mental import Programmer
	from ph.interpreter.mental import Script
	from ph.interpreter.mental import Volume
	from ph.interpreter.mental import callGirlMethod
	from ph.interpreter.mental import executeGirl
	from ph.interpreter.mental import getLibraryCore
	from ph.interpreter.mental import grammar
	from ph.interpreter.mental import invokeLibraryMethod
	from ph.interpreter.mental import newModuleTask

	from ph.interpreter.mental import findUser
	from ph.interpreter.mental import findUserByName
	from ph.interpreter.mental import findCurrentUser

	from ph.interpreter.mental import nullproc

	from ph.interpreter.mental.objects import Library
	from ph.interpreter.mental.objects import LibraryNode
	from ph.interpreter.mental.objects import Instance
	from ph.interpreter.mental.objects import GirlSystemModule
	from ph.interpreter.mental.objects import SyntheticClass

	from ph.interpreter.mental.grammar import GrammaticalError

	from ph.interpreter.mental.native import sleep

	from ph.interpreter.mental.library.model import GirlCore
	from ph.interpreter.mental.library.model import LIB_ROOT
	from ph.interpreter.mental.library import views as libraryViews
	from ph.interpreter.mental.library.views import LibraryView, wm
	from ph.interpreter.mental.library.extensions import serverChannel

# Disable interpreter.
except ImportError as e:
	# debugOn()
	pass


##    XXX MOBILE_TRIGGER_TYPES
##    XXX getMobileTriggerSheet
##    XXX getMobileTriggerType
##    XXX libraryViews

