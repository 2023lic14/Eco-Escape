from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.clock import Clock
from radio_button import RadioImageButton  # Import the new class

class ToolboxButton(Button):
    def __init__(self, passcode_callback=None, **kwargs):
        super(ToolboxButton, self).__init__(**kwargs)
        self.original_size = kwargs.get('size', (256, 256))  # Save the original size
        self.original_image_normal = kwargs.get('background_normal', 'toolbox.png')  # Save the original image
        self.original_image_down = kwargs.get('background_down', 'closerToolbox.png')  # Save the original image
        self.background_normal = self.original_image_normal
        self.background_down = self.original_image_down
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
        self.toolbox_button.bind(on_press=self.toggle_unlock_mode)
        layout.add_widget(self.toolbox_button)

        # Add the door image with adjusted position
        self.door_image = Image(source='scissors.png', size=(500, 500), pos=(600, 300), opacity=0)
        layout.add_widget(self.door_image)

        # Add the new image button (using RadioImageButton instead of RadioButton)
        self.radio_button = RadioImageButton(size_hint=(None, None), size=(200, 200), pos=(400, 400))
        self.radio_button.bind(on_press=self.on_radio_button_press)
        layout.add_widget(self.radio_button)

        # Initialize TextInput as an instance variable and hide it initially
        self.text_input = TextInput(hint_text='Type in the code', multiline=False,
                                     size_hint=(None, None), size=(300, 60), pos=(-1000, -1000))
        self.text_input.bind(on_text_validate=self.check_passcode)  # Bind on_text_validate event
        layout.add_widget(self.text_input)

        # Set the aspect ratio for the window
        Window.size = (800, 600)  # Set your desired width and height here

        # Add a Label to display passcode confirmation
        self.passcode_label = Label(text='', pos=(400, 500), font_size=50)
        layout.add_widget(self.passcode_label)

        # State variable to track whether the toolbox is unlocked
        self.toolbox_unlocked = False

        # State variable to track whether the correct passcode has been entered for the first time
        self.first_time_unlock = True

        return layout

    def toggle_unlock_mode(self, instance):
        if self.toolbox_unlocked:
            # Move the toolbox back to the original position
            self.toolbox_button.pos = (100, 700)
            # Reset the size and image properties
            self.toolbox_button.size = self.toolbox_button.original_size
            self.toolbox_button.background_normal = self.toolbox_button.original_image_normal
            self.toolbox_button.background_down = self.toolbox_button.original_image_down
            self.toolbox_unlocked = False
            # Hide the TextInput
            self.text_input.pos = (-1000, -1000)
            self.text_input.text = ''
            # Hide the door image
            #self.door_image.opacity = 0
            #self.toolbox_unlocked = False
            # Hide the door image if it's not the first time
            if not self.first_time_unlock:
                self.door_image.opacity = 0
            self.toolbox_unlocked = False
        else:
            # Update the door appearance and position
            instance.background_normal = 'closerToolbox.png'
            instance.size = (1500, 1500)  # New size
            instance.pos = (50, 0)  # New position
            # Show the TextInput
            self.text_input.pos = (instance.pos[0] + instance.width + 10, instance.pos[1])
            self.text_input.focus = True
            self.toolbox_unlocked = True

    def check_passcode(self, instance):
        # Check the entered passcode
        passcode = instance.text
        if passcode == '12345':  # Replace 'your_passcode' with the actual passcode
            self.passcode_label.text = 'Correct passcode!'
            # Add your logic for unlocking the door or performing other actions
            # Show the door image
            #self.door_image.opacity = 1
            if self.first_time_unlock:
                self.door_image.opacity = 1
                self.first_time_unlock = False
                # Schedule a function to hide the door image after 3 seconds (adjust as needed)
            Clock.schedule_once(self.hide_door_image, 3.0)

        else:
            self.passcode_label.text = 'Incorrect passcode!'
            # Add your logic for handling incorrect passcode

        # Reset the TextInput position
        #instance.pos = (-1000, -1000)
        #instance.text = ''

        # Show the passcode confirmation label
        self.passcode_label.pos = (0, -500)

        Clock.schedule_once(self.reset_confirmation_label, 3.0)

    def reset_confirmation_label(self, dt):
        # Reset the text of the confirmation label
        self.passcode_label.text = ''

    #def hide_door_image(self, dt):
        # Hide the door image
        #self.door_image.opacity = 0
    def hide_door_image(self, dt):
        # Hide the door image if it's not the first time
        if not self.first_time_unlock:
            self.door_image.opacity = 0

    def on_radio_button_press(self, instance):
        instance.toggle_unlock_mode()  # Toggle between states
        parent = instance.parent
        parent.remove_widget(instance)
        parent.add_widget(instance)


if __name__ == '__main__':
    EscapeRoomApp().run()
