# Visual pitfalls (all found in real renders)

Read before building scenes. Each entry: symptom → cause → fix.

## Manim behavior

**A box's contents vanish when its outline animates** (e.g. a crashed component loses its title and table).
Animating a submobject (`panel.animate.set_stroke(...)`) makes Manim draw it on top, and an opaque panel then covers its own contents.
Fix: the components set fixed z-indexes (`Z_PANEL < Z_CELL < text < Z_TOKEN < Z_PACKET < Z_ALERT`). Keep them, and give any new opaque background a low z-index.

**Captions garble mid-transition.**
`Transform(text_a, text_b)` morphs letters into each other.
Fix: use `Narrator.say()`, which cross-fades. For one label turning into another in the same spot (e.g. `send(record)` → `callback: ok`), a Transform is fine because the two texts are short.

**A box or table flashes into a solid colored block.**
`Indicate` recolors fill as well as stroke.
Fix: `Circumscribe(mob, color=..., buff=...)` for boxes, panels, tables and packets. Use `Indicate` only on text, arrows and small tokens.

**Positional args after keyword args.**
`self.play(a, run_time=1, *cap.say(...))` is a SyntaxError. Put `*cap.say(...)` before `run_time=`.

**Fade-outs that keep a persistent element.**
Don't pick elements by list position (`self.mobjects[0]`): the order changes as things are added and removed. Keep a reference (`title = chapter_title(...)`) and exclude it by identity.

## Layout

**Moving objects cover labels.** Packets traveling through box centers hide the box names; tokens landing in a box sit on its title.
Fix: travel under the boxes (`next_to(box, DOWN, buff=0.2)`), land tokens beside or below boxes, and put annotations above (`UP`) when the path runs below.

**Messages travel along a row that holds other UI** (an "ack lost" cross landed on a config chip).
Fix: route messages through the empty gap between the two components, with acks offset ~0.3 above the data path.

**Return paths cut through other boxes.** Start a return route from the outer edge of a stack (`leaders.get_bottom()`), not the middle element.

**Two labels in the same slot.** Labels added later in a scene (`callback: ok` above a box that already has `send(record)` above it) collide. Before adding a label, check what's already next to that edge.

**Timeline labels overlap.** Put markers alternately above and below the axis, and give duration bars their own row (`span(..., offset=0.62)`).

**Readers can't tell same-looking items apart.** Ordering demos with identical tokens are unreadable.
Fix: tag each log entry with a short label above its cell ("dep", "wd").

**Text clipped at the frame edge.** Anything `next_to` a left-edge element can fall off-frame; check the left 0.5 units in contact sheets.

## Review technique

- Contact sheets (`tools/contact_sheet.sh`) every 2.5 s, 5 columns, at 480p15. Read the PNG, then fix everything found in one pass.
- A sheet frame can catch a mid-transition. Before fixing something that "doesn't appear", extract the exact window at 2 fps and look again.
- Small text looks borderline at 480p but is fine at 1080p. Judge readability on a full-resolution frame.
- After fixing, re-render only the changed scenes (`-ql`) and re-sheet them.
