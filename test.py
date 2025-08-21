import streamlit as st
import random

st.title("📚 공부 도우미")

# -------------------------
# 오늘의 기분 + 상태 선택
# -------------------------
mood = st.selectbox("오늘 기분은?", ["😊 좋음", "😐 그냥저냥", "😟 별로임"])
state = st.selectbox("현재 상태는?", ["💪 에너지 충분", "😴 피곤함", "🤯 스트레스"])

# 기분/상태별 명언 모음
quotes = {
    "😊 좋음": [
        "좋은 기분은 최고의 시작이다!",
        "행복은 성취의 연료다.",
        "웃음은 최고의 공부 에너지다."
    ],
    "😐 그냥저냥": [
        "작은 걸음이 큰 변화를 만든다.",
        "꾸준히 하면 반드시 성장한다.",
        "오늘도 어제보다 한 발자국."
    ],
    "😟 별로임": [
        "힘들수록 성장의 기회다.",
        "포기하지 마라, 내일의 너가 고마워할 것이다.",
        "어둠 속에서 별은 더 빛난다."
    ],
    "💪 에너지 충분": [
        "지금의 열정을 공부에 쏟아라!",
        "할 수 있다면 지금 해라. 기회는 두 번 오지 않는다.",
        "불타는 열정이 최고의 무기다."
    ],
    "😴 피곤함": [
        "조금씩이라도 하면 분명 쌓인다.",
        "쉬어가는 것도 전략이다.",
        "작게라도 해내는 자신을 믿어라."
    ],
    "🤯 스트레스": [
        "호흡을 가다듬고 다시 시작하라.",
        "마음의 평화가 최고의 무기다.",
        "잠시 쉬어도 괜찮다, 멈추지만 않으면 된다."
    ]
}

# 버튼 누르면 명언 추천
if st.button("✨ 오늘의 명언 보기"):
    candidates = quotes.get(mood, []) + quotes.get(state, [])
    if candidates:
        st.success(random.choice(candidates))

# -------------------------
# 할 일 체크리스트
# -------------------------
st.header("📝 오늘의 할 일")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

new_task = st.text_input("할 일을 입력하세요:")

if st.button("추가하기"):
    if new_task.strip():
        st.session_state.tasks.append({"task": new_task, "done": False})

for i, t in enumerate(st.session_state.tasks):
    checked = st.checkbox(t["task"], value=t["done"], key=i)
    st.session_state.tasks[i]["done"] = checked

if st.button("✅ 완료한 항목 지우기"):
    st.session_state.tasks = [t for t in st.session_state.tasks if not t["done"]]
