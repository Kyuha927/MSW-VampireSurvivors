# MSW 뱀서라이크 프로젝트

메이플스토리 월드에서 개발하는 뱀서라이크(Vampire Survivors-like) 게임입니다.

## 프로젝트 구조

```
MSW-VampireSurvivors/
├── docs/
│   └── game-design.md                   # 전체 게임 기획서
├── scripts/
│   ├── components/                       # 엔티티에 붙이는 컴포넌트
│   │   ├── PlayerMovement.mlua           # 플레이어 8방향 이동
│   │   ├── EnemyChase.mlua               # 적 추적 AI
│   │   ├── Health.mlua                   # HP 시스템 (공용)
│   │   ├── ContactDamage.mlua            # 접촉 데미지
│   │   ├── AutoAttack.mlua               # 기본 자동 공격 (선택적)
│   │   ├── Projectile.mlua               # 투사체 이동 + 충돌
│   │   ├── ExpGem.mlua                   # 경험치 보석 + 자석
│   │   ├── LevelSystem.mlua              # 경험치/레벨 관리
│   │   ├── PlayerStats.mlua              # 승수 기반 스탯
│   │   ├── OrbBehavior.mlua              # 회전 구체 공전
│   │   ├── BossEnemy.mlua                # 보스 특수 행동
│   │   ├── FieldItem.mlua                # 필드 아이템 (치유/자석/폭탄)
│   │   ├── SurvivalTimerUI.mlua          # 생존 타이머 UI
│   │   ├── KillCountUI.mlua              # 킬 카운트 UI
│   │   └── HpBarUI.mlua                  # HP바 UI
│   └── logics/                           # 전역 게임 로직
│       ├── GameManagerLogic.mlua          # 게임 상태 관리
│       ├── EnemySpawnerLogic.mlua         # 적 웨이브 스폰
│       ├── BossSpawnerLogic.mlua          # 보스 주기 스폰
│       ├── ExpGemSpawnerLogic.mlua        # 경험치 보석 스폰
│       ├── FieldItemSpawnerLogic.mlua     # 필드 아이템 스폰
│       ├── WeaponManagerLogic.mlua        # 무기 슬롯/공격 실행
│       ├── WeaponData.mlua                # 5종 무기 데이터
│       ├── PassiveData.mlua               # 7종 패시브 데이터
│       ├── LevelUpUILogic.mlua            # 레벨업 선택지 UI
│       └── ResultScreenLogic.mlua         # 결과 화면 표시
└── README.md
```

## MSW 메이커 설정 가이드

### 사전 준비

1. **메이플스토리 월드 메이커** 접속
2. **LocalWorkspace 활성화** (Workspace > WorldConfig > LocalWorkspace)
3. **ExtendedScriptFormat 활성화** (UseExtendedScriptFormat 체크)
4. **VS Code 연동 활성화** (File > Setting > 만들기 > LocalWorkspace)

### Step 1: 스크립트 등록

메이커에서 아래 스크립트 엔트리를 생성하고, 이 프로젝트의 `.mlua` 파일 내용을 복사합니다.

| 스크립트 | 타입 | 용도 |
|----------|------|------|
| `PlayerMovement` | Component | 플레이어 이동 |
| `EnemyChase` | Component | 적 추적 AI |
| `Health` | Component | HP 관리 |
| `ContactDamage` | Component | 접촉 데미지 |
| `AutoAttack` | Component | 기본 자동 공격 (선택적) |
| `Projectile` | Component | 투사체 이동/충돌 |
| `ExpGem` | Component | 경험치 보석 |
| `LevelSystem` | Component | 레벨/경험치 |
| `PlayerStats` | Component | 스탯 승수 관리 |
| `OrbBehavior` | Component | 회전 구체 공전 |
| `BossEnemy` | Component | 보스 특수 행동 |
| `FieldItem` | Component | 필드 아이템 |
| `SurvivalTimerUI` | Component | 타이머 UI |
| `KillCountUI` | Component | 킬 카운트 UI |
| `HpBarUI` | Component | HP바 UI |
| `GameManagerLogic` | Logic | 게임 상태 관리 |
| `EnemySpawnerLogic` | Logic | 적 스폰 관리 |
| `BossSpawnerLogic` | Logic | 보스 스폰 관리 |
| `ExpGemSpawnerLogic` | Logic | 보석 스폰 관리 |
| `FieldItemSpawnerLogic` | Logic | 아이템 스폰 관리 |
| `WeaponManagerLogic` | Logic | 무기 슬롯/공격 |
| `WeaponData` | Logic | 무기 데이터 |
| `PassiveData` | Logic | 패시브 데이터 |
| `LevelUpUILogic` | Logic | 레벨업 UI |
| `ResultScreenLogic` | Logic | 결과 화면 |

### Step 2: Model 생성 (적, 투사체, 보석, 아이템 등)

**Enemy Model:**
1. 새 엔티티 → TransformComponent, SpriteRendererComponent, TriggerComponent
2. + `EnemyChase` (Speed: 80) + `Health` (MaxHP: 10) + `ContactDamage` (Damage: 10)
3. **Model로 등록** → ID 복사

**Projectile Models (쿠나이, 도끼 등):**
1. 새 엔티티 → TransformComponent, SpriteRendererComponent, TriggerComponent
2. + `Projectile` (Speed/Damage/Lifetime 기본값)
3. 무기 종류별 각각 Model 등록 → ID 복사

**Orb Model (회전 구체):**
1. 새 엔티티 → TransformComponent, SpriteRendererComponent, TriggerComponent
2. + `Projectile` + `OrbBehavior`
3. Model 등록 → ID 복사

**ExpGem Model:**
1. 새 엔티티 → TransformComponent, SpriteRendererComponent, TriggerComponent
2. + `ExpGem`
3. Model 등록 → ID 복사

**Boss Model:**
1. 새 엔티티 → TransformComponent, SpriteRendererComponent (크게), TriggerComponent (넓게)
2. + `EnemyChase` (Speed: 50) + `Health` (MaxHP: 500) + `ContactDamage` (Damage: 30) + `BossEnemy`
3. Model 등록 → ID 복사

**FieldItem Models (힐/자석/폭탄/EXP):**
1. 아이템별 엔티티 → TransformComponent, SpriteRendererComponent, TriggerComponent
2. + `FieldItem` (ItemType 설정: "heal"/"magnet"/"bomb"/"exp_all")
3. 각각 Model 등록 → ID 복사

### Step 3: Player 엔티티 설정

1. Player 엔티티에 아래 컴포넌트를 추가합니다:
   - `PlayerMovement` → MoveSpeed: 200
   - `Health` → MaxHP: 100, InvincibleDuration: 0.5
   - `LevelSystem` → RequiredExpBase: 20, ExpGrowthRate: 1.3
   - `PlayerStats` → (기본값 사용)
   - `TriggerComponent` → 피격 판정 영역 설정

### Step 4: UI 엔티티 설정

1. **생존 타이머** 엔티티 → TextComponent + `SurvivalTimerUI`
2. **킬 카운트** 엔티티 → TextComponent + `KillCountUI`
3. **HP 바** 엔티티 → SpriteRendererComponent + `HpBarUI`
4. **레벨업 패널** 엔티티 → 3개 버튼 엔티티 (선택지)

### Step 5: Logic 설정

1. `GameManagerLogic` → TimeLimit: 600
2. `EnemySpawnerLogic` → EnemyModelId: (Step 2에서 복사한 ID)
3. `BossSpawnerLogic` → Boss1ModelId: (보스 Model ID), BossInterval: 60
4. `ExpGemSpawnerLogic` → GemModelId: (보석 Model ID)
5. `FieldItemSpawnerLogic` → 각 아이템 Model ID 설정
6. `WeaponManagerLogic` → 각 무기 투사체 Model ID 설정
7. `WeaponData`, `PassiveData`, `LevelUpUILogic`, `ResultScreenLogic` 등록

### Step 6: 게임 시작 연결

게임 시작 시 `GameManagerLogic:StartGame(playerEntityId)`를 호출해야 합니다.
플레이어 접속 이벤트에서 이를 자동 호출하도록 연결합니다.

## 개발 단계

- [x] **1단계:** 코어 생존 루프 (이동, 적 스폰, 추적, 피격)
- [x] **2단계:** 자동 공격 + 경험치 (투사체, EXP 보석, 레벨)
- [x] **3단계:** 레벨업 선택 시스템 (무기/패시브 데이터, UI, 스탯)
- [x] **4단계:** 무기 다양화 (WeaponManager, 회전구체, 5종 무기)
- [x] **5단계:** 마무리 (보스, 필드아이템, HP바, 타이머, 결과화면)

## 무기 종류 (5종)

| 무기 | 설명 | 최대 레벨 |
|------|------|-----------|
| 쿠나이 (kunai) | 가까운 적 방향 직선 투사체 | 8 |
| 회전 구체 (orb) | 플레이어 주위 공전 | 8 |
| 도끼 (axe) | 위로 포물선 궤적 | 8 |
| 보호 오라 (aura) | 주변 범위 지속 데미지 | 8 |
| 번개 (lightning) | 랜덤 위치 즉발 데미지 | 8 |

## 패시브 종류 (7종)

| 패시브 | 레벨당 효과 | 최대 레벨 |
|--------|-------------|-----------|
| 이동속도 증가 | +10% | 5 |
| 공격력 증가 | +15% | 5 |
| 쿨다운 감소 | -8% | 5 |
| 최대 HP 증가 | +20 | 5 |
| HP 재생 | +1 HP/5s | 5 |
| 아이템 자석 | +30% 범위 | 5 |
| 범위 증가 | +10% | 5 |
