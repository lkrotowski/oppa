import gtk

class Gui(gtk.Window):
	def __init__(self):
		super(Gui, self).__init__()

		self.connect("key-press-event", self.on_keypress)

		self.maximize()
		self.show_all()

	def on_keypress(self, window, event):
		if event.keyval == gtk.keysyms.q:
			gtk.main_quit()

def run():
	Gui()
	gtk.main()
