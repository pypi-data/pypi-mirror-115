from .frame import Frame
from .box import Box


class ScrollBar(Frame):
    def __init__(self, parent, scroll_height, **kwargs):
        super().__init__(parent,
                         x=lambda: parent.get_property('width') * 0.98,
                         width=lambda: parent.get_property('width') * 0.02,
                         height=lambda: parent.get_property('height'),
                         border_thickness=2,
                         fixed_x=True,
                         **kwargs)
        self.scroll_height = scroll_height
        self.box = Box(self, x=0, y=0,
                       width=lambda: self.get_property('width'),
                       height=lambda: self.get_property('height') * parent.get_property('height') / self.get_property('scroll_height'),
                       bg_colour=(100, 100, 100),
                       draggable=True,
                       fixed_x=True)
        self.bind_scroll_events()
        self.previous_y = 0

    def draw(self, screen):
        super().draw(screen)
        self.box.draw(screen)

    def scroll(self):
        if not self.box.get_property('dragging'):
            return False

        y = self.box.get_property('y')
        height = self.get_property('height')
        scroll_height = self.get_property('scroll_height')
        previous_y = self.get_property('previous_y')
        dy = (y - previous_y) * (scroll_height / height)
        self.set_previous_y(y)

        for component in self.parent.get_components():
            if component is self:
                continue
            y = component.get_property('y')
            component.set_y(y - dy)

        return True

    def set_previous_y(self, y):
        self.previous_y = y
        return self

    def bind_scroll_events(self):
        self.box.bind('mousemotion', lambda target: self.scroll())