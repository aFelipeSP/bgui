import sys

# So we can find the bgui module
sys.path.append('../..')

import bgui
import bge

class MySys(bgui.System):
	"""
	A subclass to handle our game specific gui
	"""
	def __init__(self):
		# Initiate the system
		bgui.System.__init__(self, '../../themes/default')
		
		# Use a frame to store all of our widgets
		self.frame = bgui.Frame(self, 'window', border=0)
		self.frame.colors = [(0, 0, 0, 0) for i in range(4)]

		# Create an image to display
		self.img = bgui.Image(self.frame, 'image', 'img.jpg', size=[.75, .75],
			options =  bgui.BGUI_CENTERED | bgui.BGUI_DEFAULT)

		# A button
		self.button = bgui.FrameButton(self.frame, 'button', text='Click Me!', size=[.3, .1], pos=[0, .05],
			options = bgui.BGUI_DEFAULT | bgui.BGUI_CENTERX)
		# Setup an on_click callback for the image
		self.button.on_click = self.on_img_click

		# Add a label
		self.lbl = bgui.Label(self.img, 'label', text="I'm a label!", pt_size=70, pos=[0, 1.0],
			options = bgui.BGUI_DEFAULT | bgui.BGUI_CENTERX)

		# A themed frame
		self.win = bgui.Frame(self, 'win', size=[0.5, 0.5],
			options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)
			
		# A couple of progress bars to demonstrate sub themes
		self.progress = bgui.ProgressBar(self.win, "progess", percent=0.75, size=[0.9, 0.01], pos=[0, 0.5],
											sub_theme="Progress", options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX)
											
		self.health = bgui.ProgressBar(self.win, "health", percent=0.5, size=[0.9, 0.01], pos=[0, 0.2],
											sub_theme="Health",	options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX)
			
		# A TextInput widget
		# self.lbl = bgui.TextInput(self.img, 'label', "I'm a label!", 'myfont.otf', 70, pos=[0, 0.8],
			# options = bgui.BGUI_DEFAULT | bgui.BGUI_CENTERX)
		
		# A counter property used for the on_img_click() method
		self.counter = 0
		
		# Create a keymap for keyboard input
		self.keymap = {getattr(bge.events, val): getattr(bgui, val) for val in dir(bge.events) if val.endswith('KEY') or val.startswith('PAD')}

	def on_img_click(self, widget):
		self.counter += 1
		self.lbl.text = "You've clicked me %d times" % self.counter

		if self.counter % 2 == 1:
			self.img.update_image('img_flipped.jpg')
		else:
			self.img.update_image('img.jpg')
	
	def main(self):
		"""A high-level method to be run every frame"""
		
		# Handle the mouse
		mouse = bge.logic.mouse
		
		pos = list(mouse.position)
		pos[0] *= bge.render.getWindowWidth()
		pos[1] = bge.render.getWindowHeight() - (bge.render.getWindowHeight() * pos[1])
		
		mouse_state = bgui.BGUI_MOUSE_NONE
		mouse_events = mouse.events
				
		if mouse_events[bge.events.LEFTMOUSE] == bge.logic.KX_INPUT_JUST_ACTIVATED:
			mouse_state = bgui.BGUI_MOUSE_CLICK
		elif mouse_events[bge.events.LEFTMOUSE] == bge.logic.KX_INPUT_JUST_RELEASED:
			mouse_state = bgui.BGUI_MOUSE_RELEASE
		elif mouse_events[bge.events.LEFTMOUSE] == bge.logic.KX_INPUT_ACTIVE:
			mouse_state = bgui.BGUI_MOUSE_ACTIVE
		
		self.update_mouse(pos, mouse_state)
		
		# Handle the keyboard
		keyboard = bge.logic.keyboard
		
		key_events = keyboard.events
		is_shifted = key_events[bge.events.LEFTSHIFTKEY] == bge.logic.KX_INPUT_ACTIVE or \
					key_events[bge.events.RIGHTSHIFTKEY] == bge.logic.KX_INPUT_ACTIVE
					
		for key, state in keyboard.events.items():
			if state == bge.logic.KX_INPUT_JUST_ACTIVATED:
				self.update_keyboard(self.keymap[key], is_shifted)
		
		# Now setup the scene callback so we can draw
		bge.logic.getCurrentScene().post_draw = [self.render]

def main(cont):
	own = cont.owner
	mouse = bge.logic.mouse

	if 'sys' not in own:
		# Create our system and show the mouse
		own['sys'] = MySys()
		mouse.visible = True

	else:
		own['sys'].main()
