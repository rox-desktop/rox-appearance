# Most of the common code needed by ROX applications is in ROX-Lib2.
# Except this code, which is needed to find ROX-Lib2 in the first place!

# Just make sure you import findrox before importing anything inside
# ROX-Lib2...

import os, sys
from os.path import exists
import string

def version(major, minor, micro):
	"""Find ROX-Lib2, with a version >= (major, minor, micro), and
	add it to sys.path. If version is missing or too old, either
	prompt the user, or (if possible) upgrade it automatically."""

	if not os.getenv('ROXLIB_DISABLE_ZEROINSTALL') and os.path.exists('/uri/0install/rox.sourceforge.net'):
		# We're using ZeroInstall. Good :-)
		zpath = '/uri/0install/rox.sourceforge.net/lib/ROX-Lib2/' \
			'latest'
		if os.path.exists(zpath):
			vs = os.readlink(zpath).split('-')[-1]
			v = map(int, vs.split('.'))
			if v[0] < major or v[1] < minor or v[2] < micro:
				if os.system('0refresh rox.sourceforge.net'):
					report_error('Using ROX-Lib in Zero Install, but cached version (%s) is too old (need %d.%d.%d) and updating failed (is zero-install running?)' % (vs, major, minor, micro))
			sys.path.append(zpath + '/python')
			return
		print >>sys.stderr, "Using Zero Install, but failed to " \
			"fetch", zpath, "-- trying non-0install system."

	try:
		path = os.environ['LIBDIRPATH']
		paths = string.split(path, ':')
	except KeyError:
		paths = [os.environ['HOME'] + '/lib',
			 '/usr/local/lib', '/usr/lib' ]

	for p in paths:
		p = os.path.join(p, 'ROX-Lib2')
		if exists(p):
			# TODO: check version is new enough
			sys.path.append(os.path.join(p, 'python'))
			import rox
			if major == 1 and minor == 9 and micro < 10:
				return	# Can't check version
			if not hasattr(rox, 'roxlib_version'):
				break
			if (major, minor, micro) <= rox.roxlib_version:
				return	# OK
	report_error("This program needs ROX-Lib2 (version %d.%d.%d) " % \
		(major, minor, micro) + "to run.\n" + \
		"I tried all of these places:\n\n" + \
		string.join(paths, '\n') + '\n\n' + \
		"ROX-Lib2 is available from:\n" + \
		"http://rox.sourceforge.net")

def report_error(err):
	"Write 'error' to stderr and, if possible, display a dialog box too."
	try:
		sys.stderr.write('*** ' + err + '\n')
	except:
		pass
	try:
		import pygtk; pygtk.require('2.0')
		import gtk; g = gtk
	except:
		import gtk
		win = gtk.GtkDialog()
		message = gtk.GtkLabel(err + 
				'\n\nAlso, pygtk2 needs to be present')
		win.set_title('Missing ROX-Lib2')
		win.set_position(gtk.WIN_POS_CENTER)
		message.set_padding(20, 20)
		win.vbox.pack_start(message)

		ok = gtk.GtkButton("OK")
		ok.set_flags(gtk.CAN_DEFAULT)
		win.action_area.pack_start(ok)
		ok.connect('clicked', gtk.mainquit)
		ok.grab_default()
		
		win.connect('destroy', gtk.mainquit)
		win.show_all()
		gtk.mainloop()
	else:
		box = g.MessageDialog(None, g.MESSAGE_ERROR, 0,
					g.BUTTONS_OK, err)
		box.set_title('Missing ROX-Lib2')
		box.set_position(g.WIN_POS_CENTER)
		box.set_default_response(g.RESPONSE_OK)
		box.run()
	sys.exit(1)
