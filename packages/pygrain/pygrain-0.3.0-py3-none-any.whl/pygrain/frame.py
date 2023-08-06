from .component import Component
from collections import defaultdict


class Frame(Component):
    """
    Class for a collection of components.
    """
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.components = []
        parent.switch_frame(self)

    def event(self, events, events_done=None):
        """
        Pass events to all sub-components inside the frame.
        :param events_done:
        :param events:
        :return: if events was valid for any component
        """
        if events_done is None:
            events_done = set()
        for component in self.components[::-1]:
            component.event(events, events_done=events_done)

        return super().event(events, events_done=events_done)

    def draw(self, screen):
        """
        Draw frame and all sub-components from bottom to top order.
        :param screen:
        :return: None
        """
        super().draw(screen)
        for component in self.components:
            component.draw(screen)

    def add_component(self, component):
        """
        Add new component to the front of list.
        :param component: Component
        :return: None
        """
        self.components.append(component)

    def get_components(self):
        return self.components

    def update(self):
        """
        Update parent component (or App).
        :return:
        """
        self.parent.update()

