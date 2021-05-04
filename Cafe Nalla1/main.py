# Third party imports
from kivy.app import App
from kivy.graphics import *
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.toast import toast
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivymd.uix.list import MDList
from kivy.animation import Animation
from kivymd.uix.label import MDLabel
from kivy.uix.checkbox import CheckBox
from kivy.uix.dropdown import DropDown
from kivymd.uix.dialog import MDDialog
from kivymd.theming import ThemeManager
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.spinner import MDSpinner
from kivy.clock import Clock, mainthread
from kivymd.uix.toolbar import MDToolbar
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import ButtonBehavior
from kivy.uix.scrollview import ScrollView
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivymd.uix.menu import MDDropdownMenu
from kivymd.theming import ThemableBehavior
from kivymd.uix.textfield import MDTextField
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.progressbar import ProgressBar
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.uix.card import MDSeparator, MDCard
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.dropdownitem import MDDropDownItem
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.picker import MDDatePicker, MDTimePicker
from kivy.uix.actionbar import ActionSeparator, ActionButton
from kivymd.uix.navigationdrawer import NavigationLayout, MDNavigationDrawer
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from kivymd.uix.button import (MDIconButton, MDFloatingActionButton, MDFlatButton,
                            MDRaisedButton, MDRectangleFlatButton, MDRectangleFlatIconButton,
                            MDRoundFlatButton, MDRoundFlatIconButton, MDFillRoundFlatButton,
                            MDFillRoundFlatIconButton, MDTextButton, MDFloatingActionButtonSpeedDial)
from kivymd.uix.list import (OneLineAvatarListItem, TwoLineAvatarListItem, ThreeLineAvatarListItem,
                             OneLineIconListItem, TwoLineIconListItem, ThreeLineIconListItem,
                             OneLineAvatarIconListItem, TwoLineAvatarIconListItem, ThreeLineAvatarIconListItem,
                             TwoLineListItem, ThreeLineListItem)
# STANDARD LIBRARY
import time
import threading
from queue import Queue
from functools import partial

# Local imports
from sent import Sent
from menu import Menu
from user  import User
from orders import Orders
from enquiry import Enquiry
from checkout import Checkout
from incoming import Incoming
from dbupdate import UpdateDB
from dbsignup import Login_User
from dbsendorder import SendOrder
from contentdrawer import Content
from emailconfirmation import Email
from dbcreateuser import Create_User
from dialog import Dialog, ListDialog
from check_credentials import Credentials
from widgets import Widgets, PlaceOrderPopUp, PlaceOrderVariable

# Screens 
class HomeScreen(Screen):
	pass

class MealsScreen(Screen):
	pass

class OrderScreen(Screen):
	pass

class LoginScreen(Screen):
	pass

class SignUpScreen(Screen):
	pass

class CheckoutScreen(Screen):
	pass

class AccountScreen(Screen):
	pass

class ViewScreen(Screen):
	pass


# Custom widgets
class LabelButton(ButtonBehavior, Label):
    pass

class FloatLayoutB(ButtonBehavior, FloatLayout):
	pass

class CafeNallaApp(MDApp):
	finalorderQ = Queue()
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		self.theme_cls = ThemeManager()
		self.theme_cls.theme_style = "Dark"
		self.theme_cls.primary_palette = "Amber" 
		self.GUI = Builder.load_file('cafenalla.kv')
		self.user = User()
		self.menu = Menu()
		self.orders = Orders()
		self.widgets = Widgets()
		self.incoming_orders = Incoming()
		self.sent_orders = Sent()

	def build(self):
		return self.GUI

	def on_start(self):
		logged =False
		try:
			logged = self.user.logged_on
			if logged == True:
				self.change_screen('home_screen')
				self.refresh_home()
			else:
				self.login()
		except Exception as e:
			print(f'Something went wrong... {e}')
			self.login()

	def go_home(self, **kwargs):
		self.change_screen('home_screen')
		self.refresh_home()

	def login(self, **kwargs):
		def hide_text(eye_man, password, val):
			if password.password == True:
				password.password = False
				eye_man.icon = "eye"
			elif password.password == False:
				password.password = True
				eye_man.icon = "eye-off"

		def dismiss(pop, val):
			pop.dismiss()

		def check_login(f_name, p_word, current_screen, value):
			# A python requirement for calling functions inn different classes
			cred = Credentials()

			# Check if credentials are valid
			is_cred_valid = Credentials.check_credentials(cred, First_name=f_name, Password=p_word,
			                                            login_type="login")

			# Now we cansend this data to our data base as a user, if cred is valid of course
			if is_cred_valid == True:
				name = f_name.text
				password = p_word.text
				#bigPoppa = self.root.ids["home_screen"].ids["condition_banner"]

				# Look for the user locally first before consulting the database
				user_local = False
				if name == self.user.first_name:
					if password == self.user.password:
						print("Found the user locally")
						self.user.logged_on = True
						self.user.cache_user(self.user)

						self.change_screen("home_screen")
						self.refresh_home()
						user_local = True
					else:
						pass
				else:
					pass

				if user_local == False:
					conQ = Queue()
					db = Login_User(conQ=conQ)

					connected = conQ.get()

					if isinstance(connected, bool):

						# Create a new user in our data base
						found_user = db.find_user(first_name=f_name, password=p_word, user=self.user)

						if isinstance(found_user, list):
							if found_user[0] == True:
								self.user.user_id = found_user[1]["user_id"]
								self.user.logged_on = found_user[1]["logged_on"]
								self.user.first_name = found_user[1]["first_name"]
								self.user.email = found_user[1]["email"]
								self.user.password = found_user[1]["password"]
								self.user.last_name = found_user[1]["last_name"]
								self.user.regular_drink = found_user[1]["regular_drink"]
								self.user.loyalty_points = found_user[1]['loyalty_points']
								self.user.cache_user(self.user)

								self.change_screen("home_screen")
								self.refresh_home()
							else:
								# Invalid user
								warning = self.root.ids["login_screen"].ids["warning"]
								warning.clear_widgets()

								with warning.canvas.before:
									Color(rgba=(0.922, 0.541, 0.565, 0.25))
									Rectangle(size=warning.size, pos=warning.pos)

								warning_lbl = Label(text="Invalid user name or password.")

								label_num = 0
								label = self.widgets.configure_new_widget(widget_type="label",value=0, widget_num=label_num, widget=self.widgets.label,
								                                          layout="gridlayout", current_screen=current_screen, text=text)
								self.widgets.label = label[0]
								label_num = label[1]

								warning.add_widget(self.widgets.label["widgets"][label_num])

								f_name.background_color = (0.922, 0.541, 0.565, 0.25)

								p_word.text = ""
								p_word.background_color = (0.922, 0.541, 0.565, 0.25)

						elif isinstance(found_user, bool):
							# Invalid user 
							# #FF8A80 background error color
							error_grid = self.root.ids["login_screen"].ids["warning"]
							error_grid.clear_widgets()
							r = 255/255
							g = 138/255
							b = 128/255
							with error_grid.canvas:
							    Color(rgba=(r, g, b, 0.5))

							error_lbl = Label(text="Invalid user name or password!!")
							toast('Access denied')

							error_grid.add_widget(error_lbl)
							f_name.background_color = (0.922, 0.541, 0.565, 0.25)

							p_word.text = ""
							p_word.background_color = (0.922, 0.541, 0.565, 0.25)

					elif isinstance(connected, str):

						confirm_btn = MDRaisedButton(text="Confirm")

						failed_con_pop = MDDialog(title ="Failed connection!!", 
						                 text = connected,
						                 size_hint=[0.5,0.5], buttons=[confirm_btn])

						confirm_btn.bind(on_press=partial(dismiss, failed_con_pop))
						failed_con_pop.open()

			else:
				toast("Invalid Entry!!")
				print("Invalid credentials")

		def OTPPop(val):
			def cancel(pop, val):
				pop.dismiss()

			def confirm_passwords(pop, passwords, user_cached, user_id, email, spinner, dialogs,val):
				new_pass = passwords[0].text
				confirm_pass = passwords[1].text

				if new_pass == confirm_pass:
					pop.dismiss()
					toast("Setting you up please be patient")
					spinner[0].add_widget(spinner[1])

					# Use the email id to get all the information for this particular user
					if user_cached == True:
						# Look for user locally
						self.user.password = new_pass
						self.user.logged_on = True
						self.user.cache_user(self.user)
						self.change_screen("home_screen")
						self.refresh_home()
						spinner[0].remove_widget(spinner[1])
						# Now update database from pickle
					else: 
						# Search for user in the data base
						self.user.user_id = user_id
						self.user.logged_on = True
						self.user.email = email
						self.user.password = new_pass

						def lets_get_this_user():
							conQ = Queue()
							get_info = Login_User(conQ=conQ)
							connected = conQ.get()

							if isinstance(connected, bool):
								self.user = get_info.get_user_info(user=self.user)

							self.user.cache_user(self.user)
							self.change_screen("home_screen")
							self.refresh_home()
							spinner[0].remove_widget(spinner[1])

						threading.Thread(target=lets_get_this_user).start()
						# Get user from database using a thread
				else:
					passwords[0].text = ""
					passwords[1].text = ""
					toast("Passwords do not match!!")
					return

			def confirm_pin(pop, input_field, random_val, time_up, found_local, user_id, email, spinner, dialogs,val):
				plausable_pin = False
				try:
					pin = input_field.text
					pin = int(pin)
					plausable_pin = True

				except Exception as e:
					print("Enter an integer please")
					toast("Invalid pin!!")

				if plausable_pin == True:
					if time_up == True:
						pop.dismiss()
						toast("Your pin has expired try again!!")
					    
					else:
						if pin == random_val:
							pop.dismiss()
							dialogs["passwords"]["buttons"]["confirm_btn"].bind(on_press=partial(confirm_passwords, dialogs["passwords"]["dialog"], dialogs["passwords"]["textfield"], 
							                                                                    found_local, user_id, email, spinner, dialogs))
							dialogs["passwords"]["buttons"]["cancel_btn"].bind(on_press=partial(cancel, dialogs["passwords"]["dialog"]))
							dialogs["passwords"]["dialog"].open()
     
						else:
							print(f"Enter the pin sent to your email. \nYou entered: {pin} of type{type(pin)}\n However we looking for: {random_val} of type {type(random_val)}")
							toast("Invalid pin!!")

				else:
					pass



			def confirm_email(pop, input_field, dialogs,val):
				def start_e_confirmation(pop, input_field, spinner, dialogs):

					def create_dialog(**kwargs):

						confirm = kwargs["con_text"]
						cancel = kwargs["can_text"]
						title = kwargs["title"]
						note = kwargs["note"]
						description= kwargs["description"]


						confirm_btn = MDRaisedButton(text=confirm)
						cancel_btn = MDFlatButton(text=cancel)


						verify_pin = MDDialog(title =title, text=description,
						                 size_hint=[0.5,0.5], buttons=[cancel_btn, confirm_btn],
						                 content_cls=name_popup(note=note), type="custom") 

						for child in verify_pin.content_cls.children:

						        if isinstance(child, MDTextField):
						            pin = child

						return confirm_btn, cancel_btn, pin, verify_pin

					valid_email = Queue()
					connectionQ = Queue()
					email_text = input_field.text
					found_local = False
					error_grid = self.root.ids["login_screen"].ids["warning"]
					error_grid.clear_widgets()

					if email_text != "" or email_text != " ":

						email = Email(emailQ=valid_email, connection=connectionQ, email=email_text)

						valid_mail = valid_email.get()
						if valid_mail == True:
							# Check if we have this email in our database, in a threading
							if self.user.email != None:
								if email_text == self.user.email:
									DBconnected = True
									found_local = True
								else:
									conQ = Queue()
									find_mail = Login_User(conQ=conQ)
									DBconnected = conQ.get()
							else:
								conQ = Queue()
								find_mail = Login_User(conQ=conQ)
								DBconnected = conQ.get()

							if isinstance(DBconnected, bool):
								if found_local == True:
									connected = True
									found_email = self.user.user_id
								else:
									found_email = find_mail.find_email(email=email_text) 
									connected = connectionQ.get()

								if isinstance(found_email, int): 

									if connected == True:
										pop.dismiss()
										random_val = random.randint(100000,999999)
										subject = "Cafe Nalla - One Time Pin"
										message = f"This is your pin '{random_val}', enter it in the text area. It will expire in 5 mins."
										mail_sent = Queue()
										email.prep_email(subject=subject, message=message, email_sent=mail_sent)

										sent_email = mail_sent.get()
										if sent_email == True:
											#start timer
											time_up = False
											thread = threading.Thread(target=CountDown.start_CD,  kwargs={"seconds":300, "time_up":time_up}, 
											                          args=(CountDown,)).start()

											#confirm_btn, cancel_btn, pin, verify_pin = create_dialog(con_text="Confirm", can_text="Cancel", title="Enter Pin", note="Pin:", description=description)
											dialogs["pin"]["buttons"]["cancel_btn"].bind(on_press=partial(cancel, dialogs["pin"]["dialog"]))
											dialogs["pin"]["buttons"]["confirm_btn"].bind(on_press=partial(confirm_pin, dialogs["pin"]["dialog"], dialogs["pin"]["textfield"], random_val, 
											                                                                time_up, found_local, found_email, email_text, spinner, dialogs))
											dialogs["pin"]["dialog"].open()
											#cancel_btn.bind(on_press=partial(cancel, verify_pin))
											#confirm_btn.bind(on_press=partial(confirm_pin, verify_pin, pin, random_val, time_up, found_local, found_email, email_text, spinner))
											#verify_pin.open()
											spinner[0].remove_widget(spinner[1])

										else:
											spinner[0].remove_widget(spinner[1])
											toast("Failed to send email")
											r = 255/255
											g = 138/255
											b = 128/255
											with error_grid.canvas:
											    Color(rgba=(r, g, b, 0.5))

											error_lbl = MDLabel(text="Failed to send an email, check your connection!!")

											error_grid.add_widget(error_lbl)
											input_field.text = ""

											pop.dismiss()
									else:
										spinner[0].remove_widget(spinner[1])
										toast("No connection")
										r = 255/255
										g = 138/255
										b = 128/255
										with error_grid.canvas:
										    Color(rgba=(r, g, b, 0.5))

										error_lbl = MDLabel(text="Please check your connection and try again!!")

										error_grid.add_widget(error_lbl)
										input_field.text = ""

										pop.dismiss()#Please check your connection and try again
								else:
									spinner[0].remove_widget(spinner[1])
									toast("Account not found")
									r = 255/255
									g = 138/255
									b = 128/255
									with error_grid.canvas:
									    Color(rgba=(r, g, b, 0.5))

									error_lbl = MDLabel(text="Email not found, make sure you already have an account or create a new one!!")

									input_field.text = ""
									pop.dismiss()
							else:
								spinner[0].remove_widget(spinner[1])
								toast("No connection")
								r = 255/255
								g = 138/255
								b = 128/255
								with error_grid.canvas:
								    Color(rgba=(r, g, b, 0.5))

								error_lbl = MDLabel(text="Please check your connection and try again!!")

								error_grid.add_widget(error_lbl)
								input_field.text = ""
								pop.dismiss()
						else:
							spinner[0].remove_widget(spinner[1])
							toast("Invalid email")
							r = 255/255
							g = 138/255
							b = 128/255
							with error_grid.canvas:
							    Color(rgba=(r, g, b, 0.5))

							error_lbl = MDLabel(text="Please enter a valid email!!")

							error_grid.add_widget(error_lbl)

							input_field.text = ""
							pop.dismiss()
					else:
						spinner[0].remove_widget(spinner[1])
						toast("No email")
						r = 255/255
						g = 138/255
						b = 128/255
						with error_grid.canvas:
						    Color(rgba=(r, g, b, 0.5))

						error_lbl = MDLabel(text="Please enter your email!!")

						error_grid.add_widget(error_lbl)

						input_field.text = ""
						pop.dismiss()

				# Create spinner right here
				spinner_grid = self.root.ids["login_screen"].ids["bottom_floatie"]

				spinner = MDSpinner(size_hint=(None, None), size=(46, 46),
				                        pos_hint={'center_x': .5, 'center_y': .5}, active=True)
				spinner_tools = []
				spinner_tools.append(spinner_grid)
				spinner_tools.append(spinner)
				spinner_tools[0].add_widget(spinner_tools[1])

				t = threading.Thread(target=start_e_confirmation, args=(pop, input_field, spinner_tools, dialogs))
				t.start()

			popup = Dialog()
			dialogs = popup.dialogs()

			dialogs["email"]["buttons"]["confirm_btn"].bind(on_press=partial(confirm_email, dialogs["email"]["dialog"], dialogs["email"]["textfield"], dialogs))
			dialogs["email"]["buttons"]["cancel_btn"].bind(on_press=partial(cancel, dialogs["email"]["dialog"]))
			dialogs["email"]["dialog"].open()

		# Collect data fro the sign up page
		first_name = self.root.ids["login_screen"].ids["first_name"]
		if self.user.first_name != None:
		    first_name.text = self.user.first_name

		eye_man = self.root.ids["login_screen"].ids["hide_password"]
		password = self.root.ids["login_screen"].ids["password"]

		# Submit button
		login_btn = self.root.ids["login_screen"].ids["login"]
		forgot_password = self.root.ids["login_screen"].ids["forgot_password"]
		screen_manager = self.root.ids["screen_manager"]
		current_screen = screen_manager.current

		forgot_password.bind(on_press=partial(OTPPop,))
		login_btn.bind(on_press=partial(check_login, first_name, password, current_screen)) 
		eye_man.bind(on_release=partial(hide_text, eye_man, password)) 

	def sign_up(self):
		def hide_text(eye_man, password, val):
			if password.password == True:
				password.password = False
				eye_man.icon = "eye"
			elif password.password == False:
				password.password = True
				eye_man.icon = "eye-off"

		def dismiss(pop, val):
			pop.dismiss()

		def check_sign_up(f_name, l_name, e_mail, p_word, value):
			# A python requirement for calling functions inn different classes
			cred = Credentials()

			# Check if credentials are valid
			is_cred_valid = Credentials.check_credentials(cred, First_name=f_name,
			                                              Last_name=l_name, Email=e_mail,
			                                              Password=p_word, login_type="signin")

			# Now we cansend this data to our data base as a user, if cred is valid of course
			if is_cred_valid == True:
				conQ = Queue()
				user_created = Queue()
				userQ = Queue()

				admin = 2
				create_user = Create_User(first_name=f_name, last_name=l_name,
                                        email=e_mail, password=p_word, conQ=conQ, user_created=user_created,
                                        user=self.user, userQ=userQ, admin=admin)

				connected = conQ.get()

				if isinstance(connected, bool):
					# After creating a user in the database we switch screen
					created = user_created.get()

					if created == True:
						user = userQ.get()

						if user != None:
							self.user = user
							self.user.cache_user(self.user)
							self.change_screen("home_screen")
							self.refresh_home()
						else:
							toast("Something went terribly wrong please try again!!")

					else:
						toast("Something went wrong please try again!!")

				elif isinstance(connected, str):
					toast("Please check your connection and try again!!")

					print("Something went wrong. Either database got corrupted or connection was lost.")

			else:
				print("Invalid credentials")
            

		# Collect data fro the sign up page
		first_name = self.root.ids["sign_up_screen"].ids["first_name"]
		last_name = self.root.ids["sign_up_screen"].ids["last_name"]
		email = self.root.ids["sign_up_screen"].ids["email"]
		password = self.root.ids["sign_up_screen"].ids["password"]
		eye_man = self.root.ids["sign_up_screen"].ids["hide_password"]

		submit_btn = self.root.ids["sign_up_screen"].ids["submit"]

		submit_btn.bind(on_press=partial(check_sign_up, first_name, last_name, email, password))
		eye_man.bind(on_press=partial(hide_text, eye_man, password))

	def refresh_home(self, **kwargs):
		bigPoppa = self.root.ids["home_screen"].ids['menu']
		bigPoppa.clear_widgets()
		def output_something(params, btn):
			btn = params[0]
			meal_group = params[1]
			print(f"Pressed: {params}")
			self.change_screen('meals_screen')

			self.load_meals(meal_group=meal_group)

		r_btn_num = 0
		card_num = 0
		image_num = 0
		box_num = 0
		floatie_num = 0
		label_num = 0
		icon_num = 0
		screen_manager = self.root.ids['screen_manager']
		current_screen = screen_manager.current_screen

		for key, val in self.menu.menu.items():
			meal_group = key
			image = self.menu.menu[meal_group]['image']
			card = self.widgets.configure_new_widget(widget_type='card', widget_num=card_num,
													widget=self.widgets.card, layout='floatlayout',
													current_screen=current_screen, top=0.975,side='right',side_val=0.975,
													width=0.95,height=0.95, orientation='vertical')
			self.widgets.card = card[0]
			card_num = card[1]

			#select_box = BoxLayout(orientation='horizontal', size_hint_y=0.25)
			boxlayout = self.widgets.configure_new_widget(widget_type='boxlayout', widget_num=box_num,
														  widget=self.widgets.boxlayout, layout='boxlayout',
														  orientation='horizontal', size_hint_y=0.20,
														  pop_orientation='vertical', current_screen=current_screen)
			self.widgets.boxlayout = boxlayout[0]
			box_num = boxlayout[1]

			label = self.widgets.configure_new_widget(widget_type="mdlabel",value=0, widget_num=label_num, widget=self.widgets.label,
													layout="boxlayout", current_screen=current_screen, text=f'{meal_group.replace("_", " ")}',
													size_hint_x=0.75, orientation='horizontal')
			self.widgets.label = label[0]
			label_num = label[1]

			icon_button = self.widgets.configure_new_widget(widget_type="icon_button", widget_num=icon_num, widget=self.widgets.icon_button,
													layout="boxlayout", current_screen=current_screen, icon='arrow-right',
													orientation='horizontal', size_hint_x=0.25, params=('active_widget', f'{meal_group}'), 
													func=output_something)
			self.widgets.icon_button = icon_button[0]
			icon_num = icon_button[1]

			image = self.widgets.configure_new_widget(widget_type="image", widget_num=image_num, widget=self.widgets.image,
													layout="boxlayout", current_screen=current_screen, source=f'Images/{image}',
													orientation='vertical', size_hint_y=0.80)
			self.widgets.image = image[0]
			image_num = image[1]

			floatlayout = self.widgets.configure_new_widget(widget_type="floatlayout", widget_num=floatie_num, widget=self.widgets.floatlayout,
													layout="gridlayout", current_screen=current_screen)
			self.widgets.floatlayout = floatlayout[0]
			floatie_num = floatlayout[1]

			#menu_image = Image(source="Images/La coffee.jpg", allow_stretch=True, size_hint_y=0.75, keep_ratio=False)
			self.widgets.boxlayout['widgets'][box_num].add_widget(MDLabel(text=f'{meal_group.replace("_", " ")}', size_hint_x=0.75))
			self.widgets.boxlayout['widgets'][box_num].add_widget(self.widgets.icon_button['widgets'][icon_num])

			self.widgets.card["widgets"][card_num].add_widget(self.widgets.image["widgets"][image_num])
			self.widgets.card["widgets"][card_num].add_widget(self.widgets.boxlayout['widgets'][box_num])

			self.widgets.floatlayout['widgets'][floatie_num].add_widget(self.widgets.card["widgets"][card_num])
			bigPoppa.add_widget(self.widgets.floatlayout['widgets'][floatie_num])
			card_num = card_num+1
			image_num = image_num+1
			box_num = box_num+1
			floatie_num = floatie_num+1
			label_num = label_num+1
			icon_num = icon_num+1

	def log_out(self, **kwargs):
		def logout(btn, pop, val):
			self.user.logged_on = False
			self.user.cache_user(self.user)
			self.change_screen("login_screen")
			self.refresh_home()
			self.login()
			pop.dismiss()

		def stay_logged(btn, pop, val):
		    pop.dismiss()
		    
		yes_btn = MDRaisedButton(text="Yes")
		no_btn = MDFlatButton(text="Cancel")
		popup = MDDialog(title ='Logout?', 
		                     text = 'You sure you want to logout ? ',
		                     size_hint=[0.9,0.5], buttons=[no_btn, yes_btn])

		yes_btn.bind(on_press=partial(logout, yes_btn, popup))
		no_btn.bind(on_press=partial(stay_logged, no_btn, popup))
		popup.open()

	def populate_drawer(self, **kwargs):
		screen_manager = kwargs['sm']
		nav_drawer = kwargs['nav']
		print('We in the nav')

		page = screen_manager.current
		userContent = False

		if page == 'home_screen':
			layout = Content(orientation='vertical', padding='8dp', spacing='20dp')
			layout.nav_drawer = nav_drawer
			layout.screen_manager = screen_manager
			content = Content.home_screen(layout, nav_drawer, self.change_screen, meal_page_func=self.load_meals,
										log_out=self.log_out)
			userContent = True

		elif page == 'meals_screen':
			layout = Content(orientation='vertical', padding='8dp', spacing='20dp')
			layout.nav_drawer = nav_drawer
			layout.screen_manager = screen_manager
			content = Content.meals_screen(layout, nav_drawer, self.change_screen)
			userContent = True

		elif page == 'order_screen':
			layout = Content(orientation='vertical', padding='8dp', spacing='20dp')
			layout.nav_drawer = nav_drawer
			layout.screen_manager = screen_manager
			content = Content.order_screen(layout, nav_drawer, self.change_screen)
			userContent = True

		elif page == 'checkout_screen':
			layout = Content(orientation='vertical', padding='8dp', spacing='20dp')
			layout.nav_drawer = nav_drawer
			layout.screen_manager = screen_manager
			content = Content.checkout_screen(layout, nav_drawer, self.change_screen)
			userContent = True

		elif page == 'account_screen':
			layout = Content(orientation='vertical', padding='8dp', spacing='20dp')
			layout.nav_drawer = nav_drawer
			layout.screen_manager = screen_manager
			content = Content.account_screen(layout, nav_drawer, self.change_screen)
			userContent = True

		elif page == 'view_screen':
			layout = Content(orientation='vertical', padding='8dp', spacing='20dp')
			layout.nav_drawer = nav_drawer
			layout.screen_manager = screen_manager
			content = Content.view_screen(layout, nav_drawer, self.change_screen)
			userContent = True

		for child in nav_drawer.children:
			nav_drawer.remove_widget(child)
			del(child)

		# Add details about the user 
		if userContent == True:
			# Add permanent header
			scroll = ScrollView()
			scrollgrid = GridLayout(cols=1, size_hint_y=None, row_default_height='50dp', row_force_default=True)
			scrollgrid.height = scrollgrid.minimum_height
			scroll.add_widget(scrollgrid)

			for draw in content:
				scrollgrid.add_widget(draw)

			layout.add_widget(scroll)
			nav_drawer.add_widget(layout)

	def change_screen(self, screen, **kwargs):
		print(f'Going to page: {screen}')
		screen_manager = self.root.ids['screen_manager']
		prev_screen = screen_manager.current

		if screen == 'meals_screen' and prev_screen == 'order_screen':
			screen_manager.transition.direction = 'left'
		elif screen == 'order_screen' and prev_screen == 'meals_screen':
			screen_manager.transition.direction = 'right'
		elif screen == 'home_screen' and prev_screen == 'order_screen':
			screen_manager.transition.direction = 'left'
		elif screen == 'home_screen' and prev_screen == 'meals_screen':
			screen_manager.transition.direction = 'left'
		elif screen == 'home_screen' and prev_screen == 'checkout_screen':
			screen_manager.transition.direction = 'left'
		elif screen == 'order_screen' and prev_screen == 'home_screen':
			screen_manager.transition.direction = 'right'
		elif screen == 'checkout_screen' and prev_screen == 'home_screen':
			screen_manager.transition.direction = 'right'
		elif screen == 'meals_screen' and prev_screen == 'home_screen':
			screen_manager.transition.direction = 'right'

		screen_manager.current = screen
		nav_drawer = self.root.ids["nav_drawer"]
		self.populate_drawer(sm=screen_manager, nav=nav_drawer)

		if screen == 'account_screen':
			self.account()

	def load_meals(self, **kwargs):
		def place_order(params, btn):
			print(f'Pressed: {params}')
			self.change_screen('order_screen')
			self.confirm_order(active_meal=params)

		bigPoppa =self.root.ids['meals_screen'].ids['menu']
		screen_manager = self.root.ids['screen_manager']
		current_screen = screen_manager.current
		bigPoppa.clear_widgets()

		meal_group = kwargs['meal_group']

		box_num = 0
		label_num = 0
		label_num2 = 0
		twolinelist_num = 0
		meal_dict = {}
		fill_meal = False
		if meal_group == "Breakfast" or meal_group == 'Salads' or meal_group == 'Specials':
			if len(list(self.menu.menu[meal_group]['Meal'].keys())) > 0:
				meal_dict = self.menu.menu[meal_group]['Meal']
				fill_meal = True
		else: 
			if len(list(self.menu.menu[meal_group].keys())) > 0:
				meal_dict = self.menu.menu[meal_group]
				fill_meal = True

		if fill_meal == True:
			for key, val in meal_dict.items():
				if meal_group == 'Meals':
					if key != 'image':
						label = self.widgets.configure_new_widget(widget_type="label",value=0, widget_num=label_num, widget=self.widgets.label,
														layout="boxlayout", current_screen=current_screen, text=f'{key.replace("_", " ")}',
														size_hint_x=0.75, orientation='horizontal')
						self.widgets.label = label[0]
						label_num = label[1]

						bigPoppa.add_widget(self.widgets.label['widgets'][label_num])

						for vey, kal in meal_dict[key]['Meal'].items():
							# box layout for this meal
							boxlayout = self.widgets.configure_new_widget(widget_type='boxlayout', widget_num=box_num,
															  widget=self.widgets.boxlayout, layout='gridlayout',
															  orientation='horizontal', size_hint_y=0.20,
															  current_screen=current_screen)
							self.widgets.boxlayout = boxlayout[0]
							box_num = boxlayout[1]

							ingredients = ''
							for ingre in meal_dict[key]['Meal'][vey]['Ingredients']:
								if ingre != meal_dict[key]['Meal'][vey]['Ingredients'][-1]:
									ingredients = ingredients+ingre+', '
								else:
									ingredients = ingredients+ingre

							twolinelist = self.widgets.configure_new_widget(widget_type='twolinelist', widget_num=twolinelist_num,
															  widget=self.widgets.twolinelist, layout='boxlayout', text=vey.replace("_", ' '),
															  orientation='horizontal', size_hint_x=0.85, secondary_text=ingredients,
															  current_screen=current_screen, func=place_order, params=('active_widget', vey, meal_group, key))
							self.widgets.twolinelist = twolinelist[0]
							twolinelist_num = twolinelist[1]

							price = meal_dict[key]['Meal'][vey]['Price']
							label = self.widgets.configure_new_widget(widget_type="label",value=0, widget_num=label_num2, widget=self.widgets.label,
														layout="boxlayout", current_screen=current_screen, text=f'R{str(price)}',
														size_hint_x=0.15, orientation='horizontal')
							self.widgets.label = label[0]
							label_num2 = label[1]

							self.widgets.boxlayout['widgets'][box_num].add_widget(self.widgets.twolinelist['widgets'][twolinelist_num])
							self.widgets.boxlayout['widgets'][box_num].add_widget(self.widgets.label['widgets'][label_num2])
							bigPoppa.add_widget(self.widgets.boxlayout['widgets'][box_num])
							
							box_num=box_num+1
							label_num2 = label_num2+1
							twolinelist_num = twolinelist_num+1
				else:
					if key != 'image':
						boxlayout = self.widgets.configure_new_widget(widget_type='boxlayout', widget_num=box_num,
															  widget=self.widgets.boxlayout, layout='gridlayout',
															  orientation='horizontal', size_hint_y=0.20,
															  current_screen=current_screen)
						self.widgets.boxlayout = boxlayout[0]
						box_num = boxlayout[1]

						ingredients = ''            #Ingredients
						for ingre in meal_dict[key]['Ingredients']:
							if ingre != meal_dict[key]['Ingredients'][-1]:
								ingredients = ingredients+ingre+', '
							else:
								ingredients = ingredients+ingre

						twolinelist = self.widgets.configure_new_widget(widget_type='twolinelist', widget_num=twolinelist_num,
														  widget=self.widgets.twolinelist, layout='boxlayout', text=key.replace("_", ' '),
														  orientation='horizontal', size_hint_x=0.85, secondary_text=ingredients,
														  current_screen=current_screen, func=place_order, params=('active_widget', key, meal_group))
						self.widgets.twolinelist = twolinelist[0]
						twolinelist_num = twolinelist[1]

						price = meal_dict[key]['Price']
						label = self.widgets.configure_new_widget(widget_type="label",value=0, widget_num=label_num2, widget=self.widgets.label,
													layout="boxlayout", current_screen=current_screen, text=f'R{str(price)}',
													size_hint_x=0.15, orientation='horizontal')
						self.widgets.label = label[0]
						label_num2 = label[1]

						self.widgets.boxlayout['widgets'][box_num].add_widget(self.widgets.twolinelist['widgets'][twolinelist_num])
						self.widgets.boxlayout['widgets'][box_num].add_widget(self.widgets.label['widgets'][label_num2])
						bigPoppa.add_widget(self.widgets.boxlayout['widgets'][box_num])

						box_num=box_num+1
						label_num2 = label_num2+1
						twolinelist_num = twolinelist_num+1

					else:
						pass

				label_num = label_num+1
		else:
			self.change_screen('home_screen')
			self.refresh_home()

	def confirm_order(self, **kwargs):
		active_meal = kwargs['active_meal']
		meal_group = active_meal[2]
		meal = active_meal[1]

		screen_manager = self.root.ids['screen_manager']
		current_screen = screen_manager.current
		def cancel_order(params, btn):
			print(f'Cancelling order: {params}')

		def confirm_order1(params, btn):
			print(f'Confirming order:  {params}')

		def on_checkbox_active(price, price_lbl, checkbox, value):
			if value:
				price_ = int(price_lbl.text.replace('R',''))
				new_price = int(price) + price_

				price_lbl.text = f'R{str(new_price)}'
			else:
				price_ = int(price_lbl.text.replace('R',''))
				new_price = price_ - int(price)

				price_lbl.text = f'R{str(new_price)}'

		# Configure order page
		meal_name_lbl = self.root.ids['order_screen'].ids['meal_name']
		meal_price_lbl = self.root.ids['order_screen'].ids['meal_price']
		navigation_label = self.root.ids['order_screen'].ids['navigation']
		ingredients_label = self.root.ids['order_screen'].ids['ingredients']
		extra_banner = self.root.ids['order_screen'].ids['extras']

		extra_banner.clear_widgets()

		# Create confirmation popup
		if meal_group == 'Breakfast' or meal_group == 'Salads':
			ingredients=self.menu.menu[meal_group]['Meal'][meal]['Ingredients']
			price=self.menu.menu[meal_group]['Meal'][meal]['Price']
			if 'Add_ons' in list(self.menu.menu[meal_group].keys()):
				add_ons = self.menu.menu[meal_group]['Add_ons']

				meal_price_lbl.text = f'R{str(price)}'
				meal_name_lbl.text = f'{meal.replace("_", " ")}'

				# Configure navigation value
				navigation_label.text = f'{meal_group.replace("_", " ")}>{meal.replace("_", " ")}'

				# Add ingredients
				ingredient = ''
				for ingre in ingredients:
					if ingre == ingredients[-1]:
						ingredient = ingredient+ingre
					else:
						ingredient = ingredient+ingre+', '
				ingredients_label.text=ingredient

				# Add guiding label
				label = MDLabel(text='Add ons:')
				extra_banner.add_widget(label)

				# Include adds ons
				for key, val in add_ons.items():
					item = PlaceOrderVariable(extra_type='Add_ons', name=key, price=val, 
											  price_lbl=meal_price_lbl, func=on_checkbox_active)
					extra_banner.add_widget(item)

			else:
				# Add code here if a meal is required that does not contain add ons
				pass

		elif meal_group == 'Meals':
			meal_type = active_meal[3]
			ingredients = self.menu.menu[meal_group][meal_type]['Meal'][meal]['Ingredients']
			price=self.menu.menu[meal_group][meal_type]['Meal'][meal]['Price']

			if 'Add_ons' in list(self.menu.menu[meal_group][meal_type].keys()):
				add_ons = self.menu.menu[meal_group][meal_type]['Add_ons']

				meal_price_lbl.text = f'R{str(price)}'
				meal_name_lbl.text = f'{meal.replace("_", " ")}'

				# Add ingredients
				ingredient = ''
				for ingre in ingredients:
					if ingre == ingredients[-1]:
						ingredient = ingredient+ingre
					else:
						ingredient = ingredient+ingre+', '
				ingredients_label.text=ingredient


				navigation_label.text = f'{meal_group.replace("_", " ")}>{meal_type.replace("_", " ")}>{meal.replace("_", " ")}'

				label = MDLabel(text='Add ons:')
				extra_banner.add_widget(label)
				for key, val in add_ons.items():
					item = PlaceOrderVariable(extra_type='Add_ons', name=key, price=val,
											  price_lbl=meal_price_lbl, func=on_checkbox_active)
					extra_banner.add_widget(item)
			else:
				# Add code here if a meal is required that does not contain add ons
				pass

		elif meal_group == 'Smoothies' or meal_group == 'Shakes' or meal_group == 'Something_cold':
			ingredients=self.menu.menu[meal_group][meal]['Ingredients']
			price=self.menu.menu[meal_group][meal]['Price']

			if 'Extra' in list(self.menu.menu[meal_group][meal].keys()):
				extras = self.menu.menu[meal_group][meal]['Extra']

				meal_price_lbl.text = f'R{str(price)}'
				meal_name_lbl.text = f'{meal.replace("_", " ")}'

				# Add ingredients
				ingredient = ''
				for ingre in ingredients:
					if ingre == ingredients[-1]:
						ingredient = ingredient+ingre
					else:
						ingredient = ingredient+ingre+', '
				ingredients_label.text=ingredient

				navigation_label.text = f'{meal_group.replace("_", " ")}>{meal.replace("_", " ")}'

				label = MDLabel(text='Extras:')
				extra_banner.add_widget(label)
				for key, val in extras.items():
					item = PlaceOrderVariable(extra_type='Extras', name=key, price=val, 
											 price_lbl=meal_price_lbl, func=on_checkbox_active)
					extra_banner.add_widget(item)
			else:
				meal_price_lbl.text = f'R{str(price)}'
				meal_name_lbl.text = f'{meal.replace("_", " ")}'

				navigation_label.text = f'{meal_group.replace("_", " ")}>{meal.replace("_", " ")}'

				# Add ingredients
				ingredient = ''
				for ingre in ingredients:
					if ingre == ingredients[-1]:
						ingredient = ingredient+ingre
					else:
						ingredient = ingredient+ingre+', '
				ingredients_label.text=ingredient

	def place_order(self, **kwargs):
		def start_thread(pbQ, pb, home_float):
			@mainthread
			def update_pb(pb, value):
				pb.value = value.get() 

			progress = 0
			orders = {}

			# Collect data from screen
			nav_label = self.root.ids['order_screen'].ids['navigation']
			cost_lbl = self.root.ids['order_screen'].ids['meal_price']
			ingredients_lbl = self.root.ids['order_screen'].ids['ingredients']
			extra_banner = self.root.ids['order_screen'].ids['extras']

			pbQ.put(progress+10)
			progress = progress+10
			update_pb(pb, pbQ)

			# Figure out which order it is
			nav_text = nav_label.text

			meal_group = ''
			for l in range(len(nav_text)):
				if nav_text[l] == '>':
					break
				else:
					meal_group = meal_group+nav_text[l]

			pbQ.put(progress+10)
			progress = progress+10
			update_pb(pb, pbQ)

			meal_group = meal_group.replace(' ', '_')
			if meal_group == 'Breakfast' or meal_group == 'Salads':
				meal = (nav_text[l+1:]).replace(' ', '_')

				orders[meal_group] = {'Meal':
											{meal:
												{'price':0,
												 'ingredients':ingredients_lbl.text}}}
				add_on_boxes = []
				add_ons = {}

				pbQ.put(progress+10)
				progress = progress+10
				update_pb(pb, pbQ)

				# Are there any add ons or extras
				for box in extra_banner.children:
					got_check = False
					for wigi in box.children:
						if got_check == False:
							if isinstance(wigi, MDCheckbox):
								if wigi.active:
									got_check = True
								else:
									pass
							else:
								pass
						else:
							if isinstance(wigi, MDLabel):
								add_on_text = wigi.text
								add_on_cost = ''
								count = 1
								letter = add_on_text[-count]
								while letter != 'R':
									add_on_cost = letter + add_on_cost
									count = count+1
									letter = add_on_text[-count]

								addon_name = add_on_text[:-(count+1)]
								add_ons[addon_name] = int(add_on_cost)
								
				total_addon_cost = 0
				for key, val in add_ons.items():
					total_addon_cost = total_addon_cost+val
				
				meal_cost = int((cost_lbl.text).replace('R', ''))
				orders[meal_group]['Meal'][meal]['price'] = meal_cost-total_addon_cost
				orders[meal_group]['Add_ons'] = add_ons
				orders[meal_group]['Status'] = None

				self.orders.orders.append(orders)


				pbQ.put(progress+10)
				progress = progress+10
				update_pb(pb, pbQ)

				while progress < 100:
					pbQ.put(progress)
					update_pb(pb, pbQ)
					progress = progress+0.5

				self.orders.save_new_orders(self.orders.orders)
				self.finalorderQ.put(self.orders.orders)

			elif meal_group == 'Meals':
				nav_text = nav_text[l+1:]
				meal_type = ''
				meal = ''
				got_type = False
				for le in range(len(nav_text)):
					if got_type == False:
						if nav_text[le] == '>':
							got_type = True
							meal_type = meal_type.replace(' ', '_')
						else:
							meal_type = meal_type+nav_text[le]
					else:
						meal = nav_text[le:].replace(' ', '_')
						break

				orders[meal_group] = {meal_type:
												{'Meal':
													{meal:
														{'price':0,
													 	'ingredients':ingredients_lbl.text}}}}

				add_on_boxes = []
				add_ons = {}

				pbQ.put(progress+10)
				progress = progress+10
				update_pb(pb, pbQ)

				# Are there any add ons or extras
				for box in extra_banner.children:
					got_check = False
					for wigi in box.children:
						if got_check == False:
							if isinstance(wigi, MDCheckbox):
								if wigi.active:
									got_check = True
								else:
									pass
							else:
								pass
						else:
							if isinstance(wigi, MDLabel):
								add_on_text = wigi.text
								add_on_cost = ''
								count = 1
								letter = add_on_text[-count]
								while letter != 'R':
									add_on_cost = letter + add_on_cost
									count = count+1
									letter = add_on_text[-count]

								addon_name = add_on_text[:-(count+1)]
								add_ons[addon_name] = float(add_on_cost)
								
				total_addon_cost = 0
				for key, val in add_ons.items():
					total_addon_cost = total_addon_cost+val
				
				meal_cost = float((cost_lbl.text).replace('R', ''))
				orders[meal_group][meal_type]['Meal'][meal]['price'] = meal_cost-total_addon_cost
				orders[meal_group]['Add_ons'] = add_ons
				orders[meal_group]['Status'] = None

				self.orders.orders.append(orders)

				while progress < 100:
					pbQ.put(progress)
					update_pb(pb, pbQ)
					progress = progress+0.5
				self.orders.save_new_orders(self.orders.orders)
				self.finalorderQ.put(self.orders.orders)

			elif meal_group == 'Smoothies' or meal_group == 'Shakes' or meal_group=='Something_cold':
				meal = (nav_text[l+1:]).replace(' ', '_')
				extras = {}

				# Are there any add ons or extras
				for box in extra_banner.children:
					got_check = False
					for wigi in box.children:
						if got_check == False:
							if isinstance(wigi, MDCheckbox):
								if wigi.active:
									got_check = True
								else:
									pass
							else:
								pass
						else:
							if isinstance(wigi, MDLabel):
								extras_text = wigi.text
								extras_cost = ''
								count = 1
								letter = extras_text[-count]
								while letter != 'R':
									extras_cost = letter + extras_cost
									count = count+1
									letter = extras_text[-count]

								extras_name = extras_text[:-(count+1)]
								extras[extras_name] = float(extras_cost)
								
				total_extras_cost = 0
				for key, val in extras.items():
					total_extras_cost = total_extras_cost+val

				orders[meal_group] = {meal:
										  {'price':int((cost_lbl.text).replace('R', '')),
										   'Extras': extras,
											'ingredients':ingredients_lbl.text},
									  'Status':None}

				self.orders.orders.append(orders)

				while progress < 100:
					pbQ.put(progress)
					update_pb(pb, pbQ)
					progress = progress+0.5

				self.orders.save_new_orders(self.orders.orders)
				self.finalorderQ.put(self.orders.orders)

			home_float.remove_widget(pb)

		self.change_screen('home_screen')
		self.refresh_home()
		home_float = self.root.ids['home_screen'].ids['home_float']
		pb = MDProgressBar(pos_hint={"top":0.9,"right":1}, size_hint=(1,0.01))
		home_float.add_widget(pb)
		progressbarQ = Queue()

		thread = threading.Thread(target=start_thread, args=(progressbarQ, pb, home_float))
		thread.start()

	def checkout(self,**kwargs):
		def update_label(val, func, wigi):
			total_cost = self.root.ids['checkout_screen'].ids['total_cost']
			bigPoppa = self.root.ids['checkout_screen'].ids['orders']
			current_cost = float((total_cost.text).replace('R', ''))
			if func == 'sub':
				current_cost = current_cost-val
			elif func == 'add':
				current_cost = current_cost+val

			total_cost.text = f'R{str(current_cost)}'
			bigPoppa.remove_widget(wigi)


		self.change_screen('checkout_screen')
		
		# Get required widgets
		total_cost = self.root.ids['checkout_screen'].ids['total_cost']
		bigPoppa = self.root.ids['checkout_screen'].ids['orders']
		bigPoppa.clear_widgets()
		screen_manager = self.root.ids['screen_manager']
		current_screen = screen_manager.current

		# The list we will base the order from
		self.finalorderQ.put(self.orders.orders)

		# Loop throught available meals create card for each
		print(f'Length of orders: {self.orders.orders}')
		if len(self.orders.orders) == 0:
			label = MDLabel(text='Select a meal to order!')
			total_cost.text = 'R0'
			toast('Pick a meal!')
			bigPoppa.add_widget(label)
		else:
			check_out = Checkout()
			checkout_widgets, damage, self.widgets = check_out.checkout_widgets(orders=self.orders, order=self.orders.orders,
																				current_screen=current_screen, widgets=self.widgets,
																				bigPoppa=bigPoppa, finalorderQ=self.finalorderQ,
																	  			cost_lbl=total_cost, up_lbl=update_label) 

			for widget in checkout_widgets:
				bigPoppa.add_widget(widget)

			total_cost.text = f'R{str(int(damage))}'

	def send_order(self, **kwargs):
		def redeem_points(date, picker_widget, time):
			print(f'date: {date}\ntime: {time}')
			@mainthread
			def update_pb(proBar, que):
				proBar.value = que.get()

			proQue = Queue()
			progress = 0
			thread = threading.Thread(target=send2db, args=(date, time, proQue, progress))
			thread.start()

			self.change_screen('home_screen')
			self.refresh_home()

			toast('Sending order')

		def send2db(date, time, proQue, progress):
			@mainthread
			def update_pb(proBar, que):
				proBar.value = que.get()

			conQ = Queue()
			home_float = self.root.ids['home_screen'].ids['home_float']
			pb = MDProgressBar(pos_hint={"top":0.9,"right":1}, size_hint=(1,0.01))

			sendMe = SendOrder(conQ=conQ)
			proQue.put(progress+10)
			progress = progress+10
			update_pb(pb, proQue)

			connected = conQ.get()
			if connected == True:
				userQ = Queue()
				sentQ = Queue()
				home_float.add_widget(pb)

				proQue.put(progress+10)
				progress = progress+10
				update_pb(pb, proQue)

				SendOrder.send_order(sendMe, order=self.orders.orders, progress=progress, 
									 pb=pb, user=self.user, sentQ=sentQ,
									 date=date, time=time, update_pb=update_pb,
									 progressQ=proQue, home_float=home_float)
				
				# Refresh sent orders
				new_sent = sentQ.get()
				for sent in new_sent:
					self.sent_orders.sent.append(sent)
				self.sent_orders.save_sent_orders(self.sent_orders.sent)

				# Refresh orders
				self.orders.orders = []
				self.orders.save_new_orders(self.orders.orders)

				self.user.loyalty_points = self.user.loyalty_points+1
				self.user.cache_user(self.user)

				# This button was sent through the above function initially and it worked 
				toast("Order sent")

			else:
				toast('Failed to send order')
				self.change_screen('checkout_screen')

		def update_date_button( val):
			picker = MDTimePicker()
			picker.bind(time=partial(redeem_points, val))
			picker.open()
			

		orders = self.finalorderQ.get()
		self.finalorderQ.put(orders)

		loyalty_reward = 10

		picker = MDDatePicker(callback=partial(update_date_button,))
		picker.open()
		toast('Select pickup date')

	def fill_incoming_orders(self, **kwargs):
		def update(**kwargs):
			spinner_tools = kwargs['spinner_tools']
			new_status = kwargs['new_status']
			drop_down = kwargs['drop_down']
			btn = kwargs['btn']
			id_ = kwargs['id']

			# Update the database than change text
			conQ = Queue()
			update_db = UpdateDB(conQ=conQ)
			connected = conQ.get()

			if connected == True:
				updated_status = update_db.update_status(user=self.user, new_status=new_status, 
														id_=id_)
				if update_status == True:
					btn.text = new_status
					drop_down.dismiss()
					spinner_tools[0].remove_widget(spinner_tools[1])

				else:
					drop_down.dismiss()
					toast('Failed to update status')
					spinner_tools[0].remove_widget(spinner_tools[1])

			else:
				drop_down.dismiss()
				spinner_tools[0].remove_widget(spinner_tools[1])
				toast('No connection')

		def open_dialog(var, val):
			popup = ListDialog(var)
			popup.size_hint = (0.8, 0.9)
			popup.open()

		def open_drop(drop_, btn, val):
			drop_.open()

		def change_text(btn, drop_, id_, new_text):
			# Add a spinner and open a thread to the database
			spinner_grid = self.root.ids["view_screen"].ids["load_floatie"]

			spinner = MDSpinner(size_hint=(None, None), size=(46, 46),
			                        pos_hint={'center_x': .5, 'center_y': .5}, active=True)
			spinner_tools = []
			spinner_tools.append(spinner_grid)
			spinner_tools.append(spinner)
			spinner_tools[0].add_widget(spinner_tools[1])

			thread = threading.Thread(target=update,kwargs={'spinner_tools':spinner_tools,
															'new_status':new_text.text,
															'drop_down':drop_,
															'btn':btn, 
															'id':id_})
			thread.start()
			
		# Get required widgets
		bigPoppa = self.root.ids['view_screen'].ids['view_banner']
		heading_lbl = self.root.ids['view_screen'].ids['heading']
		bigPoppa.clear_widgets()

		heading_lbl.text = 'Incoming Orders'

		# Get required variables
		incoming_orders = kwargs['incoming_orders']
		statuses = ['Sent', 'Preparing', 'Ready', 'Collected']
		play = True

		if play == True:
			for order in incoming_orders:
				for m_g, value in order.items():
					if m_g == 'Breakfast' or m_g =='Salads':
						meal_group= m_g
						add_ons = order[meal_group]['Add_ons']
						status = order[meal_group]['Status']
						collection_date = order[meal_group]['collection_date']
						order_date = order[meal_group]['order_date']
						id_ =  order[meal_group]['id']

						if status == 'None':
							status = 'Sent'

						meal = ''
						meal_price = 0
						addon_price = 0
						addon_name = ''
						ingredients = ''
						for meal_, v, in order[meal_group].items():
							if meal_ == 'Add_ons':
								for k, vl in order[meal_group][meal_].items():
									addon_name = k
									addon_price = vl

							elif meal_ == 'collection_date':
								pass
							elif meal_ == 'order_date':
								pass
							elif meal_ == 'id':
								pass
							elif meal_ == 'Status':
								pass
							else:
								meal = meal_
								meal_price = order[meal_group][meal_]['price']
								ingredients = order[meal_group][meal_]['price']

						# Create boxlayouts and view orders
						status_lbl = MDLabel(text="Status: ",size_hint_y=0.1,
										 halign="left", theme_text_color='Hint',
										 valign='center')
						order_box = BoxLayout(orientation='horizontal')
						status_box = BoxLayout(orientation='vertical', size_hint_x=0.25)
						status_btn = MDDropDownItem(size_hint_y=0.9)
						status_btn.text=status
						status_btn.current_item = status

						status_drop = MDDropdownMenu(caller=status_btn, width_mult=8)
						status_drop.callback = partial(change_text, status_btn, status_drop, id_)
						for sta in statuses:
							if sta != status:
								btn = {'viewclass': 'MDMenuItem',
									   'text':sta}

								status_drop.items.append(btn)

						status_btn.bind(on_press=partial(open_drop, status_drop, status_btn))

						pop_var = [f'Order #{str(id_)}', meal_group, meal.replace('_', ' '), meal_price, addon_name, addon_price, meal_price+addon_price, status, collection_date, str(order_date)]
						order_btn = TwoLineListItem(text=f"{meal.replace('_', ' ')} #{str(id_)}", secondary_text=f'{collection_date}', size_hint_x=0.75)
						order_btn.bind(on_press=partial(open_dialog, pop_var))

						status_box.add_widget(status_lbl)
						status_box.add_widget(status_btn)
						order_box.add_widget(order_btn)
						order_box.add_widget(status_box)

						bigPoppa.add_widget(order_box)

					elif m_g == 'Meals':
						meal_group= m_g
						add_ons = order[meal_group]['Add_ons']
						status = order[meal_group]['Status']
						collection_date = order[meal_group]['collection_date']
						order_date = order[meal_group]['order_date']
						id_ =  order[meal_group]['id']

						if status == 'None':
							status = 'Sent'

						meal = ''
						meal_price = 0
						addon_price = 0
						addon_name = ''
						ingredients = ''
						meal_type = ''
						for meal_t, v, in order[meal_group].items():
							if meal_t == 'Add_ons':
								for k, vl in order[meal_group]['Add_ons'].items():
									addon_name = k
									addon_price = vl
							elif meal_t == 'collection_date':
								pass
							elif meal_t == 'order_date':
								pass
							elif meal_t == 'id':
								pass
							elif meal_t == 'Status':
								pass
							else:
								meal_type = meal_t
								for meal_, vl in order[meal_group][meal_type].items():
									meal = meal_
									meal_price = order[meal_group][meal_type][meal]['price']
									ingredients = order[meal_group][meal_type][meal]['ingredients']

						# Create boxlayouts and view orders
						order_box = BoxLayout(orientation='horizontal')
						status_box = BoxLayout(orientation='vertical',size_hint_x=0.25)
						status_lbl = MDLabel(text='Status: ',size_hint_y=0.1,
											 halign="left", theme_text_color='Hint',
											 valign='center')
						status_btn = MDDropDownItem(size_hint_y=0.9)
						status_btn.text=statuses[0]
						status_btn.current_item = statuses[0]

						status_drop = MDDropdownMenu(caller=status_btn, width_mult=8)
						status_drop.callback = partial(change_text, status_btn, status_drop)
						for sta in statuses[1:]:
							btn = {'viewclass': 'MDMenuItem',
								   'text':sta}

							status_drop.items.append(btn)

						status_btn.bind(on_press=partial(open_drop, status_drop, status_btn))

						pop_var = [f'Order #{str(id_)}', meal_group, meal.replace('_', ' '), meal_price, addon_name, addon_price, meal_price+addon_price, status, collection_date, str(order_date)]
						order_btn = TwoLineListItem(text=f"{meal.replace('_', ' ')} #{str(id_)}", secondary_text=f'{collection_date}', size_hint_x=0.75)
						order_btn.bind(on_press=partial(open_dialog, pop_var))

						status_box.add_widget(status_lbl)
						status_box.add_widget(status_btn)
						order_box.add_widget(order_btn)
						order_box.add_widget(status_box)

						bigPoppa.add_widget(order_box)

					elif m_g == 'Smoothies' or m_g == 'Shakes'or m_g == 'Something_cold':
						meal_group = m_g
						status = order[meal_group]['Status']
						extras = order[meal_group]['Extras']
						collection_date = order[meal_group]['collection_date']
						order_date = order[meal_group]['order_date']
						id_ =  order[meal_group]['id']

						if status == 'None':
							status = 'Sent'

						meal = ''
						meal_price = 0
						addon_price = 0
						addon_name = ''
						ingredients = ''

						for addon, pr in extras.items():
							if addon == list(extras.keys())[-1]:
								addon_name = addon_name + addon.replace(' -', '')
								addon_price = addon_price+pr
							else:
								addon_name = addon_name+addon.replace(' -', '')+', '
								addon_price = addon_price+pr

						for meal_, val in order[meal_group].items():
							if meal_ == 'Status':
								pass
							elif meal_ == 'collection_date':
								pass
							elif meal_ == 'Extras':
								pass
							elif meal_ == 'order_date':
								pass
							elif meal_ == 'id':
								pass
							elif meal_ == 'Status':
								pass
							else:
								meal = meal_
								meal_price = order[meal_group][meal]['price']
								ingredients = order[meal_group][meal]['ingredients']

						# Create boxlayouts and view orders
						order_box = BoxLayout(orientation='horizontal')
						status_box = BoxLayout(orientation='vertical', size_hint_x=0.25)
						status_lbl = MDLabel(text='Status: ',size_hint_y=0.1,
											 halign="left", theme_text_color='Hint',
											 valign='center')
						status_btn = MDDropDownItem(size_hint_y=0.9)
						status_btn.text=statuses[0]
						status_btn.current_item = statuses[0]

						status_drop = MDDropdownMenu(caller=status_btn, width_mult=8)
						status_drop.callback = partial(change_text, status_btn, status_drop)
						for sta in statuses[1:]:
							btn = {'viewclass': 'MDMenuItem',
								   'text':sta}

							status_drop.items.append(btn)

						status_btn.bind(on_press=partial(open_drop, status_drop, status_btn))

						pop_var = [f'Order #{str(id_)}', meal_group, meal.replace('_', ' '), meal_price, addon_name, addon_price, meal_price+addon_price, status, collection_date, str(order_date)]
						order_btn = TwoLineListItem(text=f"{meal.replace('_', ' ')} #{str(id_)}", secondary_text=f'{collection_date}', size_hint_x=0.75)
						order_btn.bind(on_press=partial(open_dialog, pop_var))

						status_box.add_widget(status_lbl)
						status_box.add_widget(status_btn)
						order_box.add_widget(order_btn)
						order_box.add_widget(status_box)

						bigPoppa.add_widget(order_box)

	def fill_sent_orders(self, **kwargs):
		def open_dialog(var, val):
			popup = ListDialog(var)
			popup.size_hint = (0.8, 0.9)
			popup.open()

		# Get required widgets
		bigPoppa = self.root.ids['view_screen'].ids['view_banner']
		heading_lbl = self.root.ids['view_screen'].ids['heading']
		bigPoppa.clear_widgets()

		heading_lbl.text = 'Orders'

		# Get required variables
		sent_orders = kwargs['sent_orders']
		play = True
		
		if play == True:
			for order in sent_orders:
				for m_g, value in order.items():
					if m_g == 'Breakfast' or m_g =='Salads':
						meal_group= m_g
						add_ons = order[meal_group]['Add_ons']
						status = order[meal_group]['Status']
						id_ = order[meal_group]['id']
						collection_date = order[meal_group]['collection_date']
						order_date = order[meal_group]['order_date']

						if status == 'None':
							status = 'Sent'

						meal = ''
						meal_price = 0
						addon_price = 0
						addon_name = ''
						ingredients = ''
						for meal_, v, in order[meal_group].items():
							if meal_ == 'Add_ons':
								for k, vl in order[meal_group][meal_].items():
									addon_name = k
									addon_price = vl

							elif meal_ == 'collection_date':
								pass
							elif meal_ == 'Status':
								pass
							elif meal_ == 'id':
								pass
							elif meal_ == 'order_date':
								pass
							else:
								meal = meal_
								meal_price = order[meal_group][meal_]['price']
								ingredients = order[meal_group][meal_]['ingredients']

						# Create boxlayouts and view orders
						order_box = BoxLayout(orientation='horizontal')
						status_box = BoxLayout(orientation='vertical', size_hint_x=0.25)
						status_lbl = MDLabel(text='Status:',size_hint_y=0.1,
											 halign="center", theme_text_color='Hint',
											 valign='center')
						status_ = MDLabel(text=status,size_hint_y=0.9,
										 halign="center", valign='center')

						pop_var = [f'Order #{str(id_)}', meal_group, meal.replace('_', ' '), meal_price, addon_name, addon_price, meal_price+addon_price, status, collection_date, str(order_date)]
						order_btn = TwoLineListItem(text=f"{meal.replace('_', ' ')} #{str(id_)}", secondary_text=f'{collection_date}', size_hint_x=0.75)
						order_btn.bind(on_press=partial(open_dialog, pop_var))

						status_box.add_widget(status_lbl)
						status_box.add_widget(status_)
						order_box.add_widget(order_btn)
						order_box.add_widget(status_box)

						bigPoppa.add_widget(order_box)

					elif m_g == 'Meals':
						meal_group= m_g
						add_ons = order[meal_group]['Add_ons']
						status = order[meal_group]['Status']
						id_ = order[meal_group]['id']
						collection_date = order[meal_group]['collection_date']
						order_date = order[meal_group]['order_date']

						if status == 'None':
							status = 'Sent'

						meal = ''
						meal_price = 0
						addon_price = 0
						addon_name = ''
						ingredients = ''
						meal_type = ''
						for meal_t, v, in order[meal_group].items():
							if meal_t == 'Add_ons':
								for k, vl in order[meal_group]['Add_ons'].items():
									addon_name = k
									addon_price = vl
							elif meal_t == 'collection_date':
								pass
							elif meal_t == 'Status':
								pass
							elif meal_t == 'id':
								pass 
							elif meal_t == 'order_date':
								pass
							else:
								meal_type = meal_t
								for meal_, vl in order[meal_group][meal_type].items():
									meal = meal_
									meal_price = order[meal_group][meal_type][meal]['price']
									ingredients = order[meal_group][meal_type][meal]['ingredients']

						# Create boxlayouts and view orders
						order_box = BoxLayout(orientation='horizontal')
						status_box = BoxLayout(orientation='vertical', size_hint_x=0.25)
						status_lbl = MDLabel(text='Status:',size_hint_y=0.1,
											 halign="center", theme_text_color='Hint',
											 valign='center')
						status_ = MDLabel(text=status,size_hint_y=0.9,
										 halign="center", valign='center')
						pop_var = [f'Order #{str(id_)}', meal_group, meal.replace('_', ' '), meal_price, addon_name, addon_price, meal_price+addon_price, status, collection_date, str(order_date)]
						order_btn = TwoLineListItem(text=f"{meal.replace('_', ' ')} #{str(id_)}", secondary_text=f'{collection_date}', size_hint_x=0.75)
						order_btn.bind(on_press=partial(open_dialog, pop_var))

						status_box.add_widget(status_lbl)
						status_box.add_widget(status_)
						order_box.add_widget(order_btn)
						order_box.add_widget(status_box)

						bigPoppa.add_widget(order_box)

					elif m_g=='Smoothies' or m_g=='Shakes'or m_g=='Something_cold':
						meal_group = m_g
						status = order[meal_group]['Status']
						extras = order[meal_group]['Extras']
						id_ = order[meal_group]['id']
						collection_date = order[meal_group]['collection_date']
						order_date = order[meal_group]['order_date']

						meal = ''
						meal_price = 0
						addon_price = 0
						addon_name = ''
						ingredients = ''

						if status == 'None':
							status = 'Sent'

						for addon, pr in extras.items():
							if addon == list(extras.keys())[-1]:
								addon_name = addon_name + addon.replace(' -', '')
								addon_price = addon_price+pr
							else:
								addon_name = addon_name+addon.replace(' -', '')+', '
								addon_price = addon_price+pr

						for meal_, val in order[meal_group].items():
							if meal_ == 'Status':
								pass
							elif meal_ == 'collection_date':
								pass
							elif meal_ == 'Extras':
								pass
							elif meal_ == 'order_date':
								pass
							elif meal_ == 'id':
								pass
							else:
								meal = meal_
								meal_price = order[meal_group][meal]['price']
								ingredients = order[meal_group][meal]['ingredients']

						# Create boxlayouts and view orders
						order_box = BoxLayout(orientation='horizontal')
						status_box = BoxLayout(orientation='vertical', size_hint_x=0.25)
						status_lbl = MDLabel(text='Status:',size_hint_y=0.1,
											 halign="center", theme_text_color='Hint',
											 valign='center')
						status_ = MDLabel(text=status,size_hint_y=0.9,
										 halign="center", valign='center')
						pop_var = [f'Order #{str(id_)}', meal_group, meal.replace('_', ' '), meal_price, addon_name, addon_price, meal_price+addon_price, status, collection_date, str(order_date)]
						order_btn = TwoLineListItem(text=f"{meal.replace('_', ' ')} #{str(id_)}", secondary_text=f'{collection_date}', size_hint_x=0.75)
						order_btn.bind(on_press=partial(open_dialog, pop_var))

						status_box.add_widget(status_lbl)
						status_box.add_widget(status_)
						order_box.add_widget(order_btn)
						order_box.add_widget(status_box)

						bigPoppa.add_widget(order_box)

	def account(self, **kwargs):
		def view_orders(val):
			def querydb(spinner_tools):
				# Prepare required data
				bigPoppa = self.root.ids['view_screen'].ids['view_banner']
				heading = self.root.ids['view_screen'].ids['heading']
				conQ = Queue()

				enquiry = Enquiry(heading_lbl=heading, bigPoppa=bigPoppa, conQ=conQ)
				connected = conQ.get()

				if connected == True:
					sent_orders = enquiry.order_enquiries(user=self.user)

					if isinstance(sent_orders, list):
						self.sent_orders.save_sent_orders(sent_orders)
						self.fill_sent_orders(sent_orders=sent_orders)
						self.change_screen('view_screen')
						spinner_tools[0].remove_widget(spinner_tools[1])
					else:
						toast('Failed to view orders')
						spinner_tools[0].remove_widget(spinner_tools[1])
				else:
					toast('No connection')

					spinner_tools[0].remove_widget(spinner_tools[1])
					spinner_tools.hide = True

			# Add a spinner and open a thread to the database
			spinner_grid = self.root.ids["account_screen"].ids["load_floatie"]

			spinner = MDSpinner(size_hint=(None, None), size=(46, 46),
			                        pos_hint={'center_x': .5, 'center_y': .5}, active=True)
			spinner_tools = []
			spinner_tools.append(spinner_grid)
			spinner_tools.append(spinner)
			spinner_tools[0].add_widget(spinner_tools[1])

			thread = threading.Thread(target=querydb,args=(spinner_tools,))
			thread.start()

		def view_incoming(val):
			def querydb(spinner_tools):
				bigPoppa = self.root.ids['view_screen'].ids['view_banner']
				heading = self.root.ids['view_screen'].ids['heading']
				conQ = Queue()

				enquiry = Enquiry(heading_lbl=heading, bigPoppa=bigPoppa, conQ=conQ)
				connected = conQ.get()

				if connected == True:
					incoming_orders = enquiry.incoming_enquiries(user=self.user)

					if isinstance(incoming_orders, list):
						self.incoming_orders.save_incoming_orders(incoming_orders)
						self.fill_incoming_orders(incoming_orders=incoming_orders)
						self.change_screen('view_screen')
						spinner_tools[0].remove_widget(spinner_tools[1])
					
					elif isinstance(incoming_orders, str):
						toast(incoming_orders)
						spinner_tools[0].remove_widget(spinner_tools[1])
				else:
					toast('No connection')

					spinner_tools[0].remove_widget(spinner_tools[1])

			# Add a spinner and open a thread to the database
			spinner_grid = self.root.ids["account_screen"].ids["load_floatie"]
			spinner_grid.hide = False

			spinner = MDSpinner(size_hint=(None, None), size=(46, 46),
			                        pos_hint={'center_x': .5, 'center_y': .5}, active=True)
			spinner_tools = []
			spinner_tools.append(spinner_grid)
			spinner_tools.append(spinner)
			spinner_tools[0].add_widget(spinner_tools[1])

			thread = threading.Thread(target=querydb,args=(spinner_tools,))
			thread.start()

		def create_user(val):
			pass

		bigPoppa = self.root.ids['account_screen'].ids['account_banner']
		bigPoppa.clear_widgets()

		name_grid = GridLayout(cols=2)
		name_tag = MDLabel(text='First name:')
		name_lbl = MDLabel(text=self.user.first_name)
		name_grid.add_widget(name_tag)
		name_grid.add_widget(name_lbl)
		bigPoppa.add_widget(name_grid)

		name_grid = GridLayout(cols=2)
		name_tag = MDLabel(text='Last name:')
		name_lbl = MDLabel(text=self.user.last_name)
		name_grid.add_widget(name_tag)
		name_grid.add_widget(name_lbl)
		bigPoppa.add_widget(name_grid)

		name_grid = GridLayout(cols=2)
		name_tag = MDLabel(text='Loyalty points:')
		name_lbl = MDLabel(text=str(self.user.loyalty_points))
		name_grid.add_widget(name_tag)
		name_grid.add_widget(name_lbl)
		bigPoppa.add_widget(name_grid)

		if self.user.regular_drink != None:
			regular_drink = self.user.regular_drink
		else:
			regular_drink = 'None'
		
		name_grid = GridLayout(cols=2)
		name_tag = MDLabel(text='Regular drink:')
		name_lbl = MDLabel(text=regular_drink)
		name_grid.add_widget(name_tag)
		name_grid.add_widget(name_lbl)
		bigPoppa.add_widget(name_grid)

		# Sent orders
		orders_btn = TwoLineListItem(text='Orders')
		orders_btn.bind(on_press=partial(view_orders,))
		bigPoppa.add_widget(orders_btn)

		if self.user.admin == 1:
			incoming_orders = TwoLineListItem(text='Incoming orders')
			incoming_orders.bind(on_press=partial(view_incoming,))
			bigPoppa.add_widget(incoming_orders)

		elif self.user.admin == 2:
			incoming_orders = TwoLineListItem(text='Incoming orders')
			incoming_orders.bind(on_press=partial(view_incoming,))
			bigPoppa.add_widget(incoming_orders)
if __name__ == '__main__':
	CafeNallaApp().run()