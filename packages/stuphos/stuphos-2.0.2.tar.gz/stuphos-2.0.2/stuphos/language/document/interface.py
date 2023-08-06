# mud.lang.structure
# from op.runtime.structural import document as _document
from . import structural as _document
getContextVariable = _document.Context.__getitem__

from stuphos.structure import Factory, SystemFactory

def getContextEnvironment(name):
	return getContextVariable('loader').environ[name]

def load(source, classes, defaultName, **kwd):
	source = source.replace('\r', '') # scrub from any source.
	# source = 'Westmetal Configuration::\n\n' + source
	source = 'WMC []\n\n' + source

	return _document.loadStructuredMessageFromClasses \
			(source, classes, raw = True,
			 default = defaultName, **kwd)

def getFactories():
	yield 'stuph', Factory

	from stuphos import getConfig
	from stuphos.etc import isYesValue

	if isYesValue(getConfig('converge-spatial')):
		from spatial.spherical import structure as spatial
		yield 'world', spatial.Factory

def document(source, **kwd):
	# A raw load skips installation of core factory classes, so we
	# can create a controlled, discriminatory environment.
	# Auto WMC
	#import pdb; pdb.set_trace()
	return load(source, dict(getFactories()), 'stuph', **kwd)

def system(source, **kwd):
	return load(source, dict(system = SystemFactory), 'system', **kwd)

def resource(base, path, *names):
	base = io.path(base).folder(*path)
	return access(document(base.read()), *names)
