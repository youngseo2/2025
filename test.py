
import streamlit as st
import random

st.title("📚 아침 공부 명언 추천")

# 기분, 상태 선택
mood = st.selectbox("오늘 기분은 어떤가요?", ["😊 좋음", "😐 그냥저냥", "😟 별로임"])
state = st.selectbox("현재 상태는?", ["💪 에너지 충분", "😴 피곤함", "🤯 스트레스"])

# 명언 모음
quotes = [
    "시작이 반이다. — 아리스토텔레스",
    "오늘의 노력이 내일의 너를 만든다.",
    "꾸준함이 결국 재능을 이긴다.",
    "할 수 있다고 믿는 순간, 반은 이루어진다. — 루스벨트",
    "포기하고 싶을 때가 진짜 시작이다."
]

# 버튼 누르면 추천
if st.button("오늘의 명언 보기"):
    st.success(random.choice(quotes))
