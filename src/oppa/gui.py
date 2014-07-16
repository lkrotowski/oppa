import cairo
import gtk
import state

win         = gtk.Window()
statusicon  = gtk.status_icon_new_from_stock(gtk.STOCK_GOTO_TOP)
drawcalls   = [lambda cr, c=state.color(): cr.set_source_rgb(*c)]
drawtrigger = 0

def init():
	statusicon.connect("activate", on_status_clicked)
	win.add_events(gtk.gdk.BUTTON_PRESS_MASK   |
	               gtk.gdk.BUTTON_RELEASE_MASK |
	               gtk.gdk.POINTER_MOTION_MASK)

	win.connect("key-press-event", on_keypress)
	win.connect("button-press-event", on_buttonpress)
	win.connect("button-release-event", on_buttonrelease)
	win.connect("motion-notify-event", on_motionnotify)
	win.connect("delete-event", on_delete)
	win.connect("expose-event", on_expose)

	win.screen = win.get_screen()
	colormap = win.screen.get_rgba_colormap()
	if (colormap is not None and win.screen.is_composited()):
		win.set_colormap(colormap)
	else:
		print "Screen is not composited, transparency disabled!"

	win.set_app_paintable(True)
	win.maximize()
	win.set_keep_above(True)
	win.set_decorated(False)
	win.show_all()
	win.get_window().set_cursor(gtk.gdk.Cursor(gtk.gdk.CROSSHAIR))

	if state.minimized:
		statusicon.set_from_stock(gtk.STOCK_GOTO_BOTTOM)
		win.iconify()

def on_keypress(window, event):
	global drawcalls

	if event.keyval == gtk.keysyms.q:
		gtk.main_quit()
	if event.keyval == gtk.keysyms.t:
		state.toggle_opaque()
		win.queue_draw()
	if event.keyval == gtk.keysyms.space:
		toggle()
	if event.keyval == gtk.keysyms.Delete:
		win.get_window().set_cursor(gtk.gdk.Cursor(gtk.gdk.CROSSHAIR))
		drawcalls = [lambda cr, c=state.color(): cr.set_source_rgb(*c)]
		win.queue_draw()
	if event.keyval == gtk.keysyms.e:
		win.get_window().set_cursor(gtk.gdk.Cursor(gtk.gdk.PIRATE))
		drawcalls.append(lambda cr: cr.stroke())
		drawcalls.append(lambda cr: cr.set_operator(cairo.OPERATOR_CLEAR))
		drawcalls.append(lambda cr: cr.set_line_width(50.0))
	if event.keyval in [gtk.keysyms.w, gtk.keysyms.r, gtk.keysyms.g, gtk.keysyms.b]:
		win.get_window().set_cursor(gtk.gdk.Cursor(gtk.gdk.CROSSHAIR))
		if event.keyval == gtk.keysyms.w:
			state.white()
		if event.keyval == gtk.keysyms.r:
			state.red()
		if event.keyval == gtk.keysyms.g:
			state.green()
		if event.keyval == gtk.keysyms.b:
			state.blue()
		drawcalls.append(lambda cr: cr.stroke())
		drawcalls.append(lambda cr: cr.set_operator(cairo.OPERATOR_OVER))
		drawcalls.append(lambda cr: cr.set_line_width(2.0))
		drawcalls.append(lambda cr, c=state.color(): cr.set_source_rgb(*c))

def on_buttonpress(window, event):
	drawcalls.append(lambda cr, x=event.x, y=event.y: cr.move_to(x, y))

def on_buttonrelease(window, event):
	win.queue_draw()

def on_motionnotify(window, event):
	if event.state & gtk.gdk.BUTTON1_MASK:
		drawcalls.append(lambda cr, x=event.x, y=event.y: cr.line_to(x, y))
		delayed_queue_draw()

def on_delete(window, event):
	toggle()
	return True

def on_expose(widget, event):
	cr = widget.get_window().cairo_create()
	cr.set_source_rgba(0, 0, 0, 1.0 if state.opaque else 0.0)
	cr.set_operator(cairo.OPERATOR_SOURCE)
	cr.paint()

	cr.set_operator(cairo.OPERATOR_OVER)
	for drawcall in drawcalls:
		drawcall(cr)
	cr.stroke()
	return False

def on_status_clicked(status):
	toggle()

def toggle():
	if not state.minimized:
		statusicon.set_from_stock(gtk.STOCK_GOTO_BOTTOM)
		win.iconify()
	else:
		statusicon.set_from_stock(gtk.STOCK_GOTO_TOP)
		win.deiconify()
	state.toggle_minimized()

def delayed_queue_draw():
	global drawtrigger
	# For performance reasons draw is queued every N-th time
	# from MOTION_NOTIFY event.
	N = 5
	if drawtrigger % N == 0:
		win.queue_draw()
	drawtrigger += 1

def run():
	init()
	gtk.main()
