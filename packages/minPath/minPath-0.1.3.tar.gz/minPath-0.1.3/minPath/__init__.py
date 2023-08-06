try:
	from StringIO import StringIO ## for Python 2
except ImportError:
	from io import StringIO ## for Python 3
import pickle
import time
import re
import datetime
#from typing import Any,Callable
from os.path import split as split_path
from .Objects import *
from .Errors  import *

InvaildChars = r"[\\/*?:<>|]"
Invaildsyntax = r"[*?<>|]"
InvaildName_pattern = re.compile(InvaildChars)
Invaildsynt_pattern = re.compile(Invaildsyntax)

__version__ = "0.1.3"
__author__ = 'Alawi Hussein Adnan Al Sayegh'


def parser_path(content:str,prefixs=("/", "\\")):
	token = []
	tok   = ""
	for char in content:
		if char in prefixs:
			token.append(tok)
			tok = ""
		else:
			tok+=char
	if tok.strip():
		token.append(tok)
	return token

def vaild_name(name:str):
	""" check if name is vaild. error if not """
	if not isinstance(name,str):
		raise ValueError(f"excepted str (not {type(name).__name__})")
	if InvaildName_pattern.search(name):
		raise InvaildNameError(f"Invalid char detected, ({repr(name)}). Invaild Chars: {(InvaildChars)}")
	elif name == "":
		raise InvaildNameError(f"Invalid name. name mustn't be empty")
	return name

def vaild_path(path:str):
	""" check if path is vaild. error if not """
	if not isinstance(path,str):
		raise ValueError(f"excepted str (not {type(path).__name__})")
	if Invaildsynt_pattern.search(path):
		raise InvaildPathSyntex(f"Invalid char detected, ({repr(path)}). Invaild Chars: {(Invaildsyntax)}")
	return path

def recreate_file(file):
	""" recreate a file """
	newfile = File(file.name,file.getvalue())
	newfile.time    = file.time
	return newfile

def search(files:iter,filename:any):
	""" search a file if found return file else None """
	for file in files:
		if file.name == filename:
			return file
	return

def isfile(file):
	""" returns type(file.type) is FileType; checks if object is a file """
	return type(file.type) is FileType
def isdir(folder):
	""" returns type(folder.type) is FolderType; checks if a object is a folder """
	return type(folder.type) is FolderType



class Folder_Array(object):
	"""docstring for Folder_Array"""
	def __init__(self, Files):
		super(Folder_Array, self).__init__()
		self.Files = {}
		self.type = FolderType(None)
		self._Files(Files);self.name = None
	def _Files(self,Files):
		if not isinstance(Files,(list,dict)):
			raise ValueError(f"excepted a any(list,dict) but get {type(Files).__name__}")
		my_files = Files if isinstance(Files,list) else list(Files.values())
		[self.append(file) for file in my_files] # append files/folders
		return self.Files
	def checkFileObject(self,file):
		if isinstance(file,File) or isinstance(file,Folder):
			return file
		else:
			raise isNotaFileObject(f"{file} is not a File object")
	def append(self,file):
		file = self.checkFileObject(file)
		if file.name in self.Files:
			raise FileExistsError(f"file already Exists {file.name}:{file}")
		self.Files[file.name] = obj = file
		return obj
	def replace(self,file):
		file = self.checkFileObject(file)
		if file.name not in self.Files:
			raise FileNotFoundError(f"The system cannot find the file specified: {repr(file)}")
		self.Files[file.name] = file
	def remove(self,file,byname=False):
		if byname:
			if not isinstance(file,str):
				raise ValueError(f"excepted str (not {type(file).__name__})")
			if file not in self.Files:
				raise FileNotFoundError(f"The system cannot find the file specified: {repr(file)}")
			del self.Files[file]
			return
		# find file object
		if file not in self.Files.values():
			raise FileNotFoundError(f"The system cannot find the file specified: {repr(file)}")
		try:
			file = self.checkFileObject(file).name
			file = self.list()[self.list_objs().index(file)]
			return self.remove(file,byname=True)
		except ValueError:
			raise FileNotFoundError(f"The system cannot find the file specified: {repr(file)}")
		return
	def find(self,file,byname=False):
		if byname:
			if not isinstance(file,str):
				raise ValueError(f"excepted str (not {type(file).__name__})")
			if file not in self.Files:
				raise FileNotFoundError(f"The system cannot find the file specified: {repr(file)}")
			return self.Files[file]
		# find file object
		if file not in self.Files.values():
			raise FileNotFoundError(f"The system cannot find the file specified: {repr(file)}")
		try:
			file = self.checkFileObject(file).name
			file = self.list()[self.list_objs().index(file)]
			return file
		except ValueError:
			raise FileNotFoundError(f"The system cannot find the file specified: {repr(file)}")
	def copy(self,copy_files:bool=True):
		return {file.name:(file.copy() if copy_files else file) for file in self.list_objs()}
	def list(self):
		return list(self.Files.keys())
	def list_objs(self):
		return list(self.Files.values())
	def __iter__(self):
		return iter(self.Files.items())
	def __getitem__(self,name):
		""" get file/dir by name """
		return self.find(name,byname=True)
	def __delitem__(self,name):
		""" remove file/dir by name """
		return self.remove(name,byname=True)
	def __setitem__(self,name,file):
		try:
			self.append(file)
		except FileExistsError:
			self.replace(file)
		return file






class File(StringIO):
	def __init__(self,name,*args,**kw):
		super(File, self).__init__(*args,**kw)
		self.name = self.rename(name)

		self.time = time.time()
	@property
	def created_at(self):
		return datetime.datetime.fromtimestamp(self.time)
	def rename(self,name):
		self.name = vaild_name(name)
		try:
			if "." in name:
				self.type = FileType(name.split(".").pop())
			else:
				self.type = FileType(None)
		except IndexError:
			self.type = FileType(None)
		return name
	def copy(self):
		file = self.__class__(self.name,self.getvalue())
		file.time = self.time
		return file
	def __repr__(self):
		return f"{type(self).__name__}({repr(self.name)})"


class Folder(Folder_Array):
	def __init__(self,name,Files={}):
		super(Folder, self).__init__(Files = Files)
		self.name = self.rename(name)

		self.time = time.time()
	@property
	def created_at(self):
		return datetime.datetime.fromtimestamp(self.time)
	def rename(self,name):
		self.name = vaild_name(name)
		try:
			if "." in name:
				self.type = FolderType(name.split(".").pop())
			else:
				self.type = FolderType(None)
		except IndexError:
			self.type = FolderType(None)
		return name
	def copy(self,copy_files=0):
		folder = self.__class__(name = self.name, Files = \
			(self.Files.copy() if copy_files==1 else \
			(self.Files if copy_files != 2 else {file.name:file.copy() for file in self.list_objs()})))
		folder.time = self.time
		return file
	def open(self,name,mode="rw"):
		""" test function^ """
		byname=True
		if any((all(( "w" in (mode) , "r" in (mode) )),mode in ["w","x","a","+"])):
			if all(( "w" in (mode) , "r" in (mode) )) or mode == "+":
				file = self.find(name,byname=byname)
			elif mode == "w":
				wfile = self.find(name,byname=byname)
				file = wfile.copy()
				self.replace(file)
			else:
				try:
					self.append(File(name))
				except FileExistsError as error:
					if mode == "x":
						raise error
				file = self.find(name,byname=byname)
		else:
			raise ValueError(f"Unknown mode {mode}")
		if mode=="a" and file.seekable():
			file.seek(0)
			file.read()
		elif file.seekable():
			file.seek(0)
		return file
	def __refreah(self,recreate=False):
		if recreate:
			print("recreate is a test code. that may break something")
			for name,file in self:
				try:
					newfile = file.copy()
					self.replace(newfile)
				except FileNotFoundError:
					pass
				except AttributeError:
					pass
			return
		for name,file in self:
			try:
				if not type(file.type) is FileType:
					continue
				if file.seekable():
					file.seek(0)
			except AttributeError:
				pass
	def refreah(self):
		return self.__refreah()
	def __repr__(self):
		return f"{type(self).__name__}({repr(self.name)})"

class Drive(object):
	def __init__(self,letter,name,echo=True):
		super(Drive, self).__init__()
		if echo : print("the class still in development or it will be removed in the new updates")
		if len(letter) > 1:
			raise ValueError("letter len must be 1")
		if not isinstance(letter,str):
			raise ValueError("letter must be a str")
		if not isinstance(name,str):
			raise ValueError("name must be a str")
		self.letter = letter
		self.name = name
		self.lets = letter+":"
	def __repr__(self):
		return "<"+type(self).__name__+"({}) object at ".format(repr(f"{self.name} ({self.lets})"))+hex(id(self))+">"

class MiniPath(object):
	def __init__(self,name="C:",Files=[],path_sep="/"):
		super(MiniPath, self).__init__()
		self.path_sep = path_sep
		self.paths = [ name ]
		self.path = self.path_sep.join(self.paths)
		self.parent = Folder_Array(Files)
		self.parent_dir = self.parent.list()
		self.parents = []
		self.parent.name = self.name = name

		self.last_parent = self.parent
		self.last_dir = self.parent_dir
		self.time = time.time()
	@property
	def created_at(self):
		return datetime.datetime.fromtimestamp(self.time)
	@property
	def current_parent(self):
		""" get last_parent """
		return self.last_parent
	@property
	def current_dir(self):
		""" get last_dir """
		return self.last_dir
	def chdir(self,path):
		""" Change the current working directory to the specified path """
		if vaild_path(path) == "":
			raise MPError(f"The filename, directory name syntax is incorrect: {repr(path)}")
		elif path == ".":
			return self.paths
		elif path=="..":
			if len(self.parents)==0:
				self.last_parent = self.parent
				self.last_dir = self.parent.list()
				self.path = self.path_sep.join(self.paths)
				return self.paths
			self.parents.pop()
			name = self.paths.pop()
			try:
				parent = self.parents[-1]
			except IndexError: # if len(self.parents)==0:
				self.last_parent = self.parent
				self.last_dir = self.parent.list()
				self.path = self.join(*self.paths)
				return self.paths
			dirlist  = parent.list()
			self.last_parent = parent
			self.last_dir = dirlist
			self.path = self.join(*self.paths)
			return self.paths
		children = self.last_parent.list_objs()
		dirlist = self.last_parent.list()
		pathing = parser_path(path)
		parents = []
		paths = []
		for sep in pathing:
			if sep in dirlist:
				folder = search(children,sep)
				if isdir(folder):
					parent = folder
					children = parent.list_objs()
					dirlist = parent.list()
					parents.append(parent)
					paths.append(parent.name)
				else:
					raise NotADirectoryError(f"The directory name is invalid: {repr(sep)}")
			else:
				raise FileNotFoundError(f"The MiniPath cannot find the file specified: {repr(path)}.")
		self.parents.extend(parents)
		self.paths.extend(paths)
		self.last_parent = parent
		self.last_dir = dirlist
		self.path = self.join(*self.paths)
		return self.paths
	def get(self,path):
		""" get (a file or a folder) with path """
		if vaild_path(path) == "":
			raise MPError(f"The filename, directory name syntax is incorrect: {repr(path)}")
		pathing = parser_path(path)
		children = self.last_parent.list_objs()
		dirlist = self.last_parent.list()
		index = 0
		while len(pathing)>index:
			sep = pathing[index]
			if sep in dirlist:
				file = search(children,sep)
				if index==len(pathing)-1:
					return file
				else:
					if not isdir(file):
						raise NotADirectoryError(f"The directory name is invalid: {repr(sep)}")
					children = file.list_objs()
					dirlist = file.list()
			else:
				raise FileNotFoundError(f"The MiniPath cannot find the file specified: {repr(path)}.")
			index += 1
		raise FileNotFoundError(f"The MiniPath cannot find the file specified: {repr(path)}.")
	def get_parent(self,path):
		""" get a folder with path """
		if path is None:
			return self.last_parent
		elif vaild_path(path) == "":
			raise MPError(f"The filename, directory name syntax is incorrect: {repr(path)}")
		pathing = parser_path(path)
		children = self.last_parent.list_objs()
		dirlist = self.last_parent.list()
		for sep in pathing:
			if sep in dirlist:
				folder = search(children,sep)
				if isdir(folder):
					parent = folder
					children = parent.list_objs()
					dirlist = parent.list()
				else:
					raise NotADirectoryError(f"The directory name is invalid: {repr(sep)}")
			else:
				raise FileNotFoundError(f"The MiniPath cannot find the file specified: {repr(path)}.")
		return parent
	def listdir(self,path=None):
		""" list a folder with the specified path """
		return self.get_parent(path).list()
	def rmdir(self,path):
		""" remove dir """
		head, tail = split_path(path)
		parent_of_parent = self.get_parent(head if head != "" else None)
		is_dirarray = self.get_parent(path)
		return parent_of_parent.remove(tail if tail != "" else head, byname=True)
	def removedirs(self,path):
		self.rmdir(path)
		head, tail = split_path(path)
		if not tail:
			head, tail = split_path(head)
		while head and tail:
			try:
			    self.rmdir(head)
			except OSError:
				break
			head, tail = split_path(head)
	def remove(self, path):
		""" remove any type file """
		head, tail = split_path(path)
		parent_of_parent = self.get_parent(head if head != "" else None)
		return parent_of_parent.remove(tail if tail != "" else head, byname=True)
	def walk(self,top=None,sep="\\"):
		""" Directory tree generator """
		parent = self.get_parent(top)
		def walk_wrapper(tail_root,child):
			tail_root = ((tail_root+sep) if tail_root is not None else "")+child.name
			dirs,files = self._list_parent(child)
			yield (tail_root,list(dirs.keys()),list(files.keys()))
			if dirs.values():
				for child_parent in list(dirs.values()):
					yield from walk_wrapper(tail_root,child_parent)
		yield from walk_wrapper(None,parent)
	def _list_parent(self,parent):
		""" split files and dirs returns dirs:dict,files:dict """
		dirs  = {}
		files = {}
		for name,file in parent:
			if isdir(file):
				dirs[name] = file
			else:
				files[name] = name
		return dirs,files
	def find(self,*args,**kw):
		""" find a file/folder in the current parent """
		return self.last_parent.find(*args,**kw)
	def list(self,*args,**kw):
		""" list the current parent """
		return self.last_parent.list(*args,**kw)
	def isdir(self,path):
		""" is folder with path"""
		return isdir(self.get(path))
	def isfile(self,path):
		""" is file with path"""
		return isfile(self.get(path))
	def makedirs(self,path,exist_ok=False):
		if vaild_path(path) == "":
			raise MPError(f"The filename, directory name syntax is incorrect: {repr(path)}")
		pathing = parser_path(path)
		path = ""
		for sep in pathing:
			if path:
				path += "\\"+sep
			else:
				path = sep
			try:
			   last = self.mkdir(path)
			except FileExistsError as error:
				if not exist_ok: raise error
		return last
	def mkdir(self,path):
		""" create a folder """
		if vaild_path(path) == "":
			raise MPError(f"The filename, directory name syntax is incorrect: {repr(path)}")
		path,name = split_path(path)
		parent = self.get_parent(path if path!="" else None)
		return parent.append(Folder(name))
	def exists(self,path):
		""" returns False when (file not found) or (NotADirectoryError rsvie) """
		try:
			self.get(path)
		except (FileNotFoundError,NotADirectoryError):
			return False
		return True
	def getcwd(self):
		""" get the current path """
		return str(self)
	def join(self,path,*paths):
		""" join one (or more) paths """
		return self.path_sep.join([path]+list(paths))
	def __str__(self):
		""" get the cwd """
		self.path = self.join(*self.paths)
		return self.path

