from kivy.core.window import Window

class Navigation(Widget):
	def __init__(self, **kwargs):
		self.func = kwargs['func']

		kwargs.pop('func', None)
		super(PongGame, self).__init__(**kwargs)
		self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
		self._keyboard.bind(on_key_down=self._on_keyboard_down)

	def _keyboard_closed(self):
		self._keyboard.unbind(on_key_down=self._on_keyboard_down)
		self._keyboard = None

	def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'esc':
            self.func()
        return True