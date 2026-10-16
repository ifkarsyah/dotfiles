"""Reusable visual building blocks for narrated technical explainers.

Each component is a Manim VGroup. Methods that change what a viewer sees
return animations rather than playing them, so scenes stay in control of
timing:

    self.play(log.append(packet))
"""

from __future__ import annotations

from manim import (
    DOWN, LEFT, RIGHT, UP, UL,
    AnimationGroup, Circle, Create, Cross, DashedVMobject, Dot, FadeIn,
    FadeOut, Line, RoundedRectangle, Rectangle, Text,
    Transform, VGroup, Arrow, Indicate,
)

from . import style as S

# Draw order. Manim renders by z_index first, so an animated panel can never
# jump in front of the content it contains.
Z_PANEL, Z_CELL, Z_TEXT, Z_TOKEN, Z_PACKET, Z_ALERT = -3, -2, 0, 1, 2, 4


# ======================================================================= text

def txt(s: str, size: int = S.BODY_SIZE, color: str = S.INK, mono: bool = False,
        weight: str = "NORMAL") -> Text:
    """Single source of truth for on-screen text."""
    return Text(s, font=S.MONO if mono else S.FONT, font_size=size,
                color=color, weight=weight)


def chapter_title(number: int, title: str) -> VGroup:
    """Small top-left chapter marker: 'CH 2  Producer-side problems'."""
    num = txt(f"CH {number}", S.SMALL_SIZE, S.MUTED, weight="BOLD")
    name = txt(title, S.LABEL_SIZE, S.INK, weight="BOLD")
    g = VGroup(num, name).arrange(RIGHT, buff=0.25)
    g.to_corner(UL, buff=0.4)
    return g


def caption(s: str, y: float = S.CAPTION_Y, size: int = S.LABEL_SIZE,
            color: str = S.MUTED) -> Text:
    """One-line statement of what the current animation teaches."""
    return txt(s, size, color).move_to([0, y, 0])


def takeaway(s: str, color: str = S.INK) -> VGroup:
    """Boxed key idea, shown in the bottom band."""
    t = txt(s, S.BODY_SIZE, color, weight="BOLD")
    box = RoundedRectangle(corner_radius=0.12, width=t.width + 0.6,
                           height=t.height + 0.4, stroke_color=color,
                           stroke_width=2, fill_color=S.PANEL, fill_opacity=1)
    g = VGroup(box, t)
    t.move_to(box)
    g.move_to([0, S.BOTTOM_BAND_Y - 0.6, 0])
    return g


def config_chip(s: str, color: str = S.MUTED) -> VGroup:
    """Pill showing a configuration value, e.g. 'acks=all'."""
    t = txt(s, S.TINY_SIZE, color, mono=True)
    pill = RoundedRectangle(corner_radius=0.14, width=t.width + 0.3,
                            height=t.height + 0.18, stroke_color=color,
                            stroke_width=1.5, fill_color=S.BG, fill_opacity=1)
    t.move_to(pill)
    return VGroup(pill, t)


# ================================================================= components

class ComponentBox(VGroup):
    """A pipeline component: outlined panel with a title on top."""

    def __init__(self, name: str, hue: str, width: float = 2.4,
                 height: float = 1.6, subtitle: str | None = None):
        super().__init__()
        self.hue = hue
        self.panel = RoundedRectangle(corner_radius=0.15, width=width,
                                      height=height, stroke_color=hue,
                                      stroke_width=2.5, fill_color=S.PANEL,
                                      fill_opacity=1)
        self.panel.set_z_index(Z_PANEL)
        self.title = txt(name, S.LABEL_SIZE, hue, weight="BOLD")
        self.title.next_to(self.panel.get_top(), DOWN, buff=0.14)
        self.add(self.panel, self.title)
        if subtitle:
            self.subtitle = txt(subtitle, S.TINY_SIZE, S.MUTED)
            self.subtitle.next_to(self.title, DOWN, buff=0.06)
            self.add(self.subtitle)
        self._cross = None

    def crash(self):
        """Red outline and a cross. Returns an animation."""
        self._cross = Cross(self.panel, stroke_color=S.FAILURE,
                            stroke_width=5).scale(0.55).set_z_index(Z_ALERT)
        return AnimationGroup(
            self.panel.animate.set_stroke(S.FAILURE),
            Create(self._cross),
        )

    def recover(self):
        """Back to normal, in the recovery color first."""
        anims = [self.panel.animate.set_stroke(S.RECOVERY)]
        if self._cross is not None:
            anims.append(FadeOut(self._cross))
            self._cross = None
        return AnimationGroup(*anims)

    def flash(self, color: str = S.INK):
        return Indicate(self.panel, color=color, scale_factor=1.04)


class EventPacket(VGroup):
    """An event tile. `fields` are shown as 'key value' lines under the id."""

    def __init__(self, event_id: str, fields: dict | None = None,
                 color: str = S.NORMAL, width: float | None = None):
        super().__init__()
        self.event_id = event_id
        self.color = color
        lines = [txt(event_id, S.SMALL_SIZE, S.INK, mono=True, weight="BOLD")]
        for k, v in (fields or {}).items():
            lines.append(txt(f"{k} {v}", S.TINY_SIZE, S.MUTED, mono=True))
        self.body = VGroup(*lines).arrange(DOWN, buff=0.06, aligned_edge=LEFT)
        w = width or max(self.body.width + 0.3, 0.9)
        self.tile = RoundedRectangle(corner_radius=0.08, width=w,
                                     height=self.body.height + 0.24,
                                     stroke_color=color, stroke_width=2.5,
                                     fill_color=S.BG, fill_opacity=1)
        self.body.move_to(self.tile)
        self.tile.set_z_index(Z_PACKET)
        self.body.set_z_index(Z_PACKET + 1)
        self.add(self.tile, self.body)

    def recolor(self, color: str):
        self.color = color
        return self.tile.animate.set_stroke(color)

    def duplicate_outline(self):
        """Dashed magenta outline: duplicates read even without color."""
        dashed = DashedVMobject(
            RoundedRectangle(corner_radius=0.1, width=self.tile.width + 0.16,
                             height=self.tile.height + 0.16)
            .move_to(self.tile).set_stroke(S.DUPLICATE, 2.5),
            num_dashes=24)
        return dashed


def token(color: str = S.NORMAL, size: float = 0.22) -> RoundedRectangle:
    """Tiny event marker for dense scenes (logs, queues)."""
    return RoundedRectangle(corner_radius=0.04, width=size, height=size,
                            stroke_width=0, fill_color=color,
                            fill_opacity=1).set_z_index(Z_TOKEN)


class PartitionLog(VGroup):  # generic: any append-only log / queue
    """Append-only log: a row of cells with offsets underneath.

    `start_offset` lets a log start mid-stream (offset 40 rather than 0) so the
    viewer understands that offsets are positions, not counts.
    """

    def __init__(self, name: str, n_cells: int = 6, start_offset: int = 0,
                 filled: int = 0, cell: float = 0.42, hue: str = S.HUE_B,
                 fill_color: str = S.MUTED):
        super().__init__()
        self.start_offset = start_offset
        self.cells = VGroup(*[
            Rectangle(width=cell, height=cell, stroke_color=S.FAINT,
                      stroke_width=2, fill_color=S.BG, fill_opacity=1)
            .set_z_index(Z_CELL)
            for _ in range(n_cells)
        ]).arrange(RIGHT, buff=0)
        self.offsets = VGroup(*[
            txt(str(start_offset + i), S.TINY_SIZE, S.MUTED, mono=True)
            .next_to(c, DOWN, buff=0.08)
            for i, c in enumerate(self.cells)
        ])
        self.name = txt(name, S.SMALL_SIZE, hue, mono=True)
        self.name.next_to(self.cells, LEFT, buff=0.18)
        self.add(self.name, self.cells, self.offsets)
        self.entries: list = []
        for i in range(filled):
            t = token(fill_color, cell * 0.62).move_to(self.cells[i])
            self.entries.append(t)
            self.add(t)

    @property
    def next_index(self) -> int:
        return len(self.entries)

    @property
    def next_offset(self) -> int:
        return self.start_offset + self.next_index

    def slot(self, i: int | None = None):
        return self.cells[self.next_index if i is None else i]

    def append(self, mob, color: str | None = None, run_time: float = 0.8):
        """Move `mob` into the next free cell, shrinking it into a token.

        The original mobject is transformed in place and becomes the log entry.
        """
        target_cell = self.slot()
        tok = token(color or S.NORMAL, target_cell.width * 0.62)
        tok.move_to(target_cell)
        self.entries.append(mob)
        self.add(mob)
        return Transform(mob, tok, run_time=run_time)

    def highlight_offset(self, i: int, color: str):
        return AnimationGroup(
            self.cells[i].animate.set_stroke(color, 3),
            self.offsets[i].animate.set_color(color),
        )


class StateTable(VGroup):
    """Two-column key/value table, e.g. Flink keyed state or sink rows."""

    def __init__(self, title: str, rows: dict, hue: str = S.HUE_C,
                 key_w: float = 1.2, val_w: float = 1.0, row_h: float = 0.36):
        super().__init__()
        self.row_h = row_h
        self.key_w, self.val_w = key_w, val_w
        self.title = txt(title, S.TINY_SIZE, hue) if title else VGroup()
        self.rows: dict = {}
        self.values: dict = dict(rows)
        body = VGroup()
        for k, v in rows.items():
            body.add(self._row(k, v))
        body.arrange(DOWN, buff=0)
        if title:
            self.title.next_to(body, UP, buff=0.1)
        self.body = body
        self.add(self.title, body)
        for row in body:
            self.rows[row.key] = row

    def _row(self, k, v) -> VGroup:
        kc = Rectangle(width=self.key_w, height=self.row_h, stroke_color=S.FAINT,
                       stroke_width=1.5, fill_color=S.BG,
                       fill_opacity=1).set_z_index(Z_CELL)
        vc = Rectangle(width=self.val_w, height=self.row_h, stroke_color=S.FAINT,
                       stroke_width=1.5, fill_color=S.BG,
                       fill_opacity=1).set_z_index(Z_CELL)
        vc.next_to(kc, RIGHT, buff=0)
        kt = txt(str(k), S.TINY_SIZE, S.MUTED, mono=True).move_to(kc)
        vt = txt(str(v), S.TINY_SIZE, S.INK, mono=True).move_to(vc)
        row = VGroup(kc, vc, kt, vt)
        row.key, row.val_cell, row.val_text = k, vc, vt
        return row

    def set_value(self, k, v, color: str = S.PENDING):
        """Animate a value change. Highlight color says what kind of change."""
        row = self.rows[k]
        new = txt(str(v), S.TINY_SIZE, color, mono=True).move_to(row.val_cell)
        old = row.val_text  # Transform mutates `old` in place
        self.values[k] = v
        return AnimationGroup(
            Transform(old, new),
            row.val_cell.animate.set_stroke(color, 2.5),
        )

    def settle(self, color: str = S.INK):
        """Return all value cells to neutral styling."""
        anims = []
        for row in self.rows.values():
            anims.append(row.val_cell.animate.set_stroke(S.FAINT, 1.5))
            anims.append(row.val_text.animate.set_color(color))
        return AnimationGroup(*anims)

    def value_of(self, k):
        return self.values[k]


class Timeline(VGroup):
    """Horizontal time axis. Events are placed with `at(t)` in [0, 1]."""

    def __init__(self, label: str, length: float = 5.5, color: str = S.MUTED):
        super().__init__()
        self.length = length
        self.axis = Arrow(LEFT * length / 2, RIGHT * length / 2, buff=0,
                          stroke_width=2, color=color, tip_length=0.15,
                          max_tip_length_to_length_ratio=0.04)
        self.label = txt(label, S.SMALL_SIZE, color)
        self.label.next_to(self.axis, LEFT, buff=0.2)
        self.add(self.axis, self.label)

    def at(self, t: float):
        start = self.axis.get_start()
        return start + RIGHT * (self.length * 0.97) * t

    def mark(self, t: float, text: str, color: str = S.INK,
             above: bool = True) -> VGroup:
        """Dot on the axis plus a short label. Returns the group (not added)."""
        d = Dot(self.at(t), radius=0.07, color=color)
        lab = txt(text, S.TINY_SIZE, color)
        lab.next_to(d, UP if above else DOWN, buff=0.12)
        return VGroup(d, lab)

    def span(self, t0: float, t1: float, color: str, text: str = "",
             above: bool = False, offset: float = 0.22) -> VGroup:
        """Bar for a duration (e.g. 'timeout'). `offset` sets its row."""
        y_off = UP * offset if above else DOWN * offset
        bar = Line(self.at(t0) + y_off, self.at(t1) + y_off, color=color,
                   stroke_width=4)
        g = VGroup(bar)
        if text:
            lab = txt(text, S.TINY_SIZE, color)
            lab.next_to(bar, UP if above else DOWN, buff=0.08)
            g.add(lab)
        return g


class Checklist(VGroup):
    """Vertical list of stages with status circles."""

    def __init__(self, items: list[str], size: int = S.SMALL_SIZE):
        super().__init__()
        self.items = VGroup()
        for s in items:
            c = Circle(radius=0.1, stroke_color=S.FAINT, stroke_width=2,
                       fill_opacity=0)
            t = txt(s, size, S.MUTED)
            t.next_to(c, RIGHT, buff=0.18)
            self.items.add(VGroup(c, t))
        self.items.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        self.add(self.items)

    def mark(self, i: int, color: str):
        c, t = self.items[i]
        return AnimationGroup(
            c.animate.set_fill(color, 1).set_stroke(color),
            t.animate.set_color(S.INK),
        )

    def reset(self):
        anims = []
        for c, t in self.items:
            anims += [c.animate.set_fill(opacity=0).set_stroke(S.FAINT),
                      t.animate.set_color(S.MUTED)]
        return AnimationGroup(*anims)


def connector(a, b, color: str = S.FAINT) -> Arrow:
    """Arrow between two component boxes, edge to edge."""
    return Arrow(a.get_right(), b.get_left(), buff=0.12, stroke_width=2.5,
                 color=color, tip_length=0.18,
                 max_tip_length_to_length_ratio=0.2)


class Narrator:
    """Owns the one caption line. Captions cross-fade instead of morphing
    letter by letter, which reads as noise.

        self.play(*cap.say("New idea."), other_animation)
    """

    def __init__(self, y: float = S.CAPTION_Y):
        self.y = y
        self.current = None

    def say(self, s: str, color: str = S.MUTED) -> list:
        new = caption(s, self.y, color=color)
        anims = [FadeIn(new, shift=UP * 0.08)]
        if self.current is not None:
            anims.insert(0, FadeOut(self.current, shift=UP * 0.08))
        self.current = new
        return anims

    def clear(self) -> list:
        if self.current is None:
            return []
        old, self.current = self.current, None
        return [FadeOut(old)]


def flow(stages, y: float = 0.9, width: float = 2.3, height: float = 1.1,
         span: float = 10.0, scale: float = 1.0) -> dict:
    """A left-to-right row of boxes joined by arrows.

    stages: [(name, hue), ...]. Returns boxes, arrows and a group. Use it for
    any system diagram: producer -> broker -> consumer, client -> API -> DB...
    """
    n = len(stages)
    xs = [-span / 2 + span * i / (n - 1) for i in range(n)] if n > 1 else [0.0]
    boxes = []
    for (name, hue), x in zip(stages, xs):
        b = ComponentBox(name, hue, width, height)
        b.title.move_to(b.panel)
        b.move_to([x, y, 0])
        boxes.append(b)
    arrows = VGroup(*[connector(a, b) for a, b in zip(boxes, boxes[1:])])
    group = VGroup(*boxes, arrows).scale(scale)
    return dict(boxes=VGroup(*boxes), arrows=arrows, group=group)


def series_mark() -> VGroup:
    """Top-left series brand used outside chapters."""
    a = txt(S.SERIES_NAME.upper(), S.SMALL_SIZE, S.MUTED, weight="BOLD")
    b = txt(S.SERIES_TAG, S.SMALL_SIZE, S.NORMAL, weight="BOLD")
    g = VGroup(a, b).arrange(RIGHT, buff=0.15)
    g.to_corner(UL, buff=0.4)
    return g


def badge(number, label: str, color: str = S.INK, radius: float = 0.27) -> VGroup:
    """Numbered chapter badge with a label underneath."""
    c = Circle(radius=radius, stroke_color=color, stroke_width=2.5,
               fill_color=S.PANEL, fill_opacity=1)
    n = txt(str(number), S.LABEL_SIZE, color, weight="BOLD").move_to(c)
    lab = txt(label, S.TINY_SIZE + 1, S.INK)
    lab.next_to(c, DOWN, buff=0.1)
    g = VGroup(c, n, lab)
    g.circle, g.number, g.label = c, n, lab
    return g
