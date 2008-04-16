#!/usr/bin/python
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
import sys
import traceback
import optparse
import configuration as config
from module import *


def configure_environment():
	os.environ['LD_LIBRARY_PATH'] = config.INSTALL_PATH + '/lib'+ ':' + os.environ.get('LD_LIBRARY_PATH', '')
	os.environ['C_INCLUDE_PATH'] = config.INSTALL_PATH + '/include'+ ':' + os.environ.get('C_INCLUDE_PATH', '')
	os.environ['ACLOCAL_PATH'] = config.INSTALL_PATH + '/share/aclocal'
	os.environ['PKG_CONFIG_PATH'] = config.INSTALL_PATH + '/lib/pkgconfig'+ ':' + os.environ.get('PKG_CONFIG_PATH', '')
	os.environ['PATH'] = config.INSTALL_PATH + '/bin'+ ':' + os.environ.get('PATH', '')
	os.environ['CONFIG_SITE'] = '/tmp/autoconf.site'
	config_site = open(os.environ['CONFIG_SITE'], 'w')
	config_site.write('test "$prefix" = NONE && prefix=%s \n' % config.INSTALL_PATH)
	config_site.close()

if __name__ == '__main__':
	configure_environment()
	global moduleset
	parser = optparse.OptionParser()
	parser.add_option('-s', '--start', dest='start', help='Start from which module')
	parser.add_option('-e', '--shell', action='store_true', dest='shell', help='Open a shell inside the new environment')
	parser.add_option('-r', '--run', action='store_true', dest='run', help='Run a program inside the new environment')
	parser.add_option('-u', '--update', action='store_true', dest='update', help='Update and rebuild all modules')
	parser.add_option('-v', '--verbose', action='store_true', dest='verbose', help='Show output of commands')
	(options, args) = parser.parse_args()
	
	try:
		if options.shell:
			os.environ['PS1'] = '[mcbuild]' + os.environ.get('PS1', '[\u@\h \W]\$ ')
			user_shell = os.environ.get('SHELL', '/bin/sh')
			os.execvpe(user_shell, [], os.environ)

		if options.run:
			os.execlp(*args)
			
		if options.update:
			args = ['update', 'uninstall', 'configure', 'compile']

		execfile(config.MODULESET_PATH)

		if options.start is not None:
			names = [m.name for m in moduleset]
			moduleset = moduleset[names.index(options.start):]
			
		if not os.path.exists(config.SOURCES_PATH):
			os.makedirs(config.SOURCES_PATH)
			
		if not os.path.isdir(config.SOURCES_PATH):
			print '**** Configuration Error: SOURCES_PATH is not a valid directory'
			sys.exit()
			
		os.chdir(config.SOURCES_PATH)

		for module in moduleset:
			for cmd in args:
				module.command(cmd, options.verbose)
				
	except CommandError, exc:
		print 'Command Error (%s):' % exc.command
		print 'Command Output:'
		print exc.output
	except CommandNotFound, exc:
		print 'Command "%s" not found.' % exc.command
	except Exception, exc:
		print 'error desconocido', exc
		traceback.print_exc(file=sys.stdout)

