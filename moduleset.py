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

# this module is compiled with mono
MonoModule(
	name = 'olive',
	configure_cmd = None,
	compile_cmd = None,
	install_cmd = None,
	uninstall_cmd = None,
)

MonoModule(
	name = 'mono',
)

MonoModule(
	name = 'monodoc',
)

MonoModule(
	name = 'gtk-sharp-2.12',
	configure_cmd = './bootstrap-2.10',
)
 
MonoModule(
	name = 'gnome-sharp',
	configure_cmd = './bootstrap-2.16',
)

MonoModule(
	name = 'gnome-desktop-sharp',
)


MonoModule(
	name = 'gtksourceview-sharp',
)

MonoModule(
	name = 'gtkmozembed-sharp',
)

MonoModule(
	name = 'mono-tools',
)

MonoModule(
	name = 'moon',
)

# this module is compiled from monodevelop
MonoModule(
	name = 'lunareclipse',
	configure_cmd = None,
	compile_cmd = None,
	install_cmd = None,
)

