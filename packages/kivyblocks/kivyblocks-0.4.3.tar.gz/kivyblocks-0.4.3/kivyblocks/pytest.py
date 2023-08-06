from io import StringIO
from contextlib import redirect_stdout

from kivy.app import App
from kivy.factory import Factory
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput inport TextInput

from appPublic.Singleton import SingletonDecorator, GlobalEnv

from .baseWidget import PressableText
from .tab import TabsPanel
from .utils import *
from kivy.utils import platform
import plyer
if platform == 'android':
	import android
	import jnius
elif platform == 'ios':
	from pyobjus import autoclass, protocol, objc_str
	from pyobjus.dylib_manager import load_framework, INCLUDE

class Pyinterpretor(TextInput):
	def __init__(self, **kw):
		kw['multiline'] = True
		super().__init__(**kw)
		self.env = {}
		for n,f in Factory.classes.items():
			if f['cls']:
			self.env[n] = f['cls']
		self.text = '>>>'
		self.bind(on_key_up=self.check_enter_key)

	def check_enter_key(self, kb, keycode, text, modifiers):
		_, key = keycode
		if key == 'enter':
			script = self.get_script()
			self.exec_script(script)
			
	def get_script(self):	
		ts = self.text.split('\n')
		s = ts[-1][3:]
		return s

	def exec_script(self, script):
		env = globals().copy()
		locals={}
		env.update(self.env.copy())

		f = StringIO()
		with redirect_stdout(f):
			exec(script, env, locals)
		s = f.getvalue()
		self.text = self.text + s + '\n'

