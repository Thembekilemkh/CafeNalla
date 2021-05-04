from kivymd.uix.label import MDLabel

class Checkout():
	def checkout_widgets(self, **kwargs):
		def edit_final_order(params, val):
			print(params)
			if params[1].empty():
				toast('Select a meal!')
			else:
				'''('active_widget', finalorderQ, widgets.floatlayout['widgets'][floatie_num],
				 order, bigPoppa, update_label, orders)'''
				order = params[3]
				orders_ = params[6]
				ordersQ = params[1]
				sub_cost = 0
				orders = ordersQ.get()
				for o in range(len(orders)):
					if orders[o] == order:
						if 'Breakfast' in list(orders[o].keys()) or 'Salads' in list(orders[o].keys()):
							if 'Breakfast' in list(orders[o].keys()):
								meal_gr = 'Breakfast'
							elif 'Salads' in list(orders[o].keys()):
								meal_gr = 'Salads'

							meaL = orders[o][meal_gr]['Meal']
							sub_cost = 0
							for key, val in meaL.items():
								sub_cost = sub_cost+meaL[key]['price']

							add_ons = orders[o][meal_gr]['Add_ons']
							for key, val in add_ons.items():
								sub_cost = sub_cost+add_ons[key]

							print('Subbing')
							update_label(sub_cost, 'sub', params[2])
						elif 'Meals' in list(orders[o].keys()):
							meal_ty = ''
							add_ons = {}
							for key, val in orders[o]['Meals'].items():
								if key == "Tramezzini's":
									meal_ty = key

								elif key == 'From_The_Grill':
									meal_ty = key

								elif key == 'Add_ons':
									add_ons = orders[o]['Meals']['Add_ons']

							meaL = orders[o]['Meals'][meal_ty]['Meal']
							sub_cost = 0
							for key, val in meaL.items():
								sub_cost = sub_cost+meaL[key]['price']

							for key, val in add_ons.items():
								sub_cost = sub_cost+add_ons[key]

							update_label(sub_cost, 'sub', params[2])

						elif 'Smoothies' in list(orders[o].keys()) or 'Shakes' in list(orders[o].keys()) or 'Something_cold' in list(orders[o].keys()):
							if 'Smoothies' in list(orders[o].keys()):
								meal_gr = 'Smoothies'
							elif 'Shakes' in list(orders[o].keys()):
								meal_gr = 'Shakes'
							elif 'Something_cold' in list(orders[o].keys()):
								meal_gr = 'Something_cold'

							meal_ty = ''
							extras = {}
							sub_cost = 0
							for key, val in orders[o][meal_gr].items():
								if key == 'Add_ons':
									pass
								elif key == 'Status':
									pass
								elif key == 'Extras':
									extras = orders[o][meal_gr]['Extras']
								else:
									sub_cost = sub_cost+orders[o][meal_gr][key]['price']

							for key, val in extras.items():
								sub_cost = sub_cost+extras[key]

							update_label(sub_cost, 'sub', params[2])
						
						del orders[o]
						ordersQ.put(orders)
						orders_.save_new_orders(orders)

						break




		orderlist = kwargs['order']
		orders = kwargs['orders']
		current_screen = kwargs['current_screen']
		widgets = kwargs['widgets']
		finalorderQ = kwargs['finalorderQ']
		bigPoppa = kwargs['bigPoppa']
		cost_lbl = kwargs['cost_lbl']
		update_label = kwargs['up_lbl']
		checkout_widgets = []
		total_cost = 0

		card_num = 0
		label_num = 0
		box_num = 0
		floatie_num = 0
		icon_num = 0
		for order in orderlist:
			for meal_group_, val in order.items():
				if meal_group_ == 'Breakfast' or meal_group_ == 'Salads':
					meal_group = order[meal_group_]['Meal']
					add_ons = order[meal_group_]['Add_ons']

					meal = ''
					add_cost = 0
					meal_cost = 0
					ingredients = ''
					for meal_, vals in meal_group.items():
						meal = meal_
						meal_cost = meal_group[meal_]['price']
						ingredients = meal_group[meal_]['ingredients']
						total_cost = total_cost+meal_cost

					# Card creation
					card = widgets.configure_new_widget(widget_type='card', widget_num=card_num,
													widget=widgets.card, layout='gridlayout',
													current_screen=current_screen, orientation='vertical',
													top=0.95, side="right",side_val=0.95, width=0.9, height=0.9)
					widgets.card = card[0]
					card_num = card[1]

					floatlayout = widgets.configure_new_widget(widget_type="floatlayout", widget_num=floatie_num, widget=widgets.floatlayout, current_screen=current_screen, 
					                                layout="gridlayout")
					widgets.floatlayout = floatlayout[0]
					floatie_num = floatlayout[1]

					boxlayout = widgets.configure_new_widget(widget_type='boxlayout', widget_num=box_num,
														  widget=widgets.boxlayout, layout='boxlayout',
														  orientation='horizontal', size_hint_y=0.25,
														  pop_orientation='vertical', current_screen=current_screen)
					widgets.boxlayout = boxlayout[0]
					box_num1 = boxlayout[1]
					box_num = box_num+1

					label = widgets.configure_new_widget(widget_type="mdlabel",value=0, widget_num=label_num, widget=widgets.label,
															layout="boxlayout", current_screen=current_screen, text=f'{meal.replace("_", " ")}',
															size_hint_x=0.75, orientation='horizontal')
					widgets.label = label[0]
					label_num1 = label[1]
					label_num = label_num+1

					icon_button = widgets.configure_new_widget(widget_type="icon_button", widget_num=icon_num, widget=widgets.icon_button,
															layout="boxlayout", current_screen=current_screen, icon='trash-can',
															orientation='horizontal', size_hint_x=0.25, params=('active_widget', finalorderQ, widgets.floatlayout['widgets'][floatie_num],
															order, bigPoppa, update_label, orders, orderlist), func=edit_final_order)
					widgets.icon_button = icon_button[0]
					icon_num = icon_button[1]

					# Ingredients
					label = widgets.configure_new_widget(widget_type="mdlabel",value=0, widget_num=label_num, widget=widgets.label,
															layout="boxlayout", current_screen=current_screen, text=ingredients,
															size_hint_y=0.5, orientation='vertical')
					widgets.label = label[0]
					label_num2 = label[1]
					label_num = label_num+1

					# Add ons
					boxlayout = widgets.configure_new_widget(widget_type='boxlayout', widget_num=box_num,
														  widget=widgets.boxlayout, layout='boxlayout',
														  orientation='vertical', size_hint_y=0.25,
														  pop_orientation='vertical', current_screen=current_screen)
					widgets.boxlayout = boxlayout[0]
					box_num3 = boxlayout[1]
					box_num = box_num+1

					for key, v in add_ons.items():
						add_cost = add_cost+v
						addon = (key.replace(' ','')).replace('-', '')

						label = widgets.configure_new_widget(widget_type="mdlabel",value=0, widget_num=label_num, widget=widgets.label,
															layout="boxlayout", current_screen=current_screen, text=f'{addon}: R{v}',
															size_hint_x=0.75/len(list(add_ons.keys())), orientation='horizontal')
						widgets.label = label[0]
						label_num6 = label[1]
						label_num = label_num+1

						total_cost = total_cost+v
						widgets.boxlayout['widgets'][box_num3].add_widget(MDLabel(text=f'{addon}: R{v}', size_hint_y=1/len(list(add_ons.keys()))))


					# Subtotal
					boxlayout = widgets.configure_new_widget(widget_type='boxlayout', widget_num=box_num,
														  widget=widgets.boxlayout, layout='boxlayout',
														  orientation='horizontal', size_hint_y=0.25,
														  pop_orientation='vertical', current_screen=current_screen)
					widgets.boxlayout = boxlayout[0]
					box_num2 = boxlayout[1]
					box_num = box_num+1

					label = widgets.configure_new_widget(widget_type="mdlabel",value=0, widget_num=label_num, widget=widgets.label,
															layout="boxlayout", current_screen=current_screen, text=f'Price: ',
															size_hint_x=0.75, orientation='horizontal')
					widgets.label = label[0]
					label_num3 = label[1]
					label_num = label_num+1

					label = widgets.configure_new_widget(widget_type="mdlabel",value=0, widget_num=label_num, widget=widgets.label,
															layout="boxlayout", current_screen=current_screen, text=f'R{meal_cost}',
															size_hint_x=0.25, orientation='horizontal')
					widgets.label = label[0]
					label_num4 = label[1]
					label_num = label_num+1

					# Populate top box
					#widgets.boxlayout['widgets'][box_num1].add_widget(widgets.label['widgets'][label_num1])
					widgets.boxlayout['widgets'][box_num1].add_widget(MDLabel(text=f'{meal.replace("_", " ")}', size_hint_x=0.75))
					widgets.boxlayout['widgets'][box_num1].add_widget(widgets.icon_button['widgets'][icon_num])

					# Populate bottom box
					#widgets.boxlayout['widgets'][box_num2].add_widget(widgets.label['widgets'][label_num3])
					#widgets.boxlayout['widgets'][box_num2].add_widget(widgets.label['widgets'][label_num4])
					widgets.boxlayout['widgets'][box_num2].add_widget(MDLabel(text=f'Price: ', size_hint_x=0.75))
					widgets.boxlayout['widgets'][box_num2].add_widget(MDLabel(text=f'R{meal_cost}', size_hint_x=0.25))
					
					# Populate card
					widgets.card['widgets'][card_num].add_widget(widgets.boxlayout['widgets'][box_num1])
					#widgets.card['widgets'][card_num].add_widget(widgets.label['widgets'][label_num2])
					widgets.card['widgets'][card_num].add_widget(MDLabel(text=ingredients, size_hint_y=0.25))
					widgets.card['widgets'][card_num].add_widget(widgets.boxlayout['widgets'][box_num3])
					widgets.card['widgets'][card_num].add_widget(widgets.boxlayout['widgets'][box_num2])

					widgets.floatlayout['widgets'][floatie_num].add_widget(widgets.card['widgets'][card_num])
					checkout_widgets.append(widgets.floatlayout['widgets'][floatie_num])

				elif meal_group_ == 'Meals':
					if "Tramezzini's" in list(order[meal_group_].keys()):
						meal_type = "Tramezzini's"
					elif "From_The_Grill" in list(order[meal_group_].keys()):
						meal_type = 'From_The_Grill'

					meal_group = order[meal_group_][meal_type]['Meal']
					add_ons = order[meal_group_]['Add_ons']

					meal = ''
					add_cost = 0
					meal_cost = 0
					ingredients = ''
					for meal_, vals in meal_group.items():
						meal = meal_
						meal_cost = meal_group[meal_]['price']
						ingredients = meal_group[meal_]['ingredients']
						total_cost = total_cost+meal_cost

					# Card creation
					card = widgets.configure_new_widget(widget_type='card', widget_num=card_num,
													widget=widgets.card, layout='gridlayout',
													current_screen=current_screen, orientation='vertical',
													top=0.95, side="right",side_val=0.95, width=0.9, height=0.9)
					widgets.card = card[0]
					card_num = card[1]

					floatlayout = widgets.configure_new_widget(widget_type="floatlayout", widget_num=floatie_num, widget=widgets.floatlayout, current_screen=current_screen, 
					                                layout="gridlayout")
					widgets.floatlayout = floatlayout[0]
					floatie_num = floatlayout[1]

					boxlayout = widgets.configure_new_widget(widget_type='boxlayout', widget_num=box_num,
														  widget=widgets.boxlayout, layout='boxlayout',
														  orientation='horizontal', size_hint_y=0.25,
														  pop_orientation='vertical', current_screen=current_screen)
					widgets.boxlayout = boxlayout[0]
					box_num1 = boxlayout[1]
					box_num = box_num+1

					label = widgets.configure_new_widget(widget_type="mdlabel",value=0, widget_num=label_num, widget=widgets.label,
															layout="boxlayout", current_screen=current_screen, text=f'{meal.replace("_", " ")}',
															size_hint_x=0.75, orientation='horizontal')
					widgets.label = label[0]
					label_num1 = label[1]
					label_num = label_num+1

					icon_button = widgets.configure_new_widget(widget_type="icon_button", widget_num=icon_num, widget=widgets.icon_button,
															layout="boxlayout", current_screen=current_screen, icon='trash-can',
															orientation='horizontal', size_hint_x=0.25, params=('active_widget', finalorderQ, widgets.floatlayout['widgets'][floatie_num],
															order, bigPoppa, update_label, orders, orderlist), func=edit_final_order)
					widgets.icon_button = icon_button[0]
					icon_num = icon_button[1]

					# Ingredients
					label = widgets.configure_new_widget(widget_type="mdlabel",value=0, widget_num=label_num, widget=widgets.label,
															layout="boxlayout", current_screen=current_screen, text=ingredients,
															size_hint_y=0.5, orientation='vertical')
					widgets.label = label[0]
					label_num2 = label[1]
					label_num = label_num+1

					# Add ons
					boxlayout = widgets.configure_new_widget(widget_type='boxlayout', widget_num=box_num,
														  widget=widgets.boxlayout, layout='boxlayout',
														  orientation='vertical', size_hint_y=0.25,
														  pop_orientation='vertical', current_screen=current_screen)
					widgets.boxlayout = boxlayout[0]
					box_num3 = boxlayout[1]
					box_num = box_num+1

					for key, v in add_ons.items():
						add_cost = add_cost+v
						addon = (key.replace(' ','')).replace('-', '')

						label = widgets.configure_new_widget(widget_type="mdlabel",value=0, widget_num=label_num, widget=widgets.label,
															layout="boxlayout", current_screen=current_screen, text=f'{addon}: R{v}',
															size_hint_x=0.9/len(list(add_ons.keys())), orientation='horizontal')
						widgets.label = label[0]
						label_num6 = label[1]
						label_num = label_num+1

						total_cost = total_cost+v

						#widgets.boxlayout['widgets'][box_num3].add_widget(widgets.label['widgets'][label_num6])
						widgets.boxlayout['widgets'][box_num3].add_widget(MDLabel(text=f'{addon}: R{v}', size_hint_y=1/len(list(add_ons.keys()))))


					# Subtotal
					boxlayout = widgets.configure_new_widget(widget_type='boxlayout', widget_num=box_num,
														  widget=widgets.boxlayout, layout='boxlayout',
														  orientation='horizontal', size_hint_y=0.25,
														  pop_orientation='vertical', current_screen=current_screen)
					widgets.boxlayout = boxlayout[0]
					box_num2 = boxlayout[1]
					box_num = box_num+1

					label = widgets.configure_new_widget(widget_type="mdlabel",value=0, widget_num=label_num, widget=widgets.label,
															layout="boxlayout", current_screen=current_screen, text=f'Price: ',
															size_hint_x=0.75, orientation='horizontal')
					widgets.label = label[0]
					label_num3 = label[1]
					label_num = label_num+1

					label = widgets.configure_new_widget(widget_type="mdlabel",value=0, widget_num=label_num, widget=widgets.label,
															layout="boxlayout", current_screen=current_screen, text=f'R{meal_cost}',
															size_hint_x=0.25, orientation='horizontal')
					widgets.label = label[0]
					label_num4 = label[1]
					label_num = label_num+1

					# Populate top box
#					widgets.boxlayout['widgets'][box_num1].add_widget(widgets.label['widgets'][label_num1])
					widgets.boxlayout['widgets'][box_num1].add_widget(MDLabel(text=f'{meal.replace("_", " ")}', size_hint_x=0.75))
					widgets.boxlayout['widgets'][box_num1].add_widget(widgets.icon_button['widgets'][icon_num])

					# Populate bottom box
					#widgets.boxlayout['widgets'][box_num2].add_widget(widgets.label['widgets'][label_num3])
					#widgets.boxlayout['widgets'][box_num2].add_widget(widgets.label['widgets'][label_num4])
					widgets.boxlayout['widgets'][box_num2].add_widget(MDLabel(text=f'Price: ', size_hint_x=0.75))
					widgets.boxlayout['widgets'][box_num2].add_widget(MDLabel(text=f'R{meal_cost}', size_hint_x=0.25))
					
					# Populate card
					widgets.card['widgets'][card_num].add_widget(widgets.boxlayout['widgets'][box_num1])
					#widgets.card['widgets'][card_num].add_widget(widgets.label['widgets'][label_num2])
					widgets.card['widgets'][card_num].add_widget(MDLabel(text=ingredients, size_hint_y=0.25))
					widgets.card['widgets'][card_num].add_widget(widgets.boxlayout['widgets'][box_num3])
					widgets.card['widgets'][card_num].add_widget(widgets.boxlayout['widgets'][box_num2])

					widgets.floatlayout['widgets'][floatie_num].add_widget(widgets.card['widgets'][card_num])
					checkout_widgets.append(widgets.floatlayout['widgets'][floatie_num])

				elif meal_group_ == 'Smoothies' or meal_group_ == 'Shakes' or meal_group_ == 'Something_cold':
					meal_group = order[meal_group_]

					meal = ''
					extras_cost = 0
					meal_cost = 0
					ingredients = ''
					print(meal_group)
					for meal_, vals in meal_group.items():
						if meal_ != 'Status':
							meal = meal_
							meal_cost = meal_group[meal_]['price']
							ingredients = meal_group[meal_]['ingredients']
							total_cost = total_cost+meal_cost

					extras = {}
					if 'Extras' in list(meal_group[meal].keys()):
						extras = meal_group[meal]['Extras']

					# Card creation
					card = widgets.configure_new_widget(widget_type='card', widget_num=card_num,
													widget=widgets.card, layout='gridlayout',
													current_screen=current_screen, orientation='vertical',
													top=0.95, side="right",side_val=0.95, width=0.9, height=0.9)
					widgets.card = card[0]
					card_num = card[1]

					floatlayout = widgets.configure_new_widget(widget_type="floatlayout", widget_num=floatie_num, widget=widgets.floatlayout, current_screen=current_screen, 
					                                layout="gridlayout")
					widgets.floatlayout = floatlayout[0]
					floatie_num = floatlayout[1]


					boxlayout = widgets.configure_new_widget(widget_type='boxlayout', widget_num=box_num,
														  widget=widgets.boxlayout, layout='boxlayout',
														  orientation='horizontal', size_hint_y=0.25,
														  pop_orientation='vertical', current_screen=current_screen)
					widgets.boxlayout = boxlayout[0]
					box_num1 = boxlayout[1]
					box_num = box_num+1

					label = widgets.configure_new_widget(widget_type="mdlabel",value=0, widget_num=label_num, widget=widgets.label,
															layout="boxlayout", current_screen=current_screen, text=f'{meal.replace("_", " ")}',
															size_hint_x=0.75, orientation='horizontal')
					widgets.label = label[0]
					label_num1 = label[1]
					label_num = label_num+1

					icon_button = widgets.configure_new_widget(widget_type="icon_button", widget_num=icon_num, widget=widgets.icon_button,
															layout="boxlayout", current_screen=current_screen, icon='trash-can',
															orientation='horizontal', size_hint_x=0.25, params=('active_widget', finalorderQ, widgets.floatlayout['widgets'][floatie_num],
															order, bigPoppa, update_label, orders, orderlist), func=edit_final_order)
					widgets.icon_button = icon_button[0]
					icon_num = icon_button[1]

					# Ingredients
					label = widgets.configure_new_widget(widget_type="mdlabel",value=0, widget_num=label_num, widget=widgets.label,
															layout="boxlayout", current_screen=current_screen, text=ingredients,
															size_hint_y=0.4, orientation='vertical')
					widgets.label = label[0]
					label_num2 = label[1]
					label_num = label_num+1

					# Add ons
					boxlayout = widgets.configure_new_widget(widget_type='boxlayout', widget_num=box_num,
														  widget=widgets.boxlayout, layout='boxlayout',
														  orientation='vertical', size_hint_y=0.25,
														  pop_orientation='vertical', current_screen=current_screen)
					widgets.boxlayout = boxlayout[0]
					box_num3 = boxlayout[1]
					box_num = box_num+1

					for key, v in extras.items():
						extras_cost = extras_cost+v
						extra = (key.replace(' ','')).replace('-', '')

						label = widgets.configure_new_widget(widget_type="mdlabel",value=0, widget_num=label_num, widget=widgets.label,
															layout="boxlayout", current_screen=current_screen, text=f'{extra}: R{v}',
															size_hint_x=0.9/len(list(extras.keys())), orientation='horizontal')
						widgets.label = label[0]
						label_num6 = label[1]
						label_num = label_num+1

						total_cost = total_cost+v

						#widgets.boxlayout['widgets'][box_num3].add_widget(widgets.label['widgets'][label_num6])
						widgets.boxlayout['widgets'][box_num3].add_widget(MDLabel(text=f'{extra}: R{v}', size_hint_y=1/len(list(add_ons.keys()))))


					# Subtotal
					boxlayout = widgets.configure_new_widget(widget_type='boxlayout', widget_num=box_num,
														  widget=widgets.boxlayout, layout='boxlayout',
														  orientation='horizontal', size_hint_y=0.25,
														  pop_orientation='vertical', current_screen=current_screen)
					widgets.boxlayout = boxlayout[0]
					box_num2 = boxlayout[1]
					box_num = box_num+1

					label = widgets.configure_new_widget(widget_type="mdlabel",value=0, widget_num=label_num, widget=widgets.label,
															layout="boxlayout", current_screen=current_screen, text=f'Price: ',
															size_hint_x=0.75, orientation='horizontal')
					widgets.label = label[0]
					label_num3 = label[1]
					label_num = label_num+1

					label = widgets.configure_new_widget(widget_type="mdlabel",value=0, widget_num=label_num, widget=widgets.label,
															layout="boxlayout", current_screen=current_screen, text=f'R{meal_cost}',
															size_hint_x=0.25, orientation='horizontal')
					widgets.label = label[0]
					label_num4 = label[1]
					label_num = label_num+1

					# Populate top box
					#widgets.boxlayout['widgets'][box_num1].add_widget(widgets.label['widgets'][label_num1])
					widgets.boxlayout['widgets'][box_num1].add_widget(MDLabel(text=f'{meal.replace("_", " ")}', size_hint_x=0.75))
					widgets.boxlayout['widgets'][box_num1].add_widget(widgets.icon_button['widgets'][icon_num])

					# Populate bottom box
					#widgets.boxlayout['widgets'][box_num2].add_widget(widgets.label['widgets'][label_num3])
					#widgets.boxlayout['widgets'][box_num2].add_widget(widgets.label['widgets'][label_num4])
					widgets.boxlayout['widgets'][box_num2].add_widget(MDLabel(text=f'Price: ', size_hint_x=0.75))
					widgets.boxlayout['widgets'][box_num2].add_widget(MDLabel(text=f'R{meal_cost}', size_hint_x=0.25))
					
					# Populate card
					widgets.card['widgets'][card_num].add_widget(widgets.boxlayout['widgets'][box_num1])
					#widgets.card['widgets'][card_num].add_widget(widgets.label['widgets'][label_num2])
					widgets.card['widgets'][card_num].add_widget(MDLabel(text=ingredients, size_hint_y=0.25))
					widgets.card['widgets'][card_num].add_widget(widgets.boxlayout['widgets'][box_num3])
					widgets.card['widgets'][card_num].add_widget(widgets.boxlayout['widgets'][box_num2])

					widgets.floatlayout['widgets'][floatie_num].add_widget(widgets.card['widgets'][card_num])
					checkout_widgets.append(widgets.floatlayout['widgets'][floatie_num])

			card_num = card_num+1
			icon_num = icon_num+1
			floatie_num = floatie_num+1


		return checkout_widgets, total_cost, widgets