# Workflow definitions for MSW Maker Automation

CREATE_SCRIPT_WORKFLOW = [
    {"action": "right_click"}, # Uses anchor
    {"action": "select_menu", "goal": "Create Scripts"},
    {"action": "select_menu", "goal": "Create Script"},
    {"action": "type_text", "text": "SCRIPT_NAME", "delay": 0.2},
    {"action": "press_key", "key": "enter", "delay": 0.5},
]


# Phase 3: Create script + paste lua code + save (Robust)
CREATE_AND_PASTE_SCRIPT_WORKFLOW = [
    {"action": "right_click"},
    {"action": "select_menu", "goal": "Create Scripts"},
    {"action": "select_menu", "goal": "Create Script"},
    {"action": "type_text", "text": "SCRIPT_NAME", "delay": 0.2},
    {"action": "press_key", "key": "enter", "delay": 0.5},
    {"action": "press_key", "key": "enter", "delay": 0.5}, # Added extra enter to select script
    
    # Wait for editor tab to open
    {"action": "wait", "seconds": 2.0},
    
    # Ensure Plain Text tab is selected
    {"action": "select_menu", "goal": "Plain Text", "region": "PLAINTEXT_TAB_REGIONS", "cache": True},
    {"action": "wait", "seconds": 0.5},
    
    # Explicitly focus the editor content area
    {"action": "click_region_center", "region": "EDITOR_TEXT_REGIONS"},
    {"action": "wait", "seconds": 0.2},
    
    # Clear and Paste
    {"action": "hotkey", "keys": ["ctrl", "a"]},
    {"action": "press_key", "key": "delete"},
    {"action": "wait", "seconds": 0.1},
    {"action": "paste_file_content", "file": "LUA_FILE_PATH"},
    
    # Save
    {"action": "wait", "seconds": 0.5},
    {"action": "hotkey", "keys": ["ctrl", "s"]},
    {"action": "wait", "seconds": 0.5},
]

