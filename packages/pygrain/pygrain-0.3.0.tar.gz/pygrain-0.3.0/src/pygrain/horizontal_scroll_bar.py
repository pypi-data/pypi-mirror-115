from .frame import Frame
from .box import Box


class HorizontalScrollBar(Frame):
    def __init__(self, parent, scroll_width, **kwargs):
        super().__init__(parent,
                         x=0,
                         y=lambda: parent.get_property('height') * 0.98,
                         height=lambda: parent.get_property('height') * 0.02,
                         width=lambda: parent.get_property('width'),
                         border_thickness=2,
                         fixed_y=True,
                         **kwargs)
        self.scroll_width = scroll_width
        self.box = Box(self, x=0, y=0,
                       height=lambda: self.get_property('height'),
                       width=lambda: self.get_property('width') * parent.get_property('width') / self.get_property('scroll_width'),
                       bg_colour=(100, 100, 100),
                       draggable=True,
                       fixed_y=True)
        self.bind_scroll_events()
        self.previous_x = 0

    def draw(self, screen):
        super().draw(screen)
        self.box.draw(screen)

    def scroll(self):
        if not self.box.get_property('dragging'):
            return False

        x = self.box.get_property('x')
        width = self.get_property('width')
        scroll_width = self.get_property('scroll_width')
        previous_x = self.get_property('previous_x')
        dx = (x - previous_x) * (scroll_width / width)
        self.set_previous_x(x)

        for component in self.parent.get_components():
            if component is self:
                continue
            x = component.get_property('x')
            component.set_x(x - dx)

        return True

    def set_previous_x(self, x):
        self.previous_x = x
        return self

    def bind_scroll_events(self):
        self.box.bind('mousemotion', lambda target: self.scroll())