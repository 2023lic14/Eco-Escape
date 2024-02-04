# radio_button.py

from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.properties import BooleanProperty
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.metrics import dp

class RadioImageButton(Image):
    def __init__(self, original_size=(200, 200), original_pos=(400, 400), **kwargs):
        super(RadioImageButton, self).__init__(**kwargs)

        self.original_image_normal = 'radiostart.png'
        self.new_image_normal = 'radio.png'
        self.is_unlocked = BooleanProperty(False)
        self.click_counter = 0  # Track the number of clicks
        self.key_sequence = []  # Track the key sequence

        self.original_size = original_size
        self.original_pos = original_pos

        self.source = self.original_image_normal
        self.pos = self.original_pos
        self.size = self.original_size

        # Create two buttons with the same behavior as the textbox
        self.button_up = Button(text="Up", size_hint=(None, None), size=(150, 60), pos=(-1000, -1000))
        self.button_down = Button(text="Down", size_hint=(None, None), size=(150, 60), pos=(-1000, -1000))
        self.add_widget(self.button_up)
        self.add_widget(self.button_down)
        self.button_up.opacity = 0
        self.button_down.opacity = 0

        # Create a text box for displaying messages
        self.textbox = Button(text="", size_hint=(None, None), size=(300, 60), pos=(-1000, -1000))
        self.add_widget(self.textbox)
        self.textbox.opacity = 0

        # Bind button events
        self.button_up.bind(on_press=self.on_button_up_press)
        self.button_down.bind(on_press=self.on_button_down_press)

        # Bind keyboard events
        Window.bind(on_key_down=self.on_key_down)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.toggle_unlock_mode()
            return True
        return super(RadioImageButton, self).on_touch_down(touch)

    def toggle_unlock_mode(self):
        self.click_counter += 1

        if self.click_counter % 2 == 1:  # Show the buttons on odd clicks (third, fifth, etc.)
            self.source = self.new_image_normal
            new_size = (4000, 4000)  # Adjust the values for a larger size
            self.size_hint = (None, None)
            self.size = new_size
            self.pos = ((Window.width - new_size[0]) / 2, (Window.height - new_size[1]) / 2)
            self.button_up.pos = (Window.width / 2 - self.button_up.width, Window.height / 2 - 400)
            self.button_down.pos = (Window.width / 2, Window.height / 2 - 400)
            self.button_up.opacity = 1
            self.button_down.opacity = 1
            self.is_unlocked = True
        else:  # Hide the buttons on even clicks (fourth, sixth, etc.)
            self.source = self.original_image_normal
            self.size_hint = (None, None)
            self.size = self.original_size
            self.pos = self.original_pos
            self.button_up.opacity = 0
            self.button_down.opacity = 0
            self.textbox.opacity = 0
            self.is_unlocked = False
            self.key_sequence = []  # Reset key sequence on hiding

    def on_button_down_press(self, instance):
        if instance.text == "Down":
            self.key_sequence.append("Down")
            self.check_key_sequence()

    def on_button_up_press(self, instance):
        if instance.text == "Up":
            self.key_sequence.append("Up")
            self.check_key_sequence()

    def on_key_down(self, keyboard, keycode, text, modifiers, _):
        if self.is_unlocked:
            if keycode in [274, 273]:  # Handle only "down" (274) and "up" (273) arrow keys
                self.key_sequence.append(keycode)
                self.check_key_sequence()

    def check_key_sequence(self):
        print("Entered key sequence:", self.key_sequence)  # Add this line for debugging

        if len(self.key_sequence) == 4:
            if self.key_sequence == [274, 274, 273, 273]:  # Check for "down", "down", "up", "up"
                self.textbox.text = "Correct!"
                Clock.schedule_once(self.hide_confirmation, 3)  # Schedule hiding confirmation after 3 seconds
                Clock.schedule_once(self.show_additional_text, 3)  # Schedule showing additional text after 3 seconds
            else:
                self.textbox.text = "Incorrect!"

            # Show the text box
            self.textbox.pos = (Window.width / 2 - self.textbox.width / 2,
                                Window.height / 2 - self.textbox.height / 2 - 300)
            self.textbox.opacity = 1
            # Reset key sequence after displaying the message
            self.key_sequence = []

    def hide_confirmation(self, dt):
        # Hide the confirmation text box
        self.textbox.opacity = 0

    def show_additional_text(self, dt):
        # Show the additional text
        additional_text = "Seven-hundred species are endangered because of ocean plastic pollution..."
        self.textbox.text = additional_text
        text_width = dp(len(additional_text)) * 8  # Assuming an average character width of 8dp
        text_height = 100  # Set an appropriate height
        self.textbox.size = (text_width, text_height)
        self.textbox.pos = (Window.width / 2 - text_width / 2,
                            Window.height / 2 - text_height / 2 - 200)  # Move up by 200 pixels
        self.textbox.opacity = 1
        Clock.schedule_once(self.hide_additional_text, 3)  # Schedule hiding additional text after 3 seconds

    def hide_additional_text(self, dt):
        # Hide the additional text
        self.textbox.opacity = 0

