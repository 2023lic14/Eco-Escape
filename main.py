from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.clock import Clock
from radio_button import RadioImageButton  # Import the new class
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Rectangle, Color
from kivy.animation import Animation
from kivy.uix.boxlayout import BoxLayout

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
        self.door_image = Image(source='scissors.png', size=(500, 500), pos=(300, 200), opacity=0)
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
        self.second_toolbox_unlocked = False

        # State variable to track whether the correct passcode has been entered for the first time
        self.first_time_unlock = True

        self.second_toolbox_button = ToolboxButton(size_hint=(None, None), size=(256, 256), pos=(1700, 100),
                                                   background_normal='fish.png',
                                                   background_down='hook.png')
        self.second_toolbox_button.bind(on_press=self.toggle_second_unlock_mode)
        layout.add_widget(self.second_toolbox_button)

        self.success_text_box_layout = BoxLayout(orientation='vertical', size_hint=(None, None),
                                                 size=(400, 0), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.success_text_box = TextInput(text="You escaped! Learn more about conservation on out website!", multiline=True,
                                          readonly=True, font_size=40, background_color=(0, 0, 0, 0))
        # Bind the height of the TextBox to its content
        self.success_text_box.bind(height=self.adjust_text_box_size)
        self.success_text_box_layout.add_widget(self.success_text_box)
        self.success_text_box_layout.opacity = 0  # Initially hide the success TextBox
        layout.add_widget(self.success_text_box_layout)

        initial_text_label = Label(text="A fishnet... I need to get out of here...",
                                   font_size=20, size_hint=(None, None), size=(400, 100),
                                   pos_hint={'center_x': 0.5, 'center_y': 0.5})
        layout.add_widget(initial_text_label)

        # Schedule a function to hide the initial story Label after 10 seconds
        Clock.schedule_once(lambda dt: self.hide_initial_text_label(initial_text_label), 10.0)

        # ... (rest of your layout)

        return layout

    def hide_initial_text_label(self, label):
        # Hide the initial story Label
        label.opacity = 0

    def adjust_text_box_size(self, instance, value):
        # Adjust the size of the TextBox layout based on its content height
        instance.parent.size = (400, value)

    def toggle_second_unlock_mode(self, instance):
        # Similar logic to toggle_unlock_mode but for the second toolbox button
        if not self.second_toolbox_unlocked:
            # Update the appearance and position of the second toolbox
            instance.background_normal = 'hook.png'
            instance.size = (1500, 1500)  # New size
            instance.pos = (50, 0)  # New position
            # Hide the text input if the image is changing to 'hook.png'
            if instance.background_normal == 'hook.png':
                self.text_input.pos = (-1000, -1000)
                self.text_input.text = ''
            else:
                # Show the TextInput for the second toolbox
                self.text_input.pos = (instance.pos[0] + instance.width + 10, instance.pos[1])
                self.text_input.focus = True
            self.second_toolbox_unlocked = True
            # Hide the radio button
            self.radio_button.opacity = 0

            # Schedule a function to revert the appearance after 5 seconds
            Clock.schedule_once(lambda dt: self.revert_toolbox_appearance(instance), 5.0)

    def revert_toolbox_appearance(self, instance):
        # Revert the appearance of the second toolbox to its original state 'fish.png'
        instance.background_normal = 'fish.png'
        instance.size = (256, 256)  # Original size
        instance.pos = (1700, 300)  # Original position
        self.second_toolbox_unlocked = False
        # Show the radio button
        self.radio_button.opacity = 1

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
            # Hide the door image if it's not the first time
            if not self.first_time_unlock:
                self.door_image.opacity = 0
            self.toolbox_unlocked = False
            # Make the radio button visible
            self.radio_button.opacity = 1
        else:
            # Update the door appearance and position
            instance.background_normal = 'closerToolbox.png'
            instance.size = (1500, 1500)  # New size
            instance.pos = (50, 0)  # New position
            # Show the TextInput
            self.text_input.pos = (instance.pos[0] + instance.width + 10, instance.pos[1])
            self.text_input.focus = True
            self.toolbox_unlocked = True
            # Hide the radio button
            self.radio_button.opacity = 0

    def adjust_text_box_size(self, instance, value):
        # Adjust the size of the TextBox layout based on the content height
        self.success_text_box_layout.height = self.success_text_box.minimum_height

    def check_passcode(self, instance):
        # Check the entered passcode
        passcode = instance.text
        if passcode == '700':  # Replace 'your_passcode' with the actual passcode
            self.passcode_label.text = 'Correct passcode!'
            # Add your logic for unlocking the door or performing other actions
            # Show the door image
            # self.door_image.opacity = 1
            if self.first_time_unlock:
                self.door_image.opacity = 1
                self.first_time_unlock = False
                # Schedule a function to hide the door image after 3 seconds (adjust as needed)
                Clock.schedule_once(self.hide_door_image, 3.0)

                # Display the success TextBox after 3 seconds
                Clock.schedule_once(self.display_success_text_box, 3.0)
            else:
                self.passcode_label.text = 'Incorrect passcode!'
                # Add your logic for handling incorrect passcode

    def display_success_text_box(self, dt):
        # Display the success TextBox
        self.success_text_box_layout.opacity = 1

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
