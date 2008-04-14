import os
import commands
import string

moduleset = []

class CommandError(Exception):
	def __init__(self, command, output=''):
		self.command = command
		self.output = output
		Exception.__init__(self, 'Command Error')

class CommandNotFound(Exception):
	def __init__(self, command):
		self.command = command
		Exception.__init__(self, 'Command Not Found')
	
class Module:
	name = ''
	source_dir = '$name'
	checkout_cmd = ''
	update_cmd = ''
	configure_cmd = './configure'
	compile_cmd = 'make'
	install_cmd = 'make install'
	uninstall_cmd = 'make uninstall'
	clean_cmd = 'make clean'

	def __init__ (self, name, **args):
		self.name = name
		self.__dict__.update(args)
		global moduleset
		if self not in moduleset:
			moduleset.append(self)

	def command(self, command, verbose=False):
		try:
			cmd = getattr(self, command + '_cmd')
		except:
			raise CommandNotFound(command)
		if cmd is None:
			return
		prev_dir = os.getcwd()
		src_dir = self._process_template(self.source_dir)
		if not os.path.isdir(src_dir):
			self._execute_cmd(self.checkout_cmd, verbose)
		os.chdir(src_dir)
		self._execute_cmd(cmd, verbose)
		os.chdir(prev_dir)

	def _execute_cmd (self, cmd, verbose):
		command = self._process_template(cmd)
		print '**** Performing "%s" on %s...' % (cmd, self.name)
		if verbose:
			result = os.system(command)
			if result != 0:
				raise CommandError(cmd)
		else:
			result = commands.getstatusoutput(command)
			if result[0] != 0:
				raise CommandError(cmd, result[1])
		print 'Done.'

	def _process_template (self, pattern):
		template = string.Template(pattern)
		d = dict([(prop, getattr(self, prop)) for prop in dir(self)])
		return template.substitute(d).strip()

class SVNModule(Module):
	repository = ''
	checkout_cmd = 'svn checkout $repository/$name'
	update_cmd = 'svn update'
	configure_cmd= './autogen.sh'

