# radio_button.py

from kivy.uix.image import Image
from kivy.properties import BooleanProperty
from kivy.uix.textinput import TextInput
from kivy.core.window import Window

class RadioImageButton(Image):
    def __init__(self, original_size=(200, 200), original_pos=(400, 400), **kwargs):
        super(RadioImageButton, self).__init__(**kwargs)

        self.original_image_normal = 'radiostart.png'
        self.new_image_normal = 'radio.png'
        self.is_unlocked = BooleanProperty(False)
        self.click_counter = 0  # Track the number of clicks

        self.original_size = original_size
        self.original_pos = original_pos

        self.source = self.original_image_normal
        self.pos = self.original_pos
        self.size = self.original_size

        # Create a separate TextInput for the textbox
        self.textbox = TextInput(text="Press the correct keys on your keyboard.", readonly=True,
                                 size_hint=(None, None), size=(300, 60), pos=(-1000, -1000))
        self.add_widget(self.textbox)  # Add the textbox initially
        self.textbox.opacity = 0  # Hide the textbox initially

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.toggle_unlock_mode()
            return True
        return super(RadioImageButton, self).on_touch_down(touch)

    def toggle_unlock_mode(self):
        self.click_counter += 1

        if self.click_counter % 2 == 1:  # Show the textbox on odd clicks (third, fifth, etc.)
            self.source = self.new_image_normal
            new_size = (4000, 4000)  # Adjust the values for a larger size
            self.size_hint = (None, None)
            self.size = new_size
            self.pos = ((Window.width - new_size[0]) / 2, (Window.height - new_size[1]) / 2)
            self.textbox.pos = (Window.width / 2 - self.textbox.width / 2,
                                Window.height / 2 - self.textbox.height / 2 - 200)  # Move 200 pixels lower
            self.textbox.opacity = 1
            self.is_unlocked = True
        else:  # Hide the textbox on even clicks (fourth, sixth, etc.)
            self.source = self.original_image_normal
            self.size_hint = (None, None)
            self.size = self.original_size
            self.pos = self.original_pos
            self.textbox.opacity = 0
            self.is_unlocked = False
