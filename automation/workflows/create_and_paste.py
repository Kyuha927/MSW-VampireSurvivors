# v1.5 + Plain Text tab + Code paste
CREATE_AND_PASTE_WORKFLOW = [
    {"action": "right_click"},
    {"action": "select_menu", "goal": "Create Scripts"},
    {"action": "select_menu", "goal": "Create Script"},
    {"action": "type_text", "text": "SCRIPT_NAME", "delay": 0.2},
    {"action": "press_key", "key": "enter", "delay": 0.5},
    {"action": "wait", "seconds": 2.0},  # 에디터 열림 대기
    {"action": "select_menu", "goal": "Plain Text", "region": "PLAINTEXT_TAB_REGIONS"},
    {"action": "wait", "seconds": 0.5},
    {"action": "click_region_center", "region": "EDITOR_TEXT_REGIONS"},
    {"action": "hotkey", "keys": ["ctrl", "a"]},
    {"action": "wait", "seconds": 0.2},
    {"action": "paste_file_content", "file": "LUA_FILE_PATH"},
    {"action": "wait", "seconds": 0.3},
    {"action": "hotkey", "keys": ["ctrl", "s"]},
    {"action": "wait", "seconds": 0.5},
]
