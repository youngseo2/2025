# app.py
# 실행: streamlit run app.py
import streamlit as st
import pandas as pd
import random
import hashlib
from datetime import datetime, date

st.set_page_config(page_title="아침 공부 명언 추천", page_icon="📚", layout="centered")

# -------------------------------
# 데이터: 카테고리별 공부 명언 (ko)
# -------------------------------
QUOTES = {
    "동기부여": [
        "시작이 반이다. 지금 1분을 잡으면 하루가 달라진다. — 아리스토텔레스",
        "완벽보다 완수가 낫다. 오늘의 작은 완수가 내일의 큰 자신감이 된다.",
        "성공은 열심히 준비한 사람이 기회와 만났을 때 온다. — 세네카",
        "천재의 1% 영감보다 99% 노력. — 에디슨",
        "오늘의 노력이 내일의 너를 만든다.",
        "지금의 불편함은 성장의 영수증이다.",
        "포기하고 싶을 때가 끝이 아니라, 진짜 시작점이다.",
        "작게라도 움직여라. 관성은 움직임 속에서 생긴다."
    ],
    "집중": [
        "중요한 일부터 하라. 사소함이 집중을 가장 잘 훔친다. — 스티븐 코비",
        "한 번에 하나. 깊게 파야 물이 나온다.",
        "집중은 ‘하지 않을 용기’에서 시작된다.",
        "방해를 줄이면 실력은 자연히 드러난다.",
        "몰입은 재능이 아니라 환경의 결과다.",
        "오늘 할 3가지만 정하고 끝까지 밀어라.",
        "소음은 멀리, 호흡은 깊이, 시선은 한 곳에.",
        "집중은 근육이다. 매일 조금씩 단련하라."
    ],
    "꾸준함": [
        "매일 1%의 개선이 1년 후 너를 바꾼다. — 제임스 클리어",
        "천천히 가도 멈추지 않으면 도착한다. — 공자",
        "루틴은 의지의 아껴 쓰기다.",
        "작은 승리를 기록하라. 기록은 습관을 만든다.",
        "지속이 곧 실력이다.",
        "오늘도 쌓았다면 성공한 하루다.",
        "꾸준함은 재능을 이긴다.",
        "세월이 흐를수록 중요한 건 ‘속도’가 아니라 ‘지속’이다."
    ],
    "회복/리셋": [
        "넘어졌다면 일어나라. 일어나면 그건 훈련이었다.",
        "실수는 데이터다. 다음 시도를 더 똑똑하게 만든다.",
        "휴식도 계획의 일부다.",
        "어제의 나를 용서해야 오늘의 내가 달린다.",
        "한 걸음 물러섬이 더 큰 도약이 된다.",
        "괜찮다. 다시 정리하고, 다시 시작하면 된다.",
        "완벽한 하루보다 회복 가능한 하루가 더 강하다.",
        "호흡을 고르면 생각도 정리된다."
    ],
    "자신감": [
        "할 수 있다고 믿는 순간, 반은 이루었다. — 시어도어 루스벨트",
        "비교는 자신감을 훔친다. 어제의 나와만 겨뤄라.",
        "작은 성공을 크게 칭찬하라. 뇌는 보상을 기억한다.",
        "나는 충분히 해낼 수 있다.",
        "두려움은 상상이고, 가능성은 사실이다.",
        "자신감은 결과가 아니라 선택이다.",
        "모르는 건 약점이 아니라 시작점이다.",
        "스스로를 응원하는 법을 배우자."
    ],
    "불안/스트레스": [
        "불안은 준비로 줄일 수 있다. 25분만 집중해서 시작하라.",
        "완벽한 계획보다 지금의 첫 줄이 낫다.",
        "호흡 4·7·8, 그리고 첫 문제 한 개.",
        "해야 할 것보다 할 수 있는 것부터.",
        "일단 자리에 앉는 것이 절반이다.",
        "할 일을 쪼개면 걱정도 쪼개진다.",
        "불안은 ‘미지’에서 오니, ‘시작’으로 줄여라.",
        "긴장은 실력을 꺼내는 스위치다."
    ],
    "슬럼프/권태": [
        "새로운 입력이 새로운 출력을 만든다. 공부 장소를 바꿔보자.",
        "작은 도전 하나. 문제 난이도를 반 단계만 올려라.",
        "권태는 신호다. 방법을 바꿔보라는.",
        "목표를 감정으로 연결하라. ‘왜’가 ‘어떻게’를 이끈다.",
        "5분만 하자. 그리고 5분을 한 번 더.",
        "루틴에 재미 한 스푼: 타이머, 체크리스트, 보상.",
        "완벽히 재충전한 뒤 다시 달려도 늦지 않다.",
        "슬럼프는 기록의 일부이지 결론이 아니다."
    ]
}

# -------------------------------
# 매핑: 기분/상태 → 추천 카테고리 가중치
# -------------------------------
MOODS = ["😊 상쾌함", "🙂 평온함", "😐 보통", "😵 피곤함", "😟 불안/걱정", "🥱 의욕저하", "😕 산만함", "🤩 의욕충만"]
STATES = ["잘 잤다", "수면부족", "스트레스 많음", "할 일 많음", "여유 있음", "시험/평가 임박", "슬럼프 느낌"]

PREFERENCES = {
    "😊 상쾌함": {"꾸준함": 3, "집중": 3, "동기부여": 2, "자신감": 2},
    "🙂 평온함": {"집중": 3, "꾸준함": 3, "동기부여": 2},
    "😐 보통": {"집중": 2, "꾸준함": 2, "동기부여": 2, "자신감": 1},
    "😵 피곤함": {"회복/리셋": 4, "꾸준함": 2, "집중": 1},
    "😟 불안/걱정": {"불안/스트레스": 4, "자신감": 2, "집중": 1},
    "🥱 의욕저하": {"슬럼프/권태": 4, "동기부여": 3, "자신감": 1},
    "😕 산만함": {"집중": 4, "불안/스트레스": 2},
    "🤩 의욕충만": {"동기부여": 4, "집중": 2, "꾸준함": 2, "자신감": 2},
}

STATE_BOOSTS = {
    "잘 잤다": {"집중": 2, "꾸준함": 1},
    "수면부족": {"회복/리셋": 3, "집중": -1},
    "스트레스 많음": {"불안/스트레스": 3, "회복/리셋": 1},
    "할 일 많음": {"집중": 3, "꾸준함": 1},
    "여유 있음": {"꾸준함": 2, "동기부여": 1},
    "시험/평가 임박": {"집중": 3, "자신감": 2, "불안/스트레스": 1},
    "슬럼프 느낌": {"슬럼프/권태": 3, "동기부여": 2}
}

GOALS = ["개념학습", "문제풀이/실전", "복습/정리", "암기", "모의고사 대비", "프로젝트/리포트"]

GOAL_TWEAKS = {
    "개념학습": {"집중": 1},
    "문제풀이/실전": {"집중": 1, "자신감": 1},
    "복습/정리": {"꾸준함": 1},
    "암기": {"집중": 1},
    "모의고사 대비": {"불안/스트레스": 1, "자신감": 1},
    "프로젝트/리포트": {"집중": 1, "동기부여": 1}
}

# -------------------------------
# 유틸리티
# -------------------------------
def weighted_categories(mood, state, goal):
    weights = {}
    for k, v in PREFERENCES.get(mood, {}).items():
        weights[k] = weights.get(k, 0) + v
    for k, v in STATE_BOOSTS.get(state, {}).items():
        weights[k] = weights.get(k, 0) + v
    for k, v in GOAL_TWEAKS.get(goal, {}).items():
        weights[k] = weights.get(k, 0) + v

    # 음수 방지 및 최소 가중치 보정
    for cat in QUOTES.keys():
        weights[cat] = max(0, weights.get(cat, 0))
    total = sum(weights.values())
    if total == 0:
        # 전부 0이면 기본 가중치
        for cat in QUOTES.keys():
            weights[cat] = 1
    return weights

def deterministic_choice(options, seed_str):
    """seed_str(문자열)을 해시로 변환하여 하루 고정 추천 생성"""
    h = hashlib.sha256(seed_str.encode()).hexdigest()
    idx = int(h, 16) % len(options)
    return options[idx]

def pick_quote(mood, state, goal, stable=True, exclude=None):
    weights = weighted_categories(mood, state, goal)
    cats = list(weights.keys())
    # 안정 모드: 오늘 날짜 기반으로 고정
    if stable:
        today = date.today().isoformat()
        # 카테고리 선택
        weighted_list = []
        for c in cats:
            weighted_list += [c] * max(1, weights[c])
        cat = deterministic_choice(weighted_list, f"{today}|{mood}|{state}|{goal}|cat")
        # 명언 선택
        candidates = QUOTES[cat]
        if exclude:
            candidates = [q for q in candidates if q not in exclude] or QUOTES[cat]
        quote = deterministic_choice(candidates, f"{today}|{mood}|{state}|{goal}|quote")
        return cat, quote
    else:
        # 비안정 모드: 가중 무작위
        population = []
        for c, w in weights.items():
            population += [c] * max(1, w)
        cat = random.choice(population)
        candidates = QUOTES[cat]
        if exclude:
            candidates = [q for q in candidates if q not in exclude] or QUOTES[cat]
        quote = random.choice(candidates)
        return cat, quote

def init_state():
    if "logs" not in st.session_state:
        st.session_state["logs"] = []  # [{date, mood, state, goal, quote, category, memo}]
    if "last_quote" not in st.session_state:
        st.session_state["last_quote"] = None
    if "today_fixed" not in st.session_state:
        st.session_state["today_fixed"] = None

init_state()

# -------------------------------
# UI
# -------------------------------
st.title("📚 아침 공부 명언 추천")
st.caption("매일 아침 기분과 상태에 맞춰 딱 맞는 한 줄. 꾸준함은 결국 실력이 됩니다 🙂")

col1, col2 = st.columns(2)
with col1:
    mood = st.selectbox("오늘 기분", MOODS, index=0)
with col2:
    state = st.selectbox("현재 상태", STATES, index=0)

goal = st.radio("오늘 공부 목표", GOALS, horizontal=True, index=1)

st.divider()

# 오늘의 고정 추천 생성 & 표시
if st.session_state["today_fixed"] is None:
    cat, q = pick_quote(mood, state, goal, stable=True)
    st.session_state["today_fixed"] = {"category": cat, "quote": q}

fixed = st.session_state["today_fixed"]
st.subheader("🌤️ 오늘의 명언")
st.markdown(f"> **[{fixed['category']}]** {fixed['quote']}")

colA, colB, colC = st.columns([1,1,1])
with colA:
    if st.button("📋 명언 복사"):
        st.toast("클립보드로 복사했습니다! (브라우저에서 직접 복사해 주세요.)")
with colB:
    # 오늘의 고정은 유지, 다른 후보 보기
    if st.button("🎲 다른 후보 보기"):
        cat2, q2 = pick_quote(mood, state, goal, stable=False, exclude={fixed["quote"]})
        st.session_state["last_quote"] = {"category": cat2, "quote": q2}
with colC:
    if st.button("🔄 기분/상태 반영해 오늘 명언 다시 고정"):
        cat_new, q_new = pick_quote(mood, state, goal, stable=True)
        st.session_state["today_fixed"] = {"category": cat_new, "quote": q_new}
        st.session_state["last_quote"] = None
        st.success("오늘의 명언을 현재 선택에 맞춰 새로 고정했어요!")

if st.session_state["last_quote"]:
    st.write("**또 다른 추천**")
    st.markdown(f"> [{st.session_state['last_quote']['category']}] {st.session_state['last_quote']['quote']}")

st.divider()

# 메모 및 기록 저장
memo = st.text_area("오늘의 한 줄 다짐/메모", placeholder="예) 오늘은 오답노트 30분 + 수학 N제 20문제")
save_col1, save_col2 = st.columns([1,1])
with save_col1:
    if st.button("📝 오늘 기록 저장"):
        today_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        entry = {
            "datetime": today_str,
            "mood": mood,
            "state": state,
            "goal": goal,
            "category": st.session_state["today_fixed"]["category"],
            "quote": st.session_state["today_fixed"]["quote"],
            "memo": memo.strip()
        }
        st.session_state["logs"].append(entry)
        st.success("기록이 저장되었습니다!")
with save_col2:
    if st.button("🧹 입력 초기화"):
        st.session_state["last_quote"] = None
        st.experimental_rerun()

# 기록 테이블 & 다운로드
st.divider()
st.subheader("📒 나의 기록")
if st.session_state["logs"]:
    df = pd.DataFrame(st.session_state["logs"])
    st.dataframe(df, use_container_width=True, hide_index=True)
    csv = df.to_csv(index=False).encode("utf-8-sig")
    st.download_button("⬇️ CSV로 다운로드", data=csv, file_name="study_quotes_logs.csv", mime="text/csv")
else:
    st.info("아직 저장된 기록이 없습니다. ‘오늘 기록 저장’을 눌러보세요!")

# 풋터
st.caption("Tip) ‘오늘의 명언’은 날짜·기분·상태·목표 조합으로 하루 동안 고정됩니다. \
다른 후보를 보고 싶으면 ‘다른 후보 보기’를 눌러보세요.")

