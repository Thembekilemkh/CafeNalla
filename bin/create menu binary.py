import pickle
import datetime
import os
'''
menu = {'Specials':{'Meal':{},
					'image':'coffee section.jpeg'},
		'Breakfast':{'image':'toast.jpeg',
					'Meal':{
							"Organic_Oats":{'Price':45,
											'Ingredients':['Peanut Butter','Honey', 'Milk']},
							'Egg_On_Toast':{'Price':36,
											'Ingredients':['2 eggs poached/fried/scrambled', 
														   'Two slices of low GI/Rye toast']},
							'Fresh_Fruit_Salad':{'Price':38,
											     'Ingredients':['Vegetarian'],
												 'Extras':{'Low Fat plain yoghurt & wheat free muesli':16,
												 		   'Mixed berry coulis':12,
												 		   'The whole shebang':58}},
							'Express_Health_Breakfast':{'Price':45,
											'Ingredients':['Rye toast', 'Hummus', 'Rockets' 
														   'Avaocado', 'Poached eggs']},
							'Express_Breakfast':{'Price':40,
											'Ingredients':['1 egg', 'Bacon', 'Fresh tomato' 
														   'Toast']},
							'New_English_Breakfast':{'Price':68,
													 'Ingredients':['2 eggs of choice', 'Beef sausage' 
														   'Bacon', 'Fresh tomato'],
													  'Extras':{'Avocado':14,
													  			'Lean mince or chicken strips':24}},
							'Lean_Mince_on_Toast':{'Price':38,
											'Ingredients':[''],
											'Extras':{'Scrambled or fried eggs':14,
													  'Avocado or rocket':14}},
							'Three_Egg_Omelette_Or_Scrambled_Eggs':{'Price':36,
											'Ingredients':['']},
							'Egg_White_Omelette_Or_Scrambled_Egg_Whites':{'Price':42,
											'Ingredients':[''],
											'Toppings':{1:{'Ingredients':['Ham/Bacon', 'Mushrooms',
													    				  'Caramalised onion', 'Peppers'],
													       'Price':68},
													    2:{'Ingredients':['Lean mince', 'Spinach', 'Feta'],
													       'Price':68},
													    3:{'Ingredients':['Chicken strips', 'Mushrooms', 'Peppers'],
													       'Price':70},
													    4:{'Ingredients':['Ham', "Cheese", 'Fresh tomato'],
													       'Price':68}}}},
					'Add_ons':{'Almond milk':6,
							   'Honey and almonds':15,
							   'Fresh banana slices and mixed seeds':12,
							   'Protein oats(whey protein)':16}},
		'Meals':{'image':'wrap.jpeg',
				 "Tramezzini's":{
				 				 'Meal':{
				 				 		 'Bacon/Mince':{'Price':50,
				 				 		 				'Ingredients':['']},
				 				 		 'Chicken_Mayo':{'Price':50,
				 				 		 				 'Ingredients':['']},
				 				 		 'Pasta':{'Price':74,
				 				 		 		  'Ingredients':['Free range chicken strips',
				 				 		 		  				 'Creamy white wine mushroom sauce',
				 				 		 		  				 'Sun dried tomato presto']}},
				 				 'Add_ons':{'100g chips':8}
				 },
				 'From_The_Grill':{'Meal':{
				 						   'Herbed_Grilled_Hake':{'Price':78,
				 						   						  'Ingredients':['Served fresh green salad']},
								   		   'Sirloin_Steak':{'Price':80,
								   		   					'Ingredients':['Green peppercorn glaze and creamy mushroom sauce']},
								   		   'Lemon_&_Herb_Free_Range_Chicken':{'Price':74,
								   		   									  'Ingredients':['Free range chicken breast grilled to perfection and served with brown rice']}},				   
				 				   'Add_ons':{"100g chips":8}}},
		'Salads':{'image':'avocado.jpg',
				  'Meal':{
						  'Fresh_Gourmet_Green':{'Price':60,
						  						 'Ingredients':['Baby lettuce leaves',
						  						 				'Cucumber', 'Cherry tomatoes',
						  						 				'Carrots ribos', 'Grated beetroot',
						  						 				'Mixed peppers', 'sprouts',
						  						 				'Toasted seeds', 'Cranberry mix']},
						  'Free_Range_Chicken_Breakfast_Salad':{'Price':72,
						  						 				'Ingredients':['Fresh green salad',
						  						 							   'Lemon & Herb chicken breast',
						  						 							   'Avocado', 'Honey and mustard dressing']},
						  'Grassed_Beef_Biltong_Salad':{'Price':76,
						  						 		'Ingredients':['Fresh green salad',
						  						 					   'Beef biltong', 'Caramalised onions',
						  						 					   'Pecorino shavings', 'Avocado', 'Balsamic glaze']},
						  'Chicken,Brown_Rice_And_Broccoli':{'Price':70,
						  						 			 'Ingredients':['Free range chicken', 'Brown rice', 
						  						 			 				'Corn', 'Sundried tomato',
						  						 			 				'Feta', 'Broccoli']},
						  'Tuna_Niscoise_Salad':{'Price':66,
						  						 'Ingredients':['Fresh green salad', 'Shredded tuna', 
						  						 				'Boiled eggs', 'Green beans', 'Yoghurt herb dressing']}},
				  'Add_ons':{'Avocado':14,
				  			 'Feta':18,
				  			 'Halloumi':18}},
		'Smoothies':{'image':'almonds.jpg',
					'Ginga_Ninja':{'Price':40,
									'Ingredients':['Banana', 'Ginger',
												   'Pineapple', 'Carrot Juice',
												   'Chia Seeds', 'Lemons', 'Honey',
												   'Turmeric', 'Water']},
					 'Klap_Gym':{'Price':40,
									'Ingredients':['Almonds', 'Banana',
												   'Chia Seeds', 'Cinnamon',
												   'Peanut Butter', 'Honey',
												   'Whey Protein', 'Yoghurt']},
					 'Green_Mamba':{'Price':40,
									'Ingredients':['Cucumber', 'Ginger',
												   'Kiwi', 'Lemon', 'Spinach',
												   'Celery', 'Mint', 'Honey']},
					 'Hulk':{'Price':40,
									'Ingredients':['Banana', 'Ginger',
												   'Spinach', 'Cardamon', 
												   'Peanut Butter', 'Honey', 
												   'Whey Protein', 'Water']},
					 'Halie_Berry':{'Price':40,
									'Ingredients':['Almonds', 'Mixed Berries',
												   'Honey', "Yoghurt"]},
					 'Very_Berry_Smoothie':{'Price':40,
									'Ingredients':["Berries", 'Banana',
												   'Cranberry Juice', 'Ice Blended']},
					 'Strawberry_Smoothie':{'Price':40,
									'Ingredients':['Strawberry', "Banana",
												   'Cranberry Juice', 'Ice Blended', ]},
					 'Mango_Smoothie':{'Price':40,
									'Ingredients':['Mango', 'Banana',
												   'Cranberry Juice', "Ice Blended"]},
					 'Peanut_Butter_Delight':{'Price':40,
									'Ingredients':['Whey Protein', 'Milk',
												   'Ice', 'Honey', 'Peanut Butter'],
									'Extra':{'Milk alternative':5}},
					 'Hangover_Cure':{'Price':40,
									'Ingredients':['Mixed Berries', 'Watermelon',
												   'Chia seeds', 'Lemon Juice', 'Mint']}},
		'Shakes':{'image':'ginger.jpg',
				  'Whey_Protein_Premium_Shake':{'Price':35,
												'Ingredients':['Available in vanilla, strawberry, banana & chocolate']},
				  'Chocolate_Based_Protein':{'Price':35,
											 'Ingredients':['Vegan, no sugar & best tasting plant protein around']},
				  'Pre_Workout_Boost':{'Price':35,
										'Ingredients':['']},
				  'BCAA_Post_Workout':{'Price':35,
									   'Ingredients':['Stimulant free']},
				  'Diet_Shake':{'Price':35,
								'Ingredients':['High fibre, low GI meal replacement']},
								},
		'Something_cold':{'image':'colddrinks.jpeg',
						  'Cold_Brew':{'Price':29,
									   'Ingredients':['Double expresso poured over ice',
									   				  'Cold milk'],
									   'Extra': {'Dollop of condensed milk':2}},
						  'Frozen_Latte':{'Price':38,
									   'Ingredients':['Frozen latte', 'Ice', 'Water blended into a slushy']},
						  'Red_Iced_Tea':{'Price':29,
									   'Ingredients':['Shot of red expresso', 'Ice', 'Cranberry']},
						  'Iced_Green_Tea':{'Price':29,
									   'Ingredients':['Chilled tea', 'Lemon', 'Lime ice', 'Fresh mint']}}}
'''
'''
for key, val in menu.items():
	offer = menu[key]
	print(f'CHECKING: {key}')
	for ley, bal in offer.items():
		print(f"Offer: {ley}")

# Open menu pickle
'''
'''
#UNMUTE TO CREATE UPDATE MENU
with open('menu.pickle', 'wb') as pickle_out:
	pickle.dump(menu, pickle_out)
	print("Dumped")
'''


with open('menu.pickle', 'rb') as pickle_in:
	myMenu = pickle.load(pickle_in)
	for key, val in myMenu.items():
		offer = myMenu[key]
		print(f'CHECKING: {key}')
		for ley, bal in offer.items():
			print(f"Offer: {ley}")

