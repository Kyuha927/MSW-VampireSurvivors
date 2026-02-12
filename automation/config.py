# Feature flags for MSW Automation

# OCR matching strategy
USE_SIMPLE_FUZZY = True          # True=v1.5 style, False=filtered with must_contain/reject
MIN_SIMILARITY = 0.45            # 0.45=v1.5, higher=more strict

# Menu verification
USE_MENU_VERIFICATION = False    # True=verify menu open before OCR, False=direct OCR (v1.5)

# Click position
CLICK_FIRST_LETTER = True        # True=click left_x (first letter), False=click center (v1.5)

# Debug
SAVE_DEBUG_IMAGES = False        # True=save screenshots on each OCR attempt
