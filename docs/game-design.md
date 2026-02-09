# 뱀서라이크 (Vampire Survivors-like) 게임 기획서

> **플랫폼:** 메이플스토리 월드 (MSW)  
> **장르:** 뱀서라이크 (자동공격 로그라이크 서바이벌)  
> **핵심 컨셉:** 자동 공격 + 이동 생존 + 성장 선택

---

## 1. 게임 개요

플레이어는 끊임없이 몰려오는 적들 사이에서 생존하며, 자동으로 발사되는 무기로 적을 처치합니다.
적을 처치하면 경험치를 획득하고, 레벨업 시 새로운 무기나 패시브 능력을 선택해 점점 강해집니다.
제한 시간(15~30분)까지 생존하면 클리어합니다.

---

## 2. 핵심 기능 목록

### Phase 1 - 코어 루프 (생존의 기본)

| # | 기능 | 구현 파일 | 상태 |
|---|------|----------|------|
| 1 | **플레이어 이동** | `PlayerMovement.mlua` | ✅ |
| 2 | **적 스폰 시스템** | `EnemySpawnerLogic.mlua` | ✅ |
| 3 | **적 AI (추적)** | `EnemyChase.mlua` | ✅ |
| 4 | **충돌/피격 판정** | `Health.mlua`, `ContactDamage.mlua` | ✅ |
| 5 | **게임 상태 관리** | `GameManagerLogic.mlua` | ✅ |

### Phase 2 - 자동 공격 + 경험치 시스템

| # | 기능 | 구현 파일 | 상태 |
|---|------|----------|------|
| 6 | **자동 공격** | `AutoAttack.mlua` | ✅ |
| 7 | **투사체** | `Projectile.mlua` | ✅ |
| 8 | **경험치 젬** | `ExpGem.mlua` | ✅ |
| 9 | **레벨 시스템** | `LevelSystem.mlua` | ✅ |
| 10 | **보석 스폰** | `ExpGemSpawnerLogic.mlua` | ✅ |

### Phase 3 - 성장 선택 시스템

| # | 기능 | 구현 파일 | 상태 |
|---|------|----------|------|
| 11 | **레벨업 UI** | `LevelUpUILogic.mlua` | ✅ |
| 12 | **무기 데이터** | `WeaponData.mlua` | ✅ |
| 13 | **패시브 데이터** | `PassiveData.mlua` | ✅ |
| 14 | **플레이어 스탯** | `PlayerStats.mlua` | ✅ |

### Phase 4 - 무기 다양화

| # | 기능 | 구현 파일 | 상태 |
|---|------|----------|------|
| 15 | **무기 관리** | `WeaponManagerLogic.mlua` | ✅ |
| 16 | **회전 구체** | `OrbBehavior.mlua` | ✅ |
| 17 | **5종 무기** | 쿠나이, 구체, 도끼, 오라, 번개 | ✅ |

### Phase 5 - 게임 완성도

| # | 기능 | 구현 파일 | 상태 |
|---|------|----------|------|
| 18 | **보스 시스템** | `BossEnemy.mlua`, `BossSpawnerLogic.mlua` | ✅ |
| 19 | **필드 아이템** | `FieldItem.mlua`, `FieldItemSpawnerLogic.mlua` | ✅ |
| 20 | **생존 타이머 UI** | `SurvivalTimerUI.mlua` | ✅ |
| 21 | **킬 카운트 UI** | `KillCountUI.mlua` | ✅ |
| 22 | **HP바 UI** | `HpBarUI.mlua` | ✅ |
| 23 | **결과 화면** | `ResultScreenLogic.mlua` | ✅ |

---

## 3. 개발 단계별 계획

### 1단계: 코어 생존 루프
> **목표:** "적이 쫓아오고, 부딪히면 데미지를 받는다"

- [x] PlayerMovement - 플레이어 8방향 이동
- [x] EnemySpawnerLogic - 주기적 적 생성
- [x] EnemyChase - 적이 플레이어를 향해 이동
- [x] Health - HP 시스템 (데미지, 사망)
- [x] ContactDamage - 접촉 시 데미지
- [x] GameManagerLogic - 기본 게임 상태 관리

### 2단계: 자동 공격 + 경험치
> **목표:** "적을 죽이고 경험치를 먹는다"

- [x] AutoAttack - 자동 투사체 발사
- [x] Projectile - 투사체 이동 + 충돌 판정
- [x] ExpGem - 경험치 젬 드롭 + 수집
- [x] LevelSystem - 경험치 누적 → 레벨업
- [x] ExpGemSpawnerLogic - 적 사망 시 보석 스폰

### 3단계: 레벨업 + 성장 선택
> **목표:** "레벨업하고 무기/패시브를 고른다"

- [x] LevelUpUILogic - 3지선다 선택 UI
- [x] WeaponData - 5종 무기 데이터 정의
- [x] PassiveData - 7종 패시브 데이터 정의
- [x] PlayerStats - 승수 기반 스탯 관리

### 4단계: 무기 다양화 + 밸런싱
> **목표:** "다양한 무기로 재미있게 플레이"

- [x] WeaponManagerLogic - 무기 슬롯/쿨타임/실행 관리
- [x] OrbBehavior - 회전 구체 공전 행동
- [x] LevelUpUILogic 업데이트 - WeaponManager 연동

### 5단계: 마무리
> **목표:** "완성된 게임"

- [x] BossEnemy - 보스 전용 컴포넌트 (돌진/소환/범위)
- [x] BossSpawnerLogic - 60초 주기 보스 출현
- [x] SurvivalTimerUI - 생존 타이머 UI
- [x] KillCountUI - 킬 카운트 UI
- [x] HpBarUI - HP바 UI
- [x] FieldItem - 필드 아이템 (치유/자석/폭탄/EXP)
- [x] FieldItemSpawnerLogic - 랜덤 아이템 스폰
- [x] ResultScreenLogic - 결과 화면 표시

---

## 4. MSW 기술 구현 매핑

| 게임 기능 | MSW 구현 방식 |
|-----------|---------------|
| 플레이어 이동 | `TransformComponent.Position` 직접 조작 |
| 적 추적 AI | 매 프레임 플레이어 방향 계산 → Position 이동 |
| 적 스폰 | Model 미리 등록 → `_SpawnService:SpawnByModelId()` |
| 충돌 판정 | `TriggerComponent` + 이벤트 핸들러 |
| HP 시스템 | `@Sync` 프로퍼티로 HP 동기화 |
| UI (레벨업 선택) | `UIGroupComponent` + `ButtonComponent` |
| 실행 공간 | 이동 입력/UI → Client, 스폰/HP/데미지 → Server |

---

## 5. 엔티티 구조 설계

```
[Player Entity]
├── TransformComponent
├── SpriteRendererComponent (캐릭터 스프라이트)
├── TriggerComponent (피격 판정 영역)
├── PlayerMovement (커스텀 - 이동 입력)
├── Health (커스텀 - HP 관리)
├── LevelSystem (커스텀 - 경험치/레벨)
├── PlayerStats (커스텀 - 승수 기반 스탯)
└── AutoAttack (커스텀 - 기본 자동 공격, 선택적)

[Enemy Entity] (Model로 등록)
├── TransformComponent
├── SpriteRendererComponent (적 스프라이트)
├── TriggerComponent (접촉 판정 영역)
├── EnemyChase (커스텀 - 추적 AI)
├── Health (커스텀 - HP)
└── ContactDamage (커스텀 - 접촉 데미지)

[Boss Entity] (Model로 등록)
├── TransformComponent
├── SpriteRendererComponent (보스 스프라이트, 크게)
├── TriggerComponent (넓은 충돌 영역)
├── EnemyChase (커스텀 - 추적 AI)
├── Health (커스텀 - 높은 HP)
├── ContactDamage (커스텀 - 높은 접촉 데미지)
└── BossEnemy (커스텀 - 특수 행동 패턴)

[Projectile Entity] (Model로 등록)
├── TransformComponent
├── SpriteRendererComponent
├── TriggerComponent
└── Projectile (커스텀 - 방향 이동 + 충돌)

[Orb Entity] (Model로 등록)
├── TransformComponent
├── SpriteRendererComponent
├── TriggerComponent
├── Projectile (커스텀 - 데미지 판정)
└── OrbBehavior (커스텀 - 공전 운동)

[ExpGem Entity] (Model로 등록)
├── TransformComponent
├── SpriteRendererComponent
├── TriggerComponent
└── ExpGem (커스텀 - 자석 효과 + 수집)

[FieldItem Entity] (Model로 등록)
├── TransformComponent
├── SpriteRendererComponent
├── TriggerComponent
└── FieldItem (커스텀 - 아이템 효과)

[UI Entities]
├── SurvivalTimerUI (시간 표시)
├── KillCountUI (킬 카운트 표시)
├── HpBarUI (플레이어 HP바)
└── LevelUpPanel (레벨업 선택지 3개 버튼)

[Global Logics]
├── GameManagerLogic (게임 상태, 타이머, 점수)
├── EnemySpawnerLogic (적 웨이브 스폰)
├── BossSpawnerLogic (보스 주기 스폰)
├── ExpGemSpawnerLogic (경험치 보석 스폰)
├── FieldItemSpawnerLogic (필드 아이템 스폰)
├── WeaponManagerLogic (무기 슬롯/공격 실행)
├── WeaponData (무기 데이터 테이블)
├── PassiveData (패시브 데이터 테이블)
├── LevelUpUILogic (레벨업 선택지 UI)
└── ResultScreenLogic (결과 화면)
```

---

## 6. 데이터 설계 (밸런스 초안)

### 플레이어
| 항목 | 기본값 |
|------|--------|
| 최대 HP | 100 |
| 이동 속도 | 200 px/s |
| 피격 무적 시간 | 0.5초 |

### 적 (기본형)
| 항목 | 기본값 |
|------|--------|
| HP | 10 |
| 이동 속도 | 80 px/s |
| 접촉 데미지 | 10 |

### 스폰
| 항목 | 기본값 |
|------|--------|
| 초기 스폰 주기 | 2.0초 |
| 최소 스폰 주기 | 0.3초 |
| 웨이브당 스폰 수 | 1 → 시간 경과 시 증가 |
| 스폰 거리 | 플레이어 기준 500~700px |
| 최대 동시 적 수 | 50 |

### 무기 시스템 (5종)

| 무기 ID | 이름 | 타입 | 최대 레벨 | 특징 |
|---------|------|------|-----------|------|
| kunai | 쿠나이 | 직선 투사체 | 8 | 가까운 적 방향 고속 발사, 레벨업 시 개수↑ 관통↑ |
| orb | 회전 구체 | 공전 | 8 | 플레이어 주위 회전, 레벨업 시 개수↑ |
| axe | 도끼 | 포물선 | 8 | 위로 포물선 궤적, 넓은 범위 |
| aura | 보호 오라 | 범위 AoE | 8 | 주변 지속 데미지, 빠른 쿨타임 |
| lightning | 번개 | 즉발 타격 | 8 | 랜덤 위치 즉발 데미지, 레벨업 시 타겟 수↑ |

### 패시브 시스템 (7종)

| 패시브 ID | 이름 | 효과 | 최대 레벨 | 레벨당 증가량 |
|-----------|------|------|-----------|--------------|
| speed_up | 이동속도 증가 | 이동속도 승수 | 5 | +10% |
| damage_up | 공격력 증가 | 데미지 승수 | 5 | +15% |
| cooldown_down | 쿨다운 감소 | 쿨타임 승수 | 5 | -8% (곱연산) |
| max_hp_up | 최대 HP 증가 | 최대 HP | 5 | +20 |
| hp_regen | HP 재생 | HP 자동 회복 | 5 | +1 HP/5초 |
| magnet | 아이템 자석 | 보석 흡수 범위 | 5 | +30% |
| area_up | 범위 증가 | 무기/투사체 크기 | 5 | +10% |

### 보스 시스템

| 항목 | 기본값 |
|------|--------|
| 스폰 주기 | 60초 |
| 기본 HP | 500 (웨이브마다 1.5배 증가) |
| 접촉 데미지 | 30 |
| 특수 행동 쿨타임 | 5초 |

**보스 유형:**
- **돌진형 (charge):** 3배 속도로 1초간 돌진
- **소환형 (summon):** 주변에 일반 적 5마리 소환
- **범위형 (aoe):** 300px 범위 내 플레이어에게 데미지

### 필드 아이템

| 아이템 ID | 이름 | 효과 | 생존 시간 | 스폰 확률 |
|-----------|------|------|-----------|----------|
| heal | 힐 아이템 | HP +50 회복 | 15초 | 40% |
| magnet | 자석 | 화면 모든 보석 즉시 흡수 | 15초 | 20% |
| bomb | 폭탄 | 화면 모든 적 대미지 | 15초 | 20% |
| exp_all | EXP 부스트 | 즉시 경험치 +100 | 15초 | 20% |

**필드 아이템 스폰:**
- 스폰 간격: 20초마다 랜덤 1개
- 스폰 범위: 플레이어 기준 100~500px 랜덤 위치

### 레벨 시스템

| 항목 | 값 |
|------|-----|
| 레벨 1 필요 경험치 | 20 |
| 경험치 증가율 | 1.3배 (지수 성장) |
| 레벨 공식 | RequiredExp = 20 × (1.3 ^ (level - 1)) |

**예시:**
- Lv.1→2: 20 EXP
- Lv.2→3: 26 EXP
- Lv.3→4: 34 EXP
- Lv.10: 약 238 EXP

---

## 7. 게임 플레이 흐름

1. **게임 시작** → 플레이어에게 기본 무기(쿠나이) 지급
2. **적 스폰 시작** → 2초마다 적 생성, 30초마다 난이도 증가
3. **전투 루프** → 자동 공격으로 적 처치 → 경험치 보석 드롭 → 보석 수집
4. **레벨업** → 3개 선택지 제시 (무기 신규/강화, 패시브)
5. **보스 등장** → 60초마다 보스 출현 (체력 높음, 특수 패턴)
6. **필드 아이템** → 20초마다 랜덤 아이템 스폰 (힐/자석/폭탄/EXP)
7. **게임 종료**
   - **클리어:** 제한 시간(10분) 생존 성공
   - **게임 오버:** 플레이어 HP 0
8. **결과 화면** → 생존 시간, 처치 수, 최종 레벨 표시

---

## 8. 구현 완료 파일 목록

### Components (15개)
1. `PlayerMovement.mlua` - 8방향 이동 입력
2. `EnemyChase.mlua` - 적 추적 AI
3. `Health.mlua` - HP 관리 (공용)
4. `ContactDamage.mlua` - 접촉 데미지
5. `AutoAttack.mlua` - 기본 자동 공격
6. `Projectile.mlua` - 투사체 이동/충돌
7. `ExpGem.mlua` - 경험치 보석 자석
8. `LevelSystem.mlua` - 레벨/경험치
9. `PlayerStats.mlua` - 승수 기반 스탯
10. `OrbBehavior.mlua` - 회전 구체 공전
11. `BossEnemy.mlua` - 보스 특수 행동
12. `FieldItem.mlua` - 필드 아이템 효과
13. `SurvivalTimerUI.mlua` - 생존 타이머 UI
14. `KillCountUI.mlua` - 킬 카운트 UI
15. `HpBarUI.mlua` - HP바 UI

### Logics (10개)
1. `GameManagerLogic.mlua` - 게임 전체 상태 관리
2. `EnemySpawnerLogic.mlua` - 적 웨이브 스폰
3. `BossSpawnerLogic.mlua` - 보스 주기 스폰
4. `ExpGemSpawnerLogic.mlua` - 보석 스폰
5. `FieldItemSpawnerLogic.mlua` - 아이템 스폰
6. `WeaponManagerLogic.mlua` - 무기 슬롯/공격 실행
7. `WeaponData.mlua` - 5종 무기 데이터
8. `PassiveData.mlua` - 7종 패시브 데이터
9. `LevelUpUILogic.mlua` - 레벨업 선택지 UI
10. `ResultScreenLogic.mlua` - 결과 화면 표시

**총 25개 스크립트 파일로 완전한 뱀서라이크 게임 구현 완료** ✅
