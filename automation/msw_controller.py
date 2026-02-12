import time
import pyautogui
import ctypes
from pathlib import Path
from msw_menu_vision import capture_menu_items_auto
from msw_menu_vision import capture_menu_items_auto
import difflib
import pyperclip
import os

# Settings
MIN_SIMILARITY = 0.45
MYDESK_X = 1824
MYDESK_Y = 894

def is_esc_pressed():
    """Check if ESC key is pressed asynchronously."""
    return ctypes.windll.user32.GetAsyncKeyState(0x1B) != 0

def _normalize(s: str) -> str:
    s = s.lower().strip()
    for ch in " \t_-·•….:;,()[]{}":
        s = s.replace(ch, "")
    return s

def fuzzy_pick(menu_texts: list[str], goal: str) -> int:
    goal_norm = _normalize(goal)
    best_idx = -1
    best_ratio = 0.0
    for i, text in enumerate(menu_texts):
        norm = _normalize(text)
        ratio = difflib.SequenceMatcher(None, goal_norm, norm).ratio()
        if goal_norm in norm or norm in goal_norm:
            ratio = max(ratio, 0.85)
        if ratio > best_ratio:
            best_ratio = ratio
            best_idx = i
    return best_idx if best_ratio >= MIN_SIMILARITY else -1

class MSWController:
    def __init__(self, anchor_xy):
        self.anchor_xy = anchor_xy
        self._cached_coords = {}  # goal -> (x, y) 매크로 캐시
        self._interrupted = False
        pyautogui.PAUSE = 0.02
        
    def was_interrupted(self):
        return self._interrupted

    def _sleep_interruptible(self, seconds: float) -> bool:
        """Sleeps for `seconds` but checks ESC every 50ms. Returns False if interrupted."""
        if self._interrupted: return False
        end_time = time.time() + seconds
        while time.time() < end_time:
            if is_esc_pressed():
                self._interrupted = True
                print("\n[STOP] ESC detected during sleep.")
                return False
            time.sleep(0.05)
        return True
    
    def execute_workflow(self, workflow, params=None):
        """
        Executes a list of steps. 
        Each step: {"action": "...", "target": ..., "goal": ...}
        """
        self._interrupted = False # Reset flag at start of workflow
        
        for step in workflow:
            if self._interrupted or is_esc_pressed():
                self._interrupted = True
                print("\n[STOP] User interrupted.")
                return False
                
            action = step.get("action")
            
            if action == "right_click":
                target = step.get("target") or self.anchor_xy
                pyautogui.click(target[0], target[1])
                if not self._sleep_interruptible(0.15): return False
                pyautogui.rightClick(target[0], target[1])
                if not self._sleep_interruptible(0.5): return False
                
            elif action == "select_menu":
                goal = step.get("goal")
                region = step.get("region")
                if params and isinstance(region, str) and region in params:
                    region = params[region]
                
                # Phase 2: Anti-Misclick (Cache Verification)
                # Note: We only use cache if region is NOT specified (context menus).
                # Fixed regions (like tabs) usually don't need 'cache verification' in the same way, 
                # or strictly speaking, they are static. But let's support cache for them too if needed.
                # However, for now, let's assume cache is mostly for context menus.
                
                cache_key = goal
                if region:
                    # If region is specific, we might use a different cache key or just skip cache verification for simplicity/safety
                    # For Plain Text tab, it's a fixed region, so cache might be less critical or just (x,y).
                    # Let's simple use the goal as key for now, hoping names are unique.
                    pass
                
                if goal in self._cached_coords:
                    # A: 바로 클릭 (검증 제거)
                    cx, cy = self._cached_coords[goal]
                    print(f"  > MACRO click '{goal}' @ ({cx},{cy})")
                    pyautogui.click(cx, cy)
                    if not self._sleep_interruptible(0.3): return False
                else:
                    # 첫 회: OCR로 찾고 좌표 기록
                    print(f"  > OCR scan '{goal}'")
                    coords = self._ocr_click_menu(goal, region=region)
                    if not coords:
                        return False
                    self._cached_coords[goal] = coords
                    if not self._sleep_interruptible(0.3): return False
                
            elif action == "type_text":
                text = step.get("text")
                if params and text in params:
                    text = params[text]
                pyautogui.write(text, interval=0.01)
                
            elif action == "press_key":
                pyautogui.press(step.get("key"))
                
            elif action == "hotkey":
                pyautogui.hotkey(*step.get("keys"))
            
            elif action == "click_region_center":
                region_key = step.get("region")
                if params and region_key in params:
                    # params[region_key] could be a single tuple or list of tuples
                    r = params[region_key]
                    if isinstance(r, list): r = r[0] # Take first if list
                    if r and len(r) == 4:
                        cx = r[0] + r[2] // 2
                        cy = r[1] + r[3] // 2
                        print(f"  > Click region center ({cx}, {cy})")
                        pyautogui.click(cx, cy)
                
            elif action == "wait":
                if not self._sleep_interruptible(step.get("seconds", 1)): return False

            elif action == "paste_file_content":
                file_path = step.get("file")
                if params and file_path in params:
                    file_path = params[file_path]
                
                if file_path:
                    try:
                        # Resolve path assuming it's relative to CWD if not absolute
                        p = Path(file_path).resolve()
                        print(f"  > Reading file: {p}")
                        
                        text = ""
                        encodings = ["utf-8", "utf-8-sig", "cp949", "euc-kr", "latin-1"]
                        for i, enc in enumerate(encodings):
                            try:
                                text = p.read_text(encoding=enc, errors="replace")
                                if i > 0:
                                    print(f"  [WARN] Read file with encoding '{enc}' (utf-8 failed)")
                                else:
                                    print(f"  > Read file with encoding: {enc}")
                                break
                            except Exception:
                                continue
                        
                        if not text:
                             print(f"  [ERROR] Failed to read file with any encoding: {encodings}")
                             return False

                        pyperclip.copy(text)
                        print(f"  > Clipboard copy ({len(text)} chars)")
                        time.sleep(0.3)
                        pyautogui.hotkey("ctrl", "v")
                        print(f"  > Paste (Ctrl+V)")
                        time.sleep(0.5)
                    except Exception as e:
                        print(f"  [ERROR] Failed to read/paste file {file_path}: {e}")
                        return False

            if not self._sleep_interruptible(step.get("delay", 0.15)): return False
            
        return True

    def _ocr_click_menu(self, goal, region=None):
        """OCR로 메뉴를 찾아 클릭하고 좌표를 반환. 실패 시 None."""
        from msw_menu_vision import capture_region_bgr, extract_menu_items_from_roi
        
        # Region이 주어지면 해당 영역만 스캔 (Plain Text 탭 등)
        if region:
            # Normalize region list
            regions = [region] if isinstance(region, (tuple, list)) and len(region) == 4 and isinstance(region[0], int) else region
            if isinstance(region, list) and len(region) > 0 and isinstance(region[0], (list, tuple)):
                regions = region
            
            for attempt in range(3):
                if self._interrupted: return None
                
                for r in regions:
                    if not r or len(r) != 4: continue
                    left, top, w, h = r
                    
                    t0 = time.time()
                    roi_bgr = capture_region_bgr(left, top, w, h)
                    items = extract_menu_items_from_roi(roi_bgr)
                    ocr_ms = int((time.time() - t0) * 1000)
                    
                    if items:
                        menu_texts = [it.text for it in items]
                        idx = fuzzy_pick(menu_texts, goal)
                        if idx != -1:
                            it = items[idx]
                            click_x = int(left) + it.center_xy[0]
                            click_y = int(top) + it.center_xy[1]
                            print(f"    OCR({ocr_ms}ms) matched '{it.text}' -> ({click_x},{click_y}) [NEW CACHE]")
                            pyautogui.click(click_x, click_y)
                            return (click_x, click_y)
                        else:
                            print(f"    OCR({ocr_ms}ms) no match for '{goal}' in: {menu_texts[:6]}")
                    else:
                        print(f"    OCR({ocr_ms}ms) no text detected")
                
                if not self._sleep_interruptible(0.3): return None
            
            print(f"    [FAIL] Could not find: {goal}")
            return None

        # Region이 없으면 Anchor 주변 Context Menu 스캔 (기존 로직)
        anchor = self.anchor_xy
        for attempt in range(3):
            if self._interrupted: return None
            
            t0 = time.time()
            cap = capture_menu_items_auto(anchor)
            ocr_ms = int((time.time() - t0) * 1000)
            if cap and cap.items:
                menu_texts = [it.text for it in cap.items]
                idx = fuzzy_pick(menu_texts, goal)
                if idx != -1:
                    it = cap.items[idx]
                    click_x = cap.left + cap.crop_dx_dy[0] + it.center_xy[0]
                    click_y = cap.top + cap.crop_dx_dy[1] + it.center_xy[1]
                    print(f"    OCR({ocr_ms}ms) matched '{it.text}' -> ({click_x},{click_y}) [NEW CACHE]")
                    pyautogui.click(click_x, click_y)
                    return (click_x, click_y)
                else:
                    print(f"    OCR({ocr_ms}ms) no match for '{goal}' in: {menu_texts[:6]}")
            else:
                print(f"    OCR({ocr_ms}ms) no menu detected (attempt {attempt+1})")
            
            if not self._sleep_interruptible(0.3): return None
            
        print(f"    [FAIL] Could not find: {goal}")
        return None
