from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.button import (MDRaisedButton, MDIconButton, MDFlatButton)
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog, BaseDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import MDList
from kivymd.uix.label import MDLabel
from functools import partial

class ListMDDialog(BaseDialog):
	# Get required data
	title = ''
	meal_group = ''
	meal = ''
	price = ''
	addon = ''
	aprice = ''
	tprice = ''
	status =''
	date = ''
	placed = ''

class ListDialog(ListMDDialog):
	def __init__(self, order_data):
		super().__init__()
		order_value = ['title', 'meal_group', 'meal','price','addon','aprice','tprice','status','date','placed']
		for o in range(len(order_data)):
			order_att  = str(order_data[o])
			order_val = order_value[o]
			setattr(self, order_att, order_val)

class ListDialog1(BaseDialog):
	def __init__(self, **kwargs):
		# Get required data
		title = kwargs['title']
		halign = kwargs['halign'] # 'left' if not root.device_ios else 'center'
		root = kwargs['root']
		meal_group =kwargs['meal_group']
		meal =kwargs['meal']
		price =kwargs['price']
		addon = kwargs['addon']
		aprice = kwargs['aprice']
		tprice = kwargs['tprice']
		status = kwargs['status']
		date = kwargs['date']
		placed = kwargs['placed']

		super().__init__()

		# Declare all main widgets
		main_box = MDBoxLayout(orientation='vertical', spacing='10dp', padding='15dp')
		title_lbl = MDLabel(text=title, valign='top', halign=halign, size_hint_y=None)
		main_scroll = ScrollView(size_hint_y=None) # Height=
		main_list = MDList(size_hint_y=None, spacing='15dp')
		main_list.height=main_list.height

		# Meal group
		mg_box = MDBoxLayout(orientation='horizontal', padding=('0dp', '0dp', '10dp', '0dp'),
							size_hint_y=None)
		mg_lbl = MDLabel(text='Meal Group: ')
		mg_name = MDLabel(text=meal_group)
		mg_box.add_widget(mg_lbl)
		mg_box.add_widget(mg_name)
		main_list.add_widget(mg_box)
		
		# Meal
		meal_box = MDBoxLayout(orientation='horizontal', padding=('0dp', '0dp', '10dp', '0dp'),
							size_hint_y=None)
		meal_lbl = MDLabel(text='Meal: ')
		meal_name = MDLabel(text=meal)
		meal_box.add_widget(meal_lbl)
		meal_box.add_widget(meal_name)
		main_list.add_widget(meal_box)
		
		# Price
		price_box = MDBoxLayout(orientation='horizontal', padding=('0dp', '0dp', '10dp', '0dp'),
							size_hint_y=None)
		price_lbl = MDLabel(text='Price: ')
		price_name = MDLabel(text=str(price))
		price_box.add_widget(price_lbl)
		price_box.add_widget(price_name)
		main_list.add_widget(price_box)

		# Add on
		addon_box = MDBoxLayout(orientation='horizontal', padding=('0dp', '0dp', '10dp', '0dp'),
							size_hint_y=None)
		addon_lbl = MDLabel(text='Add ons: ')
		addon_name = MDLabel(text=addon)
		addon_box.add_widget(addon_lbl)
		addon_box.add_widget(addon_name)
		main_list.add_widget(addon_box)
		
		# Add on price
		aprice_box = MDBoxLayout(orientation='horizontal', padding=('0dp', '0dp', '10dp', '0dp'),
							size_hint_y=None)
		aprice_lbl = MDLabel(text='Add ons price: ')
		aprice_name = MDLabel(text=str(aprice))
		aprice_box.add_widget(aprice_lbl)
		aprice_box.add_widget(aprice_name)
		main_list.add_widget(aprice_box)
		
		# Total price
		tprice_box = MDBoxLayout(orientation='horizontal', padding=('0dp', '0dp', '10dp', '0dp'),
							size_hint_y=None)
		tprice_lbl = MDLabel(text='Total price: ')
		tprice_name = MDLabel(text=str(tprice))
		tprice_box.add_widget(tprice_lbl)
		tprice_box.add_widget(tprice_name)
		main_list.add_widget(tprice_box)
		
		# Order Status
		status_box = MDBoxLayout(orientation='horizontal', padding=('0dp', '0dp', '10dp', '0dp'),
							size_hint_y=None)
		status_lbl = MDLabel(text='Status: ')
		status_name = MDLabel(text=status)
		status_box.add_widget(status_lbl)
		status_box.add_widget(status_name)
		main_list.add_widget(status_box)

		# Collection date and time
		date_box = MDBoxLayout(orientation='horizontal', padding=('0dp', '0dp', '10dp', '0dp'),
							size_hint_y=None)
		date_lbl = MDLabel(text='Collection time: ')
		date_name = MDLabel(text=date)
		date_box.add_widget(date_lbl)
		date_box.add_widget(date_name)
		main_list.add_widget(date_box)
		
		# Order placed on
		placed_box = MDBoxLayout(orientation='horizontal', padding=('0dp', '0dp', '10dp', '0dp'),
							size_hint_y=None)
		placed_lbl = MDLabel(text='Order placed on: ')
		placed_name = MDLabel(text=placed)
		placed_box.add_widget(placed_lbl)
		placed_box.add_widget(placed_name)
		main_list.add_widget(placed_box)
		
		main_scroll.add_widget(main_list)
		main_box.add_widget(title_lbl)
		main_box.add_widget(main_scroll)
		self.add_widget(main_box)

class reset_password(BoxLayout):
    def __init__(self, **kwargs):
        super(reset_password, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.height = "60dp"
        self.spacing = "12dp"
        self.size_hint_y = None

        self.new_floatie = FloatLayout()
        self.confirm_floatie = FloatLayout()

        self.new_password = MDTextField(multiline=False, size_hint=(0.6,0.75), pos_hint={"top":0.875, "right":0.8})
        self.new_password.hint_text = "Enter new password"
        self.new_eye = MDIconButton(icon="eye-off", pos_hint={"top":0.875, "right":0.95}, size_hint=(0.15, 0.75))
        self.new_password.required = True
        self.new_password.password = True

        self.confirm_password = MDTextField(multiline=False, size_hint=(0.6,0.75), pos_hint={"top":0.875, "right":0.8})
        self.confirm_eye = MDIconButton(icon="eye-off", pos_hint={"top":0.875, "right":0.95}, size_hint=(0.15, 0.75))
        self.confirm_password.hint_text = "Confirm new password"
        self.confirm_password.required = True
        self.confirm_password.password = True

        self.new_eye.bind(on_press=partial(self.hide_text, password=self.new_password, eye_man=self.new_eye))
        self.confirm_eye.bind(on_press=partial(self.hide_text, password=self.confirm_password, eye_man=self.confirm_eye))

        self.new_floatie.add_widget(self.new_password)
        self.new_floatie.add_widget(self.new_eye)
        self.confirm_floatie.add_widget(self.confirm_password)
        self.confirm_floatie.add_widget(self.confirm_eye)

        self.add_widget(self.new_floatie)
        self.add_widget(self.confirm_floatie)

    def hide_text(self, val, **kwargs):
        password = kwargs["password"]
        eye_man = kwargs["eye_man"]

        if password.password == True:
            password.password = False
            eye_man.icon = "eye"
        elif password.password == False:
            password.password = True
            eye_man.icon = "eye-off"

class name_popup(BoxLayout):

    def __init__(self, **kwargs):
        note = kwargs["note"]
        kwargs.pop("note", None)
        super(name_popup, self).__init__(**kwargs)
        # Input to enter your name
        self.orientation = "vertical"
        self.height = "60dp"
        self.spacing = "12dp"
        self.size_hint_y = None

        self.name_input = MDTextField(multiline=False, size_hint=(0.9, 0.5), pos_hint={"top":0.75, "right":0.95})
        self.name_input.hint_text = note
        self.name_input.required = True

        # Add the text input to layout
        self.add_widget(self.name_input)

class Dialog():
	def dialogs(self, **kwargs):
		dialogs = {}

		# Email Dialog
		confirm_email_btn = MDRaisedButton(text="Confirm")
		cancel_email_btn = MDFlatButton(text="Cancel")
		description = "Enter your email so we can send you a one time pin"

		verify_email = MDDialog(title ="Verify your email", text=description,
		                 size_hint=[0.9,0.5], buttons=[cancel_email_btn, confirm_email_btn],
		                 content_cls=name_popup(note="Email:"), type="custom") 

		for child in verify_email.content_cls.children:

		        if isinstance(child, MDTextField):
		            email = child

		dialogs["email"] = {}
		dialogs["email"]["buttons"] = {}
		dialogs["email"]["buttons"]["confirm_btn"] = confirm_email_btn
		dialogs["email"]["buttons"]["cancel_btn"] = cancel_email_btn
		dialogs["email"]["dialog"] = verify_email
		dialogs["email"]["textfield"] = email

		# Pin Dialog
		description = ""
		confirm_pin_btn = MDRaisedButton(text="Confirm")
		cancel_pin_btn = MDFlatButton(text="Cancel")
		verify_pin = MDDialog(title ="Enter Pin", text=description,
		                 size_hint=[0.9,0.5], buttons=[cancel_pin_btn, confirm_pin_btn],
		                 content_cls=name_popup(note="Pin:"), type="custom")
		for child in verify_pin.content_cls.children:
		    if isinstance(child, MDTextField):
		        pin = child

		dialogs["pin"] = {}
		dialogs["pin"]["buttons"] = {}
		dialogs["pin"]["buttons"]["confirm_btn"] = confirm_pin_btn
		dialogs["pin"]["buttons"]["cancel_btn"] = cancel_pin_btn
		dialogs["pin"]["dialog"] = verify_pin
		dialogs["pin"]["textfield"] = pin

		# Passwords Dialog
		confirm_btn = MDRaisedButton(text="Confirm")
		cancel_btn = MDFlatButton(text="Cancel")
		description = "Confirm your new password" #Create new password

		reset_pass = MDDialog( text=description,
		                 size_hint=[0.9,0.8], buttons=[cancel_btn, confirm_btn],
		                 content_cls=reset_password(), type="custom") #title ="Create new password",
		passwords = []
		for child in reset_pass.content_cls.children:
		    if isinstance(child, FloatLayout):
		        for grandchild in child.children:
		            if isinstance(grandchild, MDTextField):
		                passwords.append(grandchild)
		            else:
		                pass
		    else:
		        pass

		dialogs["passwords"] = {}
		dialogs["passwords"]["buttons"] = {}
		dialogs["passwords"]["buttons"]["confirm_btn"] = confirm_btn
		dialogs["passwords"]["buttons"]["cancel_btn"] = cancel_btn
		dialogs["passwords"]["dialog"] = reset_pass
		dialogs["passwords"]["textfield"] = passwords

		return dialogs

class ListMDDialog(BaseDialog):
	# Get required data
	title = ''
	meal_group = ''
	meal = ''
	price = ''
	addon = ''
	aprice = ''
	tprice = ''
	status =''
	date = ''
	placed = ''
"""
<ListMDDialog>:
	BoxLayout:
		orientation:'vertical'
		padding: dp(15)
		spacing: dp(10)

		MDLabel:
			id:title
			text: root.title
			halign:'left' if not root.device_ios else 'center'
			valign: 'top'
			size_hint_y: None
			text_size: self.width, None
			height:self.texture_size[1]

		ScrollView:
			id:scroll
			size_hint_y: None
			height: root.height - (title.height + dp(48)+sep.height)
			canvas:
				Rectangle:
					pos:self.pos
					size:self.size
					source: 'Images\\White.png'


			MDList:
				id: list_layout
				size_hint_y: None
				height:self.minimum_height
				spacing: dp(15)
				canvas.before:
					Rectangle:
						pos: self.pos
						size: self.size
					Color:
						rgba: [1,1,1,1]

				MDBoxLayout:
					MDLabel:
						text:'Meal group: '
					MDLabel:
						text:root.meal_group

				MDBoxLayout:
					MDLabel:
						text:'Meal: '
					MDLabel:
						text:root.meal

				MDBoxLayout:
					MDLabel:
						text:'Price: '
					MDLabel:
						text:root.price

				MDBoxLayout:
					MDLabel:
						text:'Add ons: '
					MDLabel:
						text:root.addon

				MDBoxLayout:
					MDLabel:
						text:'Add on price: '
					MDLabel:
						text:root.aprice

				MDBoxLayout:
					MDLabel:
						text:'Total: '
					MDLabel:
						text:root.tprice

				MDBoxLayout:
					MDLabel:
						text:'Status: '
					MDLabel:
						text:root.status

				MDBoxLayout:
					MDLabel:
						text:'Collection datetime: '
					MDLabel:
						text:root.date

				MDBoxLayout:
					MDLabel:
						text:'Order placed on: '
					MDLabel:
						text:root.placed

"""