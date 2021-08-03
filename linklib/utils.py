import os
import re
from importlib import import_module

def loader(f):
	"""
	a decorator to define the subpart-loader of a given link
	Examples:
		>>>from linklib import loader
		>>>from linklib import Link
		>>>@loader
		...def attr(base,sub):
		...    return getattr(base,sub)
		...
		>>>a = Link('os.path')
		>>>import os
		>>>attr(os,a)
		<module 'ntpath' from 'C:\\Users\\Angel Carrique\\AppData\\Local\\Programs\\Python\\Python39\\lib\\ntpath.py'>
		>>>a = Link('linklib.Link')
		>>>import linklib as lk
		>>>attr(lk,a)
		<class 'linklib.Link'>
	"""
	def wrapper(base,link):
		@link.loader
		def _cache(base,attr):
			return f(base,attr)
		return _cache(base)
	return wrapper

def path_loader(f):
	def wrapper(link):
		@link.loader 
		def _cache(pstep,lresult):
			return f(pstep,lresult)
		return _cache()
	return wrapper 

def _load_object(path):
    if not isinstance(path, str):
        if callable(path):
            return path
        else:
            raise TypeError("Unexpected argument type, expected string "
                            "or object, got: %s" % type(path))
    try:
        dot = path.rindex('.')
    except ValueError:
        raise ValueError(f"Error loading object '{path}': not a full path")
    module, name = path[:dot], path[dot + 1:]
    mod = import_module(module)
    try:
        obj = getattr(mod, name)
    except AttributeError:
        raise NameError(f"Module '{module}' doesn't define any object named '{name}'")
    return obj

class _Link:
	"""class to check if is a link of linklib,all links are subclasses of this"""
	pass

class LinkBase(_Link):
	def __init__(self,path):
		self.path = path 
		self.parts = path.split(".")
		self.last = self.parts[-1]
		self.start = self.parts[0]
	def __str__(self):
		return self.path
	def load_modobj(self):
		if len(self.parts) == 1:
			return import_module(self.path)
		else:
			return _load_object(str(self))
	def load_with(self,f):
		def load(base):
			path = self.path
			if not isinstance(path, str):
				if callable(path):
					return path
				else:
					raise TypeError("Unexpected argument type, expected string "
    	    	                    "or object, got: %s" % type(path))
			try:
				dot = path.rindex('.')
			except ValueError:
				raise ValueError(f"Error loading object '{path}': not a full path")
			name = self.last
			mod = base
			try:
				obj = f(mod, name)
			except AttributeError:
				raise NameError(f"Module '{self.parts[0]}' doesn't define any object named '{name}'")
			return obj
		return load 
	
	def loader(self,f):
		"""
		used to define a link loader (only self-util)
		examples:
			>>>from linklib import Link
			>>>a = Link("os.path")
			>>>@a.loader
			>>>def attr(base,sub): #base is the base object given and sub is the subattribute
			...    return getattr(base,sub) #just like self.load_modobj(os)
			...
			>>>import os
			>>>attr(os) #same than os.path,sub is the same in the link.
			<module 'ntpath' from 'C:\\Users\\Angel Carrique\\AppData\\Local\\Programs\\Python\\Python39\\lib\\ntpath.py'>
		"""
		return self.load_with(f)

	def exists(self,base):
		"""return if link is a valid link for base of base"""
		@self.loader 
		def _exists(base,sub):
			return hasattr(base,sub)
		return _exists(base)



class PathLink(_Link):
	def __init__(self,link):
		path = re.sub("/",r"\\",link)
		self.path = path 
		self.parts = path.split("\\")
		self.last = self.parts[-1]
		self.start = self.parts[0]

	def join(self,**paths):
		return os.path.join(self.path,**paths)

	def load_with(self,f,list_ =False):
		def loader():
			path = self.parts
			llist = []
			last = path[0]
			llist.append(last)
			for i in path[1:]:
				llist.append(last)
				if list_:
					last = f(i,last,llist)
				else:
					last = f(i,last)
			return last
		return loader

	def loader(self,f,list_=False):
		"""
		define a directory loader (self-only)
		Examples:
			>>>from linklib import PathLink as pl
			>>>link = pl("D:\\AGOTI")
			>>>@link.loader
			...def loader_one(path_step,last_result):
			...    print(path_step,last_result)
			...    return path_step
			...
			>>>loader_one()
			AGOTI D:
			'AGOTI'
			>>>link =pl("D:\\test\\python\\users\\loggers\\__main__\\")
			>>>@link.loader
			...def loader_two(pstep,lresult):
			...    print(pstep,lresult,sep=':')
			...    return pstep
			...
			>>>loader_two()
			test:D:
			python:test
			users:python
			loggers:users
			__main__:loggers
			:__main__
			>>>>@link.loader
			...def loader(pstep,lresult):
			...    print(pstep,"is the current directory")
			...    print(lresult,"is whatever the last call of self() returns")
			...    return pstep #so every iteration will show the current part of the path and the last part of the path
			...
			>>>loader()
			test is the current directory
			D: is whatever the last call of self() returns
			python is the current directory
			test is whatever the last call of self() returns
			users is the current directory
			python is whatever the last call of self() returns
			loggers is the current directory
			users is whatever the last call of self() returns
			__main__ is the current directory
			loggers is whatever the last call of self() returns
			 is the current directory
			__main__ is whatever the last call of self() returns
		first iteration last result is equal to first element of the path and
		the current directory is the second element of the path.
		NOTE:
			to save the loader traceback use kargs arguments
			Examples:
				>>>p = PathLink("D:\\test\\python")
				>>>@p.loader
				...def loader(cstep,lres,traceback=[]):
				...    traceback.append(cstep)
				...    r = ''
				...    for trace in traceback:
				...        r = r + trace +'\\'
				...    print(r)
				...    return traceback
				...
				>>>loader()
				test\\
				test\\python\\
		"""
		return self.load_with(f,list_=list_)

	def exists(self):
		return os.path.exists(self.path)

def is_link(cls):
	return issubclass(cls,_Link)

class cache:
	def valid(self,link):
		return (is_link(type(link)))
	def _connect(self,link):
		a = link()
		b = link()
		class cachecls:
			def __init__(self):
				pass
			def setinfo(self,infonm,info):
				setattr(self,infonm,info)
			def __eq__(self,other):
				return id(self) == id(other) 
		cache_cls = cachecls()
		a._to_connect(cache_cls)
		b._to_connect(cache_cls)
		a._when_setcall("setinfo")
		b._when_setcall("setinfo")
		a._when_getcall("getattr")
		b._when_getcall("getattr")
		return (a,b)

	def generator(self,link):
		if isinstance(link,str):
			link = LinkBase(link)
		for part in link.path.split('.'):
			yield part 

	def __repr__(self):
		return "<misc object>"

misc = cache()

valid = misc.valid 

import sys 
sys.modules["linklib.utils.misc"] = misc 
