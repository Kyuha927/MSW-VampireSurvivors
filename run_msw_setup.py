"""
MSW Maker 게임 컴포넌트 일괄 생성 자동화 시퀀스

목표: scripts/components/에 있는 모든 스크립트를 MSW Maker에 자동으로 생성하고 등록합니다.
"""

import sys
from pathlib import Path

# automation 모듈 경로 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "automation"))

from automation.msw_controller import MSWController, MYDESK_X, MYDESK_Y
from automation.msw_workflow import CREATE_AND_PASTE_SCRIPT_WORKFLOW
import time
import pyautogui

# 실제 프로젝트에 필요한 컴포넌트 목록
REAL_COMPONENTS = [
    "PlayerMovement",
    "EnemyChase",
    "Health",
    "ContactDamage",
    "AutoAttack",
    "Projectile",
    "ExpGem",
    "LevelSystem",
    "PlayerStats",
    "OrbBehavior",
    "BossEnemy",
]

def run_full_automation():
    print("="*60)
    print("🚀 MSW Maker MACRO ENGINE 시작")
    print("="*60)
    
    controller = MSWController(anchor_xy=(MYDESK_X, MYDESK_Y))
    
    # Screen size for region calculation
    sw, sh = pyautogui.size()
    
    # 1. Plain Text Tab Region (Measured)
    tab_x0_ratio = 0.7646
    tab_y0_ratio = 0.8222
    tab_w_ratio  = 0.0615
    tab_h_ratio  = 0.0176
    
    plaintext_tab_regions = [
        (int(sw * tab_x0_ratio), int(sh * tab_y0_ratio), int(sw * tab_w_ratio), int(sh * tab_h_ratio))
    ]

    # 2. Editor Text Region (Focus Target)
    editor_text_regions = [
        (int(sw * 0.22), int(sh * 0.30), int(sw * 0.56), int(sh * 0.58))
    ]
    
    print("\n3초 후 시작합니다. MSW Maker 창을 활성화해주세요!")
    time.sleep(3)

    success_count = 0
    for name in REAL_COMPONENTS:
        lua_path = f"scripts/components/{name}.lua"
        print(f"\n▶ [{success_count + 1}/{len(REAL_COMPONENTS)}] '{name}' 생성 + 코드 복붙 중...")
        
        ok = controller.execute_workflow(
            CREATE_AND_PASTE_SCRIPT_WORKFLOW, 
            params={
                "SCRIPT_NAME": name,
                "LUA_FILE_PATH": lua_path,
                "PLAINTEXT_TAB_REGIONS": plaintext_tab_regions,
                "EDITOR_TEXT_REGIONS": editor_text_regions,
            }
        )
        
        if ok:
            success_count += 1
            print(f"  ✅ 완료")
        else:
            if controller.was_interrupted():
                print(f"\n[STOP] ESC 감지. 프로그램을 종료합니다.")
                break

            print(f"  ❌ 실패 - 5초 대기 후 재시도합니다...")
            pyautogui.press("escape")
            time.sleep(1)
            pyautogui.press("escape")
            time.sleep(5)
            
            # 재시도
            ok2 = controller.execute_workflow(
                CREATE_AND_PASTE_SCRIPT_WORKFLOW,
                params={
                    "SCRIPT_NAME": name,
                    "LUA_FILE_PATH": lua_path,
                    "PLAINTEXT_TAB_REGIONS": plaintext_tab_regions,
                    "EDITOR_TEXT_REGIONS": editor_text_regions,
                }
            )
            if ok2:
                success_count += 1
                print(f"  ✅ 재시도 성공")
            else:
                if controller.was_interrupted():
                    print(f"\n[STOP] ESC 감지. 프로그램을 종료합니다.")
                    break
                print(f"  ❌ 재시도도 실패. 이 컴포넌트 건너뜁니다.")
                pyautogui.press("escape")
                time.sleep(1)

    print("\n" + "="*60)
    print(f"🎉 모든 작업 종료! 성공: {success_count}/{len(REAL_COMPONENTS)}")
    print("="*60)

if __name__ == "__main__":
    run_full_automation()
