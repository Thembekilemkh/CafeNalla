from kivymd.theming import ThemeManager
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivymd.uix.navigationdrawer import NavigationLayout, MDNavigationDrawer
from kivymd.uix.list import (OneLineAvatarListItem, TwoLineAvatarListItem, ThreeLineAvatarListItem,
                             OneLineIconListItem, TwoLineIconListItem, ThreeLineIconListItem,
                             OneLineAvatarIconListItem, TwoLineAvatarIconListItem, ThreeLineAvatarIconListItem,
                             TwoLineListItem)
from kivymd.uix.list import MDList
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.card import MDSeparator, MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import (MDIconButton, MDFloatingActionButton, MDFlatButton,
                            MDRaisedButton, MDRectangleFlatButton, MDRectangleFlatIconButton,
                            MDRoundFlatButton, MDRoundFlatIconButton, MDFillRoundFlatButton,
                            MDFillRoundFlatIconButton, MDTextButton, MDFloatingActionButtonSpeedDial)
from kivymd.toast import toast
from kivymd.theming import ThemableBehavior
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dropdownitem import MDDropDownItem
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.selectioncontrol import MDCheckbox, Thumb
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from kivymd.uix.picker import MDDatePicker
from kivymd.uix.behaviors import (CircularElevationBehavior,CircularRippleBehavior)
from kivymd.uix import MDAdaptiveWidget

# Standard kivy package
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.behaviors import ButtonBehavior

# STANDARD LIBRARY
from functools import partial

class PlaceOrderVariable(BoxLayout):
    def __init__(self, **kwargs):
        extra_type = kwargs['extra_type']
        if extra_type == 'Add_ons':
            # Get required variables for this selection
            name =kwargs['name'].replace('_', ' ')
            price_ = kwargs['price']
            price=f'R{str(price_)}'
            price_lbl = kwargs['price_lbl']
            func = kwargs['func']

            kwargs.pop('extra_type', None)
            kwargs.pop('name', None)
            kwargs.pop('price', None)
            kwargs.pop('price_lbl', None)
            kwargs.pop('func', None)

            self.size_hint_y=0.95
            self.orientation='horizontal'
            self.height='75dp'
            super(PlaceOrderVariable, self).__init__()

            name = MDLabel(text=name+' - '+price,size_hint_x=0.9)
            check = MDCheckbox(active=False, size_hint_x=0.1)
            check.bind(active=partial(func, price_, price_lbl))

            self.add_widget(name)
            self.add_widget(check)

        elif extra_type == 'Extras':
            name =kwargs['name'].replace('_', ' ')
            price_ = kwargs["price"]
            price=f'R{str(price_)}'
            price_lbl = kwargs['price_lbl']
            func = kwargs['func']

            self.size_hint_y=0.95
            self.orientation='horizontal'
            self.height='75dp'

            kwargs.pop('extra_type', None)
            kwargs.pop('name', None)
            kwargs.pop('price', None)
            kwargs.pop('price_lbl', None)
            kwargs.pop('func', None)
            super(PlaceOrderVariable, self).__init__()

            name = MDLabel(text=name+' - '+price,size_hint_x=0.9)
            check = MDCheckbox(active=False, size_hint_x=0.1)
            check.bind(active=partial(func, price_, price_lbl))

            self.add_widget(name)
            self.add_widget(check)

        elif extra_type == 'Toppings':
            ingredient = kwargs['ingredient']
            price_ = kwargs["price"]
            price=f'R{str(price_)}'
            price_lbl = kwargs['price_lbl']
            func = kwargs['func']

            self.size_hint_y=0.95
            self.orientation='horizontal'
            self.height='75dp'

            kwargs.pop('extra_type', None)
            kwargs.pop('ingredient', None)
            kwargs.pop('price', None)
            kwargs.pop('price_lbl', None)
            kwargs.pop('func', None)
            super(PlaceOrderVariable, self).__init__()

            #for key, val in toppings.items():
                #ingredient = toppings[key]['ingredients']
                #price = toppings[key]['price']

            ingredients = ''
            for ingre in ingredient:
                if ingre == ingredient[-1]:
                    ingredients = ingredients+ingre
                else:
                    ingredients = ingredients+ingre+', '
            ingre_lbl = MDLabel(text=f'{ingredients+" - "+price}',size_hint_x=0.9)
            ingre_check = MDCheckbox(active=False, size_hint_x=0.1)
            check.bind(active=partial(func, price_, price_lbl))

            self.add_widget(ingre_lbl)
            self.add_widget(ingre_check)

class PlaceOrderPopUp(BoxLayout):
    def __init__(self, **kwargs):
        ingredients = kwargs['ingredients']
        meal_name = kwargs['meal_name']
        meal_price = kwargs['price']
        add_ons = kwargs['add_ons']
        extras = kwargs['extras']
        toppings = kwargs['toppings']
        kwargs.pop('ingredients', None)
        kwargs.pop('meal_name', None)
        kwargs.pop('add_ons', None)
        kwargs.pop('extras', None)
        kwargs.pop('toppings', None)

        self.size_hint_y=0.95
        self.orientation='vertical'
        self.height='100dp'
        super(PlaceOrderPopUp, self).__init__()

        # HEADING
        name_box=BoxLayout(orientation='horizontal', size_hint_y=0.1)
        name_lbl=Label(text=meal_name.replace('_',' '), size_hint_x=0.85)
        self.delete=MDIconButton(icon='delete', size_hint_x=0.15)
        self.price=Label(text=f'R{str(meal_price)}',size_hint_y=0.3)
        name_box.add_widget(name_lbl)
        name_box.add_widget(self.delete)
        self.add_widget(name_box)

        # Extras, add ons, toppings
        add_on_lbl=Label(text='Add Ons', size_hint_y=0.1)
        extras_lbl=Label(text='Extras', size_hint_y=0.1)

        scroll = ScrollView(size_hint_y=0.7)
        scroll_grid = GridLayout(size_hint_y=None, row_default_height='75dp', 
                                cols=1, height=self.minimum_height)#height=scroll.minimum_height
        scroll.add_widget(scroll_grid)
        self.add_widget(scroll)

        print(f'add_ons: {add_ons}')
        print(f'extras: {extras}')
        print(f'toppings: {toppings}')

        # ADDONS
        self.add_ons = {}
        if add_ons != None:
            scroll_grid.add_widget(add_on_lbl)
            for key, val in add_ons.items():
                self.add_ons[key] = {}
                box = BoxLayout(orientation='horizontal')
                name = Label(text=key.replace('_', ' '),size_hint_x=0.7)
                price = Label(text=f'R{str(val)}',size_hint_x=0.15)
                check = MDCheckbox(active=False, size_hint_x=0.15)
                self.add_ons[key]['check'] = check
                self.add_ons[key]['name'] = name
                self.add_ons[key]['price'] = price

            for key, val in self.add_ons.items():
                scroll_grid.add_widget(self.add_ons[key]['name'])
                scroll_grid.add_widget(self.add_ons[key]['price'])
                scroll_grid.add_widget(self.add_ons[key]['check'])
        else:
            scroll_grid.add_widget(Label(text='No add ons available'))

        # Extras
        self.extras = {}
        if extras != None:
            scroll_grid.add_widget(extras_lbl)
            for key, val in extras.items():
                self.extras[key] = {}
                box = BoxLayout(orientation='horizontal')
                name = Label(text=key.replace('_', ' '),size_hint_x=0.70)
                price = Label(text=f'R{str(val)}',size_hint_x=0.15)
                check = MDCheckbox(active=False, size_hint_x=0.15)
                self.extras[key]['check'] = check
                self.extras[key]['name'] = name
                self.extras[key]['price'] = price

            for key, val in self.extras.items():
                scroll_grid.add_widget(self.extras[key]['name'])
                scroll_grid.add_widget(self.extras[key]['price'])
                scroll_grid.add_widget(self.extras[key]['check'])
        else:
            scroll_grid.add_widget(Label(text='No extras available'))

        # TOPPINGS
        if toppings != None:
            scroll_grid.add_widget(topping_lbl)
            self.toppings = {}
            for key, val in toppings.items():
                self.toppings[key] = {}
                ingredient = toppings[key]['ingredients']
                price = toppings[key]['price']

                ingredients = ''
                for ingre in ingredients:
                    if ingre == ingredient[-1]:
                        ingredients = ingredients+ingre
                    else:
                        ingredients = ingredients+ingre+', '
                ingre_box = BoxLayout(orientation='horizontal')
                price_lbl = Label(text=f'{str(price)}')
                ingre_lbl = Label(text=f'{ingredients}')
                ingre_check = MDCheckbox(active=False)

                self.toppings[key]['check'] = ingre_check
                self.toppings[key]['name'] = ingre_lbl
                self.toppings[key]['price'] = price_lbl

            for key, val in self.toppings.items():
                scroll_grid.add_widget(self.toppings[key]['name'])
                scroll_grid.add_widget(self.toppings[key]['price'])
                scroll_grid.add_widget(self.toppings[key]['check'])
        else:
            scroll_grid.add_widget(Label(text='No toppings available'))

        print('scroll view added')


class Widgets():
    def __init__(self, **kwargs):
        # LAYOUTS
        self.floatlayout = {"number":0,
                        "widgets":[],
                        "current_screen":{}}
        i = 0
        for i in range(500):
            self.floatlayout["widgets"].append(FloatLayout())
            self.floatlayout["number"] = self.floatlayout["number"]+1
            self.floatlayout["current_screen"][i] = None

        self.gridlayout = {"number":0,
                        "widgets":[],
                        "current_screen":{}}
        i = 0
        for i in range(500):
            self.gridlayout["widgets"].append(GridLayout())
            self.gridlayout["number"] = self.gridlayout["number"]+1
            self.gridlayout["current_screen"][i] = None

        self.boxlayout = {'number':0,
                          'widgets':[],
                          'current_screen':{}}
        i=0
        for i in range(500):
            self.boxlayout['widgets'].append(BoxLayout())
            self.boxlayout['number']= self.boxlayout['number']+1
            self.boxlayout['current_screen'][i] = None

        # Buttons
        self.round_flat_button = {"number":0,
                          "widgets":[],
                          "callbacks":{},
                          "current_screen":{}}
        i = 0
        for i in range(20):
            self.round_flat_button["widgets"].append(MDRoundFlatButton())
            self.round_flat_button["number"] = self.round_flat_button["number"]+1
            self.round_flat_button["current_screen"][i] = None

        self.raised_button = {"number":0,
                          "widgets":[],
                          "callbacks":{},
                          "current_screen":{}}
        i = 0
        for i in range(20):
            self.raised_button["widgets"].append(MDRaisedButton())
            self.raised_button["number"] = self.raised_button["number"]+1
            self.raised_button["current_screen"][i] = None

        MDFlatButton
        self.flat_button = {"number":0,
                          "widgets":[],
                          "callbacks":{},
                          "current_screen":{}}
        i = 0
        for i in range(20):
            self.flat_button["widgets"].append(MDFlatButton())
            self.flat_button["number"] = self.flat_button["number"]+1
            self.flat_button["current_screen"][i] = None

        self.icon_button = {"number":0,
                          "widgets":[],
                          "callbacks":{},
                          "current_screen":{}}
        i = 0
        for i in range(50):
            self.icon_button["widgets"].append(MDIconButton())
            self.icon_button["number"] = self.icon_button["number"]+1
            self.icon_button["current_screen"][i] = None

        # POPUP
        self.dialog = {"number":0,
                  "widgets":[],
                  "current_screen":{}} 
        i = 0
        for i in range(100):
            self.dialog["widgets"].append(MDDialog(type='custom'))
            self.dialog["number"] = self.dialog["number"]+1
            self.dialog["current_screen"][i] = None
        

        # LABELS
        self.label = {"number":0,
                  "widgets":[],
                  "current_screen":{}}
        i = 0
        for i in range(500):
            self.label["widgets"].append(Label())
            self.label["number"] = self.label["number"]+1
            self.label["current_screen"][i] = None

        self.mdlabel = {"number":0,
                        "widgets":[],
                        "current_screen":{}}

        i = 0
        for i in range(100):
            self.mdlabel["widgets"].append(MDLabel())
            self.mdlabel["number"] = self.mdlabel["number"]+1
            self.mdlabel["current_screen"][i] = None

        # TWOLINELIST
        self.twolinelist = {"number":0,
                        "widgets":[],
                        "callbacks":{},
                        "current_screen":{}}    #{"id":1, "params":None, "func":func}
        i = 0
        for i in range(40):
            self.twolinelist["widgets"].append(TwoLineListItem())
            self.twolinelist["number"] = self.twolinelist["number"]+1
            self.twolinelist["current_screen"][i] = None 

        # PROGRESS BAR
        self.progressbar = {"number":0,
                        "widgets":[],
                        "current_screen":{}}  
        i = 0
        for i in range(1):
            self.progressbar["widgets"].append(MDProgressBar())
            self.progressbar["number"] = self.progressbar["number"]+1
            self.progressbar["current_screen"][i] = None

        # DROP DOWN WIDGETS
        self.dropdownitem = {"number":0,
                         "widgets":[],
                         "callbacks":{},
                         "current_screen":{}}
        i = 0
        for i in range(50):
            self.dropdownitem["widgets"].append(MDDropDownItem())
            self.dropdownitem["number"] = self.dropdownitem["number"]+1
            self.dropdownitem["current_screen"][i] = None

        self.dropdownmenu = {"number":0,
                         "widgets":[],
                         "callbacks":{},
                         "current_screen":{}}
        i = 0 
        for i in range(50):
            self.dropdownmenu["widgets"].append(MDDropdownMenu(caller=self.dropdownitem["widgets"][0]))
            self.dropdownmenu["number"] = self.dropdownmenu["number"]+1
            self.dropdownmenu["current_screen"][i] = None

        # EXPANSION PANELS
        self.expansiononeline = {"number":0,
                             "widgets":[],
                             "current_screen":{}}
        i = 0
        for i in range(40):
            self.expansiononeline["widgets"].append(MDExpansionPanelOneLine())
            self.expansiononeline["number"] = self.expansiononeline["number"]+1
            self.expansiononeline["current_screen"][i] = None

        self.expansionpanel = {"number":0,
                      "widgets":[],
                      "current_screen":{}}
        i = 0
        for i in range(40):
            self.expansionpanel["widgets"].append(MDExpansionPanel(panel_cls=self.expansiononeline["widgets"][i]))
            self.expansionpanel["number"] = self.expansionpanel["number"]+1
            self.expansionpanel["current_screen"][i] = None

        # Card
        self.card = {'number':0,
                     'widgets':[],
                     'current_screen':{}}

        i=0
        for i in range(500):
            self.card['widgets'].append(MDCard())
            self.card['number'] = self.card['number']+1
            self.card['current_screen'][i] = None

        # IMAGES
        self.image = {'number':0,
                     'widgets':[],
                     'current_screen':{}}

        i=0
        for i in range(500):
            self.image['widgets'].append(Image(allow_stretch=True, keep_ratio=False))
            self.image['number'] = self.image['number']+1
            self.image['current_screen'][i] = None

    def create_new_widget(self, name, **kwargs):
        if name == "round_flat_button":
            return MDRoundFlatButton()

        elif name == 'raised_button':
            return MDRaisedButton()

        elif name == 'flat_button':
            return MDFlatButton()

        elif name == 'dialog':
            return MDDialog(type='custom')

        elif name == 'image':
            return Image(allow_stretch=True, keep_ratio=False)

        elif name == 'icon_button':
            return MDIconButton()

        elif name == "floatlayout":
            return FloatLayout()

        elif name == "label":
            return Label()

        elif name == "mdlabel":
            return MDLabel()

        elif name == "progressbar":
            return MDProgressBar()

        elif name == "twolinelist":
            try:
                lists = []
                number = kwargs["number"]
                for x in range(number):
                    twolinelist = TwoLineListItem()
                    lists.append(twolinelist)

                return lists
            except:
                return TwoLineListItem()

        elif name == "progressbar":
            return MDProgressBar()

        elif name == "gridlayout":
            return GridLayout()

        elif name == "dropdownitem":
            return MDDropDownItem()

        elif name == "dropdownmenu":
            return MDDropdownMenu()

        elif name == "expansionpanel":
            panel_cls = MDExpansionPanelOneLine()
            return MDExpansionPanel(panel_cls=panel_cls)

        elif name == "expansiononeline":
            return MDExpansionPanelOneLine()

        elif name == 'card':
            return MDCard()

        elif name == 'boxlayout':
            return BoxLayout()

    # Refer to small exercise binding and unbinding methods
    def bind_unbind(self, btn, callbacks, new_func, new_params, method, id_):
        observers = btn.get_property_observers(method)
        if observers != []:
            old_params = callbacks[id_]["params"]
            old_func = callbacks[id_]["func"]
            btn.funbind(method, old_func, old_params)

        btn.fbind(method, new_func, new_params)

        return btn

    def configure_new_widget(self, **kwargs):
        # Get the data required
        widget_type = kwargs["widget_type"]

        if widget_type == "label":
            widget_num = kwargs["widget_num"]
            widget = kwargs["widget"]
            value = kwargs["value"]
            text = kwargs["text"]

            current_screen = kwargs["current_screen"]
            layout = kwargs["layout"]

            if value == 0:
                # Find the next widget that doesn't exist already on this page
                try:
                    if widget["current_screen"][widget_num] != None:
                        if widget["current_screen"][widget_num] == current_screen:
                            screen = current_screen
                            while screen == current_screen:
                                try:
                                    if widget["current_screen"][widget_num] == current_screen:
                                        widget_num = widget_num+1
                                        screen = widget["current_screen"][widget_num]
                                    else:
                                        screen = "Its fine"
                                        break
                                except Exception as e:
                                    screen = "Its fine"
                                    break
                        else:
                            pass
                    else:
                        pass
                except Exception as e:
                    pass

                if widget_num < widget["number"]:
                    # Check for a parent
                    parent = widget["widgets"][widget_num].parent
                    if parent == None:
                        if layout == "floatlayout":
                            top = kwargs["top"]
                            side = kwargs["side"]
                            side_val = kwargs["side_val"]
                            width = kwargs["width"]
                            height = kwargs["height"]

                            widget["widgets"][widget_num].text = text
                            widget["widgets"][widget_num].pos_hint = {"top": top, side:side_val}
                            widget["widgets"][widget_num].size_hint = (width,height)
                            widget["current_screen"][widget_num] = current_screen

                            widget = [widget, widget_num]
                            return widget

                        elif layout == "gridlayout":
                            widget["widgets"][widget_num].text = text
                            widget["current_screen"][widget_num]  = current_screen

                            widget = [widget, widget_num]
                            return widget

                        elif layout == 'boxlayout':
                            orientation = kwargs['orientation']
                            if orientation == 'vertical':
                                size_hint_y = kwargs['size_hint_y']

                                widget["widgets"][widget_num].text = text
                                widget['widgets'][widget_num].size_hint_y = size_hint_y
                                widget["current_screen"][widget_num]  = current_screen

                                widget = [widget, widget_num]
                                return widget
                            elif orientation == 'horizontal':
                                size_hint_x = kwargs['size_hint_x']

                                widget["widgets"][widget_num].text = text
                                widget['widgets'][widget_num].size_hint_x = size_hint_x
                                widget["current_screen"][widget_num]  = current_screen

                                widget = [widget, widget_num]
                                return widget

                    else:
                        parent.remove_widget(widget["widgets"][widget_num])
                        if layout == 'floatlayout':
                            top = kwargs["top"]
                            side = kwargs["side"]
                            side_val = kwargs["side_val"]
                            width = kwargs["width"]
                            height = kwargs["height"]

                            widget["widgets"][widget_num].text = text
                            widget["widgets"][widget_num].pos_hint = {"top": top, side:side_val}
                            widget["widgets"][widget_num].size_hint = (width,height)
                            widget["current_screen"][widget_num] = current_screen

                            widget = [widget, widget_num]
                            return widget

                        elif layout == "gridlayout":
                            widget["widgets"][widget_num].text = text
                            widget["current_screen"][widget_num] = current_screen

                            widget = [widget, widget_num]
                            return widget

                        elif layout == 'boxlayout':
                            orientation = kwargs['orientation']
                            if orientation == 'vertical':
                                size_hint_y = kwargs['size_hint_y']

                                widget["widgets"][widget_num].text = text
                                widget['widgets'][widget_num].size_hint_y = size_hint_y
                                widget["current_screen"][widget_num]  = current_screen

                                widget = [widget, widget_num]
                                return widget
                            elif orientation == 'horizontal':
                                size_hint_x = kwargs['size_hint_x']

                                widget["widgets"][widget_num].text = text
                                widget['widgets'][widget_num].size_hint_x = size_hint_x
                                widget["current_screen"][widget_num]  = current_screen

                                widget = [widget, widget_num]
                                return widget
                else:
                    if layout == "floatlayout":
                        top = kwargs["top"]
                        side = kwargs["side"]
                        side_val = kwargs["side_val"]
                        width = kwargs["width"]
                        height = kwargs["height"]

                        widget["number"] = widget["number"]+1

                        temp_label = self.create_new_widget("label")
                        temp_label.text = str(text)
                        temp_label.pos_hint = {"top": top, side:side_val}
                        temp_label.size_hint = (width,height)

                        widget["widgets"].append(temp_label)
                        widget["current_screen"][widget_num] = current_screen

                        widget = [widget, widget_num]
                        return widget

                    elif layout == "gridlayout":
                        widget["number"] = widget["number"]+1

                        temp_label = self.create_new_widget("label")
                        temp_label.text = str(text)
                        widget["widgets"].append(temp_label)
                        widget["current_screen"][widget_num] = current_screen

                        widget = [widget, widget_num]
                        return widget

                    elif layout == 'boxlayout':
                        orientation = kwargs['orientation']
                        if orientation == 'vertical':
                            size_hint_y = kwargs['size_hint_y']

                            widget["number"] = widget["number"]+1

                            temp_label = self.create_new_widget("label")
                            temp_label.text = str(text)
                            widget["widgets"].append(temp_label)

                            widget["widgets"][widget_num].text = text
                            widget['widgets'][widget_num].size_hint_y = size_hint_y
                            widget["current_screen"][widget_num]  = current_screen

                            widget = [widget, widget_num]
                            return widget
                        elif orientation == 'horizontal':
                            size_hint_x = kwargs['size_hint_x']

                            temp_label = self.create_new_widget("label")
                            temp_label.text = str(text)
                            widget["widgets"].append(temp_label)

                            widget["widgets"][widget_num].text = text
                            widget['widgets'][widget_num].size_hint_x = size_hint_x
                            widget["current_screen"][widget_num]  = current_screen

                            widget = [widget, widget_num]
                            return widget

            elif value == 1:
				# Find the next widget that doesn't exist already on this page
                try:
                    if widget["current_screen"][widget_num] != None:
                        if widget["current_screen"][widget_num] == current_screen:
                            screen = current_screen
                            while screen == current_screen:
                                try:
                                    if widget["current_screen"][widget_num] == current_screen:
                                        widget_num = widget_num+1
                                        screen = widget["current_screen"][widget_num]
                                    else:
                                        screen = "Its fine"
                                        break
                                except Exception as e:
                                    screen = "Its fine"
                                    break
                        else:
                            pass
                    else:
                        pass
                except Exception as e:
                    pass

                if text == "record":
                    stat = kwargs["stat"]
                    if widget_num < widget["number"]:
                        parent = widget["widgets"][widget_num].parent
                        if parent == None:
                            if layout == "floatlayout":
                                top = kwargs["top"]
                                side = kwargs["side"]
                                side_val = kwargs["side_val"]
                                width = kwargs["width"]
                                height = kwargs["height"]

                                widget["widgets"][widget_num].text = str(stat[0])+" - "+str(stat[1])
                                widget["widgets"][widget_num].pos_hint = {"top": top, side:side_val}
                                widget["widgets"][widget_num].size_hint = (width,height)
                                widget["current_screen"][widget_num] = current_screen

                                widget = [widget, widget_num]
                                return widget

                            elif layout == "gridlayout":
                                widget["widgets"][widget_num].text = str(stat[0])+" - "+str(stat[1])
                                widget["current_screen"][widget_num] = current_screen

                                widget = [widget, widget_num]
                                return widget

                            elif layout == 'boxlayout':
                                orientation = kwargs['orientation']
                                if orientation == 'vertical':
                                    size_hint_y = kwargs['size_hint_y']

                                    widget["widgets"][widget_num].text = text
                                    widget['widgets'][widget_num].size_hint_y = size_hint_y
                                    widget["current_screen"][widget_num]  = current_screen

                                    widget = [widget, widget_num]
                                    return widget
                                elif orientation == 'horizontal':
                                    size_hint_x = kwargs['size_hint_x']

                                    widget["widgets"][widget_num].text = text
                                    widget['widgets'][widget_num].size_hint_x = size_hint_x
                                    widget["current_screen"][widget_num]  = current_screen

                                    widget = [widget, widget_num]
                                    return widget

                        else:
                            parent.remove_widget(widget["widgets"][widget_num])
                            if layout == "floatlayout":
                                top = kwargs["top"]
                                side = kwargs["side"]
                                side_val = kwargs["side_val"]
                                width = kwargs["width"]
                                height = kwargs["height"]

                                widget["widgets"][widget_num]

                                if isinstance(stat[0], int):
                                    wins = stat[0]
                                    losses = stat[1]
                                else:
                                    wins = stat[value][0]
                                    losses = stat[value][1]

                                    widget["widgets"][widget_num].text = f"{wins} - {losses}"
                                    widget["widgets"][widget_num].pos_hint = {"top":top, side:side_val}
                                    widget["widgets"][widget_num].size_hint = (width,height)
                                    widget["current_screen"][widget_num] = current_screen

                                    widget = [widget, widget_num]
                                    return widget

                            elif layout == "gridlayout":
                                widget["widgets"][widget_num].text = str(text)
                                widget["current_screen"][widget_num] = current_screen

                                widget = [widget, widget_num]
                                return widget

                            elif layout == 'boxlayout':
                                orientation = kwargs['orientation']
                                if orientation == 'vertical':
                                    size_hint_y = kwargs['size_hint_y']

                                    widget["widgets"][widget_num].text = str(text)
                                    widget['widgets'][widget_num].size_hint_y = size_hint_y
                                    widget["current_screen"][widget_num]  = current_screen

                                    widget = [widget, widget_num]
                                    return widget
                                elif orientation == 'horizontal':
                                    size_hint_x = kwargs['size_hint_x']

                                    widget["widgets"][widget_num].text = text
                                    widget['widgets'][widget_num].size_hint_x = size_hint_x
                                    widget["current_screen"][widget_num]  = current_screen

                                    widget = [widget, widget_num]
                                    return widget
	                
                else:
                    if widget_num < widget["number"]:
                        parent = widget["widgets"][widget_num].parent
                        if parent == None:
                            if layout == "floatlayout":
                                top = kwargs["top"]
                                side = kwargs["side"]
                                side_val = kwargs["side_val"]
                                width = kwargs["width"]
                                height = kwargs["height"]

                                widget["widgets"][widget_num].text = str(text)
                                widget["widgets"][widget_num].pos_hint = {"top": top, side:side_val}
                                widget["widgets"][widget_num].size_hint = (width,height)
                                widget["current_screen"][widget_num] = current_screen

                                widget = [widget, widget_num]
                                return widget

                            elif layout == "gridlayout":
                                widget["widgets"][widget_num].text = str(text)
                                widget["current_screen"][widget_num] = current_screen

                                widget = [widget, widget_num]
                                return widget

                            elif layout == 'boxlayout':
                                orientation = kwargs['orientation']
                                if orientation == 'vertical':
                                    size_hint_y = kwargs['size_hint_y']

                                    widget["widgets"][widget_num].text = str(text)
                                    widget['widgets'][widget_num].size_hint_y = size_hint_y
                                    widget["current_screen"][widget_num]  = current_screen

                                    widget = [widget, widget_num]
                                    return widget
                                elif orientation == 'horizontal':
                                    size_hint_x = kwargs['size_hint_x']

                                    widget["widgets"][widget_num].text = str(text)
                                    widget['widgets'][widget_num].size_hint_x = size_hint_x
                                    widget["current_screen"][widget_num]  = current_screen

                                    widget = [widget, widget_num]
                                    return widget

                        else:
                            parent.remove_widget(widget["widgets"][widget_num])
                            if layout == "floatlayout":
                                top = kwargs["top"]
                                side = kwargs["side"]
                                side_val = kwargs["side_val"]
                                width = kwargs["width"]
                                height = kwargs["height"]

                                widget["widgets"][widget_num].text = str(text)
                                widget["widgets"][widget_num].pos_hint = {"top": top, side:side_val}
                                widget["widgets"][widget_num].size_hint = (width,height)
                                widget["current_screen"][widget_num] = current_screen

                                widget = [widget, widget_num]
                                return widget

                            elif layout == "gridlayout":
                                widget["widgets"][widget_num].text = str(text)
                                widget["current_screen"][widget_num] = current_screen

                                widget = [widget, widget_num]
                                return widget

                            elif layout == 'boxlayout':
                                orientation = kwargs['orientation']
                                if orientation == 'vertical':
                                    size_hint_y = kwargs['size_hint_y']

                                    widget["widgets"][widget_num].text = str(text)
                                    widget['widgets'][widget_num].size_hint_y = size_hint_y
                                    widget["current_screen"][widget_num]  = current_screen

                                    widget = [widget, widget_num]
                                    return widget
                                elif orientation == 'horizontal':
                                    size_hint_x = kwargs['size_hint_x']

                                    widget["widgets"][widget_num].text = str(text)
                                    widget['widgets'][widget_num].size_hint_x = size_hint_x
                                    widget["current_screen"][widget_num]  = current_screen

                                    widget = [widget, widget_num]
                                    return widget

                    else:
                        if layout == "floatlayout":
                            top = kwargs["top"]
                            side = kwargs["side"]
                            side_val = kwargs["side_val"]
                            width = kwargs["width"]
                            height = kwargs["height"]

                            widget["number"] = widget["number"]+1

                            temp_label = self.create_new_widget("label")
                            temp_label.text = str(text)
                            temp_label.pos_hint = {"top": top, side:side_val}
                            temp_label.size_hint = (width,height)

                            widget["widgets"].append(temp_label)
                            widget["current_screen"][widget_num] = current_screen

                            widget = [widget, widget_num]
                            return widget

                        elif layout == "gridlayout":
                            widget["number"] = widget["number"]+1

                            temp_label = self.create_new_widget("label")
                            temp_label.text = str(text)
                            widget["widgets"].append(temp_label)
                            widget["current_screen"][widget_num] = current_screen

                            widget = [widget, widget_num]
                            return widget

                        elif layout == 'boxlayout':
                            orientation = kwargs['orientation']
                            if orientation == 'vertical':
                                size_hint_y = kwargs['size_hint_y']

                                widget["number"] = widget["number"]+1

                                temp_label = self.create_new_widget("label")
                                temp_label.text = str(text)
                                widget["widgets"].append(temp_label)

                                widget["widgets"][widget_num].text = text
                                widget['widgets'][widget_num].size_hint_y = size_hint_y
                                widget["current_screen"][widget_num]  = current_screen

                                widget = [widget, widget_num]
                                return widget
                            elif orientation == 'horizontal':
                                size_hint_x = kwargs['size_hint_x']

                                widget["number"] = widget["number"]+1

                                temp_label = self.create_new_widget("label")
                                temp_label.text = str(text)
                                widget["widgets"].append(temp_label)

                                widget["widgets"][widget_num].text = text
                                widget['widgets'][widget_num].size_hint_x = size_hint_x
                                widget["current_screen"][widget_num]  = current_screen

                                widget = [widget, widget_num]
                                return widget


        if widget_type == "mdlabel":
            widget_num = kwargs["widget_num"]
            widget = kwargs["widget"]
            value = kwargs["value"]
            text = kwargs["text"]

            current_screen = kwargs["current_screen"]
            layout = kwargs["layout"]

            if value == 0:
                # Find the next widget that doesn't exist already on this page
                try:
                    if widget["current_screen"][widget_num] != None:
                        if widget["current_screen"][widget_num] == current_screen:
                            screen = current_screen
                            while screen == current_screen:
                                try:
                                    if widget["current_screen"][widget_num] == current_screen:
                                        widget_num = widget_num+1
                                        screen = widget["current_screen"][widget_num]
                                    else:
                                        screen = "Its fine"
                                        break
                                except Exception as e:
                                    screen = "Its fine"
                                    break
                        else:
                            pass
                    else:
                        pass
                except Exception as e:
                    pass

                if widget_num < widget["number"]:
                    # Check for a parent
                    parent = widget["widgets"][widget_num].parent
                    if parent == None:
                        if layout == "floatlayout":
                            top = kwargs["top"]
                            side = kwargs["side"]
                            side_val = kwargs["side_val"]
                            width = kwargs["width"]
                            height = kwargs["height"]

                            widget["widgets"][widget_num].text = text
                            widget["widgets"][widget_num].pos_hint = {"top": top, side:side_val}
                            widget["widgets"][widget_num].size_hint = (width,height)
                            widget["current_screen"][widget_num] = current_screen

                            widget = [widget, widget_num]
                            return widget

                        elif layout == "gridlayout":
                            widget["widgets"][widget_num].text = text
                            widget["current_screen"][widget_num]  = current_screen

                            widget = [widget, widget_num]
                            return widget

                        elif layout == 'boxlayout':
                            orientation = kwargs['orientation']
                            if orientation == 'vertical':
                                size_hint_y = kwargs['size_hint_y']

                                widget["widgets"][widget_num].text = str(text)
                                widget['widgets'][widget_num].size_hint_y = size_hint_y
                                widget["current_screen"][widget_num]  = current_screen

                                widget = [widget, widget_num]
                                return widget
                            elif orientation == 'horizontal':
                                size_hint_x = kwargs['size_hint_x']

                                widget["widgets"][widget_num].text = str(text)
                                widget['widgets'][widget_num].size_hint_x = size_hint_x
                                widget["current_screen"][widget_num]  = current_screen

                                widget = [widget, widget_num]
                                return widget

                    else:
                        parent.remove_widget(widget["widgets"][widget_num])
                        if layout == 'floatlayout':
                            top = kwargs["top"]
                            side = kwargs["side"]
                            side_val = kwargs["side_val"]
                            width = kwargs["width"]
                            height = kwargs["height"]

                            widget["widgets"][widget_num].text = text
                            widget["widgets"][widget_num].pos_hint = {"top": top, side:side_val}
                            widget["widgets"][widget_num].size_hint = (width,height)
                            widget["current_screen"][widget_num] = current_screen

                            widget = [widget, widget_num]
                            return widget

                        elif layout == "gridlayout":
                            widget["widgets"][widget_num].text = text
                            widget["current_screen"][widget_num] = current_screen

                            widget = [widget, widget_num]
                            return widget

                        elif layout == 'boxlayout':
                            orientation = kwargs['orientation']
                            if orientation == 'vertical':
                                size_hint_y = kwargs['size_hint_y']

                                widget["widgets"][widget_num].text = str(text)
                                widget['widgets'][widget_num].size_hint_y = size_hint_y
                                widget["current_screen"][widget_num]  = current_screen

                                widget = [widget, widget_num]
                                return widget
                            elif orientation == 'horizontal':
                                size_hint_x = kwargs['size_hint_x']

                                widget["widgets"][widget_num].text = str(text)
                                widget['widgets'][widget_num].size_hint_x = size_hint_x
                                widget["current_screen"][widget_num]  = current_screen

                                widget = [widget, widget_num]
                                return widget
                else:
                    if layout == "floatlayout":
                        top = kwargs["top"]
                        side = kwargs["side"]
                        side_val = kwargs["side_val"]
                        width = kwargs["width"]
                        height = kwargs["height"]

                        widget["number"] = widget["number"]+1

                        temp_label = self.create_new_widget("mdlabel")
                        temp_label.text = str(text)
                        temp_label.pos_hint = {"top": top, side:side_val}
                        temp_label.size_hint = (width,height)

                        widget["widgets"].append(temp_label)
                        widget["current_screen"][widget_num] = current_screen

                        widget = [widget, widget_num]
                        return widget

                    elif layout == "gridlayout":
                        widget["number"] = widget["number"]+1

                        temp_label = self.create_new_widget("mdlabel")
                        temp_label.text = str(text)
                        widget["widgets"].append(temp_label)
                        widget["current_screen"][widget_num] = current_screen

                        widget = [widget, widget_num]
                        return widget

                    elif layout == 'boxlayout':
                        widget["number"] = widget["number"]+1
                        temp_label = self.create_new_widget("mdlabel")
                        temp_label.text = str(text)
                        widget["widgets"].append(temp_label)

                        orientation = kwargs['orientation']
                        if orientation == 'vertical':
                            size_hint_y = kwargs['size_hint_y']

                            widget["widgets"][widget_num].text = str(text)
                            widget['widgets'][widget_num].size_hint_y = size_hint_y
                            widget["current_screen"][widget_num]  = current_screen

                            widget = [widget, widget_num]
                            return widget
                        elif orientation == 'horizontal':
                            size_hint_x = kwargs['size_hint_x']

                            widget["widgets"][widget_num].text = str(text)
                            widgets['widgets'][widget_num].size_hint_x = size_hint_x
                            widget["current_screen"][widget_num]  = current_screen

                            widget = [widget, widget_num]
                            return widget

            elif value == 1:
                # Find the next widget that doesn't exist already on this page
                try:
                    if widget["current_screen"][widget_num] != None:
                        if widget["current_screen"][widget_num] == current_screen:
                            screen = current_screen
                            while screen == current_screen:
                                try:
                                    if widget["current_screen"][widget_num] == current_screen:
                                        widget_num = widget_num+1
                                        screen = widget["current_screen"][widget_num]
                                    else:
                                        screen = "Its fine"
                                        break
                                except Exception as e:
                                    screen = "Its fine"
                                    break
                        else:
                            pass
                    else:
                        pass
                except Exception as e:
                    pass

                if text == "record":
                    stat = kwargs["stat"]
                    if widget_num < widget["number"]:
                        parent = widget["widgets"][widget_num].parent
                        if parent == None:
                            if layout == "floatlayout":
                                top = kwargs["top"]
                                side = kwargs["side"]
                                side_val = kwargs["side_val"]
                                width = kwargs["width"]
                                height = kwargs["height"]

                                widget["widgets"][widget_num].text = str(stat[0])+" - "+str(stat[1])
                                widget["widgets"][widget_num].pos_hint = {"top": top, side:side_val}
                                widget["widgets"][widget_num].size_hint = (width,height)
                                widget["current_screen"][widget_num] = current_screen

                                widget = [widget, widget_num]
                                return widget

                            elif layout == "gridlayout":
                                widget["widgets"][widget_num].text = str(stat[0])+" - "+str(stat[1])
                                widget["current_screen"][widget_num] = current_screen

                                widget = [widget, widget_num]
                                return widget

                        else:
                            parent.remove_widget(widget["widgets"][widget_num])
                            if layout == "floatlayout":
                                top = kwargs["top"]
                                side = kwargs["side"]
                                side_val = kwargs["side_val"]
                                width = kwargs["width"]
                                height = kwargs["height"]

                                widget["widgets"][widget_num]

                                if isinstance(stat[0], int):
                                    wins = stat[0]
                                    losses = stat[1]
                                else:
                                    wins = stat[value][0]
                                    losses = stat[value][1]

                                    widget["widgets"][widget_num].text = f"{wins} - {losses}"
                                    widget["widgets"][widget_num].pos_hint = {"top":top, side:side_val}
                                    widget["widgets"][widget_num].size_hint = (width,height)
                                    widget["current_screen"][widget_num] = current_screen

                                    widget = [widget, widget_num]
                                    return widget

                            elif layout == "gridlayout":
                                widget["widgets"][widget_num].text = str(text)
                                widget["current_screen"][widget_num] = current_screen

                                widget = [widget, widget_num]
                                return widget
                    
                else:
                    if widget_num < widget["number"]:
                        parent = widget["widgets"][widget_num].parent
                        if parent == None:
                            if layout == "floatlayout":
                                top = kwargs["top"]
                                side = kwargs["side"]
                                side_val = kwargs["side_val"]
                                width = kwargs["width"]
                                height = kwargs["height"]

                                widget["widgets"][widget_num].text = str(text)
                                widget["widgets"][widget_num].pos_hint = {"top": top, side:side_val}
                                widget["widgets"][widget_num].size_hint = (width,height)
                                widget["current_screen"][widget_num] = current_screen

                                widget = [widget, widget_num]
                                return widget

                            elif layout == "gridlayout":
                                widget["widgets"][widget_num].text = str(text)
                                widget["current_screen"][widget_num] = current_screen

                                widget = [widget, widget_num]
                                return widget

                        else:
                            parent.remove_widget(widget["widgets"][widget_num])
                            if layout == "floatlayout":
                                top = kwargs["top"]
                                side = kwargs["side"]
                                side_val = kwargs["side_val"]
                                width = kwargs["width"]
                                height = kwargs["height"]

                                widget["widgets"][widget_num].text = str(text)
                                widget["widgets"][widget_num].pos_hint = {"top": top, side:side_val}
                                widget["widgets"][widget_num].size_hint = (width,height)
                                widget["current_screen"][widget_num] = current_screen

                                widget = [widget, widget_num]
                                return widget

                            elif layout == "gridlayout":
                                widget["widgets"][widget_num].text = str(text)
                                widget["current_screen"][widget_num] = current_screen

                                widget = [widget, widget_num]
                                return widget

                    else:
                        if layout == "floatlayout":
                            top = kwargs["top"]
                            side = kwargs["side"]
                            side_val = kwargs["side_val"]
                            width = kwargs["width"]
                            height = kwargs["height"]

                            widget["number"] = widget["number"]+1

                            temp_label = self.create_new_widget("mdlabel")
                            temp_label.text = str(text)
                            temp_label.pos_hint = {"top": top, side:side_val}
                            temp_label.size_hint = (width,height)

                            widget["widgets"].append(temp_label)
                            widget["current_screen"][widget_num] = current_screen

                            widget = [widget, widget_num]
                            return widget

                        elif layout == "gridlayout":
                            widget["number"] = widget["number"]+1

                            temp_label = self.create_new_widget("mdlabel")
                            temp_label.text = str(text)
                            widget["widgets"].append(temp_label)
                            widget["current_screen"][widget_num] = current_screen

                            widget = [widget, widget_num]
                            return widget



        elif widget_type == "floatlayout":
            widget_num = kwargs["widget_num"]
            widget = kwargs["widget"]
            layout = kwargs["layout"]
            current_screen = kwargs["current_screen"]

            widget["current_screen"][widget_num] = current_screen

            # Check next availble widget
            try:
                if widget["current_screen"][widget_num] != None:
                    if widget["current_screen"][widget_num] == current_screen:
                        screen = current_screen
                        while screen == current_screen:
                            try:
                                if widget["current_screen"][widget_num] == current_screen:
                                    widget_num = widget_num+1
                                    screen = widget["current_screen"][widget_num]
                                else:
                                    screen = "Its fine"
                                    break
                            except Exception as e:
                                screen = "Its fine"
                                break
                    else:
                        pass
                else:
                    pass
            except Exception as e:
                pass


            if widget_num < widget["number"]:
                #self.widgets.floatlayout["widgets"][floatie_num].clear_widgets
                widget["widgets"][widget_num].clear_widgets()
                if layout == "gridlayout":
                    parent = widget["widgets"][widget_num].parent
                    if parent == None:
                        widget["current_screen"][widget_num]=current_screen
                        return widget, widget_num

                    else:
                        parent.remove_widget(widget["widgets"][widget_num])
                        widget["current_screen"][widget_num]=current_screen

                        widget = [widget, widget_num]
                        return widget


            else:
                if layout == "gridlayout":
                    temp_float = self.create_new_widget("floatlayout")

                    widget["widgets"].append(temp_float)
                    widget["current_screen"][widget_num] = current_screen

                    widget = [widget, widget_num]
                    return widget

        elif widget_type == "dialog":
            widget_num = kwargs["widget_num"]
            widget = kwargs["widget"]
            layout = kwargs["layout"]
            current_screen = kwargs["current_screen"]
            content_cls = kwargs['content_cls']
            buttons = kwargs['buttons']
            title =kwargs['title']
            text=kwargs['text']

            widget["current_screen"][widget_num] = current_screen

            # Check next availble widget
            try:
                if widget["current_screen"][widget_num] != None:
                    if widget["current_screen"][widget_num] == current_screen:
                        screen = current_screen
                        while screen == current_screen:
                            try:
                                if widget["current_screen"][widget_num] == current_screen:
                                    widget_num = widget_num+1
                                    screen = widget["current_screen"][widget_num]
                                else:
                                    screen = "Its fine"
                                    break
                            except Exception as e:
                                screen = "Its fine"
                                break
                    else:
                        pass
                else:
                    pass
            except Exception as e:
                pass


            if widget_num < widget["number"]:
                #self.widgets.floatlayout["widgets"][floatie_num].clear_widgets
                widget["widgets"][widget_num].clear_widgets()
                if layout == "gridlayout":
                    parent = widget["widgets"][widget_num].parent
                    if parent == None:
                        widget["widgets"][widget_num].size_hint = size_hint
                        widget["widgets"][widget_num].title = title
                        widget["widgets"][widget_num].buttons = buttons
                        widget["widgets"][widget_num].content_cls=content_cls
                        widget["widgets"][widget_num].text=text
                        widget["current_screen"][widget_num]=current_screen
                        widget = [widget, widget_num]
                        return widget

                    else:
                        parent.remove_widget(widget["widgets"][widget_num])
                        widget["widgets"][widget_num].size_hint = size_hint
                        widget["widgets"][widget_num].title = title
                        widget["widgets"][widget_num].buttons = buttons
                        widget["widgets"][widget_num].content_cls=content_cls
                        widget["widgets"][widget_num].text=text
                        widget["current_screen"][widget_num]=current_screen

                        widget = [widget, widget_num]
                        return widget

                elif layout == "floatlayout":
                    size_hint = kwargs['size_hint']
                    parent = widget["widgets"][widget_num].parent
                    if parent == None:
                        widget["widgets"][widget_num].size_hint = size_hint
                        widget["widgets"][widget_num].title = title
                        widget["widgets"][widget_num].buttons = buttons
                        widget["widgets"][widget_num].content_cls=content_cls
                        widget["widgets"][widget_num].text=text
                        widget["current_screen"][widget_num]=current_screen
                        widget = [widget, widget_num]
                        print('Coming back')
                        return widget

                    else:
                        parent.remove_widget(widget["widgets"][widget_num])
                        widget["widgets"][widget_num].size_hint = size_hint
                        widget["widgets"][widget_num].title = title
                        widget["widgets"][widget_num].buttons = buttons
                        widget["widgets"][widget_num].content_cls=content_cls
                        widget["widgets"][widget_num].text=text
                        widget["current_screen"][widget_num]=current_screen

                        widget = [widget, widget_num]
                        return widget


            else:
                if layout == "gridlayout":
                    temp_float = self.create_new_widget("dialog")

                    widget["widgets"].append(temp_float)
                    widget["widgets"][widget_num].size_hint = size_hint
                    widget["widgets"][widget_num].title = title
                    widget["widgets"][widget_num].buttons = buttons
                    widget["widgets"][widget_num].content_cls=content_cls
                    widget["widgets"][widget_num].text=text
                    widget["current_screen"][widget_num] = current_screen

                    widget = [widget, widget_num]
                    return widget

                elif layout == "floatlayout":
                    size_hint = kwargs['size_hint']
                    temp_float = self.create_new_widget("dialog")

                    widget["widgets"].append(temp_float)
                    widget["widgets"][widget_num].size_hint = size_hint
                    widget["widgets"][widget_num].title = title
                    widget["widgets"][widget_num].buttons = buttons
                    widget["widgets"][widget_num].content_cls=content_cls
                    widget["widgets"][widget_num].text=text
                    widget["current_screen"][widget_num] = current_screen

                    widget = [widget, widget_num]
                    return widget

        elif widget_type == "boxlayout":
            widget_num = kwargs["widget_num"]
            widget = kwargs["widget"]
            layout = kwargs["layout"]
            orientation = kwargs['orientation']
            current_screen = kwargs["current_screen"]

            widget["current_screen"][widget_num] = current_screen

            # Check next availble widget
            try:
                if widget["current_screen"][widget_num] != None:
                    if widget["current_screen"][widget_num] == current_screen:
                        screen = current_screen
                        while screen == current_screen:
                            try:
                                if widget["current_screen"][widget_num] == current_screen:
                                    widget_num = widget_num+1
                                    screen = widget["current_screen"][widget_num]
                                else:
                                    screen = "Its fine"
                                    break
                            except Exception as e:
                                screen = "Its fine"
                                break
                    else:
                        pass
                else:
                    pass
            except Exception as e:
                pass


            if widget_num < widget["number"]:
                widget["widgets"][widget_num].clear_widgets()
                if layout == "gridlayout":
                    parent = widget["widgets"][widget_num].parent
                    if parent == None:
                        widget["current_screen"][widget_num]=current_screen
                        widget["widgets"][widget_num].orientation = orientation
                        widget = [widget, widget_num]
                        return widget

                    else:
                        parent.remove_widget(widget["widgets"][widget_num])
                        widget["current_screen"][widget_num]=current_screen
                        widget["widgets"][widget_num].orientation = orientation
                        widget = [widget, widget_num]
                        return widget

                elif layout == 'floatlayout':
                    parent = widget["widgets"][widget_num].parent
                    if parent == None:
                        top = kwargs["top"]
                        side = kwargs["side"]
                        side_val = kwargs["side_val"]
                        width = kwargs["width"]
                        height = kwargs["height"]
                        
                        widget["widgets"][widget_num].pos_hint={"top":top, side:side_val}
                        widget["widgets"][widget_num].size_hint=(width, height)

                        widget["widgets"][widget_num].orientation = orientation
                        widget["current_screen"][widget_num] = current_screen

                        widget = [widget, widget_num]
                        return widget

                    else:
                        parent.remove_widget(widget["widgets"][widget_num])
                        top = kwargs["top"]
                        side = kwargs["side"]
                        side_val = kwargs["side_val"]
                        width = kwargs["width"]
                        height = kwargs["height"]
                        
                        widget["widgets"][widget_num].pos_hint={"top":top, side:side_val}
                        widget["widgets"][widget_num].size_hint=(width, height)

                        widget["widgets"][widget_num].orientation = orientation
                        widget["current_screen"][widget_num] = current_screen

                        widget = [widget, widget_num]
                        return widget

                elif layout == 'boxlayout':
                    parent = widget["widgets"][widget_num].parent
                    if parent == None:
                        pop_orientation = kwargs['pop_orientation']
                        if pop_orientation == 'vertical':
                            size_hint_y = kwargs['size_hint_y']

                            widget["widgets"][widget_num].size_hint_y=size_hint_y

                            widget["widgets"][widget_num].orientation = orientation
                            widget["current_screen"][widget_num] = current_screen

                            widget = [widget, widget_num]
                            return widget

                        elif pop_orientation == 'horizontal':
                            size_hint_x = kwargs['size_hint_x']

                            widget["widgets"][widget_num].size_hint_x=size_hint_x

                            widget["widgets"][widget_num].orientation = orientation
                            widget["current_screen"][widget_num] = current_screen

                            widget = [widget, widget_num]
                            return widget

                    else:
                        parent.remove_widget(widget["widgets"][widget_num])
                        pop_orientation = kwargs['pop_orientation']
                        if pop_orientation == 'vertical':
                            size_hint_y = kwargs['size_hint_y']

                            widget["widgets"][widget_num].size_hint_y=size_hint_y

                            widget["widgets"][widget_num].orientation = orientation
                            widget["current_screen"][widget_num] = current_screen

                            widget = [widget, widget_num]
                            return widget

                        elif pop_orientation == 'horizontal':
                            size_hint_x = kwargs['size_hint_x']

                            widget["widgets"][widget_num].size_hint_x=size_hint_x

                            widget["widgets"][widget_num].orientation = orientation
                            widget["current_screen"][widget_num] = current_screen

                            widget = [widget, widget_num]
                            return widget
            else:
                widget_num = widget_num+1
                if layout == "gridlayout":
                    temp_float = self.create_new_widget("boxlayout")

                    widget["widgets"].append(temp_float)
                    widget["current_screen"][widget_num] = current_screen
                    widget["widgets"][widget_num].orientation = orientation
                    widget = [widget, widget_num]
                    return widget

                elif layout == 'floatlayout':
                    top = kwargs["top"]
                    side = kwargs["side"]
                    side_val = kwargs["side_val"]
                    width = kwargs["width"]
                    height = kwargs["height"]
                    
                    temp_float = self.create_new_widget("boxlayout")

                    widget["widgets"].append(temp_float)
                    widget["widgets"][widget_num].pos_hint={"top":top, side:side_val}
                    widget["widgets"][widget_num].size_hint=(width, height)
                    widget["widgets"][widget_num].orientation = orientation
                    widget["current_screen"][widget_num] = current_screen

                    widget = [widget, widget_num]
                    return widget

                elif layout == 'boxlayout':
                    pop_orientation = kwargs['pop_orientation']
                    if pop_orientation == 'horizontal':
                        size_hint_y = kwargs['size_hint_y']

                        temp_float = self.create_new_widget("boxlayout")
                        widget["widgets"].append(temp_float)

                        widget["widgets"][widget_num].size_hint_y=size_hint_y
                        widget["widgets"][widget_num].orientation = orientation
                        widget["current_screen"][widget_num] = current_screen

                        widget = [widget, widget_num]
                        return widget

                    elif pop_orientation == 'vertical':
                        size_hint_x = kwargs['size_hint_x']

                        temp_float = self.create_new_widget("boxlayout")
                        widget["widgets"].append(temp_float)

                        widget["widgets"][widget_num].size_hint_x=size_hint_x
                        widget["widgets"][widget_num].orientation = orientation
                        widget["current_screen"][widget_num] = current_screen

                        widget = [widget, widget_num]
                        return widget

        elif widget_type == "image":
            widget_num = kwargs["widget_num"]
            widget = kwargs["widget"]
            layout = kwargs["layout"]
            source = kwargs['source']
            current_screen = kwargs["current_screen"]

            widget["current_screen"][widget_num] = current_screen

            # Check next availble widget
            try:
                if widget["current_screen"][widget_num] != None:
                    if widget["current_screen"][widget_num] == current_screen:
                        screen = current_screen
                        while screen == current_screen:
                            try:
                                if widget["current_screen"][widget_num] == current_screen:
                                    widget_num = widget_num+1
                                    screen = widget["current_screen"][widget_num]
                                else:
                                    screen = "Its fine"
                                    break
                            except Exception as e:
                                screen = "Its fine"
                                break
                    else:
                        pass
                else:
                    pass
            except Exception as e:
                pass


            if widget_num < widget["number"]:
                widget["widgets"][widget_num].clear_widgets()
                if layout == "gridlayout":
                    parent = widget["widgets"][widget_num].parent
                    if parent == None:
                        widget["current_screen"][widget_num]=current_screen
                        widget["widgets"][widget_num].source = source
                        widget =[widget, widget_num]
                        return widget

                    else:
                        parent.remove_widget(widget["widgets"][widget_num])
                        widget["current_screen"][widget_num]=current_screen
                        widget["widgets"][widget_num].source = source
                        widget = [widget, widget_num]
                        return widget

                elif layout == 'floatlayout':
                    top = kwargs["top"]
                    side = kwargs["side"]
                    side_val = kwargs["side_val"]
                    width = kwargs["width"]
                    height = kwargs["height"]
                    
                    widget["widgets"][widget_num].pos_hint={"top":top, side:side_val}
                    widget["widgets"][widget_num].size_hint=(width, height)

                    widget["widgets"][widget_num].source = source
                    widget["current_screen"][widget_num] = current_screen

                    widget = [widget, widget_num]
                    return widget

                elif layout == 'boxlayout':
                    orientation = kwargs['orientation']
                    if orientation == 'vertical':
                        size_hint_y = kwargs['size_hint_y']

                        widget["widgets"][widget_num].size_hint_y=size_hint_y

                        widget["widgets"][widget_num].source = source
                        widget["current_screen"][widget_num] = current_screen

                        widget = [widget, widget_num]
                        return widget

                    elif orientation == 'horizontal':
                        size_hint_x = kwargs['size_hint_x']

                        widget["widgets"][widget_num].size_hint_x=size_hint_x

                        widget["widgets"][widget_num].source = source
                        widget["current_screen"][widget_num] = current_screen

                        widget = [widget, widget_num]
                        return widget
            else:
                if layout == "gridlayout":
                    temp_float = self.create_new_widget("image")

                    widget["widgets"].append(temp_float)
                    widget["current_screen"][widget_num] = current_screen
                    widget["widgets"][widget_num].orientation = orientation
                    widget = [widget, widget_num]
                    return widget

                elif layout == 'floatlayout':
                    top = kwargs["top"]
                    side = kwargs["side"]
                    side_val = kwargs["side_val"]
                    width = kwargs["width"]
                    height = kwargs["height"]
                    
                    temp_float = self.create_new_widget("image")

                    widget["widgets"].append(temp_float)
                    widget["widgets"][widget_num].pos_hint={"top":top, side:side_val}
                    widget["widgets"][widget_num].size_hint=(width, height)
                    widget["widgets"][widget_num].orientation = orientation
                    widget["current_screen"][widget_num] = current_screen

                    widget = [widget, widget_num]
                    return widget

                elif layout == 'boxlayout':
                    orientation = kwargs['orientation']
                    if orientation == 'horizontal':
                        size_hint_y = kwargs['size_hint_x']

                        temp_float = self.create_new_widget("image")
                        widget["widgets"].append(temp_float)

                        widget["widgets"][widget_num].size_hint_y=size_hint_y
                        widget["widgets"][widget_num].orientation = orientation
                        widget["current_screen"][widget_num] = current_screen

                        widget = [widget, widget_num]
                        return widget

                    elif orientation == 'vertical':
                        size_hint_x = kwargs['size_hint_y']

                        temp_float = self.create_new_widget("image")
                        widget["widgets"].append(temp_float)

                        temp_float = self.create_new_widget("image")
                        widget["widgets"].append(temp_float)

                        print('Array len: ',len(widget['widgets']))
                        print('Index: ', widget_num)
                        widget["widgets"][widget_num].size_hint_x=size_hint_x
                        widget["widgets"][widget_num].orientation = orientation
                        widget["current_screen"][widget_num] = current_screen

                        widget = [widget, widget_num]
                        return widget

        elif widget_type == "dropdownmenu":
            widget_num = kwargs["widget_num"]
            widget = kwargs["widget"]
            layout = kwargs["layout"]
            current_screen = kwargs["current_screen"]
            width = kwargs["width_mult"]

            widget["current_screen"][widget_num] = current_screen

            # Check next availble widget
            for id_, v in widget["current_screen"].items():
                if id_ == widget_num:
                    available = False
                    while available == False:
                        try:
                            if widget["current_screen"][widget_num] == current_screen:
                                widget_num = widget_num+1
                            else:
                                available = True
                        except Exception as e:
                            available = True
                else:
                    break


            if widget_num < widget["number"]:
                #self.widgets.floatlayout["widgets"][floatie_num].clear_widgets
                if layout == "gridlayout":
                    parent = widget["widgets"][widget_num].parent
                    if parent == None:
                        widget["widgets"][widget_num].width_mult = width
                        widget["current_screen"][widget_num]=current_screen
                        return widget, widget_num

                    else:
                        parent.remove_widget(widget["widgets"][widget_num])
                        widget["widgets"][widget_num].width_mult = width
                        widget["current_screen"][widget_num]=current_screen

                        widget = [widget, widget_num]
                        return widget


            else:
                if layout == "gridlayout":
                    temp_float = self.create_new_widget("dropdownmenu")

                    widget["widgets"].append(temp_float)
                    widget["widgets"][widget_num].width_multi = width
                    widget["current_screen"][widget_num] = current_screen

                    widget = [widget, widget_num]
                    return widget

        elif widget_type == "gridlayout":
            widget_num = kwargs["widget_num"]
            widget = kwargs["widget"]
            layout = kwargs["layout"]
            current_screen = kwargs["current_screen"]
            rows = kwargs["rows"]
            cols = kwargs["cols"]


            widget["current_screen"][widget_num] = current_screen

            # Check next availble widget
            for id_, v in widget["current_screen"].items():
                if id_ == widget_num:
                    available = False
                    while available == False:
                        try:
                            if widget["current_screen"][widget_num] == current_screen:
                                widget_num = widget_num+1
                            else:
                                available = True
                        except Exception as e:
                            available = True
                else:
                    break


            if widget_num < widget["number"]:
                widget["widgets"][widget_num].clear_widgets()
                if layout == "gridlayout":
                    parent = widget["widgets"][widget_num].parent
                    if parent == None:
                        widget["widgets"][widget_num].rows = rows
                        widget["widgets"][widget_num].cols = cols
                        widget["current_screen"][widget_num]=current_screen
                        return widget, widget_num

                    else:
                        parent.remove_widget(widget["widgets"][widget_num])
                        widget["widgets"][widget_num].rows = rows
                        widget["widgets"][widget_num].cols = cols
                        widget["current_screen"][widget_num]=current_screen

                        widget = [widget, widget_num]
                        return widget


            else:
                if layout == "gridlayout":
                    temp_float = self.create_new_widget("gridlayout")

                    widget["widgets"].append(temp_float)
                    widget["current_screen"][widget_num] = current_screen
                    widget["widgets"][widget_num].rows = rows
                    widget["widgets"][widget_num].cols = cols
                    widget = [widget, widget_num]
                    return widget

        elif widget_type == "dropdownitem":
            widget_num = kwargs["widget_num"]
            widget = kwargs["widget"]
            layout = kwargs["layout"]
            current_screen = kwargs["current_screen"]
            text =kwargs["text"]
            func = kwargs["func"]
            params = kwargs["params"]

            widget["current_screen"][widget_num] = current_screen

            # Check next availble widget
            for id_, v in widget["current_screen"].items():
                if id_ == widget_num:
                    available = False
                    while available == False:
                        try:
                            if widget["current_screen"][widget_num] == current_screen:
                                widget_num = widget_num+1
                            else:
                                available = True
                        except Exception as e:
                            available = True
                else:
                    break


            if widget_num < widget["number"]:
                #self.widgets.floatlayout["widgets"][floatie_num].clear_widgets
                parent = widget["widgets"][widget_num].parent
                if parent == None:
                    if layout == "gridlayout":
                        btn = widget["widgets"][widget_num]
                        btn.text = text.replace("_"," ")
                        btn.current_text = text.replace("_"," ")

                        if params != None:
                            callbacks = widget["callbacks"]
                            new_params = []
                            for param in range(len(params)):
                                if params[param] == "active_widget":
                                    new_params.append(btn)
                                elif params[param] == "active_widget_text":
                                    new_params.append(btn.text)
                                else:
                                    new_params.append(params[param])

                            widget["widgets"][widget_num] = self.bind_unbind(btn, callbacks, func, tuple(new_params), "on_release", widget_num)
                            widget["callbacks"][widget_num] = {"params":tuple(new_params), "func":func}

                        widget["current_screen"][widget_num]=current_screen
                        return widget, widget_num

                    elif layout == "floatlayout":
                        top = kwargs["top"]
                        side = kwargs["side"]
                        side_val = kwargs["side_val"]
                        width = kwargs["width"]
                        height = kwargs["height"]
                        btn = widget["widgets"][widget_num]
                        btn.text = text.replace("_"," ")
                        btn.current_text = text.replace("_"," ")
                        btn.pos_hint={"top":top, side:side_val}
                        btn.size_hint=(width, height)

                        if params != None:
                            callbacks = widget["callbacks"]
                            new_params = []
                            for param in range(len(params)):
                                if params[param] == "active_widget":
                                    new_params.append(btn)
                                elif params[param] == "active_widget_text":
                                    new_params.append(btn.text)
                                else:
                                    new_params.append(params[param])

                            widget["widgets"][widget_num] = self.bind_unbind(btn, callbacks, func, tuple(new_params), "on_release", widget_num)
                            widget["callbacks"][widget_num] = {"params":tuple(new_params), "func":func}


                        widget["current_screen"][widget_num]=current_screen
                        return widget, widget_num

                else:
                    parent.remove_widget(widget["widgets"][widget_num])
                    if layout == "gridlayout":
                        btn = widget["widgets"][widget_num]
                        btn.text = text.replace("_"," ")
                        btn.current_text = text.replace("_"," ")

                        if params != None:
                            callbacks = widget["callbacks"]
                            new_params = []
                            for param in range(len(params)):
                                if params[param] == "active_widget":
                                    new_params.append(btn)
                                elif params[param] == "active_widget_text":
                                    new_params.append(btn.text)
                                else:
                                    new_params.append(params[param])

                            widget["widgets"][widget_num] = self.bind_unbind(btn, callbacks, func, tuple(new_params), "on_release", widget_num)
                            widget["callbacks"][widget_num] = {"params":tuple(new_params), "func":func}

                        widget["current_screen"][widget_num]=current_screen
                        widget = [widget, widget_num]
                        return widget

                    elif layout == "floatlayout":
                        top = kwargs["top"]
                        side = kwargs["side"]
                        side_val = kwargs["side_val"]
                        width = kwargs["width"]
                        height = kwargs["height"]
                        btn = widget["widgets"][widget_num]
                        btn.text = text.replace("_"," ")
                        btn.current_text = text.replace("_"," ")
                        btn.pos_hint={"top":top, side:side_val}
                        btn.size_hint=(width, height)

                        if params != None:
                            callbacks = widget["callbacks"]
                            new_params = []
                            for param in range(len(params)):
                                if params[param] == "active_widget":
                                    new_params.append(btn)
                                elif params[param] == "active_widget_text":
                                    new_params.append(btn.text)
                                else:
                                    new_params.append(params[param])

                            widget["widgets"][widget_num] = self.bind_unbind(btn, callbacks, func, tuple(new_params), "on_release", widget_num)
                            widget["callbacks"][widget_num] = {"params":tuple(new_params), "func":func}


                        widget["current_screen"][widget_num]=current_screen
                        return widget, widget_num

			
            else:
                if layout == "gridlayout":
                    temp_btn = self.create_new_widget("dropdownitem")
                    temp_btn.text = text.replace("_"," ")
                    temp_btn.current_text = text.replace("_"," ")

                    if params != None:
                        callbacks = widget["callbacks"]
                        new_params = []
                        for param in range(len(params)):
                            if params[param] == "active_widget":
                                new_params.append(temp_btn)
                            elif params[param] == "active_widget_text":
                                new_params.append(temp_btn.text)
                            else:
                                new_params.append(params[param])

                        widget["widgets"][widget_num] = self.bind_unbind(temp_btn, callbacks, func, tuple(new_params), "on_release", widget_num)
                        widget["callbacks"][widget_num] = {"params":tuple(new_params), "func":func}

                    widget["current_screen"][widget_num]=current_screen
                    widget = [widget, widget_num]
                    return widget

        elif widget_type == "round_flat_button":
            widget_num = kwargs["widget_num"]
            widget = kwargs["widget"]
            layout = kwargs["layout"]
            current_screen = kwargs["current_screen"]
            func = kwargs["func"]
            params = kwargs["params"]
            text = kwargs["text"]

            for id_, v in widget["current_screen"].items():
                if id_ == widget_num:
                    available = False
                    while available == False:
                        try:
                            if widget["current_screen"][widget_num] == current_screen:
                                widget_num = widget_num+1
                            else:
                                available = True
                        except Exception as e:
                            available = True
                else:
                    break

            if widget_num < widget["number"]:
                parent = widget["widgets"][widget_num].parent
                if parent == None:
                    if layout == "floatlayout":
                        top = kwargs["top"]
                        side = kwargs["side"]
                        side_val = kwargs["side_val"]
                        width = kwargs["width"]
                        height = kwargs["height"]
                        btn = widget["widgets"][widget_num]
                        btn.text = text.replace("_"," ")
                        btn.pos_hint={"top":top, side:side_val}
                        btn.size_hint=(width, height)

                        if params != None:
                            callbacks = widget["callbacks"]
                            new_params = []
                            for param in range(len(params)):
                                if params[param] == "active_widget":
                                    new_params.append(btn)
                                elif params[param] == "active_widget_text":
                                    new_params.append(btn.text)
                                else:
                                    new_params.append(params[param])

                            widget["widgets"][widget_num] = self.bind_unbind(btn, callbacks, func, tuple(new_params), "on_press", widget_num)
                            widget["callbacks"][widget_num] = {"params":tuple(new_params), "func":func}

                        widget["current_screen"][widget_num]=current_screen
                        widget = [widget, widget_num]
                        return widget

                elif parent != None:
                    parent.remove_widget(widget["widgets"][widget_num])
                    if layout == "floatlayout":
                        top = kwargs["top"]
                        side = kwargs["side"]
                        side_val = kwargs["side_val"]
                        width = kwargs["width"]
                        height = kwargs["height"]

                        btn = widget["widgets"][widget_num]
                        btn.text = text.replace("_"," ")
                        btn.pos_hint={"top":top, side:side_val}
                        btn.size_hint=(width, height)

                        if params != None:
                            callbacks = widget["callbacks"]
                            new_params = []
                            for param in range(len(params)):
                                if params[param] == "active_widget":
                                    new_params.append(btn)
                                elif params[param] == "active_widget_text":
                                    new_params.append(btn.text)
                                else:
                                    new_params.append(params[param])

                            widget["widgets"][widget_num] = self.bind_unbind(btn, callbacks, func, tuple(new_params), "on_press", widget_num)
                            widget["callbacks"][widget_num] = {"params":tuple(new_params), "func":func}

                        widget["current_screen"][widget_num]=current_screen

                        widget = [widget, widget_num]
                        return widget

            else:
                temp_btn = self.create_new_widget("round_flat_button")

                if layout == "floatLayout":
                    top = kwargs["top"]
                    side = kwargs["side"]
                    side_val = kwargs["side_val"]
                    width = kwargs["width"]
                    height = kwargs["height"]


                    temp_btn.text = text.replace("_"," ")
                    temp_btn.pos_hint={"top":top, side:side_val}
                    temp_btn.size_hint=(width, height)
                    widget["widgets"].append(temp_btn)

                    if params != None:
                        callbacks = widget["callbacks"]
                        new_params = []
                        for param in range(len(params)):
                            if params[param] == "active_widget":
                                new_params.append(btn)
                            elif params[param] == "active_widget_text":
                                new_params.append(btn.text)
                            else:
                                new_params.append(params[param])

                        widget["widgets"][widget_num] = self.bind_unbind(btn, callbacks, func, tuple(new_params), "on_press", widget_num)
                        widget["callbacks"][widget_num] = {"params":tuple(new_params), "func":func}

                    widget["current_screen"][widget_num]=current_screen
                    widget = [widget, widget_num]
                    return widget

        elif widget_type == "icon_button":
            widget_num = kwargs["widget_num"]
            widget = kwargs["widget"]
            layout = kwargs["layout"]
            current_screen = kwargs["current_screen"]
            func = kwargs["func"]
            params = kwargs["params"]
            icon = kwargs["icon"]

            for id_, v in widget["current_screen"].items():
                if id_ == widget_num:
                    available = False
                    while available == False:
                        try:
                            if widget["current_screen"][widget_num] == current_screen:
                                widget_num = widget_num+1
                            else:
                                available = True
                        except Exception as e:
                            available = True
                else:
                    break

            if widget_num < widget["number"]:
                parent = widget["widgets"][widget_num].parent
                if parent == None:
                    if layout == "floatlayout":
                        top = kwargs["top"]
                        side = kwargs["side"]
                        side_val = kwargs["side_val"]
                        width = kwargs["width"]
                        height = kwargs["height"]
                        btn = widget["widgets"][widget_num]
                        btn.icon = icon
                        btn.pos_hint={"top":top, side:side_val}
                        btn.size_hint=(width, height)

                        if params != None:
                            callbacks = widget["callbacks"]
                            new_params = []
                            for param in range(len(params)):
                                if params[param] == "active_widget":
                                    new_params.append(btn)
                                elif params[param] == "active_widget_text":
                                    new_params.append(btn.text)
                                else:
                                    new_params.append(params[param])

                            widget["widgets"][widget_num] = self.bind_unbind(btn, callbacks, func, tuple(new_params), "on_press", widget_num)
                            widget["callbacks"][widget_num] = {"params":tuple(new_params), "func":func}

                        widget["current_screen"][widget_num]=current_screen
                        widget = [widget, widget_num]
                        return widget

                    elif layout == 'gridlayout':
                        widget["widgets"][widget_num].icon = icon
                        widget["widgets"][widget_num].pos_hint={"top":top, side:side_val}
                        widget["widgets"][widget_num].size_hint=(width, height)

                        if params != None:
                            callbacks = widget["callbacks"]
                            new_params = []
                            for param in range(len(params)):
                                if params[param] == "active_widget":
                                    new_params.append(widget["widgets"][widget_num])
                                elif params[param] == "active_widget_icon":
                                    new_params.append(widget["widgets"][widget_num].icon)
                                else:
                                    new_params.append(params[param])

                            widget["widgets"][widget_num] = self.bind_unbind(btn, callbacks, func, tuple(new_params), "on_press", widget_num)
                            widget["callbacks"][widget_num] = {"params":tuple(new_params), "func":func}

                        widget["current_screen"][widget_num]=current_screen
                        widget = [widget, widget_num]
                        return widget

                    elif layout == 'boxlayout':
                        orientation = kwargs['orientation']
                        if orientation == 'horizontal':
                            size_hint_x = kwargs['size_hint_x']

                            widget['widgets'][widget_num].size_hint_x = size_hint_x
                            widget["widgets"][widget_num].icon = icon

                            if params != None:
                                callbacks = widget["callbacks"]
                                new_params = []
                                for param in range(len(params)):
                                    if params[param] == "active_widget":
                                        new_params.append(widget["widgets"][widget_num])
                                    elif params[param] == "active_widget_icon":
                                        new_params.append(widget["widgets"][widget_num].icon)
                                    else:
                                        new_params.append(params[param])

                                widget["widgets"][widget_num] = self.bind_unbind(widget["widgets"][widget_num], callbacks, func, tuple(new_params), "on_press", widget_num)
                                widget["callbacks"][widget_num] = {"params":tuple(new_params), "func":func}

                            widget["current_screen"][widget_num]=current_screen
                            widget = [widget, widget_num]
                            return widget

                        elif orientation == 'vertical':
                            size_hint_y = kwargs['size_hint_y']

                            widget['widgets'][widget_num].size_hint_y = size_hint_y
                            widget["widgets"][widget_num].icon = icon

                            if params != None:
                                callbacks = widget["callbacks"]
                                new_params = []
                                for param in range(len(params)):
                                    if params[param] == "active_widget":
                                        new_params.append(widget["widgets"][widget_num])
                                    elif params[param] == "active_widget_icon":
                                        new_params.append(widget["widgets"][widget_num].icon)
                                    else:
                                        new_params.append(params[param])

                                widget["widgets"][widget_num] = self.bind_unbind(widget["widgets"][widget_num], callbacks, func, tuple(new_params), "on_press", widget_num)
                                widget["callbacks"][widget_num] = {"params":tuple(new_params), "func":func}

                            widget["current_screen"][widget_num]=current_screen
                            widget = [widget, widget_num]
                            return widget

                elif parent != None:
                    parent.remove_widget(widget["widgets"][widget_num])
                    if layout == "floatlayout":
                        top = kwargs["top"]
                        side = kwargs["side"]
                        side_val = kwargs["side_val"]
                        width = kwargs["width"]
                        height = kwargs["height"]

                        btn = widget["widgets"][widget_num]
                        btn.icon = icon.replace("_"," ")
                        btn.pos_hint={"top":top, side:side_val}
                        btn.size_hint=(width, height)

                        if params != None:
                            callbacks = widget["callbacks"]
                            new_params = []
                            for param in range(len(params)):
                                if params[param] == "active_widget":
                                    new_params.append(btn)
                                elif params[param] == "active_widget_text":
                                    new_params.append(btn.text)
                                else:
                                    new_params.append(params[param])

                            widget["widgets"][widget_num] = self.bind_unbind(btn, callbacks, func, tuple(new_params), "on_press", widget_num)
                            widget["callbacks"][widget_num] = {"params":tuple(new_params), "func":func}

                        widget["current_screen"][widget_num]=current_screen

                        widget = [widget, widget_num]
                        return widget

                    elif layout == 'gridlayout':
                        widget["widgets"][widget_num].icon = icon
                        widget["widgets"][widget_num].pos_hint={"top":top, side:side_val}
                        widget["widgets"][widget_num].size_hint=(width, height)

                        if params != None:
                            callbacks = widget["callbacks"]
                            new_params = []
                            for param in range(len(params)):
                                if params[param] == "active_widget":
                                    new_params.append(widget["widgets"][widget_num])
                                elif params[param] == "active_widget_icon":
                                    new_params.append(widget["widgets"][widget_num].icon)
                                else:
                                    new_params.append(params[param])

                            widget["widgets"][widget_num] = self.bind_unbind(btn, callbacks, func, tuple(new_params), "on_press", widget_num)
                            widget["callbacks"][widget_num] = {"params":tuple(new_params), "func":func}

                        widget["current_screen"][widget_num]=current_screen
                        widget = [widget, widget_num]
                        return widget

                    elif layout == 'boxlayout':
                        orientation = kwargs['orientation']
                        if orientation == 'horizontal':
                            size_hint_x = kwargs['size_hint_x']

                            widget['widgets'][widget_num].size_hint_x = size_hint_x
                            widget["widgets"][widget_num].icon = icon

                            if params != None:
                                callbacks = widget["callbacks"]
                                new_params = []
                                for param in range(len(params)):
                                    if params[param] == "active_widget":
                                        new_params.append(widget["widgets"][widget_num])
                                    elif params[param] == "active_widget_icon":
                                        new_params.append(widget["widgets"][widget_num].icon)
                                    else:
                                        new_params.append(params[param])

                                widget["widgets"][widget_num] = self.bind_unbind(widget["widgets"][widget_num], callbacks, func, tuple(new_params), "on_press", widget_num)
                                widget["callbacks"][widget_num] = {"params":tuple(new_params), "func":func}

                            widget["current_screen"][widget_num]=current_screen
                            widget = [widget, widget_num]
                            return widget

                        elif orientation == 'vertical':
                            size_hint_y = kwargs['size_hint_y']

                            widget['widgets'][widget_num].size_hint_y = size_hint_y
                            widget["widgets"][widget_num].icon = icon

                            if params != None:
                                callbacks = widget["callbacks"]
                                new_params = []
                                for param in range(len(params)):
                                    if params[param] == "active_widget":
                                        new_params.append(widget["widgets"][widget_num])
                                    elif params[param] == "active_widget_icon":
                                        new_params.append(widget["widgets"][widget_num].icon)
                                    else:
                                        new_params.append(params[param])

                                widget["widgets"][widget_num] = self.bind_unbind(btn, callbacks, func, tuple(new_params), "on_press", widget_num)
                                widget["callbacks"][widget_num] = {"params":tuple(new_params), "func":func}

                            widget["current_screen"][widget_num]=current_screen
                            widget = [widget, widget_num]
                            return widget

            else:
                temp_btn = self.create_new_widget("icon_button")

                if layout == "floatLayout":
                    top = kwargs["top"]
                    side = kwargs["side"]
                    side_val = kwargs["side_val"]
                    width = kwargs["width"]
                    height = kwargs["height"]


                    temp_btn.text = text.replace("_"," ")
                    temp_btn.pos_hint={"top":top, side:side_val}
                    temp_btn.size_hint=(width, height)
                    widget["widgets"].append(temp_btn)

                    if params != None:
                        callbacks = widget["callbacks"]
                        new_params = []
                        for param in range(len(params)):
                            if params[param] == "active_widget":
                                new_params.append(widget["widgets"][widget_num])
                            elif params[param] == "active_widget_text":
                                new_params.append(widget["widgets"][widget_num].text)
                            else:
                                new_params.append(params[param])

                        widget["widgets"][widget_num] = self.bind_unbind(widget["widgets"][widget_num], callbacks, func, tuple(new_params), "on_press", widget_num)
                        widget["callbacks"][widget_num] = {"params":tuple(new_params), "func":func}

                    widget["current_screen"][widget_num]=current_screen
                    widget = [widget, widget_num]
                    return widget

                elif layout == 'gridlayout':
                    widget["widgets"].append(temp_btn)
                    widget["widgets"][widget_num].icon = icon
                    widget["widgets"][widget_num].pos_hint={"top":top, side:side_val}
                    widget["widgets"][widget_num].size_hint=(width, height)

                    if params != None:
                        callbacks = widget["callbacks"]
                        new_params = []
                        for param in range(len(params)):
                            if params[param] == "active_widget":
                                new_params.append(widget["widgets"][widget_num])
                            elif params[param] == "active_widget_icon":
                                new_params.append(widget["widgets"][widget_num].icon)
                            else:
                                new_params.append(params[param])

                        widget["widgets"][widget_num] = self.bind_unbind(btn, callbacks, func, tuple(new_params), "on_press", widget_num)
                        widget["callbacks"][widget_num] = {"params":tuple(new_params), "func":func}

                    widget["current_screen"][widget_num]=current_screen
                    widget = [widget, widget_num]
                    return widget

                elif layout == 'boxlayout':
                    widget["widgets"].append(temp_btn)
                    orientation = kwargs['orientation']
                    if orientation == 'horizontal':
                        size_hint_x = kwargs['size_hint_x']

                        widget['widgets'][widget_num].size_hint_x = size_hint_x
                        widget["widgets"][widget_num].icon = icon

                        if params != None:
                            callbacks = widget["callbacks"]
                            new_params = []
                            for param in range(len(params)):
                                if params[param] == "active_widget":
                                    new_params.append(widget["widgets"][widget_num])
                                elif params[param] == "active_widget_icon":
                                    new_params.append(widget["widgets"][widget_num].icon)
                                else:
                                    new_params.append(params[param])

                            widget["widgets"][widget_num] = self.bind_unbind(btn, callbacks, func, tuple(new_params), "on_press", widget_num)
                            widget["callbacks"][widget_num] = {"params":tuple(new_params), "func":func}

                        widget["current_screen"][widget_num]=current_screen
                        widget = [widget, widget_num]
                        return widget

                    elif orientation == 'vertical':
                        size_hint_y = kwargs['size_hint_y']

                        widget['widgets'][widget_num].size_hint_y = size_hint_y
                        widget["widgets"][widget_num].icon = icon

                        if params != None:
                            callbacks = widget["callbacks"]
                            new_params = []
                            for param in range(len(params)):
                                if params[param] == "active_widget":
                                    new_params.append(widget["widgets"][widget_num])
                                elif params[param] == "active_widget_icon":
                                    new_params.append(widget["widgets"][widget_num].icon)
                                else:
                                    new_params.append(params[param])

                            widget["widgets"][widget_num] = self.bind_unbind(btn, callbacks, func, tuple(new_params), "on_press", widget_num)
                            widget["callbacks"][widget_num] = {"params":tuple(new_params), "func":func}

                        widget["current_screen"][widget_num]=current_screen
                        widget = [widget, widget_num]
                        return widget

        elif widget_type == 'flat_button':
            widget_num = kwargs["widget_num"]
            widget = kwargs["widget"]
            layout = kwargs["layout"]
            current_screen = kwargs["current_screen"]
            func = kwargs["func"]
            params = kwargs["params"]
            text = kwargs["text"]

            for id_, v in widget["current_screen"].items():
                if id_ == widget_num:
                    available = False
                    while available == False:
                        try:
                            if widget["current_screen"][widget_num] == current_screen:
                                widget_num = widget_num+1
                            else:
                                available = True
                        except Exception as e:
                            available = True
                else:
                    break

            if widget_num < widget["number"]:
                parent = widget["widgets"][widget_num].parent
                if parent == None:
                    if layout == "floatlayout":
                        top = kwargs["top"]
                        side = kwargs["side"]
                        side_val = kwargs["side_val"]
                        width = kwargs["width"]
                        height = kwargs["height"]
                        btn = widget["widgets"][widget_num]
                        widget['widgets'][widget_num].text = text.replace("_"," ")
                        widget['widgets'][widget_num].pos_hint={"top":top, side:side_val}
                        widget['widgets'][widget_num].size_hint=(width, height)

                        if params != None:
                            callbacks = widget["callbacks"]
                            new_params = []
                            for param in range(len(params)):
                                if params[param] == "active_widget":
                                    new_params.append(widget['widgets'][widget_num])
                                elif params[param] == "active_widget_text":
                                    new_params.append(widget['widgets'][widget_num].text)
                                else:
                                    new_params.append(params[param])

                            widget["widgets"][widget_num] = self.bind_unbind(btn, callbacks, func, tuple(new_params), "on_press", widget_num)
                            widget["callbacks"][widget_num] = {"params":tuple(new_params), "func":func}

                        widget["current_screen"][widget_num]=current_screen
                        widget = [widget, widget_num]
                        return widget

                    elif 'gridlayout':
                        btn = widget['widgets'][widget_num]
                        widget['widgets'][widget_num].text = text

                        if params != None:
                            callbacks = widget["callbacks"]
                            new_params = []
                            for param in range(len(params)):
                                if params[param] == "active_widget":
                                    new_params.append(widget['widgets'][widget_num])
                                elif params[param] == "active_widget_text":
                                    new_params.append(widget['widgets'][widget_num].text)
                                else:
                                    new_params.append(params[param])

                            widget["widgets"][widget_num] = self.bind_unbind(widget['widgets'][widget_num], callbacks, func, tuple(new_params), "on_press", widget_num)
                            widget["callbacks"][widget_num] = {"params":tuple(new_params), "func":func}

                        widget["current_screen"][widget_num]=current_screen
                        widget = [widget, widget_num]
                        return widget

                elif parent != None:
                    parent.remove_widget(widget["widgets"][widget_num])
                    if layout == "floatlayout":
                        top = kwargs["top"]
                        side = kwargs["side"]
                        side_val = kwargs["side_val"]
                        width = kwargs["width"]
                        height = kwargs["height"]

                        btn = widget["widgets"][widget_num]
                        widget['widgets'][widget_num].text = text.replace("_"," ")
                        widget['widgets'][widget_num].pos_hint={"top":top, side:side_val}
                        widget['widgets'][widget_num].size_hint=(width, height)

                        if params != None:
                            callbacks = widget["callbacks"]
                            new_params = []
                            for param in range(len(params)):
                                if params[param] == "active_widget":
                                    new_params.append(widget['widgets'][widget_num])
                                elif params[param] == "active_widget_text":
                                    new_params.append(widget['widgets'][widget_num].text)
                                else:
                                    new_params.append(params[param])

                            widget["widgets"][widget_num] = self.bind_unbind(widget['widgets'][widget_num], callbacks, func, tuple(new_params), "on_press", widget_num)
                            widget["callbacks"][widget_num] = {"params":tuple(new_params), "func":func}

                        widget["current_screen"][widget_num]=current_screen

                        widget = [widget, widget_num]
                        return widget

                    elif 'gridlayout':
                        print("Creating one for a gridlayout")
                        btn = widget['widgets'][widget_num]
                        widget['widgets'][widget_num].text = text

                        if params != None:
                            callbacks = widget["callbacks"]
                            new_params = []
                            for param in range(len(params)):
                                if params[param] == "active_widget":
                                    new_params.append(widget['widgets'][widget_num])
                                elif params[param] == "active_widget_text":
                                    new_params.append(widget['widgets'][widget_num].text)
                                else:
                                    new_params.append(params[param])

                            widget["widgets"][widget_num] = self.bind_unbind(widget['widgets'][widget_num], callbacks, func, tuple(new_params), "on_press", widget_num)
                            widget["callbacks"][widget_num] = {"params":tuple(new_params), "func":func}

                        widget["current_screen"][widget_num]=current_screen
                        widget = [widget, widget_num]
                        return widget
            else:
                temp_btn = self.create_new_widget("flat_button")

                if layout == "floatLayout":
                    top = kwargs["top"]
                    side = kwargs["side"]
                    side_val = kwargs["side_val"]
                    width = kwargs["width"]
                    height = kwargs["height"]


                    widget['widgets'][widget_num].text = text.replace("_"," ")
                    widget['widgets'][widget_num].pos_hint={"top":top, side:side_val}
                    widget['widgets'][widget_num].size_hint=(width, height)
                    widget["widgets"].append(temp_btn)

                    if params != None:
                        callbacks = widget["callbacks"]
                        new_params = []
                        for param in range(len(params)):
                            if params[param] == "active_widget":
                                new_params.append(widget['widgets'][widget_num])
                            elif params[param] == "active_widget_text":
                                new_params.append(widget['widgets'][widget_num].text)
                            else:
                                new_params.append(params[param])

                        widget["widgets"][widget_num] = self.bind_unbind(widget['widgets'][widget_num], callbacks, func, tuple(new_params), "on_press", widget_num)
                        widget["callbacks"][widget_num] = {"params":tuple(new_params), "func":func}

                    widget["current_screen"][widget_num]=current_screen
                    widget = [widget, widget_num]
                    return widget

                elif 'gridlayout':
                    print("Creating one for a gridlayout")
                    temp_btn = widget['widgets'][widget_num]
                    widget['widgets'][widget_num].text = text

                    if params != None:
                        callbacks = widget["callbacks"]
                        new_params = []
                        for param in range(len(params)):
                            if params[param] == "active_widget":
                                new_params.append(widget['widgets'][widget_num])
                            elif params[param] == "active_widget_text":
                                new_params.append(widget['widgets'][widget_num].text)
                            else:
                                new_params.append(params[param])

                        widget["widgets"][widget_num] = self.bind_unbind(widget['widgets'][widget_num], callbacks, func, tuple(new_params), "on_press", widget_num)
                        widget["callbacks"][widget_num] = {"params":tuple(new_params), "func":func}

                    widget["current_screen"][widget_num]=current_screen
                    widget = [widget, widget_num]
                    return widget

        elif widget_type == "raised_button":
            widget_num = kwargs["widget_num"]
            widget = kwargs["widget"]
            layout = kwargs["layout"]
            current_screen = kwargs["current_screen"]
            func = kwargs["func"]
            params = kwargs["params"]
            text = kwargs["text"]

            for id_, v in widget["current_screen"].items():
                if id_ == widget_num:
                    available = False
                    while available == False:
                        try:
                            if widget["current_screen"][widget_num] == current_screen:
                                widget_num = widget_num+1
                            else:
                                available = True
                        except Exception as e:
                            available = True
                else:
                    break

            if widget_num < widget["number"]:
                print("Creating raised btn widget")
                parent = widget["widgets"][widget_num].parent
                if parent == None:
                    if layout == "floatlayout":
                        top = kwargs["top"]
                        side = kwargs["side"]
                        side_val = kwargs["side_val"]
                        width = kwargs["width"]
                        height = kwargs["height"]
                        btn = widget["widgets"][widget_num]
                        btn.text = text.replace("_"," ")
                        btn.pos_hint={"top":top, side:side_val}
                        btn.size_hint=(width, height)

                        if params != None:
                            callbacks = widget["callbacks"]
                            new_params = []
                            for param in range(len(params)):
                                if params[param] == "active_widget":
                                    new_params.append(btn)
                                elif params[param] == "active_widget_text":
                                    new_params.append(btn.text)
                                else:
                                    new_params.append(params[param])

                            widget["widgets"][widget_num] = self.bind_unbind(btn, callbacks, func, tuple(new_params), "on_press", widget_num)
                            widget["callbacks"][widget_num] = {"params":tuple(new_params), "func":func}

                        widget["current_screen"][widget_num]=current_screen
                        widget = [widget, widget_num]
                        return widget

                    elif 'gridlayout':
                        print("Creating one for a gridlayout")
                        btn = widget['widgets'][widget_num]
                        btn.text = text

                        if params != None:
                            callbacks = widget["callbacks"]
                            new_params = []
                            for param in range(len(params)):
                                if params[param] == "active_widget":
                                    new_params.append(btn)
                                elif params[param] == "active_widget_text":
                                    new_params.append(btn.text)
                                else:
                                    new_params.append(params[param])

                            widget["widgets"][widget_num] = self.bind_unbind(btn, callbacks, func, tuple(new_params), "on_press", widget_num)
                            widget["callbacks"][widget_num] = {"params":tuple(new_params), "func":func}

                        widget["current_screen"][widget_num]=current_screen
                        widget = [widget, widget_num]
                        return widget

                elif parent != None:
                    parent.remove_widget(widget["widgets"][widget_num])
                    if layout == "floatlayout":
                        top = kwargs["top"]
                        side = kwargs["side"]
                        side_val = kwargs["side_val"]
                        width = kwargs["width"]
                        height = kwargs["height"]

                        btn = widget["widgets"][widget_num]
                        btn.text = text.replace("_"," ")
                        btn.pos_hint={"top":top, side:side_val}
                        btn.size_hint=(width, height)

                        if params != None:
                            callbacks = widget["callbacks"]
                            new_params = []
                            for param in range(len(params)):
                                if params[param] == "active_widget":
                                    new_params.append(btn)
                                elif params[param] == "active_widget_text":
                                    new_params.append(btn.text)
                                else:
                                    new_params.append(params[param])

                            widget["widgets"][widget_num] = self.bind_unbind(btn, callbacks, func, tuple(new_params), "on_press", widget_num)
                            widget["callbacks"][widget_num] = {"params":tuple(new_params), "func":func}

                        widget["current_screen"][widget_num]=current_screen

                        widget = [widget, widget_num]
                        return widget

                    elif 'gridlayout':
                        print("Creating one for a gridlayout")
                        btn = widget['widgets'][widget_num]
                        btn.text = text

                        if params != None:
                            callbacks = widget["callbacks"]
                            new_params = []
                            for param in range(len(params)):
                                if params[param] == "active_widget":
                                    new_params.append(btn)
                                elif params[param] == "active_widget_text":
                                    new_params.append(btn.text)
                                else:
                                    new_params.append(params[param])

                            widget["widgets"][widget_num] = self.bind_unbind(btn, callbacks, func, tuple(new_params), "on_press", widget_num)
                            widget["callbacks"][widget_num] = {"params":tuple(new_params), "func":func}

                        widget["current_screen"][widget_num]=current_screen
                        widget = [widget, widget_num]
                        return widget
            else:
                temp_btn = self.create_new_widget("raised_button")

                if layout == "floatLayout":
                    top = kwargs["top"]
                    side = kwargs["side"]
                    side_val = kwargs["side_val"]
                    width = kwargs["width"]
                    height = kwargs["height"]


                    temp_btn.text = text.replace("_"," ")
                    temp_btn.pos_hint={"top":top, side:side_val}
                    temp_btn.size_hint=(width, height)
                    widget["widgets"].append(temp_btn)

                    if params != None:
                        callbacks = widget["callbacks"]
                        new_params = []
                        for param in range(len(params)):
                            if params[param] == "active_widget":
                                new_params.append(temp_btn)
                            elif params[param] == "active_widget_text":
                                new_params.append(temp_btn.text)
                            else:
                                new_params.append(params[param])

                        widget["widgets"][widget_num] = self.bind_unbind(temp_btn, callbacks, func, tuple(new_params), "on_press", widget_num)
                        widget["callbacks"][widget_num] = {"params":tuple(new_params), "func":func}

                    widget["current_screen"][widget_num]=current_screen
                    widget = [widget, widget_num]
                    return widget

                elif 'gridlayout':
                    print("Creating one for a gridlayout")
                    temp_btn = widget['widgets'][widget_num]
                    temp_btn.text = text

                    if params != None:
                        callbacks = widget["callbacks"]
                        new_params = []
                        for param in range(len(params)):
                            if params[param] == "active_widget":
                                new_params.append(temp_btn)
                            elif params[param] == "active_widget_text":
                                new_params.append(temp_btn.text)
                            else:
                                new_params.append(params[param])

                        widget["widgets"][widget_num] = self.bind_unbind(temp_btn, callbacks, func, tuple(new_params), "on_press", widget_num)
                        widget["callbacks"][widget_num] = {"params":tuple(new_params), "func":func}

                    widget["current_screen"][widget_num]=current_screen
                    widget = [widget, widget_num]
                    return widget

	          
        elif widget_type == "progressbar":
            widget_num = kwargs["widget_num"]
            widget = kwargs["widget"]
            layout = kwargs["layout"]
            current_screen = kwargs["current_screen"]


            for id_, v in widget["current_screen"].items():
                if id_ == widget_num:
                    available = False
                    while available == False:
                        try:
                            if widget["current_screen"][widget_num] == current_screen:
                                widget_num = widget_num+1
                            else:
                                available = True
                        except Exception as e:
                            available = True
                else:
                    break


            if widget_num < widget["number"]:
                parent = widget["widgets"][widget_num].parent
                if parent == None:
                    if layout == 'floatlayout':
                        top = kwargs["top"]
                        side = kwargs["side"]
                        side_val = kwargs["side_val"]
                        width = kwargs["width"]
                        height = kwargs["height"]

                        widget["widgets"][widget_num].pos_hint={"top":top, side:side_val}
                        widget["widgets"][widget_num].size_hint=(width, height)

                        widget["current_screen"][widget_num]=current_screen
                        widget= [widget, widget_num]
                        return widget

                    elif layout == "gridlayout":
                        widget["current_screen"][widget_num]=current_screen
                        widget= [widget, widget_num]
                        return widget

                else:
                    parent.remove_widget(widget["widgets"][widget_num])
                    if layout == "floatlayout":
                        top = kwargs["top"]
                        side = kwargs["side"]
                        side_val = kwargs["side_val"]
                        width = kwargs["width"]
                        height = kwargs["height"]

                        widget["widgets"][widget_num].pos_hint={"top":top, side:side_val}
                        widget["widgets"][widget_num].size_hint=(width, height)

                        widget["current_screen"][widget_num]=current_screen
                        widget= [widget, widget_num]
                        return widget

                    elif layout == "gridlayout":
                        widget["current_screen"][widget_num]=current_screen
                        widget= [widget, widget_num]
                        return widget

            else:
                temp_progressbar = self.create_new_widget("progressbar")
                widget["widgets"].append(temp_progressbar)
                widget["number"] = widget["number"]+1
                if layout == 'floatlayout':
                    top = kwargs["top"]
                    side = kwargs["side"]
                    side_val = kwargs["side_val"]
                    width = kwargs["width"]
                    height = kwargs["height"]

                    widget["widgets"][widget_num].pos_hint={"top":top, side:side_val}
                    widget["widgets"][widget_num].size_hint=(width, height)

                    widget["current_screen"][widget_num]=current_screen
                    widget= [widget, widget_num]
                    return widget

                elif layout == "gridlayout":
                    widget["current_screen"][widget_num]=current_screen
                    widget= [widget, widget_num]
                    return widget

        # TWOLINELIST
        elif widget_type == "twolinelist":
            widget_num = kwargs["widget_num"]
            widget = kwargs["widget"]
            layout = kwargs["layout"]
            current_screen = kwargs["current_screen"]
            text = kwargs["text"]
            secondary_text = kwargs["secondary_text"]
            func = kwargs["func"]
            params = kwargs["params"]

            for id_, v in widget["current_screen"].items():
                if id_ == widget_num:
                    available = False
                    while available == False:
                        try:
                            if widget["current_screen"][widget_num] == current_screen:
                                widget_num = widget_num+1
                            else:
                                available = True
                        except Exception as e:
                            available = True
                else:
                    break

            if widget_num < widget["number"]:
                parent = widget["widgets"][widget_num].parent
                if parent == None:
                    if layout == "floatlayout":
                        top = kwargs["top"]
                        side = kwargs["side"]
                        side_val = kwargs["side_val"]
                        width = kwargs["width"]
                        height = kwargs["height"]
                        btn = widget["widgets"][widget_num]
                        widget["widgets"][widget_num].text = text.replace("_"," ")
                        widget["widgets"][widget_num].secondary_text = secondary_text.replace("_"," ")
                        widget["widgets"][widget_num].pos_hint={"top":top, side:side_val}
                        widget["widgets"][widget_num].size_hint=(width, height)

                        if params != None:
                            callbacks = widget["callbacks"]
                            new_params = []
                            for param in range(len(params)):
                                if params[param] == "active_widget":
                                    new_params.append(widget["widgets"][widget_num])
                                elif param == "active_widget_text":
                                    params[param].append(widget["widgets"][widget_num].text)
                                else:
                                    new_params.append(params[param])

                            widget["widgets"][widget_num] = self.bind_unbind(widget["widgets"][widget_num], callbacks, func, tuple(new_params), "on_press", widget_num)
                            widget["callbacks"][widget_num] = {"params":tuple(new_params), "func":func}

                        widget["current_screen"][widget_num]=current_screen
                        widget = [widget, widget_num]
                        return widget

                    elif layout == "gridlayout":
                        btn = widget["widgets"][widget_num]
                        widget["widgets"][widget_num].text = text.replace("_"," ")
                        widget["widgets"][widget_num].secondary_text = secondary_text.replace("_"," ")

                        if params != None:
                            callbacks = widget["callbacks"]
                            new_params = []
                            for param in range(len(params)):
                                if params[param] == "active_widget":
                                    new_params.append(widget["widgets"][widget_num])
                                elif params[param] == "active_widget_text":
                                    new_params.append(widget["widgets"][widget_num].text)
                                else:
                                    new_params.append(params[param])

                            widget["widgets"][widget_num] = self.bind_unbind(widget["widgets"][widget_num], callbacks, func, tuple(new_params), "on_press", widget_num)
                            widget["callbacks"][widget_num] = {"params":tuple(new_params), "func":func}

                        widget["current_screen"][widget_num]=current_screen

                        widget = [widget, widget_num]
                        return widget

                    elif layout == 'boxlayout':
                        orientation = kwargs['orientation']
                        if orientation == 'horizontal':
                            size_hint_x = kwargs['size_hint_x']

                            widget["widgets"][widget_num].text = text.replace("_"," ")
                            widget["widgets"][widget_num].size_hint_x = size_hint_x
                            widget["widgets"][widget_num].secondary_text = secondary_text.replace("_"," ")

                            if params != None:
                                callbacks = widget["callbacks"]
                                new_params = []
                                for param in range(len(params)):
                                    if params[param] == "active_widget":
                                        new_params.append(widget["widgets"][widget_num])
                                    elif params[param] == "active_widget_text":
                                        new_params.append(widget["widgets"][widget_num].text)
                                    else:
                                        new_params.append(params[param])

                                widget["widgets"][widget_num] = self.bind_unbind(widget["widgets"][widget_num], callbacks, func, tuple(new_params), "on_press", widget_num)
                                widget["callbacks"][widget_num] = {"params":tuple(new_params), "func":func}

                            widget["current_screen"][widget_num]=current_screen
                            widget = [widget, widget_num]
                            return widget

                        elif orientation == 'vertical':
                            size_hint_y = kwargs['size_hint_y']

                            widget["widgets"][widget_num].text = text.replace("_"," ")
                            widget["widgets"][widget_num].size_hint_y = size_hint_y
                            widget["widgets"][widget_num].secondary_text = secondary_text.replace("_"," ")

                            if params != None:
                                callbacks = widget["callbacks"]
                                new_params = []
                                for param in range(len(params)):
                                    if params[param] == "active_widget":
                                        new_params.append(widget["widgets"][widget_num])
                                    elif params[param] == "active_widget_text":
                                        new_params.append(widget["widgets"][widget_num].text)
                                    else:
                                        new_params.append(params[param])

                                widget["widgets"][widget_num] = self.bind_unbind(widget["widgets"][widget_num], callbacks, func, tuple(new_params), "on_press", widget_num)
                                widget["callbacks"][widget_num] = {"params":tuple(new_params), "func":func}

                            widget["current_screen"][widget_num]=current_screen

                            widget = [widget, widget_num]
                            return widget

                else:
                    parent.remove_widget(widget["widgets"][widget_num])
                    if layout == "floatlayout":
                        top = kwargs["top"]
                        side = kwargs["side"]
                        side_val = kwargs["side_val"]
                        width = kwargs["width"]
                        height = kwargs["height"]
                        btn = widget["widgets"][widget_num]
                        btn.text = text.replace("_"," ")
                        btn.secondary_text = secondary_text.replace("_"," ")
                        btn.pos_hint={"top":top, side:side_val}
                        btn.size_hint=(width, height)

                        if params != None:
                            callbacks = widget["callbacks"]
                            new_params = []
                            for param in range(len(params)):
                                if params[param] == "active_widget":
                                    new_params.append(btn)
                                elif params[param] == "active_widget_text":
                                    new_params.append(btn.text)
                                else:
                                    new_params.append(params[param])

                            widget["widgets"][widget_num] = self.bind_unbind(btn, callbacks, func, tuple(new_params), "on_press", widget_num)
                            widget["callbacks"][widget_num] = {"params":tuple(new_params), "func":func}

                        widget["current_screen"][widget_num]=current_screen
                        widget = [widget, widget_num]
                        return widget

                    elif layout == "gridlayout":
                        btn = widget["widgets"][widget_num]
                        widget["widgets"][widget_num].text = text.replace("_"," ")
                        widget["widgets"][widget_num].secondary_text = secondary_text.replace("_"," ")

                        if params != None:
                            callbacks = widget["callbacks"]
                            new_params = []
                            for param in range(len(params)):
                                if params[param] == "active_widget":
                                    new_params.append(widget["widgets"][widget_num])
                                elif params[param] == "active_widget_text":
                                    new_params.append(widget["widgets"][widget_num].text)
                                else:
                                    new_params.append(params[param])

                            widget["widgets"][widget_num] = self.bind_unbind(widget["widgets"][widget_num], callbacks, func, tuple(new_params), "on_press", widget_num)
                            widget["callbacks"][widget_num] = {"params":tuple(new_params), "func":func}

                        widget["current_screen"][widget_num]=current_screen
                        widget = [widget, widget_num]
                        return widget

                    elif layout == 'boxlayout':
                        orientation = kwargs['orientation']
                        if orientation == 'horizontal':
                            size_hint_x = kwargs['size_hint_x']

                            widget["widgets"][widget_num].text = text.replace("_"," ")
                            widget["widgets"][widget_num].size_hint_x = size_hint_x
                            widget["widgets"][widget_num].secondary_text = secondary_text.replace("_"," ")

                            if params != None:
                                callbacks = widget["callbacks"]
                                new_params = []
                                for param in range(len(params)):
                                    if params[param] == "active_widget":
                                        new_params.append(widget["widgets"][widget_num])
                                    elif params[param] == "active_widget_text":
                                        new_params.append(widget["widgets"][widget_num].text)
                                    else:
                                        new_params.append(params[param])

                                widget["widgets"][widget_num] = self.bind_unbind(widget["widgets"][widget_num], callbacks, func, tuple(new_params), "on_press", widget_num)
                                widget["callbacks"][widget_num] = {"params":tuple(new_params), "func":func}

                            widget["current_screen"][widget_num]=current_screen

                            widget = [widget, widget_num]
                            
                        elif orientation == 'vertical':
                            size_hint_y = kwargs['size_hint_y']

                            widget["widgets"][widget_num].text = text.replace("_"," ")
                            widget["widgets"][widget_num].size_hint_y = size_hint_y
                            widget["widgets"][widget_num].secondary_text = secondary_text.replace("_"," ")

                            if params != None:
                                callbacks = widget["callbacks"]
                                new_params = []
                                for param in range(len(params)):
                                    if params[param] == "active_widget":
                                        new_params.append(widget["widgets"][widget_num])
                                    elif params[param] == "active_widget_text":
                                        new_params.append(widget["widgets"][widget_num].text)
                                    else:
                                        new_params.append(params[param])

                                widget["widgets"][widget_num] = self.bind_unbind(widget["widgets"][widget_num], callbacks, func, tuple(new_params), "on_press", widget_num)
                                widget["callbacks"][widget_num] = {"params":tuple(new_params), "func":func}

                            widget["current_screen"][widget_num]=current_screen

                            widget = [widget, widget_num]
                            return widget
                        
            else:
                number = 3
                temp_twolinelist = self.create_new_widget("twolinelist", number=number)
                for x in temp_twolinelist:
                    widget["widgets"].append(x)
                    
                widget["number"] = widget["number"]+1
                widget_num = widget["number"]
                if layout == 'floatlayout':
                    top = kwargs["top"]
                    side = kwargs["side"]
                    side_val = kwargs["side_val"]
                    width = kwargs["width"]
                    height = kwargs["height"]
                    widget["widgets"][widget_num].text = text.replace("_"," ")
                    widget["widgets"][widget_num].secondary_text = secondary_text.replace("_"," ")
                    widget["widgets"][widget_num].pos_hint={"top":top, side:side_val}
                    widget["widgets"][widget_num].size_hint=(width, height)

                    if params != None:
                        callbacks = widget["callbacks"]
                        new_params = []

                        for param in range(len(params)):
                            if params[param] == "active_widget":
                                new_params.append(btn)
                            elif params[param] == "active_widget_text":
                                new_params.append(btn.text)
                            else:
                                new_params.append(params[param])

                        widget["widgets"][widget_num] = self.bind_unbind(btn, callbacks, func, tuple(new_params), "on_press", widget_num)
                        widget["callbacks"][widget_num] = {"params":tuple(new_params), "func":func}

                    widget["current_screen"][widget_num]=current_screen
                    widget= [widget, widget_num]
                    return widget

                elif layout == "gridlayout":
                    widget["widgets"][widget_num].text = text.replace("_"," ")
                    widget["widgets"][widget_num].secondary_text = secondary_text.replace("_"," ")

                    if params != None:
                        callbacks = widget["callbacks"]
                        new_params = []

                        for param in range(len(params)):
                            if params[param] == "active_widget":
                                new_params.append(widget["widgets"][widget_num])
                            elif params[param] == "active_widget_text":
                                new_params.append(widget["widgets"][widget_num].text)
                            else:
                                new_params.append(params[param])

                        widget["widgets"][widget_num] = self.bind_unbind(widget["widgets"][widget_num], callbacks, func, tuple(new_params), "on_press", widget_num)
                        widget["callbacks"][widget_num] = {"params":tuple(new_params), "func":func}


                    widget["current_screen"][widget_num]=current_screen
                    widget= [widget, widget_num]
                    return widget

                elif layout == 'boxlayout':
                    orientation = kwargs['orientation']
                    if orientation == 'horizontal':
                        size_hint_x = kwargs['size_hint_x']

                        widget["widgets"][widget_num].text = text.replace("_"," ")
                        widget["widgets"][widget_num].size_hint_x = size_hint_x
                        widget["widgets"][widget_num].secondary_text = secondary_text.replace("_"," ")

                        if params != None:
                            callbacks = widget["callbacks"]
                            new_params = []
                            for param in range(len(params)):
                                if params[param] == "active_widget":
                                    new_params.append(widget["widgets"][widget_num])
                                elif params[param] == "active_widget_text":
                                    new_params.append(widget["widgets"][widget_num].text)
                                else:
                                    new_params.append(params[param])

                            widget["widgets"][widget_num] = self.bind_unbind(widget["widgets"][widget_num], callbacks, func, tuple(new_params), "on_press", widget_num)
                            widget["callbacks"][widget_num] = {"params":tuple(new_params), "func":func}

                        widget["current_screen"][widget_num]=current_screen

                        widget = [widget, widget_num]
                        
                    elif orientation == 'vertical':
                        size_hint_y = kwargs['size_hint_y']

                        widget["widgets"][widget_num].text = text.replace("_"," ")
                        widget["widgets"][widget_num].size_hint_y = size_hint_y
                        widget["widgets"][widget_num].secondary_text = secondary_text.replace("_"," ")

                        if params != None:
                            callbacks = widget["callbacks"]
                            new_params = []
                            for param in range(len(params)):
                                if params[param] == "active_widget":
                                    new_params.append(widget["widgets"][widget_num])
                                elif params[param] == "active_widget_text":
                                    new_params.append(widget["widgets"][widget_num].text)
                                else:
                                    new_params.append(params[param])

                            widget["widgets"][widget_num] = self.bind_unbind(widget["widgets"][widget_num], callbacks, func, tuple(new_params), "on_press", widget_num)
                            widget["callbacks"][widget_num] = {"params":tuple(new_params), "func":func}

                        widget["current_screen"][widget_num]=current_screen

                        widget = [widget, widget_num]
                        return widget


        # EXPANSION PANELS
        elif widget_type == "expansionpanel":
            widget_num = kwargs["widget_num"] 
            last_num = kwargs["last_num"]
            widget = kwargs["widget"]
            current_screen = kwargs["current_screen"] 
            icon = kwargs["icon"]
            panel_cls_text = kwargs["text"]
            content = kwargs["content"]
            
            for id_, v in widget["current_screen"].items():
                if id_ == widget_num:
                    available = False
                    while available == False:
                        try:
                            if widget["current_screen"][widget_num] == current_screen:
                                widget_num = widget_num+ 1
                            elif last_num == widget_num:
                                widget_num = widget_num+ 1
                            else:
                                available = True
                                break

                        except Exception as e:
                            print(f"Current screen c'mon: {str(e)}")
                            available = True
                    
                    break
                else:
                    break
            
            last_num = widget_num
            if widget_num < widget["number"]:
                parent = widget["widgets"][widget_num].parent
                if parent == None:
                    widget["widgets"][widget_num].icon = icon
                    widget["widgets"][widget_num].panel_cls.text = panel_cls_text
                    widget["widgets"][widget_num].content = content
                    widget["current_screen"][widget_num] = current_screen
                    widget = [widget, widget_num, last_num]
                    return widget

                else:
                    parent.remove_widget(widget["widgets"][widget_num])

                    widget["widgets"][widget_num].icon = icon
                    widget["widgets"][widget_num].panel_cls.text = panel_cls_text
                    widget["widgets"][widget_num].content = content
                    widget["current_screen"][widget_num] = current_screen
                    widget = [widget, widget_num, last_num]
                    return widget

            else:
                temp_expansionpanel = self.create_new_widget("expansionpanel")
                widget["widgets"].append(temp_expansionpanel)
                widget["number"] = widget["number"]+1
                widget_num = widget["number"]

                widget["widgets"][widget_num].icon = icon
                widget["widgets"][widget_num].panel_cls.text = panel_cls_text
                widget["widgets"][widget_num].content = content
                widget["current_screen"][widget_num] = current_screen
                widget = [widget, widget_num, last_num]
                return widget

        elif widget_type == "expansiononeline":
            widget_num=kwargs["widget_num"] 
            last_num = kwargs["last_num"]
            widget=kwargs["widget"]
            current_screen=kwargs["current_screen"] 
            text=kwargs["text"]

            for id_, v in widget["current_screen"].items():				
                if id_ == widget_num:
                    available = False
                    while available == False:
                        try:
                            if widget["current_screen"][widget_num] == current_screen:
                                widget_num =+ 1

                            elif last_num == widget_num:
                                widget_num =+ 1

                            else:
                                available = True
                                break

                        except Exception as e:
                            print(f"De hell current screen: {str(e)}!!")
                            available = True

                    break

                else:
                    break

            last_num = widget_num
            if widget_num < widget["number"]:
                parent = widget["widgets"][widget_num].parent
                if parent == None:
                    widget["widgets"][widget_num].text = text
                    widget["current_screen"][widget_num] = current_screen
                    widget = [widget, widget_num, last_num]
                    return widget

                else:
                    #parent.remove_widget(widget["number"][widget_num])
                    widget["widgets"][widget_num].text = text
                    widget["current_screen"][widget_num] = current_screen
                    widget = [widget, widget_num, last_num]
                    return widget
            else:
                temp_expansiononeline = self.create_new_widget("expansiononeline")
                widget["widgets"].append(temp_expansiononeline)
                widget["number"] = widget["number"]+1
                widget_num = widget["number"]

                widget["widgets"][widget_num].text = text
                widget["current_screen"][widget_num] = current_screen
                widget = [widget, widget_num, last_num]
                return widget


        elif widget_type == 'card':
            widget_num=kwargs["widget_num"] 
            widget=kwargs["widget"]
            current_screen=kwargs["current_screen"]
            orientation = kwargs['orientation']
            layout = kwargs['layout']

            for id_, v in widget["current_screen"].items():             
                if id_ == widget_num:
                    available = False
                    while available == False:
                        try:
                            if widget["current_screen"][widget_num] == current_screen:
                                widget_num = widget_num + 1
                            else:
                                available = True
                                break

                        except Exception as e:
                            print(f"De hell current screen: {str(e)}!!")
                            available = True

                    break

                else:
                    break


            if widget_num < widget["number"]:
                widget["widgets"][widget_num].clear_widgets()
                parent = widget["widgets"][widget_num].parent
                if parent == None:
                    if layout == 'gridlayout':
                        widget["widgets"][widget_num].orientation = orientation
                        widget["current_screen"][widget_num] = current_screen
                        widget = [widget, widget_num]
                        return widget
                    elif layout == 'floatlayout':
                        top = kwargs["top"]
                        side = kwargs["side"]
                        side_val = kwargs["side_val"]
                        width = kwargs["width"]
                        height = kwargs["height"]
                        widget["widgets"][widget_num].pos_hint={"top":top, side:side_val}
                        widget["widgets"][widget_num].size_hint=(width, height)
                        widget["widgets"][widget_num].orientation = orientation

                        widget["current_screen"][widget_num]=current_screen
                        widget= [widget, widget_num]
                        return widget
                else:
                    parent.remove_widget(widget["widgets"][widget_num])
                    if layout == 'gridlayout':
                        widget["widgets"][widget_num].orientation = orientation
                        widget["current_screen"][widget_num] = current_screen
                        widget = [widget, widget_num]
                        return widget

                    elif layout == 'floatlayout':
                        top = kwargs["top"]
                        side = kwargs["side"]
                        side_val = kwargs["side_val"]
                        width = kwargs["width"]
                        height = kwargs["height"]
                        widget["widgets"][widget_num].pos_hint={"top":top, side:side_val}
                        widget["widgets"][widget_num].size_hint=(width, height)
                        widget["widgets"][widget_num].orientation = orientation

                        widget["current_screen"][widget_num]=current_screen
                        widget= [widget, widget_num]
                        return widget
            else:
                if layout == 'gridlayout':
                    temp_card = self.create_new_widget("card")
                    widget["widgets"].append(temp_card)
                    widget["number"] = widget["number"]+1
                    widget_num = widget["number"]

                    widget["widgets"][widget_num].orientation = orientation
                    widget["current_screen"][widget_num] = current_screen
                    widget = [widget, widget_num]
                    return widget

                elif layout == 'floatlayout':
                    temp_card = self.create_new_widget("card")
                    widget["widgets"].append(temp_card)
                    widget["number"] = widget["number"]+1
                    widget_num = widget["number"]

                    top = kwargs["top"]
                    side = kwargs["side"]
                    side_val = kwargs["side_val"]
                    width = kwargs["width"]
                    height = kwargs["height"]
                    widget["widgets"][widget_num].pos_hint={"top":top, side:side_val}
                    widget["widgets"][widget_num].size_hint=(width, height)
                    widget["widgets"][widget_num].orientation = orientation

                    widget["current_screen"][widget_num]=current_screen
                    widget= [widget, widget_num]
                    return widget
