from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.label import Label

class ToolboxButton(Button):
    def __init__(self, passcode_callback=None, **kwargs):
        super(ToolboxButton, self).__init__(**kwargs)
        self.background_normal = 'toolbox.png'
        self.background_down = 'closerToolbox.png'
        self.passcode_callback = passcode_callback

    def on_press(self):
        super(ToolboxButton, self).on_press()
        if self.passcode_callback and callable(self.passcode_callback):
            self.passcode_callback()

class EscapeRoomApp(App):
    def build(self):
        # Create the main layout
        layout = FloatLayout()

        # Add the background image
        background = Image(source='oceanbg.jpg', size=(1920, 1080), allow_stretch=True)
        layout.add_widget(background)

        # Add the toolbox button with adjusted position
        self.toolbox_button = ToolboxButton(size_hint=(None, None), size=(256, 256), pos=(100, 700))
        self.toolbox_button.bind(on_press=self.unlock_mode)
        layout.add_widget(self.toolbox_button)

        # Initialize TextInput as an instance variable and hide it initially
        self.text_input = TextInput(hint_text='Type in the code', multiline=False,
                                     size_hint=(None, None), size=(300, 60), pos=(-1000, -1000))
        self.text_input.bind(on_text_validate=self.check_passcode)  # Bind on_text_validate event
        layout.add_widget(self.text_input)

        # Set the aspect ratio for the window
        Window.size = (800, 600)  # Set your desired width and height here

        # Add a Label to display passcode confirmation
        self.passcode_label = Label(text='', pos=(400, 500), font_size=20)
        layout.add_widget(self.passcode_label)

        return layout

    def check_passcode(self, instance):
        # Check the entered passcode
        passcode = instance.text
        if passcode == 'your_passcode':  # Replace 'your_passcode' with the actual passcode
            self.passcode_label.text = 'Correct passcode!'
            # Add your logic for unlocking the door or performing other actions
        else:
            self.passcode_label.text = 'Incorrect passcode!'
            # Add your logic for handling incorrect passcode

        # Reset the TextInput position
        instance.pos = (-1000, -1000)
        instance.text = ''

        # Show the passcode confirmation label
        self.passcode_label.pos = (650, 190)

    def unlock_mode(self, instance):
        # Update the door appearance and position
        instance.background_normal = 'closerToolbox.png'
        instance.size = (1500, 1500)  # New size
        instance.pos = (50, 0)  # New position

        # Show the TextInput
        self.text_input.pos = (650, 200)
        self.text_input.focus = True

if __name__ == '__main__':
    EscapeRoomApp().run()