"""kivy libraries"""
import kivy
kivy.require("1.8.0")
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.base import runTouchApp
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.vkeyboard import VKeyboard
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.image import Image
from kivy.uix.scatter import Scatter
from kivy.clock import Clock
from functools import partial
from kivy.config import Config
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy import require

"""Raspberry pi serial port uses serial class"""
#import serial

"""Other python libraries"""
import numpy as np
import math
import time, timeit

# Builder, here we can add .kv code instead of building another file 
Builder.load_string('''
<MainScreen>:
    center_label: center_label
    box_label: box_label
    mode_spinner: mode_spinner
    title_label: title_label
    option_label: option_label
    FloatLayout:
        canvas:
            Color:
                rgba: 1,1,1,1
            Rectangle:
                pos: (1,170)
                size: (900,380)
        BoxLayout:
            orientation: "vertical"
            padding: "5sp"
            spacing: "5sp"
            Label:
                id: title_label
                #canvas:
                #    Color:
                #        rgba: 0, 0, 1, 0.3
                #    Rectangle:
                #        pos: self.pos
                #        size: self.size
                size_hint_y: 0.1
                font_size: '25sp'
                markup: True
            Widget:
                size_hint_y: 0.1 
            Label:
                id: box_label
                size_hint_y: 0.05
                font_size: '25sp'
                markup: True
                halign: "center"
            Label:
                id: center_label
                font_size: '25sp'
                markup: True
                size_hint_y: 0.4
            BoxLayout:
                orientation: "horizontal"
                size_hint_y: 0.3
                padding: "5sp"
                Widget:
                    size_hint_x: 0.2
                Label:
                    id: option_label
                    font_size: '25sp'
                    markup: True
                Spinner:
                    id: mode_spinner
                    font_size: '25sp'
                    background_normal: "colors/blue.png"
                    background_down: "colors/blue.png"
                    size_hint_y: 0.8
                    values: "Remove Database", "Report Database", "Find Patient", "Enroll New Patient"
                Widget:
                    size_hint_x: 0.2
            Widget:
                size_hint_y: 0.1
            BoxLayout:
                size_hint_y: 0.2
                padding: "5sp"
                spacing: "5sp"
                Button:
                    markup: True
                    font_size: '25sp'
                    background_normal: "colors/orange.png"
                    text: "[b][color=#ffffff]Close Doors[/color][/b]"
                    on_release: root.close_doors()
                Button:
                    markup: True
                    font_size: '25sp'
                    background_normal: "colors/orange.png"
                    text: "[b][color=#ffffff]Open Doors[/color][/b]"
                    on_release: root.open_doors()
            BoxLayout:
                padding: "5sp"
                spacing: "5sp"
                orientation: "horizontal"
                size_hint_y: 0.2
                Button:
                    markup: True
                    font_size: '25sp'
                    background_normal: "colors/red.png"
                    text: "[b][color=#ffffff]Exit[/color][/b]"
                    on_release: root.stop()
                Button:
                    markup: True
                    font_size: '25sp'
                    background_normal: "colors/green_bright.png"
                    text: "[b][color=#ffffff]Continue[/color][/b]"
                    on_release: root.next()
<addScreen>:
    year_spinner: year_spinner
    month_spinner: month_spinner
    day_spinner: day_spinner
    age_spinner: age_spinner
    age_label: age_label
    name_label: name_label
    name_textinput: name_textinput
    birth_label: birth_label
    birthdate_label: birthdate_label
    male: male
    female: female
    FloatLayout:
        canvas:
            Color:
                rgba: 1,1,1,1
            Rectangle:
                pos: (1,90)
                size: (900,570)
        padding: "5sp"
        spacing: "5sp"
        Label:
            id: name_label
            text: "Name:"
            markup: True
            size_hint_y: 0.1
            pos: (1,550)
            font_size: "25sp"
        TextInput:
            id: name_textinput
            text: ""
            pos: (1,500)
            size_hint_y: 0.1
            font_size: "25sp"
        Label:
            id: birth_label
            text: "Birthdate or age: "
            pos: (1,450)
            font_size: "25sp"
            markup: True
            size_hint_y: 0.1
        Label:
            id: birthdate_label
            text: "Birthdate: "
            pos: (1,415)
            markup: True
            font_size: "25sp"
            size_hint_y: 0.1
        Spinner:
            id: day_spinner
            pos: (250,360)
            font_size: '25sp'
            background_normal: "colors/blue.png"
            background_down: "colors/blue.png"
            size_hint_y: 0.1
            size_hint_x: 0.09
        Spinner:
            id: month_spinner
            font_size: '25sp'
            pos: (340,360)
            background_normal: "colors/blue.png"
            background_down: "colors/blue.png"
            size_hint_y: 0.1
            size_hint_x: 0.15
        Spinner:
            id: year_spinner
            font_size: '25sp'
            pos: (480,360)
            background_normal: "colors/blue.png"
            background_down: "colors/blue.png"
            size_hint_y: 0.1
            size_hint_x: 0.1
        Label:
            id: age_label
            markup: True
            text: "Age: "
            pos: (1,300)
            font_size: "25sp"
            size_hint_y: 0.1
        Spinner:
            id: age_spinner
            font_size: '25sp'
            pos: (340,250)
            background_normal: "colors/blue.png"
            background_down: "colors/blue.png"
            size_hint_y: 0.1
            size_hint_x: 0.15
        ToggleButton:
            id: male
            pos: (1,170)
            text:'[b][color=#000000]Male[/color][/b]'
            markup: True
            group: 'sex'
            state: 'normal'
            background_down: "colors/green.png"
            background_normal: "colors/white.png"
            font_size: '25sp'
            size_hint_y: 0.1
        ToggleButton:
            id: female
            pos: (1,100)
            text: '[b][color=#000000]Female[/color][/b]'
            markup:True
            group: 'sex'
            state: 'normal'
            background_down:"colors/green.png"
            background_normal: "colors/white.png"
            font_size: '25sp'
            size_hint_y: 0.1
        BoxLayout:
            id: kbContainer
            size_hint_y: 0.3
            orientation: "horizontal"
            padding: 10
            spacing: 10
            Button:
                background_normal: "colors/red.png"
                text: "[b][color=#ffffff]Discard[/color][/b]"
                size_hint_y: 0.45
                markup: True
                font_size: '25sp'
                on_release: root.discard()
            Button:
                background_normal: "colors/green_bright.png"
                text: "[b][color=#ffffff]Next[/color][/b]"
                size_hint_y: 0.45
                markup: True
                font_size: '25sp'
                on_release: root.save()
<omrScreen>:
    kbContainer: kbContainer   
    mode_spinner: mode_spinner     
    BoxLayout:
        canvas:
            Color:
                rgba: 1,1,1,1
            Rectangle:
                pos: (1,90)
                size: (900,570)
        id: kbContainer
        orientation: 'vertical'
        BoxLayout:
            id: kbContainer
            size_hint_y: 0.9
            orientation: "vertical"
            padding: 10
        Spinner:
            background_normal: "colors/blue.png"
            background_down: "colors/blue.png"
            id: mode_spinner
            font_size: "25sp"
            size_hint_y: 0.1
        BoxLayout:
            size_hint_y: 0.3
            orientation: "horizontal"
            padding: 10
            spacing: 10
            Button:
                background_normal: "colors/red.png"
                text: "[b][color=#ffffff]Discard[/color][/b]"
                font_size: '25sp'
                markup: True
                size_hint_y: 0.60
                on_release: root.discard()
            Button:
                background_normal: "colors/green_bright.png"
                text: "[b][color=#ffffff]Next[/color][/b]"
                font_size: '25sp'
                markup: True
                size_hint_y: 0.60
                on_release: root.save()
<add2Screen>:
    kbContainer: kbContainer        
    BoxLayout:
        canvas:
            Color:
                rgba: 1,1,1,1
            Rectangle:
                pos: (1,90)
                size: (900,570)
        orientation: 'vertical'
        BoxLayout:
            id: kbContainer
            size_hint_y: 1.30
            orientation: "vertical"
            padding: 10
        BoxLayout:
            size_hint_y: 0.3
            orientation: "horizontal"
            padding: 10
            spacing: 10
            Button:
                background_normal: "colors/red.png"
                text: "[b][color=#ffffff]Discard[/color][/b]"
                font_size: '25sp'
                markup: True
                size_hint_y: 0.75
                on_release: root.discard()
            Button:
                background_normal: "colors/green_bright.png"
                text: "[b][color=#ffffff]Next[/color][/b]"
                font_size: '25sp'
                markup: True
                size_hint_y: 0.75
                on_release: root.save()
<add3Screen>:
    kbContainer: kbContainer        
    BoxLayout:
        canvas:
            Color:
                rgba: 1,1,1,1
            Rectangle:
                pos: (1,90)
                size: (900,570)
        orientation: 'vertical'
        BoxLayout:
            id: kbContainer
            size_hint_y: 1.30
            orientation: "vertical"
            padding: 10
        BoxLayout:
            size_hint_y: 0.3
            orientation: "horizontal"
            padding: 10
            spacing: 10
            Button:
                background_normal: "colors/red.png"
                text: "[b][color=#ffffff]Discard[/color][/b]"
                font_size: '25sp'
                markup: True
                size_hint_y: 0.75
                on_release: root.discard()
            Button:
                background_normal: "colors/green_bright.png"
                text: "[b][color=#ffffff]Next[/color][/b]"
                font_size: '25sp'
                markup: True
                size_hint_y: 0.75
                on_release: root.save()
<add4Screen>:
    kbContainer: kbContainer        
    BoxLayout:
        canvas:
            Color:
                rgba: 1,1,1,1
            Rectangle:
                pos: (1,90)
                size: (900,570)
        orientation: 'vertical'
        BoxLayout:
            id: kbContainer
            size_hint_y: 1.30
            orientation: "vertical"
            padding: 10
        BoxLayout:
            size_hint_y: 0.3
            orientation: "horizontal"
            padding: 10
            spacing: 10
            Button:
                background_normal: "colors/red.png"
                text: "[b][color=#ffffff]Discard[/color][/b]"
                font_size: '25sp'
                markup: True
                size_hint_y: 0.75
                on_release: root.discard()
            Button:
                background_normal: "colors/green_bright.png"
                text: "[b][color=#ffffff]Next[/color][/b]"
                font_size: '25sp'
                markup: True
                size_hint_y: 0.75
                on_release: root.save()
<add5Screen>:
    kbContainer: kbContainer        
    BoxLayout:
        canvas:
            Color:
                rgba: 1,1,1,1
            Rectangle:
                pos: (1,90)
                size: (900,570)
        orientation: 'vertical'
        BoxLayout:
            id: kbContainer
            size_hint_y: 1.30
            orientation: "vertical"
            padding: 10
        BoxLayout:
            size_hint_y: 0.3
            orientation: "horizontal"
            padding: 10
            spacing: 10
            Button:
                background_normal: "colors/red.png"
                text: "[b][color=#ffffff]Discard[/color][/b]"
                font_size: '25sp'
                markup: True
                size_hint_y: 0.75
                on_release: root.discard()
            Button:
                background_normal: "colors/green_bright.png"
                text: "[b][color=#ffffff]Save Patient[/color][/b]"
                font_size: '25sp'
                markup: True
                size_hint_y: 0.75
                on_release: root.save()
<resultScreen>:
    displayLabel: displayLabel
    kbContainer: kbContainer
    displayButton: displayButton
    BoxLayout:
        canvas:
            Color:
                rgba: 1,1,1,1
            Rectangle:
                pos: (1,200)
                size: (900,350)
        orientation: 'vertical'
        BoxLayout:
            id: kbContainer
            size_hint_y: 0.2
            orientation: "horizontal"
            padding: 10
        Label:  
            id: displayLabel
            size_hint_y: 0.15
            markup: True
            font_size: '25sp'
            text: ""
            halign: "center"
        Button:
            id: displayButton
            background_normal: "colors/green_bright.png"
            text: "[b][color=#ffffff]Proceed[/color][/b]"
            size_hint_y: 0.2
            font_size: '25sp'
            markup: True
            on_release: root.proceed()    
        Widget:
            # Just a space taker to allow for the popup keyboard
            size_hint_y: 0.5
<takesputumsampleScreen>:
    kbContainer: kbContainer
    BoxLayout:
        canvas:
            Color:
                rgba: 1,1,1,1
            Rectangle:
                pos: (1,115)
                size: (900,550)
        orientation: 'vertical'
        BoxLayout:
            id: kbContainer
            size_hint_y: 0.99
            orientation: "horizontal"
            padding: 10
        Button:
            background_normal: "colors/green_bright.png"
            text: "[b][color=#ffffff]Next[/color][/b]"
            size_hint_y: 0.2
            markup: True
            halign: "center"
            font_size: '25sp'
            on_release: root.next()  
<takesputumsample1Screen>:
    kbContainer: kbContainer
    BoxLayout:
        canvas:
            Color:
                rgba: 1,1,1,1
            Rectangle:
                pos: self.pos
                size: self.size
        orientation: 'vertical'
        Widget:
            size_hint_y: 0.1
        BoxLayout:
            id: kbContainer
            size_hint_y: 0.99
            orientation: "vertical"
            padding: 10
            spacing: 10
            Button:
                background_normal: "colors/purple.png"
                text: "[b][color=#ffffff]Cough[/color][/b]"
                size_hint_y: 0.2
                markup: True
                halign: "center"
                font_size: '25sp'
                on_release: root.cough()
            Button:
                background_normal: "colors/orange.png"
                text: "[b][color=#ffffff]Induced[/color][/b]"
                size_hint_y: 0.2
                halign: "center"
                markup: True
                font_size: '25sp'
                on_release: root.induced()   
        Widget:
            size_hint_y: 0.1
<takesputumsample2Screen>:
    kbContainer: kbContainer
    BoxLayout:
        canvas:
            Color:
                rgba: 1,1,1,1
            Rectangle:
                pos: (1,115)
                size: (900,550)
        orientation: 'vertical'
        BoxLayout:
            id: kbContainer
            size_hint_y: 0.99
            orientation: "horizontal"
            padding: 10
        Button:
            background_normal: "colors/green_bright.png"
            text: "[b][color=#ffffff]Next[/color][/b]"
            size_hint_y: 0.2
            markup: True
            font_size: '25sp'
            halign: "center"
            on_release: root.next()  
<takesputumsample3Screen>:
    kbContainer: kbContainer
    BoxLayout:
        canvas:
            Color:
                rgba: 1,1,1,1
            Rectangle:
                pos: (1,115)
                size: (900,550)
        orientation: 'vertical'
        BoxLayout:
            id: kbContainer
            size_hint_y: 0.99
            orientation: "horizontal"
            padding: 10
        Button:
            background_normal: "colors/green_bright.png"
            text: "[b][color=#ffffff]Next[/color][/b]"
            size_hint_y: 0.2
            markup: True
            font_size: '25sp'
            halign: "center"
            on_release: root.next()  
<takesputumsample4Screen>:
    kbContainer: kbContainer
    BoxLayout:
        canvas:
            Color:
                rgba: 1,1,1,1
            Rectangle:
                pos: (1,115)
                size: (900,550)
        orientation: 'vertical'
        BoxLayout:
            id: kbContainer
            size_hint_y: 0.99
            orientation: "horizontal"
            padding: 10
        Button:
            background_normal: "colors/green_bright.png"
            text: "[b][color=#ffffff]Next[/color][/b]"
            size_hint_y: 0.2
            font_size: '25sp'
            halign: "center"
            markup: True
            on_release: root.next()  
<addObjectBoxScreen>:
    floor2_label: floor2_label
    floor2_one: floor2_one
    floor2_two: floor2_two
    floor2_three: floor2_three
    floor2_four: floor2_four
    floor2_five: floor2_five
    floor2_six: floor2_six
    floor2_seven: floor2_seven
    floor2_eight: floor2_eight
    floor2_nine: floor2_nine
    floor2_ten: floor2_ten

    floor1_label: floor1_label
    floor1_one: floor1_one
    floor1_two: floor1_two
    floor1_three: floor1_three
    floor1_four: floor1_four
    floor1_five: floor1_five
    floor1_six: floor1_six
    floor1_seven: floor1_seven
    floor1_eight: floor1_eight
    floor1_nine: floor1_nine
    floor1_ten: floor1_ten

    floor1_label: floor1_label

    FloatLayout:
        canvas:
            Color:
                rgba: 1,1,1,1
            Rectangle:
                pos: (1,105)
                size: (900,550)
        Label:
            id: floor2_label
            markup: True
            size_hint_y: 0.1
            pos: (1,550)
            font_size: "25sp"
        ToggleButton:
            id: floor2_one
            pos: (40,460)
            text:'[b][color=#000000]1[/color][/b]'
            markup: True
            group: 'floor'
            state: 'normal'
            background_down: "colors/green.png"
            background_normal: "colors/white.png"
            font_size: '25sp'
            size_hint_y: 0.15
            size_hint_x: 0.15
        ToggleButton:
            id: floor2_two
            pos: (190,460)
            text: '[b][color=#000000]2[/color][/b]'
            markup:True
            group: 'floor'
            state: 'normal'
            background_down:"colors/green.png"
            background_normal: "colors/white.png"
            font_size: '25sp'
            size_hint_y: 0.15
            size_hint_x: 0.15
        ToggleButton:
            id: floor2_three
            pos: (340,460)
            text: '[b][color=#000000]3[/color][/b]'
            markup:True
            group: 'floor'
            state: 'normal'
            background_down:"colors/green.png"
            background_normal: "colors/white.png"
            font_size: '25sp'
            size_hint_y: 0.15
            size_hint_x: 0.15
        ToggleButton:
            id: floor2_four
            pos: (490,460)
            text: '[b][color=#000000]4[/color][/b]'
            markup:True
            group: 'floor'
            state: 'normal'
            background_down:"colors/green.png"
            background_normal: "colors/white.png"
            font_size: '25sp'
            size_hint_y: 0.15
            size_hint_x: 0.15
        ToggleButton:
            id: floor2_five
            pos: (640,460)
            text: '[b][color=#000000]5[/color][/b]'
            markup:True
            group: 'floor'
            state: 'normal'
            background_down:"colors/green.png"
            background_normal: "colors/white.png"
            font_size: '25sp'
            size_hint_y: 0.15
            size_hint_x: 0.15
        ToggleButton:
            id: floor2_six
            pos: (40,360)
            text:'[b][color=#000000]6[/color][/b]'
            markup: True
            group: 'floor'
            state: 'normal'
            background_down: "colors/green.png"
            background_normal: "colors/white.png"
            font_size: '25sp'
            size_hint_y: 0.15
            size_hint_x: 0.15
        ToggleButton:
            id: floor2_seven
            pos: (190,360)
            text: '[b][color=#000000]7[/color][/b]'
            markup:True
            group: 'floor'
            state: 'normal'
            background_down:"colors/green.png"
            background_normal: "colors/white.png"
            font_size: '25sp'
            size_hint_y: 0.15
            size_hint_x: 0.15
        ToggleButton:
            id: floor2_eight
            pos: (340,360)
            text: '[b][color=#000000]8[/color][/b]'
            markup:True
            group: 'floor'
            state: 'normal'
            background_down:"colors/green.png"
            background_normal: "colors/white.png"
            font_size: '25sp'
            size_hint_y: 0.15
            size_hint_x: 0.15
        ToggleButton:
            id: floor2_nine
            pos: (490,360)
            text: '[b][color=#000000]9[/color][/b]'
            markup:True
            group: 'floor'
            state: 'normal'
            background_down:"colors/green.png"
            background_normal: "colors/white.png"
            font_size: '25sp'
            size_hint_y: 0.15
            size_hint_x: 0.15
        ToggleButton:
            id: floor2_ten
            pos: (640,360)
            text: '[b][color=#000000]10[/color][/b]'
            markup:True
            group: 'floor'
            state: 'normal'
            background_down:"colors/green.png"
            background_normal: "colors/white.png"
            font_size: '25sp'
            size_hint_y: 0.15
            size_hint_x: 0.15
        Label:
            id: floor1_label
            markup: True
            size_hint_y: 0.1
            pos: (1,300)
            font_size: "25sp"
        ToggleButton:
            id: floor1_one
            pos: (40,210)
            text:'[b][color=#000000]1[/color][/b]'
            markup: True
            group: 'floor'
            state: 'normal'
            background_down: "colors/green.png"
            background_normal: "colors/white.png"
            font_size: '25sp'
            size_hint_y: 0.15
            size_hint_x: 0.15
        ToggleButton:
            id: floor1_two
            pos: (190,210)
            text: '[b][color=#000000]2[/color][/b]'
            markup:True
            group: 'floor'
            state: 'normal'
            background_down:"colors/green.png"
            background_normal: "colors/white.png"
            font_size: '25sp'
            size_hint_y: 0.15
            size_hint_x: 0.15
        ToggleButton:
            id: floor1_three
            pos: (340,210)
            text: '[b][color=#000000]3[/color][/b]'
            markup:True
            group: 'floor'
            state: 'normal'
            background_down:"colors/green.png"
            background_normal: "colors/white.png"
            font_size: '25sp'
            size_hint_y: 0.15
            size_hint_x: 0.15
        ToggleButton:
            id: floor1_four
            pos: (490,210)
            text: '[b][color=#000000]4[/color][/b]'
            markup:True
            group: 'floor'
            state: 'normal'
            background_down:"colors/green.png"
            background_normal: "colors/white.png"
            font_size: '25sp'
            size_hint_y: 0.15
            size_hint_x: 0.15
        ToggleButton:
            id: floor1_five
            pos: (640,210)
            text: '[b][color=#000000]5[/color][/b]'
            markup:True
            group: 'floor'
            state: 'normal'
            background_down:"colors/green.png"
            background_normal: "colors/white.png"
            font_size: '25sp'
            size_hint_y: 0.15
            size_hint_x: 0.15
        ToggleButton:
            id: floor1_six
            pos: (40,110)
            text:'[b][color=#000000]6[/color][/b]'
            markup: True
            group: 'floor'
            state: 'normal'
            background_down: "colors/green.png"
            background_normal: "colors/white.png"
            font_size: '25sp'
            size_hint_y: 0.15
            size_hint_x: 0.15
        ToggleButton:
            id: floor1_seven
            pos: (190,110)
            text: '[b][color=#000000]7[/color][/b]'
            markup:True
            group: 'floor'
            state: 'normal'
            background_down:"colors/green.png"
            background_normal: "colors/white.png"
            font_size: '25sp'
            size_hint_y: 0.15
            size_hint_x: 0.15
        ToggleButton:
            id: floor1_eight
            pos: (340,110)
            text: '[b][color=#000000]8[/color][/b]'
            markup:True
            group: 'floor'
            state: 'normal'
            background_down:"colors/green.png"
            background_normal: "colors/white.png"
            font_size: '25sp'
            size_hint_y: 0.15
            size_hint_x: 0.15
        ToggleButton:
            id: floor1_nine
            pos: (490,110)
            text: '[b][color=#000000]9[/color][/b]'
            markup:True
            group: 'floor'
            state: 'normal'
            background_down:"colors/green.png"
            background_normal: "colors/white.png"
            font_size: '25sp'
            size_hint_y: 0.15
            size_hint_x: 0.15
        ToggleButton:
            id: floor1_ten
            pos: (640,110)
            text: '[b][color=#000000]10[/color][/b]'
            markup:True
            group: 'floor'
            state: 'normal'
            background_down:"colors/green.png"
            background_normal: "colors/white.png"
            font_size: '25sp'
            size_hint_y: 0.15
            size_hint_x: 0.15
        Button:
            background_normal: "colors/green_bright.png"
            text: "[b][color=#ffffff]Next[/color][/b]"
            size_hint_y: 0.15
            markup: True
            font_size: '25sp'
            on_release: root.save()
<viewScreen>:
    mode_spinner: mode_spinner
    option_label: option_label
    instruction_label: instruction_label
    option_textinput: option_textinput

    FloatLayout:    
        canvas:
            Color:
                rgba: 1,1,1,1
            Rectangle:
                pos: (1,110)
                size: (900,440)
        BoxLayout:
            orientation: 'vertical'
            padding: 10
            spacing: 10
            Label:
                id: option_label
                markup: True
                font_size: "25sp"
                size_hint_y: 0.1
            Widget:
                size_hint_y: 0.1
            Label:
                id: instruction_label
                markup: True
                font_size: "25sp"
                size_hint_y: 0.2
            Spinner:
                id: mode_spinner
                size_hint_y: 0.2
                background_normal: "colors/blue.png"
                background_down: "colors/blue.png"
                font_size: '25sp'
            Widget:
                size_hint_y: 0.1
            TextInput:
                id: option_textinput
                markup: True 
                font_size: "25sp"
                size_hint_y: 0.15
            Widget:
                size_hint_y: 0.1
            BoxLayout:
                size_hint_y: 0.3
                orientation: "horizontal"
                padding: "10sp"
                spacing: "10sp"
                Button:
                    background_normal: "colors/red.png"
                    text: "[b][color=#ffffff]Discard[/color][/b]"
                    size_hint_y: 0.75
                    markup: True
                    font_size: '25sp'
                    on_release: root.back_to_main()
                Button:
                    background_normal: "colors/green_bright.png"
                    text: "[b][color=#ffffff]Next[/color][/b]"
                    size_hint_y: 0.75
                    markup: True
                    font_size: '25sp'
                    on_release: root.show()
<seepatientScreen>:
    BoxLayout:
        canvas:
            Color:
                rgba: 1,1,1,1
            Rectangle:
                pos: self.pos
                size: self.size
        orientation: 'vertical'
        Widget:
            size_hint_y: 0.1
        Button:
            background_normal: "colors/orange.png"
            text: "[b][color=#ffffff]Show[/color][/b]"
            size_hint_y: 0.2
            markup: True
            font_size: '25sp'
            on_release: root.show()  
<removeScreen>:
    title_label: title_label
    displayLabel: displayLabel
    password_textinput: password_textinput
    BoxLayout:
        canvas:
            Color:
                rgba: 1,1,1,1
            Rectangle:
                pos: (1,100)
                size: (900,440)
        orientation: 'vertical'
        Label:
            id: title_label
            size_hint_y: 0.03
            font_size: '25sp'
            markup: True
            text: ""
            halign: "center"
        Label:
            id: displayLabel
            size_hint_y: 0.15
            font_size: '25sp'
            markup: True
            text: ""
            halign: "center"
        TextInput:
            id: password_textinput
            markup: True
            password: True 
            font_size: "25sp"
            size_hint_y: 0.03
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: 0.1
            padding: 10
            spacing: 10
            Button:
                background_normal: "colors/red.png"
                text: "[b][color=#ffffff]Discard[/color][/b]"
                size_hint_y: 0.4
                markup: True
                font_size: '25sp'
                on_release: root.back_to_main()
            Button:
                background_normal: "colors/green_bright.png"
                text: "[b][color=#ffffff]Delete Database[/color][/b]"
                size_hint_y: 0.4
                markup: True
                font_size: '25sp'
                on_release: root.erase_database()
<reportScreen>:
    title_label: title_label 
    BoxLayout:
        canvas:
            Color:
                rgba: 1,1,1,1
            Rectangle:
                pos: (1, 135)
                size: (900, 400)
        orientation: 'vertical'
        Label:
            id: title_label
            markup: True
            font_size: '25sp'
            size_hint_y: 0.2
        Widget:
            size_hint_y: 0.2
        Button:
            background_normal: "colors/green.png"
            text: "[b][color=#ffffff]Report Data to Central Server[/color][/b]"
            size_hint_y: 0.45
            markup: True
            font_size: '25sp'
            on_release: root.remote()
        Widget:
            size_hint_y: 0.2
        Button:
            background_normal: "colors/purple.png"
            text: "[b][color=#ffffff]Unload Samples at Laboratory[/color][/b]"
            size_hint_y: 0.45
            markup: True
            font_size: '25sp'
            on_release: root.unload()
        Widget:
            size_hint_y: 0.3
        Button:
            background_normal: "colors/red.png"
            text: "[b][color=#ffffff]Discard[/color][/b]"
            size_hint_y: 0.45
            markup: True
            font_size: '25sp'
            on_release: root.back_to_main()
<remoteScreen>:
    BoxLayout:
        canvas:
            Color:
                rgba: 1,1,1,1
            Rectangle:
                pos: self.pos
                size: self.size
        orientation: 'vertical'
        Widget: 
            size_hint_y: 0.1
        Button:
            background_normal: "colors/green.png"
            text: "[b][color=#ffffff]Report Data to Central Server[/color][/b]"
            size_hint_y: 0.15
            markup: True
            font_size: '25sp'
            on_release: root._remote()
        Widget:
            size_hint_y: 0.1
<unloadScreen>:
    floor2_label: floor2_label
    floor2_one: floor2_one
    floor2_two: floor2_two
    floor2_three: floor2_three
    floor2_four: floor2_four
    floor2_five: floor2_five
    floor2_six: floor2_six
    floor2_seven: floor2_seven
    floor2_eight: floor2_eight
    floor2_nine: floor2_nine
    floor2_ten: floor2_ten

    floor1_label: floor1_label
    floor1_one: floor1_one
    floor1_two: floor1_two
    floor1_three: floor1_three
    floor1_four: floor1_four
    floor1_five: floor1_five
    floor1_six: floor1_six
    floor1_seven: floor1_seven
    floor1_eight: floor1_eight
    floor1_nine: floor1_nine
    floor1_ten: floor1_ten

    floor1_label: floor1_label

    FloatLayout:
        canvas:
            Color:
                rgba: 1,1,1,1
            Rectangle:
                pos: (1,95)
                size: (900,550)
        Label:
            id: floor2_label
            markup: True
            size_hint_y: 0.1
            pos: (1,550)
            font_size: "25sp"
        ToggleButton:
            id: floor2_one
            pos: (40,460)
            text:'[b][color=#000000]1[/color][/b]'
            markup: True
            group: 'floor'
            state: 'normal'
            background_down: "colors/green.png"
            background_normal: "colors/white.png"
            font_size: '25sp'
            size_hint_y: 0.15
            size_hint_x: 0.15
        ToggleButton:
            id: floor2_two
            pos: (190,460)
            text: '[b][color=#000000]2[/color][/b]'
            markup:True
            group: 'floor'
            state: 'normal'
            background_down:"colors/green.png"
            background_normal: "colors/white.png"
            font_size: '25sp'
            size_hint_y: 0.15
            size_hint_x: 0.15
        ToggleButton:
            id: floor2_three
            pos: (340,460)
            text: '[b][color=#000000]3[/color][/b]'
            markup:True
            group: 'floor'
            state: 'normal'
            background_down:"colors/green.png"
            background_normal: "colors/white.png"
            font_size: '25sp'
            size_hint_y: 0.15
            size_hint_x: 0.15
        ToggleButton:
            id: floor2_four
            pos: (490,460)
            text: '[b][color=#000000]4[/color][/b]'
            markup:True
            group: 'floor'
            state: 'normal'
            background_down:"colors/green.png"
            background_normal: "colors/white.png"
            font_size: '25sp'
            size_hint_y: 0.15
            size_hint_x: 0.15
        ToggleButton:
            id: floor2_five
            pos: (640,460)
            text: '[b][color=#000000]5[/color][/b]'
            markup:True
            group: 'floor'
            state: 'normal'
            background_down:"colors/green.png"
            background_normal: "colors/white.png"
            font_size: '25sp'
            size_hint_y: 0.15
            size_hint_x: 0.15
        ToggleButton:
            id: floor2_six
            pos: (40,360)
            text:'[b][color=#000000]6[/color][/b]'
            markup: True
            group: 'floor'
            state: 'normal'
            background_down: "colors/green.png"
            background_normal: "colors/white.png"
            font_size: '25sp'
            size_hint_y: 0.15
            size_hint_x: 0.15
        ToggleButton:
            id: floor2_seven
            pos: (190,360)
            text: '[b][color=#000000]7[/color][/b]'
            markup:True
            group: 'floor'
            state: 'normal'
            background_down:"colors/green.png"
            background_normal: "colors/white.png"
            font_size: '25sp'
            size_hint_y: 0.15
            size_hint_x: 0.15
        ToggleButton:
            id: floor2_eight
            pos: (340,360)
            text: '[b][color=#000000]8[/color][/b]'
            markup:True
            group: 'floor'
            state: 'normal'
            background_down:"colors/green.png"
            background_normal: "colors/white.png"
            font_size: '25sp'
            size_hint_y: 0.15
            size_hint_x: 0.15
        ToggleButton:
            id: floor2_nine
            pos: (490,360)
            text: '[b][color=#000000]9[/color][/b]'
            markup:True
            group: 'floor'
            state: 'normal'
            background_down:"colors/green.png"
            background_normal: "colors/white.png"
            font_size: '25sp'
            size_hint_y: 0.15
            size_hint_x: 0.15
        ToggleButton:
            id: floor2_ten
            pos: (640,360)
            text: '[b][color=#000000]10[/color][/b]'
            markup:True
            group: 'floor'
            state: 'normal'
            background_down:"colors/green.png"
            background_normal: "colors/white.png"
            font_size: '25sp'
            size_hint_y: 0.15
            size_hint_x: 0.15
        Label:
            id: floor1_label
            markup: True
            size_hint_y: 0.1
            pos: (1,300)
            font_size: "25sp"
        ToggleButton:
            id: floor1_one
            pos: (40,210)
            text:'[b][color=#000000]1[/color][/b]'
            markup: True
            group: 'floor'
            state: 'normal'
            background_down: "colors/green.png"
            background_normal: "colors/white.png"
            font_size: '25sp'
            size_hint_y: 0.15
            size_hint_x: 0.15
        ToggleButton:
            id: floor1_two
            pos: (190,210)
            text: '[b][color=#000000]2[/color][/b]'
            markup:True
            group: 'floor'
            state: 'normal'
            background_down:"colors/green.png"
            background_normal: "colors/white.png"
            font_size: '25sp'
            size_hint_y: 0.15
            size_hint_x: 0.15
        ToggleButton:
            id: floor1_three
            pos: (340,210)
            text: '[b][color=#000000]3[/color][/b]'
            markup:True
            group: 'floor'
            state: 'normal'
            background_down:"colors/green.png"
            background_normal: "colors/white.png"
            font_size: '25sp'
            size_hint_y: 0.15
            size_hint_x: 0.15
        ToggleButton:
            id: floor1_four
            pos: (490,210)
            text: '[b][color=#000000]4[/color][/b]'
            markup:True
            group: 'floor'
            state: 'normal'
            background_down:"colors/green.png"
            background_normal: "colors/white.png"
            font_size: '25sp'
            size_hint_y: 0.15
            size_hint_x: 0.15
        ToggleButton:
            id: floor1_five
            pos: (640,210)
            text: '[b][color=#000000]5[/color][/b]'
            markup:True
            group: 'floor'
            state: 'normal'
            background_down:"colors/green.png"
            background_normal: "colors/white.png"
            font_size: '25sp'
            size_hint_y: 0.15
            size_hint_x: 0.15
        ToggleButton:
            id: floor1_six
            pos: (40,110)
            text:'[b][color=#000000]6[/color][/b]'
            markup: True
            group: 'floor'
            state: 'normal'
            background_down: "colors/green.png"
            background_normal: "colors/white.png"
            font_size: '25sp'
            size_hint_y: 0.15
            size_hint_x: 0.15
        ToggleButton:
            id: floor1_seven
            pos: (190,110)
            text: '[b][color=#000000]7[/color][/b]'
            markup:True
            group: 'floor'
            state: 'normal'
            background_down:"colors/green.png"
            background_normal: "colors/white.png"
            font_size: '25sp'
            size_hint_y: 0.15
            size_hint_x: 0.15
        ToggleButton:
            id: floor1_eight
            pos: (340,110)
            text: '[b][color=#000000]8[/color][/b]'
            markup:True
            group: 'floor'
            state: 'normal'
            background_down:"colors/green.png"
            background_normal: "colors/white.png"
            font_size: '25sp'
            size_hint_y: 0.15
            size_hint_x: 0.15
        ToggleButton:
            id: floor1_nine
            pos: (490,110)
            text: '[b][color=#000000]9[/color][/b]'
            markup:True
            group: 'floor'
            state: 'normal'
            background_down:"colors/green.png"
            background_normal: "colors/white.png"
            font_size: '25sp'
            size_hint_y: 0.15
            size_hint_x: 0.15
        ToggleButton:
            id: floor1_ten
            pos: (640,110)
            text: '[b][color=#000000]10[/color][/b]'
            markup:True
            group: 'floor'
            state: 'normal'
            background_down:"colors/green.png"
            background_normal: "colors/white.png"
            font_size: '25sp'
            size_hint_y: 0.15
            size_hint_x: 0.15
        BoxLayout:
            orientation: "horizontal"
            size_hint_y: 0.2
            padding: 10
            spacing: 10
            Button:
                background_normal: "colors/red.png"
                text: "[b][color=#ffffff]Discard[/color][/b]"
                size_hint_y: 0.7
                markup: True
                font_size: '25sp'
                on_release: root.discard()
            Button:
                background_normal: "colors/green_bright.png"
                text: "[b][color=#ffffff]Next[/color][/b]"
                size_hint_y: 0.7
                markup: True
                font_size: '25sp'
                on_release: root._unload()
''')

class MainScreen(Screen):
    center_label = ObjectProperty()
    box_label = ObjectProperty()
    mode_spinner = ObjectProperty()
    title_label = ObjectProperty()
    option_label = ObjectProperty()

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        """Set a timer"""
        refresh_time = 0.5
        Clock.schedule_interval(self.timer, refresh_time)

    def timer(self, dt):
        """Read data from the serial port"""
        '''val = port.readline()
        val = val.split(";")
        if (int(val[0]) < 20):
            line0 = "Temperature Ok, " + val[0]
        else if (int(val[1]) < 20):
            line1 = "Moisture Ok, " + val[1]
        line2 = "Storing: " + str(int(val[2]) + int(val[3]) + int(val[4])) \
        + int(val[5]) + int(val[6]) + int(val[7]) + int(val[8]) + "samples"
        self.box_label.text = "".join([str(line0), str(line1), str(line2)])
        ''' 
        line0 = "[b][color=#000000]Temp: 19[/color][/b]" 
        line1 = "[b][color=#000000] Moisture: 25[/color][/b]"
        self.box_label.text = "".join([str(line0),str(line1)])

    def on_pre_enter(self, *args):
        
        self.title_label.text = "[b][color=#ffffff]Biological Sample Collector Assistant[/color][/b]"

        line0 = "[b][color=#ff0000]Instructions:[/color][/b] "
        line1 = "[b][color=#000000] The system will aid you with the steps \n that you must follow " \
                "in order to achieve a correct collection of \n samples and retrieve patient' symptoms. [/color][/b] "
        self.center_label.text = "".join([line0, line1])

        self.option_label.text = "[b][color=#000000] Choose an option: [/color][/b]"

    def open_doors():
        pass

    def close_doors():
        pass

    def next(self):
        """ Continue to the corresponding screen based on the spinner """
        if (self.mode_spinner.text == "Enroll New Patient"):
            self.manager.current = "add"
        elif (self.mode_spinner.text == "Find Patient"):
            self.manager.current = "view"
        elif (self.mode_spinner.text == "Remove Database"):
            self.manager.current = "remove"
        elif (self.mode_spinner.text == "Report Database"):
            self.manager.current = "report"

    def stop(self):
        self.manager.app.stop()

    #"Add Patient", "View Patient", "Remove Patient", "Report patient"   

class addScreen(Screen):
    day_spinner = ObjectProperty()
    month_spinner = ObjectProperty()
    year_spinner = ObjectProperty()
    age_spinner = ObjectProperty()
    male = ObjectProperty()
    female = ObjectProperty()
    name_textinput = ObjectProperty()
    name_label = ObjectProperty()
    birth_label = ObjectProperty()
    birthdate_label = ObjectProperty()
    age_label = ObjectProperty()

    def __init__(self, **kwargs):
        super(addScreen, self).__init__(**kwargs)
        self._add_text_inputs()
        self._patient = None

    def on_enter(self, *args):
        self.male.state = "normal"
        self.female.state = "normal"

    def on_pre_enter(self, *args):
        '''day spinner'''
        list = []
        for day in range(32):
            day+=1
            list.append(str(day))
        self.day_spinner.values = list

        '''month spinner'''
        list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        self.month_spinner.values = list

        '''year spinner'''
        list = range(1920, 2016)
        list.reverse()
        list1 = []
        for each in list:
            list1.append(str(each))
        self.year_spinner.values = list1

        '''age spinner'''
        list = []
        for age in range(101):
            list.append(str(age+1))
        self.age_spinner.values = list

    def _add_text_inputs(self):
        layout = ['Name:', 'Birthdate', 'Age:', 'Gender:']
        self.name_label.text = "[b][color=#000000]Name:[/color][/b]"
        self.birth_label.text = "[b][color=#000000]Birthdate or Age:[/color][/b]"
        self.birthdate_label.text = "[b][color=#000000]Birthdate:[/color][/b]"
        self.age_label.text = "[b][color=#000000]Age:[/color][/b]"
        
        # 'Rapid Heart Beat', 'Shortness of Breath', 'Cough longer than two weeks', 'Haemoptysis', 
        # 'Chest Pain', 'Blood in the urine', 'Headache or Confusion', 
        #'Backpain', 'Hoarseness', 'Does the person have HIV?', 'Did the Person Live in a High TB Prevalence Country?', 
        #'Is the area poor?', 'Is the person living in an altitude zone?', 'Is the person living in a TBs outbreak']
                       
    def save(self):
        file = open("patient.txt", "a")
        
        line0 = self.name_textinput.text
        line2 = ""
        
        if (self.age_spinner.text == ""):
            line1 = self.day_spinner.text + self.month_spinner.text + self.year_spinner.text 
        else:
            line1 = self.age_spinner.text
        
        if ( (self.male.state == "down") and (self.female.state == "down")):
            line2 = "1"
        if ( (self.male.state == "down") and (self.female.state == "normal")):
            line2 = "1"
        elif ( (self.male.state == "down") and (self.female.state == "normal")):
            line2 = "0"

        file.write(line0 + ";" + line1 + ";" + line2 + ";")
        file.close()

        self.manager.transition.direction = "left"
        self.manager.current = "omr"

        print "Successfully wrote on file"

    def discard(self):
        '''Erase the information collected so far'''
        file = open("patient.txt", "w")
        file.write("")
        file.close()
        self.manager.transition.direction = "left"
        self.manager.current = "main"

class OMRScreen(Screen):
    mode_spinner = ObjectProperty()
    kbContainer = ObjectProperty()

    def __init__(self, **kwargs):
       super(OMRScreen, self).__init__(**kwargs)
       self.on_pre_enter()
       self._add_text_inputs()

    def on_enter(self, *args):
        self.txtIn2.state = "normal"
        self.txtIn3.state = "normal"
        
    def on_pre_enter(self, *args):
        file = open("countries.txt", "r")
        list = []
        for line in file.readlines():
            list.append(line)
        self.mode_spinner.values = list 
        file.close()

    def _add_text_inputs(self):
        #self.kbContainer.add_widget(Label(text = "[b][color=#000000]Patient's Address: [/color][/b]", markup = True, color = (1,1,1,1), font_size='25sp'))

        '''Country'''
        # Choose on spinner

        '''Residence'''
        self.txtIn0 = TextInput(text = "", multiline = False, font_size = "25sp")
        self.kbContainer.add_widget(Label(text = "[b][color=#000000]Residence[/color][/b]", markup = True, color = (1,1,1,1), font_size='25sp'))
        self.kbContainer.add_widget(self.txtIn0)

        '''Telephone Number'''
        self.txtIn1 = TextInput(text = "", multiline = False, font_size = "25sp")
        self.kbContainer.add_widget(Label(text = "[b][color=#000000]"+"Telephone"+"[/color][/b]", markup = True, color = (1,1,1,1), font_size='25sp'))
        self.kbContainer.add_widget(self.txtIn1)

        self.kbContainer.add_widget(Label(text=""))

        '''Deceased'''
        self.txtIn2 = ToggleButton(text='[b][color=#000000]Deceased[/color][/b]', markup = True, state = 'normal', background_down = "colors/green.png", background_normal = "colors/white.png", font_size='25sp')
        #self.kbContainer.add_widget(Label(text = "Deceased?"))
        self.kbContainer.add_widget(self.txtIn2)

        self.kbContainer.add_widget(Label(text = ""))

        '''Voided'''
        self.txtIn3 = ToggleButton(text='[b][color=#000000]Voided[/color][/b]', markup = True, state = 'normal', background_down = "colors/green.png", background_normal = "colors/white.png", font_size='25sp')
        #self.kbContainer.add_widget(Label(text = "Voided?"))
        self.kbContainer.add_widget(self.txtIn3)

        self.kbContainer.add_widget(Label(text = ""))        

        self.kbContainer.add_widget(Label(text = "[b][color=#000000]Country: [/color][/b]", markup = True, color = (1,1,1,1), font_size='25sp'))
       
    def save(self):
        file = open("patient.txt", "a")
        line0 = self.mode_spinner.text[:len(self.mode_spinner.text)-1] 
        line1 = self.txtIn0.text
        line2 = self.txtIn1.text  
        line3 = convert_state_toggle_box ( self.txtIn2.state )
        line4 = convert_state_toggle_box ( self.txtIn3.state )

        file.write(line0 + ";" + line1 + ";" + line2 + ";" + line3 + ";" + line4 + ";")
        file.close()

        self.manager.transition.direction = "left"
        self.manager.current = "add2"

        print "Successfully wrote on file"

    def discard(self):
        '''Erase the information collected so far'''
        file = open("patient.txt", "w")
        file.write("")
        file.close()
        self.manager.transition.direction = "left"
        self.manager.current = "main"

class add2Screen(Screen):
    kbContainer = ObjectProperty()

    def __init__(self, **kwargs):
        super(add2Screen, self).__init__(**kwargs)
        self._add_text_inputs()
        self._patient = None

    def on_enter(self, *args):
        self.txtIn0.state = "normal"
        self.txtIn1.state = "normal"
        self.txtIn2.state = "normal"
        self.txtIn3.state = "normal"
        self.txtIn4.state = "normal"

    def _add_text_inputs(self):
        layout = ['Feelings of Sickness', 'Feelings of Weakness', \
        'Loss of Apetite', 'Weight loss', 'Tiredness']
        
        '''Feelings of sickness'''
        self.txtIn0 = ToggleButton(text="[b][color=#000000]"+str(layout[0])+"[/color][/b]", state = 'normal', background_down = "colors/green.png", background_normal = "colors/white.png", font_size='25sp', markup = True)
        #self.kbContainer.add_widget(Label(text = "[b][color=#000000]"+str(layout[0])+"[/color][/b]", markup = True, color = (1,1,1,1)))
        self.kbContainer.add_widget(self.txtIn0)

        '''Feelings of weakness'''
        self.txtIn1 = ToggleButton(text="[b][color=#000000]"+str(layout[1])+"[/color][/b]", state = 'normal', background_down = "colors/green.png", background_normal = "colors/white.png", font_size='25sp', markup = True)
        #self.kbContainer.add_widget(Label(text = str(layout[1])))
        self.kbContainer.add_widget(self.txtIn1)
        
        '''Loss of Apetite'''
        self.txtIn2 = ToggleButton(text="[b][color=#000000]"+str(layout[2])+"[/color][/b]", state = 'normal', background_down = "colors/green.png", background_normal = "colors/white.png", font_size='25sp', markup = True)
        #self.kbContainer.add_widget(Label(text = str(layout[2])))
        self.kbContainer.add_widget(self.txtIn2)
        
        '''Weight loss'''
        self.txtIn3 = ToggleButton(text = "[b][color=#000000]"+str(layout[3])+"[/color][/b]", state = 'normal', background_down = "colors/green.png", background_normal = "colors/white.png", font_size='25sp', markup = True)
        #self.kbContainer.add_widget(Label(text = str(layout[3])))
        self.kbContainer.add_widget(self.txtIn3)
        
        '''Tiredness'''
        self.txtIn4 = ToggleButton(text="[b][color=#000000]"+str(layout[4])+"[/color][/b]", state = 'normal', background_down = "colors/green.png", background_normal = "colors/white.png", font_size='25sp', markup = True)
        #self.kbContainer.add_widget(Label(text = str(layout[4])))
        self.kbContainer.add_widget(self.txtIn4)
    
    def save(self):
        file = open("patient.txt", "a")
        line0 = convert_state_toggle_box( self.txtIn0.state )
        line1 = convert_state_toggle_box( self.txtIn1.state )
        line2 = convert_state_toggle_box( self.txtIn2.state )
        line3 = convert_state_toggle_box( self.txtIn3.state )
        line4 = convert_state_toggle_box( self.txtIn4.state )
        file.write(line0 + ";" + line1 + ";" + line2 + ";" + line3 + ";" + line4 + ";" )
        file.close()
        print "Successfully wrote on file"

        self.manager.transition.direction = "left"
        self.manager.current = "add3"

    def discard(self):
        '''Erase the information collected so far'''
        file = open("patient.txt", "w")
        file.write("")
        file.close()
        self.manager.transition.direction = "left"
        self.manager.current = "main"

class add3Screen(Screen):
    kbContainer = ObjectProperty()

    def __init__(self, **kwargs):
        super(add3Screen, self).__init__(**kwargs)
        self._add_text_inputs()
        self._patient = None

    def on_enter(self, *args):
        self.txtIn0.state = "normal"
        self.txtIn1.state = "normal"
        self.txtIn2.state = "normal"
        self.txtIn3.state = "normal"
        self.txtIn4.state = "normal"

    def _add_text_inputs(self):
        layout = ['Fever', 'Night Sweats', 'Fatigue', 'Rapid Heart Beat', 'Shortness of Breath']

        '''Fever'''    
        self.txtIn0 = ToggleButton(text="[b][color=#000000]"+str(layout[0])+"[/color][/b]", state = 'normal', background_down = "colors/green.png", background_normal = "colors/white.png", font_size='25sp', markup = True)
        #self.kbContainer.add_widget(Label(text = str(layout[0])))
        self.kbContainer.add_widget(self.txtIn0)
        
        '''Night Sweats'''
        self.txtIn1 = ToggleButton(text="[b][color=#000000]"+str(layout[0])+"[/color][/b]", state = 'normal', background_down = "colors/green.png", background_normal = "colors/white.png", font_size='25sp', markup = True)
        #self.kbContainer.add_widget(Label(text = str(layout[1])))
        self.kbContainer.add_widget(self.txtIn1)

        '''Fatigue'''
        self.txtIn2 = ToggleButton(text="[b][color=#000000]"+str(layout[1])+"[/color][/b]", state = 'normal', background_down = "colors/green.png", background_normal = "colors/white.png", font_size='25sp', markup = True)
        #self.kbContainer.add_widget(Label(text = str(layout[2])))
        self.kbContainer.add_widget(self.txtIn2)
        
        '''Rapid Heart Beat'''
        self.txtIn3 = ToggleButton(text="[b][color=#000000]"+str(layout[2])+"[/color][/b]", state = 'normal', background_down = "colors/green.png", background_normal = "colors/white.png", font_size='25sp', markup = True)
        #self.kbContainer.add_widget(Label(text = str(layout[3])))
        self.kbContainer.add_widget(self.txtIn3)

        '''Shortness of breath'''
        self.txtIn4 = ToggleButton(text="[b][color=#000000]"+str(layout[3])+"[/color][/b]", state = 'normal', background_down = "colors/green.png", background_normal = "colors/white.png", font_size='25sp', markup = True)
        #self.kbContainer.add_widget(Label(text = str(layout[4])))
        self.kbContainer.add_widget(self.txtIn4)

    def save(self):
        file = open("patient.txt", "a")
        line0 = convert_state_toggle_box( self.txtIn0.state )
        line1 = convert_state_toggle_box( self.txtIn1.state )
        line2 = convert_state_toggle_box( self.txtIn2.state )
        line3 = convert_state_toggle_box( self.txtIn3.state )
        line4 = convert_state_toggle_box( self.txtIn4.state )
        file.write(line0 + ";" + line1 + ";" + line2 + ";" + line3 + ";" + line4 + ";" )
        file.close()
        print "Successfully wrote on file"

        self.manager.transition.direction = "left"
        self.manager.current = "add4"

    def discard(self):
        '''Erase the information collected so far'''
        file = open("patient.txt", "w")
        file.write("")
        file.close()
        self.manager.transition.direction = "left"
        self.manager.current = "main"

class add4Screen(Screen):
    kbContainer = ObjectProperty()

    def __init__(self, **kwargs):
        super(add4Screen, self).__init__(**kwargs)
        self._add_text_inputs()
        self._patient = None

    def on_enter(self, *args):
        self.txtIn0.state = "normal"
        self.txtIn1.state = "normal"
        self.txtIn2.state = "normal"
        self.txtIn3.state = "normal"
        self.txtIn4.state = "normal"

    def _add_text_inputs(self):
        layout = ['Cough longer than two weeks', 'Haemoptysis', 'Chest Pain', 'Blood in the urine', 'Headache or Confusion']
        
        '''Cough longer than two weeks'''
        self.txtIn0 = ToggleButton(text="[b][color=#000000]"+str(layout[0])+"[/color][/b]", state = 'normal', background_down = "colors/green.png", background_normal = "colors/white.png", font_size='25sp', markup = True)
        #self.kbContainer.add_widget(Label(text = str(layout[0])))
        self.kbContainer.add_widget(self.txtIn0)

        '''Haemoptysis'''
        self.txtIn1 = ToggleButton(text="[b][color=#000000]"+str(layout[1])+"[/color][/b]", state = 'normal', background_down = "colors/green.png", background_normal = "colors/white.png", font_size='25sp', markup = True)
        #self.kbContainer.add_widget(Label(text = str(layout[1])))
        self.kbContainer.add_widget(self.txtIn1)

        '''Chest Pain'''
        self.txtIn2 = ToggleButton(text="[b][color=#000000]"+str(layout[2])+"[/color][/b]", state = 'normal', background_down = "colors/green.png", background_normal = "colors/white.png", font_size='25sp', markup = True)
        #self.kbContainer.add_widget(Label(text = str(layout[2])))
        self.kbContainer.add_widget(self.txtIn2)

        '''Blood in the urine'''
        self.txtIn3 = ToggleButton(text="[b][color=#000000]"+str(layout[3])+"[/color][/b]", state = 'normal', background_down = "colors/green.png", background_normal = "colors/white.png", font_size='25sp', markup = True)
        #self.kbContainer.add_widget(Label(text = str(layout[3])))
        self.kbContainer.add_widget(self.txtIn3)

        '''Headache or Confusion'''
        self.txtIn4 = ToggleButton(text="[b][color=#000000]"+str(layout[4])+"[/color][/b]", state = 'normal', background_down = "colors/green.png", background_normal = "colors/white.png", font_size='25sp', markup = True)
        #self.kbContainer.add_widget(Label(text = str(layout[4])))
        self.kbContainer.add_widget(self.txtIn4)
   
    def save(self):
        file = open("patient.txt", "a")
        line0 = convert_state_toggle_box( self.txtIn0.state )
        line1 = convert_state_toggle_box( self.txtIn1.state )
        line2 = convert_state_toggle_box( self.txtIn2.state )
        line3 = convert_state_toggle_box( self.txtIn3.state )
        line4 = convert_state_toggle_box( self.txtIn4.state )
        file.write(line0 + ";" + line1 + ";" + line2 + ";" + line3 + ";" + line4 + ";" )
        file.close()
        print "Successfully wrote on file"

        self.manager.transition.direction = "left"
        self.manager.current = "add5"

    def discard(self):
        '''Erase the information collected so far'''
        file = open("patient.txt", "w")
        file.write("")
        file.close()
        self.manager.transition.direction = "left"
        self.manager.current = "main"

class add5Screen(Screen):
    kbContainer = ObjectProperty()

    def __init__(self, **kwargs):
        super(add5Screen, self).__init__(**kwargs)
        self._add_text_inputs()

    def on_enter(self, *args):
        self.txtIn0.state = "normal"
        self.txtIn1.state = "normal"
        self.txtIn2.state = "normal"
        self.txtIn3.state = "normal"
        self.txtIn4.state = "normal"
        
    def _add_text_inputs(self):
        layout = ['Does the person have HIV?', 'Did the Person Live in a High TB Prevalence Country?',\
         'Is the Area Poor', 'Is the person living in an altitude zone?', 'Is the person living in a TBs outbreak']
        
        '''Does the person have HIV?'''
        self.txtIn0 = ToggleButton(text="[b][color=#000000]"+str(layout[0])+"[/color][/b]", state = 'normal', background_down = "colors/green.png", background_normal = "colors/white.png", font_size='25sp', markup = True)
        #self.kbContainer.add_widget(Label(text = str(layout[0])))
        self.kbContainer.add_widget(self.txtIn0)

        '''Did the Person Live in a High TB Prevalence Country?'''
        self.txtIn1 = ToggleButton(text="[b][color=#000000]"+str(layout[1])+"[/color][/b]", state = 'normal', background_down = "colors/green.png", background_normal = "colors/white.png", font_size='25sp', markup = True)
        #self.kbContainer.add_widget(Label(text = str(layout[1])))
        self.kbContainer.add_widget(self.txtIn1)

        '''Is the area poor?'''
        self.txtIn2 = ToggleButton(text="[b][color=#000000]"+str(layout[2])+"[/color][/b]", state = 'normal', background_down = "colors/green.png", background_normal = "colors/white.png", font_size='25sp', markup = True)
        #self.kbContainer.add_widget(Label(text = str(layout[2])))
        self.kbContainer.add_widget(self.txtIn2)

        '''Is the person living in an altitude zone?'''
        self.txtIn3 = ToggleButton(text="[b][color=#000000]"+str(layout[3])+"[/color][/b]", state = 'normal', background_down = "colors/green.png", background_normal = "colors/white.png", font_size='25sp', markup = True)
        #self.kbContainer.add_widget(Label(text = str(layout[3])))
        self.kbContainer.add_widget(self.txtIn3)

        '''Is the person living in a TBs outbreak'''
        self.txtIn4 = ToggleButton(text="[b][color=#000000]"+str(layout[4])+"[/color][/b]", state = 'normal', background_down = "colors/green.png", background_normal = "colors/white.png", font_size='25sp', markup = True)
        #self.kbContainer.add_widget(Label(text = str(layout[4])))
        self.kbContainer.add_widget(self.txtIn4)
   
    def save(self):
        file = open("patient.txt", "a")
        line0 = convert_state_toggle_box( self.txtIn0.state )
        line1 = convert_state_toggle_box( self.txtIn1.state )
        line2 = convert_state_toggle_box( self.txtIn2.state )
        line3 = convert_state_toggle_box( self.txtIn3.state )
        line4 = convert_state_toggle_box( self.txtIn4.state )
        file.write(line0 + ";" + line1 + ";" + line2 + ";" + line3 + ";" + line4 + ";" )
        file.close()
        print "Successfully wrote on file"

        self.manager.transition.direction = "left"
        self.manager.current = "result"

    def discard(self):
        '''Erase the information collected so far'''
        file = open("patient.txt", "w")
        file.write("")
        file.close()
        self.manager.transition.direction = "left"
        self.manager.current = "main"

class resultScreen(Screen):
    displayLabel = ObjectProperty()
    displayButton = ObjectProperty()
    kbContainer = ObjectProperty()

    def __init__(self, **kwargs):
        super(resultScreen, self).__init__(**kwargs)
        self._add_text_inputs()
        
    def _add_text_inputs(self):
        line0 = "[b][color=#ff0000]Result:[/color][/b]"
        line1 = " ... Computing ... " 
        self.displayLabel.text = "".join([line0, line1])
        #set_principal_file()
        result = forward_chaining()
        print "here!"
        print result 
        if (result == "100"):
            line0 = "[b][color=#ff0000]Result:[/color][/b]"
            line1 = " Not sick " 
            self.displayLabel.text = "".join([line0, line1])
            self.displayButton.text = "Go to Main"
        elif (result == "010"):
            line0 = "[b][color=#ff0000]Result:[/color][/b]"
            line1 = " Take sputum sample " 
            self.displayLabel.text = "".join([line0, line1])
            self.displayButton.text = line1
        elif (result == "001"):
            line0 = "[b][color=#ff0000]Result:[/color][/b]"
            line1 = " Take sputum sample " 
            self.displayLabel.text = "".join([line0, line1])
            self.displayButton.text = line1
        else:
            line1 = "There is no result"
            self.displayLabel.text = str(result)
            self.displayButton.text = line1
            
    def proceed(self):
        self.manager.transition.direction = "left"
        self.manager.current = "main"
        if (self.displayButton.text == "Take sputum sample"):
            self.manager.transition.direction = "left"
            self.manager.current = "takesputumsample"
        elif (self.displayButton.text == "Go to Main"):
            self.manager.transition.direction = "left"
            self.manager.current = "result"
        elif (self.displayButton.text == "No result"):
            self.manager.transition.direction = "left"
            self.manager.current = "main"

def set_principal_file():
    '''get rid of tokens'''
    file0 = open("patient.txt", "r")
    file1 = open("features.txt", "w")
    for line in file0.readlines():
        file1.write(line)
    file0.close()
    file1.close()

    '''erase data in patient.txt'''
    file = open("patient.txt", "w")
    file.write("")
    file.close()

def forward_chaining():
    '''Only two layers in the goal tree. Too simple.'''
    file0 = open("patient.txt", "r")
    file1 = open("rules.txt", "r")

    # all the features (28 total)
    # Patient's info 0:5
    # SE 6:27

    features = file0.readline()

    # check if there is 1 in the last five features
    if ("1" in features[23:27]):
        return "001"

    else:
        rule_features = np.zeros((21,1))
        rule_name = np.zeros((21,1))
        i = 0
        for rule in file1.readlines():
            rule_features[i] = (rule.split(";")[0])[4:25]
            rule_name[i] = rule.split(";")[1]
            i += 1

        for j,k in map(None, rule_features, rule_name):
            if (features[6:27] == j):
                """Found match"""
                #file2.write(features + "/n")
                return "100"
                break

    file0.close()
    file1.close()
    
    return "000"

class takesputumsampleScreen(Screen):
    """ Specimen Collection Methods
        This class handles the interaction with the user to help her in taking a sputum sample.
        The collection stage's key consideration is the quality of the sample.
        I plan on showing images on how to take a sample step by step. 
        Image 1: Materials
        Image 2: Step 1 -> Cough or Induced Sputum 
        Image 3: Step 2 -> Wear protective equipment
        Image 4: Step 3 -> Explain what is sputum and how to produce it
        Image 5: Step 4 -> Examples of sputum while collecting
     """
    kbContainer = ObjectProperty()
    
    def __init__(self, **kwargs):
        super(takesputumsampleScreen, self).__init__(**kwargs)
        self._add_text_inputs()

    def _add_text_inputs(self):
        image = Image(source="images/materials.png", pos=(100,100), size=(48,48))
        self.kbContainer.add_widget(image)
    
    def next(self):
        self.manager.transition.direction = "left"
        self.manager.current = "takesputumsample1"
        
class takesputumsample1Screen(Screen):
    kbContainer = ObjectProperty()
    
    def __init__(self, **kwargs):
        super(takesputumsample1Screen, self).__init__(**kwargs)
            
    def cough(self):
        self.manager.transition.direction = "left"
        self.manager.current = "takesputumsample2"
    def induced(self):
        self.manager.transition.direction = "left"
        self.manager.current = "takesputumsample2"

class takesputumsample2Screen(Screen):
    kbContainer = ObjectProperty()
    
    def __init__(self, **kwargs):
        super(takesputumsample2Screen, self).__init__(**kwargs)
        self._add_text_inputs()

    def _add_text_inputs(self):
        image = Image(source="images/wearprotectiveequipment.png", pos=(100,100), size=(48,48))
        self.kbContainer.add_widget(image)
    
    def next(self):
        self.manager.transition.direction = "left"
        self.manager.current = "takesputumsample3"

class takesputumsample3Screen(Screen):
    kbContainer = ObjectProperty()
    
    def __init__(self, **kwargs):
        super(takesputumsample3Screen, self).__init__(**kwargs)
        self._add_text_inputs()

    def _add_text_inputs(self):
        self.kbContainer.add_widget(Label(text = "[b][color=#000000]During specimen collection, patients produce an aerosol that may be hazardous to health-care\
            workers or other patients in close proximity. For this reason, precautionary measures for infection\
            control must be followed during sputum induction, bronchoscopy, and other common diagnostic\
            procedures[/color][/b]", markup = True, font_size = "25sp"))
        image = Image(source="images/explainsputum.png", pos=(100,100), size=(48,48))
        self.kbContainer.add_widget(image)
    
    def next(self):
        self.manager.transition.direction = "left"
        self.manager.current = "takesputumsample4"

class takesputumsample4Screen(Screen):
    kbContainer = ObjectProperty()
    
    def __init__(self, **kwargs):
        super(takesputumsample4Screen, self).__init__(**kwargs)
        self._add_text_inputs()

    def _add_text_inputs(self):
        image = Image(source="images/sputumsamples.png", pos=(100,100), size=(48,48))
        self.kbContainer.add_widget(image)
    
    def next(self):
        self.manager.transition.direction = "left"
        self.manager.current = "addObjectBox"

class addObjectBoxScreen(Screen):
    floor2_label = ObjectProperty()
    floor2_one = ObjectProperty()
    floor2_two = ObjectProperty()
    floor2_three = ObjectProperty()
    floor2_four = ObjectProperty()
    floor2_five = ObjectProperty()
    floor2_six = ObjectProperty()
    floor2_seven = ObjectProperty()
    floor2_eight = ObjectProperty()
    floor2_nine = ObjectProperty()
    floor2_ten = ObjectProperty()

    floor1_label = ObjectProperty()
    floor1_one = ObjectProperty()
    floor1_two = ObjectProperty()
    floor1_three = ObjectProperty()
    floor1_four = ObjectProperty()
    floor1_five = ObjectProperty()
    floor1_six = ObjectProperty()
    floor1_seven = ObjectProperty()
    floor1_eight = ObjectProperty()
    floor1_nine = ObjectProperty()
    floor1_ten = ObjectProperty()
    
    def __init__(self, **kwargs):
        super(addObjectBoxScreen, self).__init__(**kwargs)
        self._add_text_inputs()

    def on_enter(self, *args):
        self.floor1_one.state = "normal"
        self.floor1_two.state = "normal"
        self.floor1_three.state = "normal"
        self.floor1_four.state = "normal"
        self.floor1_five.state = "normal"
        self.floor1_six.state = "normal"
        self.floor1_seven.state = "normal"
        self.floor1_eight.state = "normal"
        self.floor1_nine.state = "normal"

        self.floor2_one.state = "normal"
        self.floor2_two.state = "normal"
        self.floor2_three.state = "normal"
        self.floor2_four.state = "normal"
        self.floor2_five.state = "normal"
        self.floor2_six.state = "normal"
        self.floor2_seven.state = "normal"
        self.floor2_eight.state = "normal"
        self.floor2_nine.state = "normal"

    def _add_text_inputs(self):
        self.floor2_label.text = "[b][color=#000000]Floor 2[/color][/b]"
        self.floor1_label.text = "[b][color=#000000]Floor 1[/color][/b]"

    def save(self):
        line = ""
        if (convert_state_toggle_box(self.floor1_one.state) == "1"):
            line = "11"
        if (convert_state_toggle_box(self.floor1_two.state) == "1"):
            line = "12"
        if (convert_state_toggle_box(self.floor1_three.state) == "1"):
            line = "13"
        if (convert_state_toggle_box(self.floor1_four.state) == "1"):
            line = "14"
        if (convert_state_toggle_box(self.floor1_five.state) == "1"):
            line = "15"
        if (convert_state_toggle_box(self.floor1_six.state) == "1"):
            line = "16"
        if (convert_state_toggle_box(self.floor1_seven.state) == "1"):
            line = "17"
        if (convert_state_toggle_box(self.floor1_eight.state) == "1"):
            line = "18"
        if (convert_state_toggle_box(self.floor1_nine.state) == "1"):
            line = "19"
        if (convert_state_toggle_box(self.floor1_ten.state) == "1"):
            line = "10"

        if (convert_state_toggle_box(self.floor2_one.state) == "1"):
            line = "21"
        if (convert_state_toggle_box(self.floor2_two.state) == "1"):
            line = "22"
        if (convert_state_toggle_box(self.floor2_three.state) == "1"):
            line = "23"
        if (convert_state_toggle_box(self.floor2_four.state) == "1"):
            line = "24"
        if (convert_state_toggle_box(self.floor2_five.state) == "1"):
            line = "25"
        if (convert_state_toggle_box(self.floor2_six.state) == "1"):
            line = "26"
        if (convert_state_toggle_box(self.floor2_seven.state) == "1"):
            line = "27"
        if (convert_state_toggle_box(self.floor2_eight.state) == "1"):
            line = "28"
        if (convert_state_toggle_box(self.floor2_nine.state) == "1"):
            line = "29"
        if (convert_state_toggle_box(self.floor2_ten.state) == "1"):
            line = "20"

        file = open("patients.txt", "a")
        file1 = open("patient.txt", "r")
        
        file.write(file1.readline() + line)
        
        file1.close()
        file.close()

        self.manager.transition.direction = "left"
        self.manager.current = "main"

    def next(self):
        self.manager.transition.direction = "left"
        self.manager.current = "main"

class viewScreen(Screen):
    option_label = ObjectProperty()
    mode_spinner = ObjectProperty() 
    instruction_label = ObjectProperty() 
    option_textinput = ObjectProperty()
    
    def __init__(self, **kwargs):
        super(viewScreen, self).__init__(**kwargs)
        self._add_text_inputs()

    def _add_text_inputs(self):
        self.option_label.text = "[b][color=#ffffff]Find a Patient[/color][/b]"
        self.instruction_label.text = "[b][color=#000000]Use the spinner or use the textinput to find a patient[/color][/b]"

    def on_pre_enter(self, *args):
        file = open("patients.txt", "r")
        list = []
        for line in file.readlines():
            line = line.split(";")
            list.append(line[0])
        self.mode_spinner.values = list 
        file.close()

    def back_to_main(self, *args):
        self.manager.transition.direction = "left"
        self.manager.current = "main"

    def show(self, *args):
        if ((self.option_textinput.text == "") and (self.mode_spinner.text == "")):
            self.manager.transition.direction = "left"
            self.manager.current = "view"
        elif ((self.option_textinput.text != "") and (self.mode_spinner.text == "")):
            file = open("patients.txt", "r")
            file1 = open("findpatient.txt", "w")
            for line in file.readlines():
                if (line[0] == self.option_textinput.text):
                    file1.write(line)
            file1.close()
            file.close()
            self.manager.transition.direction = "left"
            self.manager.current = "seepatient"
        elif ((self.option_textinput.text == "") and (self.mode_spinner.text != "")):
            file = open("patients.txt", "r")
            file1 = open("findpatient.txt", "w")
            for line in file.readlines():
                if (line[0] == self.mode_spinner.text):
                    file1.write(line)
            file1.close()
            file.close()
            self.manager.transition.direction = "left"
            self.manager.current = "seepatient"
        elif ((self.option_textinput.text != "") and (self.mode_spinner.text != "")):
            '''Search with spinner'''
            file = open("patients.txt", "r")
            file1 = open("findpatient.txt", "w")
            for line in file.readlines():
                if (line[0] == self.mode_spinner.text):
                    file1.write(line)
                    file1.close()
                    file.close()
                    self.manager.transition.direction = "left"
                    self.manager.current = "seepatient"

            '''Search with textinput'''
            file = open("patients.txt", "r")
            file1 = open("findpatient.txt", "w")
            for line in file.readlines():
                if (line[0] == self.option_textinput.text):
                    file1.write(line)
                    file1.close()
                    file.close()
                    self.manager.transition.direction = "left"
                    self.manager.current = "seepatient"

            file1.close()
            file.close()
            self.manager.transition.direction = "left"
            self.manager.current = "main"

class seepatientScreen(Screen):
    '''Check symptoms of the patient in this screen.
        I will have to make multiple screens to display the whole data 
    '''
    def __init__(self, **kwargs):
        super(seepatientScreen, self).__init__(**kwargs)

class removeScreen(Screen):
    title_label = ObjectProperty()
    displayLabel = ObjectProperty()
    password_textinput = ObjectProperty()

    def __init__(self, **kwargs):
        super(removeScreen, self).__init__(**kwargs)
        
    def on_pre_enter(self):
        self.title_label.text = "[b][color=#ffffff]Remove Database[/color][/b]"
        self.displayLabel.text = "[b][color=#000000] Do you want to erase the database?\
        \nRemember all the data will be lost. \nEnter the password to confirm the order: [/color][/b]"
        self.password_textinput.text = ""
        
    def erase_database(self, *args):
        if (self.password_textinput.text == "root"):            
            file = open("patients.txt", "w")
            file.write("")
            file.close()
            self.manager.transition.direction = "left"
            self.manager.current = "main"
        else:
            self.manager.transition.direction = "left"
            self.manager.current = "main"

    def back_to_main(self, *args):
        self.manager.transition.direction = "left"
        self.manager.current = "main"

class reportScreen(Screen):
    '''Two classes inside this screen: Remote Report, Load Samples at Laboratory'''
    title_label = ObjectProperty() 
    
    def __init__(self, **kwargs):
        super(reportScreen, self).__init__(**kwargs)
        self._add_text_inputs()

    def _add_text_inputs(self, *args):
        self.title_label.text = "[b][color=#ffffff]Report[/color][/b]"

    def remote(self, *args):
        self.manager.transition.direction = "left"
        self.manager.current = "remote"

    def unload(self, *args):
        self.manager.transition.direction = "left"
        self.manager.current = "unload"

    def back_to_main(self, *args):
        self.manager.transition.direction = "left"
        self.manager.current = "main"

class remoteScreen(Screen):
    def __init__(self, **kwargs):
        super(remoteScreen, self).__init__(**kwargs)
        self._add_text_inputs()

    def _add_text_inputs(self, *args):
        pass

    def _remote(self, *args):
        pass

    def discard(self, *args):
        self.manager.transition.direction = "left"
        self.manager.current = "main"

class unloadScreen(Screen):
    floor2_label = ObjectProperty()
    floor2_one = ObjectProperty()
    floor2_two = ObjectProperty()
    floor2_three = ObjectProperty()
    floor2_four = ObjectProperty()
    floor2_five = ObjectProperty()
    floor2_six = ObjectProperty()
    floor2_seven = ObjectProperty()
    floor2_eight = ObjectProperty()
    floor2_nine = ObjectProperty()
    floor2_ten = ObjectProperty()

    floor1_label = ObjectProperty()
    floor1_one = ObjectProperty()
    floor1_two = ObjectProperty()
    floor1_three = ObjectProperty()
    floor1_four = ObjectProperty()
    floor1_five = ObjectProperty()
    floor1_six = ObjectProperty()
    floor1_seven = ObjectProperty()
    floor1_eight = ObjectProperty()
    floor1_nine = ObjectProperty()
    floor1_ten = ObjectProperty()

    def __init__(self, **kwargs):
        super(unloadScreen, self).__init__(**kwargs)
        self._add_text_inputs()

    def _add_text_inputs(self, *args):
        self.floor1_label.text = "[b][color=#000000]Floor 1[/color][/b]"
        self.floor2_label.text = "[b][color=#000000]Floor 2[/color][/b]"

        file = open("patients.txt", "r")
        list = []
        for line in file.readlines():
            list.append(line[len(line)-1])
        if (self.floor2_one.text == "1"):
            pass
        file.close()

    def _unload(self, *args):
        pass

    def discard(self, *args):
        self.manager.transition.direction = "left"
        self.manager.current = "main"

def convert_state_toggle_box(convert_state_toggle_box):
    if (convert_state_toggle_box == "normal"):
        return "0"
    elif (convert_state_toggle_box == "down"):
        return "1"

class TBSE(App):
    sm = None  # root screen manager

    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(MainScreen(name="main"))
        
        self.sm.add_widget(addScreen(name="add"))
        self.sm.add_widget(OMRScreen(name="omr"))
        self.sm.add_widget(add2Screen(name="add2"))
        self.sm.add_widget(add3Screen(name="add3"))
        self.sm.add_widget(add4Screen(name="add4"))
        self.sm.add_widget(add5Screen(name="add5"))
        self.sm.add_widget(resultScreen(name="result"))
        
        self.sm.add_widget(takesputumsampleScreen(name="takesputumsample"))
        self.sm.add_widget(takesputumsample1Screen(name="takesputumsample1"))
        self.sm.add_widget(takesputumsample2Screen(name="takesputumsample2"))
        self.sm.add_widget(takesputumsample3Screen(name="takesputumsample3"))
        self.sm.add_widget(takesputumsample4Screen(name="takesputumsample4"))

        self.sm.add_widget(addObjectBoxScreen(name="addObjectBox"))

        self.sm.add_widget(viewScreen(name="view"))
        self.sm.add_widget(seepatientScreen(name="seepatient"))

        self.sm.add_widget(removeScreen(name="remove"))

        self.sm.add_widget(reportScreen(name="report"))
        self.sm.add_widget(remoteScreen(name="remote"))
        self.sm.add_widget(unloadScreen(name="unload"))

        self.sm.current = "main"

        return self.sm

if __name__ == "__main__":
    """Initialize serial port"""
    #try:
    #   port = serial.Serial("/dev/ttyUSB0", baudrate = 115200, timeout = 3.0)
    #except:
    #   print "Connection failed"
    #   exit()
    TBSE().run()
    
    #port.close()