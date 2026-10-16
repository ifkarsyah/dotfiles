"""Visual constants shared by every scene.

Color carries meaning, so every color here is named by what it means, never
by how it looks. Scenes must use these names, not raw hex values.
"""

from manim import config

# ---------------------------------------------------------------- background
BG = "#0E1116"
config.background_color = BG

# ------------------------------------------------------------------ semantics
NORMAL = "#58A6FF"     # healthy flow, event in transit
DURABLE = "#3FB950"    # acked, committed, checkpoint complete
PENDING = "#E3B341"    # in flight, uncommitted, unacked
FAILURE = "#F85149"    # crash, timeout, lost ack
RETRY = "#F0883E"      # retry, replay
DUPLICATE = "#DB61A2"  # duplicate effect (always paired with a dashed outline)
RECOVERY = "#39C5BB"   # restored state, new leader

# ------------------------------------------------------------------ neutrals
INK = "#E6EDF3"        # primary text
MUTED = "#8B949E"      # secondary text, labels, axes
FAINT = "#30363D"      # borders, grid, inactive cells
PANEL = "#161B22"      # component fill

# ----------------------------------------------------------- component hues
# Identity colors for up to four system components (outline + title only).
# Give them domain names in your scenes, e.g. PRODUCER_HUE = S.HUE_A.
HUE_A = "#A5D6FF"
HUE_B = "#D2A8FF"
HUE_C = "#FFA657"
HUE_D = "#7EE787"

# ------------------------------------------------------------------ series
SERIES_NAME = "Series Name"      # shown top-left outside chapters
SERIES_TAG = "101"

# ---------------------------------------------------------------- typography
FONT = "Inter"
MONO = "DejaVu Sans Mono"

TITLE_SIZE = 40
HEADING_SIZE = 30
BODY_SIZE = 24
LABEL_SIZE = 20
SMALL_SIZE = 16
TINY_SIZE = 13

# --------------------------------------------------------------------- layout
# Keep the main system diagram at fixed positions across scenes so viewers
# never re-learn the layout. Frame is ~14.2 x 8 units, origin at center.
TOP_BAND_Y = 3.3      # chapter title
CAPTION_Y = 2.65      # one-line "what this teaches"
BOTTOM_BAND_Y = -2.6  # timelines, takeaways

# --------------------------------------------------------------------- timing
FAST = 0.5
NORMAL_T = 0.9
SLOW = 1.4
BEAT = 0.6            # pause after a small idea
READ = 1.8            # pause so a sentence can be read
