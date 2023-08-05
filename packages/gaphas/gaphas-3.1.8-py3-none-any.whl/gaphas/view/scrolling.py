from typing import Callable, Optional

from gi.repository import Gtk

from gaphas.decorators import g_async
from gaphas.geometry import Rectangle
from gaphas.matrix import Matrix


class Scrolling:
    """Contains Gtk.Adjustment and related code."""

    def __init__(self, scrolling_updated: Callable[[Matrix], None]) -> None:
        self._scrolling_updated = scrolling_updated
        self.hadjustment: Optional[Gtk.Adjustment] = None
        self.vadjustment: Optional[Gtk.Adjustment] = None
        self.hscroll_policy: Optional[Gtk.ScrollablePolicy] = None
        self.vscroll_policy: Optional[Gtk.ScrollablePolicy] = None
        self._hadjustment_handler_id = 0
        self._vadjustment_handler_id = 0
        self._last_hvalue = 0.0
        self._last_vvalue = 0.0

    def get_property(self, prop):
        if prop.name == "hadjustment":
            return self.hadjustment
        elif prop.name == "vadjustment":
            return self.vadjustment
        elif prop.name == "hscroll-policy":
            return self.hscroll_policy
        elif prop.name == "vscroll-policy":
            return self.vscroll_policy
        else:
            raise AttributeError(f"Unknown property {prop.name}")

    def set_property(self, prop, value):
        if prop.name == "hadjustment":
            if value is not None:
                self.hadjustment = value
                self._hadjustment_handler_id = self.hadjustment.connect(
                    "value-changed", self.on_adjustment_changed
                )
                self._scrolling_updated(Matrix())
        elif prop.name == "vadjustment":
            if value is not None:
                self.vadjustment = value
                self._vadjustment_handler_id = self.vadjustment.connect(
                    "value-changed", self.on_adjustment_changed
                )
                self._scrolling_updated(Matrix())
        elif prop.name == "hscroll-policy":
            self.hscroll_policy = value
        elif prop.name == "vscroll-policy":
            self.vscroll_policy = value
        else:
            raise AttributeError(f"Unknown property {prop.name}")

    @g_async(single=True)
    def update_adjustments(self, width, height, bounds):
        # canvas limits (in view coordinates)
        c = Rectangle(*bounds)
        c.x -= width * 0.7
        c.width += width * 1.4
        c.y -= height * 0.7
        c.height += height * 1.4

        # view limits
        v = Rectangle(0, 0, width, height)

        # union of these limits gives scrollbar limits
        u = c if v in c else c + v
        if self.hadjustment:
            self.hadjustment.set_value(v.x)
            self.hadjustment.set_lower(u.x)
            self.hadjustment.set_upper(u.x1)
            self.hadjustment.set_step_increment(width // 10)
            self.hadjustment.set_page_increment(width)
            self.hadjustment.set_page_size(width)

        if self.vadjustment:
            self.vadjustment.set_value(v.y)
            self.vadjustment.set_lower(u.y)
            self.vadjustment.set_upper(u.y1)
            self.vadjustment.set_step_increment(height // 10)
            self.vadjustment.set_page_increment(height)
            self.vadjustment.set_page_size(height)

        self._last_hvalue = v.x
        self._last_vvalue = v.y

    def on_adjustment_changed(self, adj):
        """Change the transformation matrix of the view to reflect the value of
        the x/y adjustment (scrollbar)."""
        value = adj.get_value()
        if value == 0.0:
            return

        m = Matrix()
        if adj is self.hadjustment:
            m.translate(self._last_hvalue - value, 0)
            self._last_hvalue = value
        elif adj is self.vadjustment:
            m.translate(0, self._last_vvalue - value)
            self._last_vvalue = value

        self._scrolling_updated(m)
