from linklib.utils import _Link
from linklib.utils import misc
from linklib.utils import valid

class UNDEFINED:
	pass

undefined = UNDEFINED()


class ConnLink(_Link):
	"""
	a link to connect 2 links,
	instead of a,b = linklib.connects.ConnLink()
	use a,b = linklib.connects.connect()
	Examples:
	>>>from linklib.connects import connect
	>>>a,b = connect()
	>>>a.set("hello",True)
	>>>b.get("hello")
	True
	"""
	def __init__(self):
		self._setfunc = "setattr"
		self._getfunc = "getattr"
		self._intermediate = None

	def _to_connect(self,interface):
		self._intermediate = interface 

	def _when_setcall(self,fname):
		self._setfunc = fname 

	def _when_getcall(self,fname):
		self._getfunc = fname 

	def get(self,info):
		"""use to get a value via a key (`info`) in the n links globals"""
		if self._getfunc == 'getattr':
			try:
				return getattr(self._intermediate,info)
			except AttributeError:
				return undefined
		else:
			try:
				return getattr(self,_intermediate,self._getfunc)(info)
			except AttributeError:
				return undefined 

	def globals(self):
		if self._getfunc == 'getattr': #default
			r = {}
			for nm in dir(self._intermediate):
				if nm[0] == '_':
					continue
				else:
					r[nm] = self.get(nm)
			return r 
		else:
			return NotImplemented 

	def set(self,info,cnt,_warn=True):
		"""use to set a value with a keyword info and content cnt,set its in a n global enviorement"""
		try:
			if info[0] == '_' and warn:
				from warnings import warn 
				warn(f"{info} must be privated,using self.globals() will be ocult so ",
					"if you dont want this quit the first '_'")
			if self._setfunc == "setattr":
				setattr(self._intermediate,info,cnt)
			else:
				getattr(self._intermediate,self._setfunc)(info,cnt)
		except AttributeError:
			return undefined

	def exists(self,info):
		return self.get(info) == undefined 

def connect():
	return misc._connect(ConnLink)

def connected(a,b):
	return a._intermediate == b._intermediate


def n_connect(n=2):
	"""
	use to connect a n global enviorement via ConnLink\'s
	Examples:
		>>>from linklib import n_connect
		>>>a,b,c = n_connect(3)
		>>>a.set("hello",True)
		>>>b.set("abc",[1,2,3])
		>>>c.get("hello")
		True
		>>>c.get('abc')
		[1,2,3]
	"""
	a = [ConnLink() for x in range(n)]
	class cachecls:
		def __init__(self):
			pass
		def setinfo(self,infonm,info):
			setattr(self,infonm,info)
		def __eq__(self,other):
			return id(self) == id(other)
	cache_cls = cachecls()
	for link in a:
		link._to_connect(cache_cls)
		link._when_getcall("getattr")
		link._when_setcall("setinfo")
	return tuple(list(a)) 

