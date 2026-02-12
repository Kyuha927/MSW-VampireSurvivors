import os
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple, Optional

import cv2
import numpy as np
import pyautogui
import time

try:
    import mss  # type: ignore
except Exception:
    mss = None

try:
    # Install: python -m pip install --user rapidocr-onnxruntime
    from rapidocr_onnxruntime import RapidOCR  # type: ignore

    _RAPID_OCR = RapidOCR()
except Exception:
    _RAPID_OCR = None


@dataclass(frozen=True)
class OcrHit:
    text: str
    score: float
    center_xy: Tuple[int, int]


@dataclass(frozen=True)
class MenuItem:
    text: str
    score: float
    center_xy: Tuple[int, int]
    norm: str


def _pil_to_bgr(pil_img) -> np.ndarray:
    arr = np.array(pil_img)  # RGB
    return cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)


def _to_gray(img_bgr: np.ndarray) -> np.ndarray:
    if len(img_bgr.shape) == 2:
        return img_bgr
    return cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)


def _preprocess_for_ocr(bgr: np.ndarray) -> np.ndarray:
    gray = _to_gray(bgr)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    _, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return th


def _normalize_text(s: str) -> str:
    # Aggressive normalization for OCR output comparisons.
    s = (s or "").lower()
    for ch in [" ", "\t", "\r", "\n", "·", "•", "-", "_", "—", "–", ":", ";", ",", ".", "(", ")", "[", "]", "{", "}"]:
        s = s.replace(ch, "")
    return s


def _similar(a: str, b: str) -> float:
    # Lightweight similarity, good enough for short menu labels.
    import difflib

    return difflib.SequenceMatcher(a=a, b=b).ratio()


def _auto_crop_menu_bg(roi_bgr: np.ndarray) -> Tuple[np.ndarray, Tuple[int, int]]:
    """
    Best-effort crop to a menu-like bright rectangle inside ROI.
    Returns (cropped_bgr, (dx, dy)). Falls back to original ROI if unsure.
    """
    h, w = roi_bgr.shape[:2]
    if h < 40 or w < 80:
        return roi_bgr, (0, 0)

    gray = _to_gray(roi_bgr)
    mean = float(gray.mean())
    # Heuristic: only try bright-menu crop if ROI is overall fairly bright.
    if mean < 110:
        return roi_bgr, (0, 0)

    _, mask = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not cnts:
        return roi_bgr, (0, 0)

    roi_area = float(h * w)
    best = None
    best_area = 0.0
    for c in cnts:
        x, y, cw, ch = cv2.boundingRect(c)
        area = float(cw * ch)
        if area < roi_area * 0.05 or area > roi_area * 0.90:
            continue
        if ch < 60 or cw < 120:
            continue
        if area > best_area:
            best_area = area
            best = (x, y, cw, ch)

    if not best:
        return roi_bgr, (0, 0)

    x, y, cw, ch = best
    pad = 6
    x0 = max(0, x - pad)
    y0 = max(0, y - pad)
    x1 = min(w, x + cw + pad)
    y1 = min(h, y + ch + pad)
    cropped = roi_bgr[y0:y1, x0:x1]
    return cropped, (x0, y0)


def capture_roi_around_click(
    click_xy: Tuple[int, int],
    roi_wh: Tuple[int, int] = (520, 640),
    margin_xy: Tuple[int, int] = (20, 20),
) -> Tuple[int, int, np.ndarray]:
    """
    Capture the likely context-menu region near the click position.
    Returns (left, top, bgr_img).
    """
    screen_w, screen_h = pyautogui.size()
    menu_w, menu_h = roi_wh
    mx, my = margin_xy
    x, y = click_xy

    left = x + mx
    top = y + my
    if left + menu_w > screen_w:
        left = max(0, x - mx - menu_w)
    if top + menu_h > screen_h:
        top = max(0, y - my - menu_h)

    left = int(max(0, min(left, screen_w - 1)))
    top = int(max(0, min(top, screen_h - 1)))
    width = int(min(menu_w, screen_w - left))
    height = int(min(menu_h, screen_h - top))

    pil = pyautogui.screenshot(region=(left, top, width, height))
    return left, top, _pil_to_bgr(pil)


def _capture_roi_bgr_fast(left: int, top: int, width: int, height: int) -> np.ndarray:
    """
    Faster capture than pyautogui when mss is available.
    Returns BGR image.
    """
    if mss is None:
        pil = pyautogui.screenshot(region=(left, top, width, height))
        return _pil_to_bgr(pil)

    with mss.mss() as sct:
        mon = {"left": int(left), "top": int(top), "width": int(width), "height": int(height)}
        img = sct.grab(mon)  # BGRA
        arr = np.asarray(img)
        bgr = cv2.cvtColor(arr, cv2.COLOR_BGRA2BGR)
        return bgr


def capture_region_bgr(left: int, top: int, width: int, height: int) -> np.ndarray:
    """
    Captures a specific screen region and returns BGR image.
    Wraps _capture_roi_bgr_fast for public use.
    """
    return _capture_roi_bgr_fast(left, top, width, height)


def save_debug_image(img_bgr: np.ndarray, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(out_path), img_bgr)


def ocr_hits(roi_bgr: np.ndarray) -> List[OcrHit]:
    if _RAPID_OCR is None:
        raise RuntimeError("rapidocr-onnxruntime is not installed")

    # Use original image first (Otsu thresholding sometimes blurs thin MSW fonts)
    result, _ = _RAPID_OCR(roi_bgr)
    
    # Fallback to preprocessed if no results
    if not result:
        img = _preprocess_for_ocr(roi_bgr)
        result, _ = _RAPID_OCR(img)
        
    if not result:
        return []

    hits: List[OcrHit] = []
    for item in result:
        box, text, score = item[0], str(item[1]), float(item[2])
        if not text.strip():
            continue
        pts = [(int(p[0]), int(p[1])) for p in box]
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        cx = int((min(xs) + max(xs)) / 2)
        cy = int((min(ys) + max(ys)) / 2)
        hits.append(OcrHit(text=text, score=score, center_xy=(cx, cy)))
    return hits


def extract_menu_items_from_roi(
    roi_bgr: np.ndarray,
    *,
    min_score: float = 0.55,
    y_merge_px: int = 10,
) -> List[MenuItem]:
    """
    Convert OCR hits into menu-like items: merge tokens on the same visual line.
    Returns items sorted by y (top -> bottom).
    """
    hits = [h for h in ocr_hits(roi_bgr) if h.score >= min_score]
    if not hits:
        return []

    hits.sort(key=lambda h: (h.center_xy[1], h.center_xy[0]))

    lines: List[List[OcrHit]] = []
    for h in hits:
        if not lines:
            lines.append([h])
            continue
        prev = lines[-1]
        prev_y = int(sum(x.center_xy[1] for x in prev) / len(prev))
        if abs(h.center_xy[1] - prev_y) <= y_merge_px:
            prev.append(h)
        else:
            lines.append([h])

    items_raw: List[MenuItem] = []
    for line in lines:
        line.sort(key=lambda h: h.center_xy[0])
        text = " ".join([h.text.strip() for h in line if h.text.strip()])
        if not text:
            continue
        avg_score = float(sum(h.score for h in line) / len(line))
        cx = int(sum(h.center_xy[0] for h in line) / len(line))
        cy = int(sum(h.center_xy[1] for h in line) / len(line))
        items_raw.append(MenuItem(text=text, score=avg_score, center_xy=(cx, cy), norm=_normalize_text(text)))

    items_raw.sort(key=lambda it: it.center_xy[1])

    # Post-process: merge very similar adjacent lines (OCR splits/typos).
    merged: List[MenuItem] = []
    for it in items_raw:
        if not merged:
            merged.append(it)
            continue
        prev = merged[-1]
        if abs(it.center_xy[1] - prev.center_xy[1]) <= (y_merge_px + 2) and _similar(it.norm, prev.norm) >= 0.90:
            # Keep the higher-confidence text, but average the click point.
            if it.score > prev.score:
                keep_text = it.text
                keep_norm = it.norm
                keep_score = it.score
            else:
                keep_text = prev.text
                keep_norm = prev.norm
                keep_score = prev.score
            cx = int((it.center_xy[0] + prev.center_xy[0]) / 2)
            cy = int((it.center_xy[1] + prev.center_xy[1]) / 2)
            merged[-1] = MenuItem(text=keep_text, score=keep_score, center_xy=(cx, cy), norm=keep_norm)
        else:
            merged.append(it)

    return merged


@dataclass(frozen=True)
class MenuCapture:
    left: int
    top: int
    roi_bgr: np.ndarray
    crop_dx_dy: Tuple[int, int]
    items: List[MenuItem]


def capture_menu_items_auto(
    anchor_xy: Tuple[int, int],
    *,
    roi_sizes: Tuple[Tuple[int, int], ...] = ((520, 640), (700, 900)),
    min_items: int = 2,
) -> Optional[MenuCapture]:
    """
    Try multiple ROI sizes and optional background auto-crop; pick the best capture.
    """
    best: Optional[MenuCapture] = None
    best_score = -1e9

    t0 = time.time()
    for w, h in roi_sizes:
        # Inline the ROI math so we can use mss for speed.
        screen_w, screen_h = pyautogui.size()
        mx, my = (20, 20)
        x, y = anchor_xy

        left = x + mx
        top = y + my
        if left + w > screen_w:
            left = max(0, x - mx - w)
        if top + h > screen_h:
            top = max(0, y - my - h)

        left = int(max(0, min(left, screen_w - 1)))
        top = int(max(0, min(top, screen_h - 1)))
        width = int(min(w, screen_w - left))
        height = int(min(h, screen_h - top))

        roi = _capture_roi_bgr_fast(left, top, width, height)
        cropped, (dx, dy) = _auto_crop_menu_bg(roi)
        items = extract_menu_items_from_roi(cropped)

        if not items:
            continue

        avg_score = float(sum(it.score for it in items) / max(1, len(items)))
        ys = [it.center_xy[1] for it in items]
        span = (max(ys) - min(ys)) if ys else 0
        # Penalize if text spans almost full ROI height (likely clipped).
        clip_penalty = 0.0
        if cropped.shape[0] > 0 and span / float(cropped.shape[0]) > 0.85:
            clip_penalty = 2.0
        # Prefer more items and higher confidence.
        score = (len(items) * avg_score) - clip_penalty

        if score > best_score and len(items) >= min_items:
            best_score = score
            best = MenuCapture(left=left, top=top, roi_bgr=cropped, crop_dx_dy=(dx, dy), items=items)
            # Early exit: if we got a decent list, don't keep OCRing larger ROIs.
            if len(items) >= 4 and avg_score >= 0.70:
                break

    return best
