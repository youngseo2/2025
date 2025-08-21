import streamlit as st
import datetime

st.title("📚 공부 도우미")

# -------------------------
# 오늘 날짜
# -------------------------
today = str(datetime.date.today())

if "diary" not in st.session_state:
    st.session_state.diary = {}

if "tasks" not in st.session_state:
    st.session_state.tasks = {}

if today not in st.session_state.tasks:
    st.session_state.tasks[today] = []

# -------------------------
# 명언 추천
# -------------------------
moods = ["😊 좋음", "😐 그냥저냥", "😟 별로임"]
states = ["💪 에너지 충분", "😴 피곤함", "🤯 스트레스"]

mood = st.selectbox("오늘 기분은?", moods)
state = st.selectbox("현재 상태는?", states)

quotes = {
    ("😊 좋음", "💪 에너지 충분"): "오늘의 열정이 내일의 성공을 만든다.",
    ("😊 좋음", "😴 피곤함"): "쉬어가도 괜찮아, 꾸준함이 중요하다.",
    ("😊 좋음", "🤯 스트레스"): "웃음은 최고의 스트레스 해소제다.",
    ("😐 그냥저냥", "💪 에너지 충분"): "작은 성취가 큰 변화를 만든다.",
    ("😐 그냥저냥", "😴 피곤함"): "조금씩이라도 해내는 게 중요하다.",
    ("😐 그냥저냥", "🤯 스트레스"): "마음의 여유가 힘이 된다.",
    ("😟 별로임", "💪 에너지 충분"): "힘든 날도 결국 지나간다.",
    ("😟 별로임", "😴 피곤함"): "오늘은 쉬어도 괜찮다.",
    ("😟 별로임", "🤯 스트레스"): "포기하지 않는 것이 가장 큰 용기다."
}

if st.button("✨ 오늘의 명언 보기"):
    st.success(quotes.get((mood, state), "꾸준함이 결국 재능을 이긴다."))

# -------------------------
# 할 일 체크리스트
# -------------------------
st.header("📝 오늘의 할 일")

new_task = st.text_input("할 일을 입력하세요:")

if st.button("추가하기"):
    if new_task.strip():
        st.session_state.tasks[today].append({"task": new_task, "done": False})

for i, t in enumerate(st.session_state.tasks[today]):
    checked = st.checkbox(t["task"], value=t["done"], key=f"{today}_task_{i}")
    st.session_state.tasks[today][i]["done"] = checked

if st.button("✅ 완료한 항목 지우기"):
    st.session_state.tasks[today] = [t for t in st.session_state.tasks[today] if not t["done"]]

# -------------------------
# 오늘의 일기 / 메모
# -------------------------
st.header("📖 오늘의 메모")

diary_text = st.text_area("오늘 하루를 기록하세요:", st.session_state.diary.get(today, ""))

# 🟢 키워드 → 이모지 매핑
emoji_map = {
    # 음식
    "밥": "🍚", "라면": "🍜", "김치": "🥬", "고기": "🍖", "치킨": "🍗",
    "피자": "🍕", "햄버거": "🍔", "떡볶이": "🍢", "과일": "🍎", "케이크": "🍰",
    "커피": "☕", "음료": "🥤",

    # 활동/하루 일과
    "공부": "📖", "시험": "✏️", "학교": "🏫", "운동": "🏃", "축구": "⚽",
    "게임": "🎮", "영화": "🎬", "산책": "🚶", "여행": "✈️", "쇼핑": "🛍️",

    # 감정/상태
    "행복": "😄", "기분": "🙂", "슬픔": "😢", "피곤": "🥱", "스트레스": "😵",
    "재밌": "😂", "화남": "😡", "놀람": "😲"
}

def add_emojis(text: str) -> str:
    result = text
    for word, emoji in emoji_map.items():
        if word in result:
            result = result.replace(word, f"{word}{emoji}")
    return result

if st.button("💾 메모 저장"):
    st.session_state.diary[today] = diary_text
    st.success("오늘의 메모가 저장되었습니다 ✅")

# 저장된 메모 출력 (이모티콘 변환)
if today in st.session_state.diary:
    st.subheader("📌 오늘 기록 보기")
    st.write(add_emojis(st.session_state.diary[today]))
