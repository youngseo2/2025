import streamlit as st
import random

st.title("📚 공부 도우미")

# -------------------------
# 명언 추천
# -------------------------
quotes = [
    "시작이 반이다. — 아리스토텔레스",
    "오늘의 노력이 내일의 너를 만든다.",
    "꾸준함이 결국 재능을 이긴다.",
    "할 수 있다고 믿는 순간, 반은 이루어진다. — 루스벨트",
    "포기하고 싶을 때가 진짜 시작이다."
]

if st.button("✨ 오늘의 명언 보기"):
    st.success(random.choice(quotes))

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
