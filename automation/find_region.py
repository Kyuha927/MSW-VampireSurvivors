"""
Quick region measurement tool for MSW Maker automation.

Use this to measure a tight OCR region for the "Plain Text" tab (or any UI label).

How it works:
1) Place your mouse on the TOP-LEFT corner of the region you want to scan and press Enter.
2) Place your mouse on the BOTTOM-RIGHT corner and press Enter.

It prints both absolute pixels and screen-relative ratios you can paste into run_msw_setup.py.
"""

import pyautogui


def _prompt_point(label: str) -> tuple[int, int]:
    input(f"{label} (move mouse there, then press Enter) ")
    x, y = pyautogui.position()
    print(f"  captured: x={x}, y={y}")
    return int(x), int(y)


def main() -> None:
    print("=== Region measurement tool ===")
    print("Target: measure an OCR region (e.g. MSW editor tab strip containing 'Plain Text').")
    print()

    screen_w, screen_h = pyautogui.size()
    print(f"Screen: {screen_w} x {screen_h}")
    print()

    x0, y0 = _prompt_point("1) TOP-LEFT")
    x1, y1 = _prompt_point("2) BOTTOM-RIGHT")

    left = min(x0, x1)
    top = min(y0, y1)
    right = max(x0, x1)
    bottom = max(y0, y1)

    width = max(1, right - left)
    height = max(1, bottom - top)

    print()
    print("Absolute region (left, top, width, height):")
    print(f"  ({left}, {top}, {width}, {height})")
    print()

    x0_ratio = left / screen_w
    y0_ratio = top / screen_h
    w_ratio = width / screen_w
    h_ratio = height / screen_h

    def r(v: float) -> float:
        return round(v, 4)

    print("Ratios (relative to screen size):")
    print(f"  tab_x0_ratio = {r(x0_ratio)}")
    print(f"  tab_y0_ratio = {r(y0_ratio)}")
    print(f"  tab_w_ratio  = {r(w_ratio)}")
    print(f"  tab_h_ratio  = {r(h_ratio)}")
    print()

    print("Paste-ready snippet for run_msw_setup.py:")
    print("  plaintext_tab_regions = [")
    print(f"      ({left}, {top}, {width}, {height}),")
    print("  ]")
    print()
    print("Or paste-ready ratio snippet:")
    print(f"  tab_y0_ratio = {r(y0_ratio)}")
    print(f"  tab_h_ratio = {r(h_ratio)}")
    print(f"  tab_x0_ratio = {r(x0_ratio)}")
    print(f"  tab_w_ratio = {r(w_ratio)}")


if __name__ == "__main__":
    main()
