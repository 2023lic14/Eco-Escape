# radio_button.py

from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import BooleanProperty
from kivy.core.window import Window

class RadioImageButton(Image):
    def __init__(self, original_size=(200, 200), original_pos=(400, 400), **kwargs):
        super(RadioImageButton, self).__init__(**kwargs)
        self.original_image_normal = 'radiostart.png'
        self.new_image_normal = 'radio.png'
        self.is_unlocked = BooleanProperty(False)

        self.original_size = original_size
        self.original_pos = original_pos

        self.source = self.original_image_normal
        self.pos = self.original_pos
        self.size = self.original_size

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.toggle_unlock_mode()
            return True
        return super(RadioImageButton, self).on_touch_down(touch)

    def toggle_unlock_mode(self):
        if self.is_unlocked:
            self.source = self.original_image_normal
            self.size_hint = (None, None)
            self.size = self.original_size
            self.pos = self.original_pos
        else:
            self.source = self.new_image_normal
            new_size = (4000, 4000)  # Adjust the values for a larger size
            self.size_hint = (None, None)
            self.size = new_size
            self.pos = ((Window.width - new_size[0]) / 2, (Window.height - new_size[1]) / 2)

        self.is_unlocked = not self.is_unlocked


