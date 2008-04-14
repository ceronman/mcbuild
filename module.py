# -*- coding: utf-8 -*-
#
# Mono Development Building Script
#
# Copyright (c) 2006 - 2008. Manuel Cerón <ceronman@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

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
			if cmd is None:
				return
		except:
			raise CommandNotFound(command)
		
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

