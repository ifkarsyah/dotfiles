"""Example narrated scene. Copy this pattern for every new scene.

Render:
    .venv/bin/manim -pql scenes/example.py ExampleIntro
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from manim import (  # noqa: E402
    DOWN, UP, Circumscribe, FadeIn, FadeOut, GrowArrow, LaggedStart,
)

from explainer_kit import style as S  # noqa: E402
from explainer_kit.components import (  # noqa: E402
    EventPacket, Narrator, flow, series_mark, takeaway,
)
from explainer_kit.voice import NarratedScene  # noqa: E402


class ExampleIntro(NarratedScene):
    """Teaches: a request crosses three systems, and each can fail."""

    def construct(self):
        brand = series_mark()
        self.add(brand)
        cap = Narrator()
        f = flow([("Client", S.HUE_A), ("API", S.HUE_B), ("Database", S.HUE_D)], y=0.6)
        boxes, arrows = f["boxes"], f["arrows"]

        # `d` is this beat's narration length: use it to spread motion across
        # the sentence instead of front-loading everything.
        with self.beat("hook") as d:
            self.play(*cap.say("One request, three systems"), run_time=0.6)
            req = EventPacket("GET /orders", color=S.NORMAL).scale(0.7)
            req.next_to(boxes[0], DOWN, buff=0.2)          # travel UNDER box names
            self.play(FadeIn(boxes[0]), FadeIn(req, shift=UP * 0.2))
            step = max(0.6, (d - 1.6) / 2)
            for i in (1, 2):
                self.play(FadeIn(boxes[i]), GrowArrow(arrows[i - 1]),
                          req.animate.next_to(boxes[i], DOWN, buff=0.2), run_time=step)

        with self.beat("flow"):
            # "Each one can fail on its own." -> trace each box in turn.
            # Circumscribe (outline) rather than Indicate on boxes: Indicate
            # recolors fills and turns a panel into a solid block.
            self.play(LaggedStart(*[Circumscribe(b.panel, color=S.FAILURE, buff=0.06)
                                    for b in boxes], lag_ratio=0.5), run_time=2.4)

        with self.beat("takeaway"):
            key = takeaway("What happens in between?", S.INK).move_to([0, -2.6, 0])
            self.play(*cap.clear(), FadeIn(key, shift=UP * 0.15))

        self.play(*[FadeOut(m) for m in self.mobjects if m is not brand], run_time=0.6)
