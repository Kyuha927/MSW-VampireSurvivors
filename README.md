# MSW Maker 자동화 시스템

MSW Maker GUI를 자동으로 제어하여 컴포넌트 스크립트를 대량 생성하고 Lua 코드를 자동으로 붙여넣는 Python 기반 자동화 도구입니다.

## 기능

- **자동 스크립트 생성**: MyDesk 우클릭 → 메뉴 선택 → 이름 입력 → 생성
- **자동 코드 붙여넣기**: Plain Text 탭 선택 → Lua 파일 내용 붙여넣기 → 저장
- **OCR 기반 메뉴 인식**: RapidOCR로 메뉴 텍스트 인식 및 클릭
- **매크로 캐싱**: 첫 실행 후 좌표 캐싱으로 빠른 반복 실행
- **ESC 즉시 중단**: 실행 중 ESC 키로 안전하게 중단 가능

## 사용된 기술/기능

| 기술 | 용도 |
|------|------|
| **Python 3** | 메인 언어 |
| **pyautogui** | 마우스/키보드 제어, 화면 캡처 |
| **RapidOCR (ONNX Runtime)** | 메뉴 텍스트 OCR 인식 |
| **OpenCV (cv2)** | 이미지 전처리, ROI 처리 |
| **mss** | 빠른 화면 캡처 |
| **pyperclip** | 클립보드 복사/붙여넣기 |
| **difflib** | 퍼지 문자열 매칭 |
| **ctypes** | ESC 키 감지 (Win32 API) |

### 핵심 알고리즘

1. **OCR 메뉴 클릭**: 화면 캡처 → OCR 텍스트 추출 → 퍼지 매칭 → 클릭
2. **좌표 캐싱**: 첫 성공 좌표 저장 → 이후 캐시에서 바로 클릭
3. **Interruptible Sleep**: ESC 폴리로 즉시 중단 가능한 대기
4. **Region-based Detection**: Plain Text 탭 등 특정 영역만 OCR 스캔

## 설치 방법

### 방법 1: ZIP 다운로드

1. 링크 클릭: [Download ZIP](https://github.com/[USERNAME]/[REPO]/archive/refs/heads/master.zip)
2. 압축 해제
3. PowerShell에서 해당 폴더로 이동:

```powershell
cd C:\Users\[사용자명]\Downloads\MSW-VampireSurvivors-master
pip install -r automation/requirements.txt
python run_msw_setup.py
```

### 방법 2: PowerShell 한 줄 설치 (관리자 권한)

```powershell
iwr -useb https://raw.githubusercontent.com/[USERNAME]/[REPO]/master/install.ps1 | iex
```

### 방법 3: curl/wget (Linux/Mac용)

```bash
# ZIP 다운로드
curl -L -o msw-automation.zip https://github.com/[USERNAME]/[REPO]/archive/refs/heads/master.zip
unzip msw-automation.zip
cd MSW-VampireSurvivors-master
pip install -r automation/requirements.txt
python run_msw_setup.py
```

### 방법 4: Git Clone

```bash
git clone https://github.com/[USERNAME]/[REPO].git
cd MSW-VampireSurvivors
pip install -r automation/requirements.txt
python run_msw_setup.py
```

### 수동 설치 (의존성)

```bash
pip install pyautogui mss rapidocr-onnxruntime pyperclip opencv-python numpy
```

## 실행 방법

### 1. 전체 자동화 (생성 + 코드 붙여넣기 + 저장)

```powershell
python run_msw_setup.py
```

**동작 순서**:
1. 11개 컴포넌트 순회 (PlayerMovement, EnemyChase, Health 등)
2. 각 컴포넌트별:
   - MyDesk 우클릭
   - "Create Scripts" → "Create Script" 선택
   - 스크립트명 입력 + Enter
   - 2초 대기 (에디터 열림)
   - "Plain Text" 탭 선택
   - 편집영역 클릭 → Ctrl+A → Lua 코드 붙여넣기
   - Ctrl+S 저장
3. 다음 컴포넌트로 진행

**중지**: 실행 중 `ESC` 키 누르기 (50ms 폴링으로 즉시 반응)

### 2. 생성만 (코드 붙여넣기 없이)

```powershell
python run_create_only.py
```

스크립트 생성까지만 수행합니다.

## 주요 파일 구조

```
automation/
├── msw_controller.py          # 메인 컨트롤러 (UI 제어, OCR 클릭)
├── msw_menu_vision.py         # OCR 엔진 (RapidOCR + 이미지 처리)
├── msw_workflow.py            # 워크플로우 정의
├── find_region.py             # 리전 좌표 측정 도구
├── config.py                  # 설정 및 피처 플래그
├── requirements.txt           # Python 의존성
└── workflows/
    ├── create_only.py         # 생성-only 워크플로우
    └── create_and_paste.py    # 생성+붙여넣기 워크플로우

run_msw_setup.py               # 메인 실행 진입점
```

## 좌표 설정

**MyDesk 위치** (수동 설정 필요):
```python
# automation/msw_controller.py
MYDESK_X = 1824
MYDESK_Y = 894
```

**Plain Text 탭 리전** (1920x1080 기준 비율):
```python
# run_msw_setup.py
tab_x0_ratio = 0.7646      # 화면 너비의 76.46%
tab_y0_ratio = 0.8222      # 화면 높이의 82.22%
tab_w_ratio  = 0.0615      # 화면 너비의 6.15%
tab_h_ratio  = 0.0176      # 화면 높이의 1.76%
```

**좌표 측정 도구 사용**:
```powershell
python automation/find_region.py
# 마우스를 원하는 위치로 이동하면 좌표 표시
# Ctrl+C로 복사
```

## 문제 해결

### 1. OCR 인식 실패

**증상**: "Create Scripts"를 찾지 못함

**해결**:
- MSW Maker 창이 화면 중앙에 위치하는지 확인
- MyDesk 좌표(`MYDESK_X`, `MYDESK_Y`) 재설정
- `find_region.py`로 실제 좌표 측정 후 수정

### 2. 캐시 좌표 불일치

**증상**: 두 번째 컴포넌트부터 "Cache mismatch" 경고

**해결**:
- 이는 정상 동작 (메뉴가 닫혀서 검증 실패)
- 캐시 검증을 생략하도록 수정됨 (빠른 매크로 실행)

### 3. Plain Text 탭을 못 찾음

**증상**: "Plain Text" OCR 실패

**해결**:
- `find_region.py`로 Plain Text 탭 좌표 직접 측정
- `run_msw_setup.py`의 비율 값 수정

### 4. ESC가 안 먹음

**증상**: ESC를 눌러도 종료 안 됨

**해결**:
- `Ctrl+C`로 강제 종료
- 코드 수정: `_sleep_interruptible()` 사용 확인

## 작동 원리

### OCR 메뉴 클릭 흐름

1. **캐시 확인**: 이전 실행 좌표가 있으면 바로 클릭
2. **OCR 스캔**: 없으면 화면 캡처 후 RapidOCR로 텍스트 인식
3. **퍼지 매칭**: "Create Scripts"와 OCR 결과 비교 (유사도 0.45 이상)
4. **클릭 실행**: 매칭된 위치 클릭 후 좌표 캐싱

### 워크플로우 시스템

```python
CREATE_AND_PASTE_SCRIPT_WORKFLOW = [
    {"action": "right_click"},
    {"action": "select_menu", "goal": "Create Scripts"},
    {"action": "select_menu", "goal": "Create Script"},
    {"action": "type_text", "text": "SCRIPT_NAME"},
    {"action": "press_key", "key": "enter"},
    {"action": "wait", "seconds": 2.0},
    {"action": "select_menu", "goal": "Plain Text", "region": "PLAINTEXT_TAB_REGIONS"},
    {"action": "click_region_center", "region": "EDITOR_TEXT_REGIONS"},
    {"action": "hotkey", "keys": ["ctrl", "a"]},
    {"action": "paste_file_content", "file": "LUA_FILE_PATH"},
    {"action": "hotkey", "keys": ["ctrl", "s"]},
]
```

## 주의사항

1. **화면 해상도**: 1920x1080 기준으로 설정됨. 다른 해상도는 좌표 재조정 필요
2. **MSW Maker 창**: 실행 전 반드시 활성화 및 화면 중앙 배치
3. **관리자 권한**: 필요시 PowerShell을 관리자 권한으로 실행
4. **백업**: 중요한 프로젝트는 실행 전 백업 권장

## 라이선스

이 프로젝트는 남부럽지 않게 만든 자동화 도구입니다.
