# UI Configuration with multi-language support

# --- Language Configuration ---
LANGUAGES = {
    'en': '🇺🇸 English',
    'zh': '🇨🇳 中文'
}

# --- Period Options with multi-language support ---
PERIOD_OPTIONS = {
    'en': {
        '7_days': '7 days',
        '1_month': '1 month',
    },
    'zh': {
        '7_days': '7天',
        '1_month': '1个月',
    }
}

# Internal mapping for period days
PERIOD_DAYS = {
    '7_days': 7,
    '1_month': 30,
}

# --- Price Move Threshold Options with multi-language support ---
PRICE_MOVE_OPTIONS = {
    'en': {
        5.0: '5.0%',
        10.0: '10.0%', 
        15.0: '15.0%',
        20.0: '20.0%'
    },
    'zh': {
        5.0: '5.0%',
        10.0: '10.0%',
        15.0: '15.0%', 
        20.0: '20.0%'
    }
}

# --- Default Values ---
DEFAULT_LANGUAGE = 'zh'
DEFAULT_COMPANY = 'RKLB'
DEFAULT_PERIOD = '1_month'
DEFAULT_PRICE_MOVE_THRESHOLD = 5.0

# --- Helper Functions ---
def get_period_options_for_lang(lang: str):
    """Get period options for a specific language."""
    return list(PERIOD_OPTIONS.get(lang, PERIOD_OPTIONS['en']).values())

def get_period_key_from_display(display_text: str, lang: str):
    """Get internal period key from display text."""
    options = PERIOD_OPTIONS.get(lang, PERIOD_OPTIONS['en'])
    for key, value in options.items():
        if value == display_text:
            return key
    return DEFAULT_PERIOD

def get_price_move_options_for_lang(lang: str):
    """Get price move threshold options for a specific language."""
    return list(PRICE_MOVE_OPTIONS.get(lang, PRICE_MOVE_OPTIONS['en']).values())

def get_price_move_value_from_display(display_text: str, lang: str):
    """Get price move threshold value from display text."""
    options = PRICE_MOVE_OPTIONS.get(lang, PRICE_MOVE_OPTIONS['en'])
    for value, display in options.items():
        if display == display_text:
            return value
    return DEFAULT_PRICE_MOVE_THRESHOLD
