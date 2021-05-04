from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.list import OneLineListItem, OneLineIconListItem
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.uix.scrollview import ScrollView
from kivymd.uix.list import MDList
from functools import partial

class Content(BoxLayout):
	def __init__(self, **kwargs):
		super(Content, self).__init__(**kwargs)
		self.screen_manager = ObjectProperty() 
		self.nav_drawer = ObjectProperty()


	def home_screen(self, nav_drawer, func, **kwargs):
		def close_drawer(nav, func, screen, val):
			nav.set_state("close")
			func(screen)

		def go_2_meal(nav, func, screen, meal_group, meal_page, val):
			nav.set_state("close")
			func(screen)
			meal_page(meal_group=meal_group)

		def logout_(func, val):
			func()

		meal_page = kwargs['meal_page_func']
		log_out = kwargs['log_out']

		items = []
		# Check available bots
		account = OneLineIconListItem(text="Account")
		account.icon = 'basketball-hoop'
		account.bind(on_press=partial(close_drawer, nav_drawer, func, "account_screen"))
		items.append(account)
		
		# Breakfast
		breakfast = OneLineIconListItem(text="Breakfast")
		breakfast.icon = 'cash'
		breakfast.bind(on_press=partial(go_2_meal, nav_drawer, func, 'meals_screen', 'Breakfast', meal_page))
		items.append(breakfast)

		# Meals
		Meals = OneLineIconListItem(text="Meals")
		Meals.icon = 'cash'
		Meals.bind(on_press=partial(go_2_meal, nav_drawer, func, 'meals_screen', 'Meals', meal_page))
		items.append(Meals)

		# Salads
		Salads = OneLineIconListItem(text="Salads")
		Salads.icon = 'cash'
		Salads.bind(on_press=partial(go_2_meal, nav_drawer, func, 'meals_screen', 'Salads', meal_page))
		items.append(Salads)

		# Smoothy
		Smoothies = OneLineIconListItem(text="Smoothies")
		Smoothies.icon = 'cash'
		Smoothies.bind(on_press=partial(go_2_meal, nav_drawer, func, 'meals_screen', 'Smoothies', meal_page))
		items.append(Smoothies)

		# Shakes
		Shakes = OneLineIconListItem(text="Shakes")
		Shakes.icon = 'cash'
		Shakes.bind(on_press=partial(go_2_meal, nav_drawer, func, 'meals_screen', 'Shakes', meal_page))
		items.append(Shakes)

		# Something cold
		Something_cold = OneLineIconListItem(text="Something cold")
		Something_cold.icon = 'cash'
		Something_cold.bind(on_press=partial(go_2_meal, nav_drawer, func, 'meals_screen', 'Something_cold', meal_page))
		items.append(Something_cold)

		# Log out
		logout = OneLineIconListItem(text="Logout")
		logout.icon = 'cash'
		logout.bind(on_press=partial(logout_, log_out))
		items.append(logout)
		return items

	def meals_screen(self, nav_drawer, func):
		def close_drawer(nav, func, screen, val):
			nav.set_state("close")
			func(screen)

		items = []
		# Check available bots
		home = OneLineIconListItem(text="Home")
		home.icon = 'basketball-hoop'
		home.bind(on_press=partial(close_drawer, nav_drawer, func, "home_screen"))
		items.append(home)

		return items
	def order_screen(self, nav_drawer, func):
		def close_drawer(nav, func, screen, val):
			nav.set_state("close")
			func(screen)

		items = []
		# Check available bots
		home = OneLineIconListItem(text="Home")
		home.icon = 'basketball-hoop'
		home.bind(on_press=partial(close_drawer, nav_drawer, func, "home_screen"))
		items.append(home)

		return items

	def checkout_screen(self, nav_drawer, func):
		def close_drawer(nav, func, screen, val):
			nav.set_state("close")
			func(screen)

		items = []
		# Check available bots
		home = OneLineIconListItem(text="Home")
		home.icon = 'basketball-hoop'
		home.bind(on_press=partial(close_drawer, nav_drawer, func, "home_screen"))
		items.append(home)

		return items

	def account_screen(self, nav_drawer, func):
		def close_drawer(nav, func, screen, val):
			nav.set_state("close")
			func(screen)

		items = []
		# Check available bots
		home = OneLineIconListItem(text="Home")
		home.icon = 'basketball-hoop'
		home.bind(on_press=partial(close_drawer, nav_drawer, func, "home_screen"))
		items.append(home)

		return items

	def view_screen(self,nav_drawer, func):
		def close_drawer(nav, func, screen, val):
			nav.set_state("close")
			func(screen)

		items = []
		# Check available bots
		home = OneLineIconListItem(text="Home")
		home.icon = 'basketball-hoop'
		home.bind(on_press=partial(close_drawer, nav_drawer, func, "home_screen"))
		items.append(home)

		account = OneLineIconListItem(text="Account")
		account.icon = 'basketball-hoop'
		account.bind(on_press=partial(close_drawer, nav_drawer, func, "account_screen"))
		items.append(account)

		return items
