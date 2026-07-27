from pathlib import Path

# ==========================================================
# Project Paths
# ==========================================================
DASHBOARD_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = DASHBOARD_DIR.parent

DATA_DIR = PROJECT_ROOT / "data"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

ASSETS_DIR = DASHBOARD_DIR / "assets"
PAGES_DIR = DASHBOARD_DIR / "pages"
UTILS_DIR = DASHBOARD_DIR / "utils"

# ==========================================================
# Application Information
# ==========================================================
APP_NAME = "CricVision AI"

APP_SUBTITLE = (
    "Professional Cricket Analytics Platform"
)

PAGE_TITLE = "CricVision AI"

PAGE_ICON = "🏏"

# ==========================================================
# Dashboard Pages
# ==========================================================
DASHBOARD_PAGES = {
    "Executive": "1_Executive.py",
    "Team": "2_Team.py",
    "Batter": "3_Batter.py",
    "Bowler": "4_Bowler.py",
    "Venue": "5_Venue.py",
    "Match": "6_Match.py"
}

# ==========================================================
# Theme
# ==========================================================

PRIMARY_COLOR = "#22C55E"
PRIMARY_DARK_COLOR = "#15803D"
SECONDARY_COLOR = "#38BDF8"
ACCENT_COLOR = "#F59E0B"
SUCCESS_COLOR = "#22C55E"
WARNING_COLOR = "#F59E0B"
DANGER_COLOR = "#EF4444"
BACKGROUND_COLOR = "#0B0F17"
SECONDARY_BACKGROUND_COLOR = "#151A24"
SIDEBAR_BACKGROUND = "#171B26"
CARD_BACKGROUND_COLOR = "#111722"
TEXT_COLOR = "#F8FAFC"
MUTED_TEXT_COLOR = "#AAB2C0"
BORDER_COLOR = "#2A3140"

# ==========================================================
# Qualification Thresholds
# ==========================================================
MIN_TEAM_MATCHES = 50
MIN_BATTER_BALLS = 500
MIN_BOWLER_BALLS = 600
MIN_FINISHER_BALLS = 120
MIN_DEATH_BOWLER_BALLS = 120
MIN_PARTNERSHIP_INNINGS = 10
MIN_VENUE_MATCHES = 10

# ==========================================================
# Default Filters
# ==========================================================
DEFAULT_SEASON = "All"
DEFAULT_TEAM = "All"
DEFAULT_BATTER = "All"
DEFAULT_BOWLER = "All"
DEFAULT_VENUE = "All"

# ==========================================================
# Match Phases
# ==========================================================

POWERPLAY_START = 0
POWERPLAY_END = 5

MIDDLE_START = 6
MIDDLE_END = 14

DEATH_START = 15
DEATH_END = 19

# ==========================================================
# KPI Labels
# ==========================================================

EXECUTIVE_KPIS = [
    "Total Seasons",
    "Total Matches",
    "Total Players",
    "Total Teams",
    "Total Venues",
    "Total Runs",
    "Total Wickets",
    "Average First Innings Score",
    "Chasing Success Rate"
]