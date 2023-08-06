import io
import logging
import sys

from kivy import Config
Config.set('graphics', 'multisamples', '0')
import os
# os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'
# os.environ['KIVY_GL_BACKEND'] = 'gl'
import kivy.app
import kivy.uix.button
import kivy.uix.image
import kivy.uix.scatter
import PIL


class KivyApp(kivy.app.App):
    def __init__(self, title: str, filename: str, *args, **kwargs):
        super(KivyApp, self).__init__(*args, **kwargs)
        self.title = title
        self.filename = filename
        self._log = logging.getLogger(__name__)
        self.nick_canvas = None

    def set_pil_image(self, image: PIL.Image.Image):
        data = io.BytesIO()
        image.save(data, format='png')
        im = kivy.core.image.Image(data, ext="png")
        self.set_image(im)

    def set_image(self, image):
        self.nick_canvas.add_widget(kivy.uix.image(texture=image.texture))

    def build(self):
        print('build')
        try:
            self.nick_canvas = kivy.uix.scatter.Scatter()
        except BaseException as e:
            self._log.exception(e)
        print('scatter')
        return self.nick_canvas

    def on_touch_down(self, touch):
        self._log.debug(f'Touch down: {touch}')
        return False

    def on_touch_up(self, touch):
        self._log.debug(f'Touch up: {touch}')
        return False


class MyApp(kivy.app.App):
    def build(self):
        return kivy.uix.button.Button(label='Nick')


if __name__ == '__main__':
    MyApp().run()
    app = KivyApp('Loading...', sys.argv[1])
    app.run()
    app.set_pil_image(PIL.Image.open(sys.argv[1]))
