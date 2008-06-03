# -*- coding: utf-8 -*-

class MonoModule(SVNModule):
	repository = 'svn://anonsvn.mono-project.com/source/trunk' 

MonoModule(
	name = 'libgdiplus',
)

# this module is compiled with mono
MonoModule(
	name = 'mcs',
	configure_cmd = None,
	compile_cmd = None,
	install_cmd = None,
	uninstall_cmd = None,
)

MonoModule(
	name = 'mono',
	configure_cmd = './autogen.sh --with-moonlight=yes'
)

MonoModule(
	name = 'olive',
	configure_cmd = './configure',
)

MonoModule(
	name = 'monodoc',
)

MonoModule(
	name = 'gtk-sharp',
	configure_cmd = './bootstrap-2.12',
)
 
MonoModule(
	name = 'gnome-sharp',
	configure_cmd = './bootstrap-2.20',
)

MonoModule(
	name = 'gnome-desktop-sharp',
)


MonoModule(
	name = 'gtksourceview2-sharp',
)

MonoModule(
	name = 'gtkmozembed-sharp',
)

MonoModule(
	name = 'mono-tools',
)

MonoModule(
	name = 'mono-addins',
)

import configuration
MonoModule(
	name = 'monodevelop',
	configure_cmd = './configure --profile=core --prefix=%s' % configuration.INSTALL_PATH
)

MonoModule(
	name = 'moon',
	configure_cmd = './autogen.sh --with-mono=yes'
)

# this module is compiled with monodevelop
MonoModule(
	name = 'lunareclipse',
	configure_cmd = None,
	compile_cmd = None,
	install_cmd = None,
	uninstall_cmd = None,
)

