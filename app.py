import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go

# 1. 환경 설정 
API_KEY = st.secrets["GEMINI_API_KEY"] 
genai.configure(api_key=API_KEY)

st.set_page_config(page_title="고성과 조직 진단 AI", layout="wide")

# 2. 진단 문항 구조화 (전문가님의 CATEGORIES 데이터를 파이썬 형식으로 변환)
questions_data = {
    "심리적 안전감": [
        "팀원이 실수나 실패를 했을 때 비난받지 않고 ‘학습의 기회’로 받아들이는 분위기인가?",
        "구성원들이 불이익에 대한 두려움 없이 반대 의견이나 새로운 아이디어를 자유롭게 제안할 수 있는가?",
        "갈등을 회피하지 않고 투명하게 공개하며 ‘문제 해결’을 위한 과정으로 다루는가?",
        "상하 관계를 떠나 서로에게 솔직하고 건설적인 피드백을 주고받는 문화가 형성되어 있는가?",
        "직급이나 연차와 관계없이 누구나 자유롭게 의견을 낼 수 있는 소통 채널이 활성화되어 있는가?"
    ],
    "업무 방식": [
        "시장 변화에 빠르게 대응할 수 있는 애자일 조직 구조를 갖추고 있는가?",
        "과거의 성공 방식에 안주하지 않고 끊임없이 새로운 시도와 혁신을 추구하는가?",
        "불필요한 통제와 규정을 줄이고 구성원의 자율성과 판단을 신뢰하는가?",
        "짧은 주기(2~4주)로 결과를 도출하고 피드백을 반영하는 프로세스가 있는가?",
        "모든 업무와 의사결정이 고객의 니즈에서 시작하여 거꾸로 기획하는 방식을 따르는가?"
    ],
    "리더십": [
        "리더십 원칙이 실제 의사결정의 기준으로 활용되고 있는가?",
        "탁월한 소수의 고성과자를 유지하려는 노력(채용 기준, 보상)을 하고 있는가?",
        "인재 선발 기준에 대한 눈높이가 일치하며 장기적 잠재력을 보고 채용하는가?",
        "리더가 지시보다 맥락을 공유하고 장애물을 제거해 주는 코치 역할을 하는가?",
        "각 구성원의 역할과 책임(R&R)이 명확히 공유되고 유연하게 조정되는가?"
    ],
    "시스템": [
        "프로젝트 종료 후 ‘배운 점’과 ‘개선할 점’을 논의하는 회고가 정기적인가?",
        "팀 전체의 협력과 성과를 인정하고 보상하는 체계를 갖추고 있는가?",
        "실패하더라도 도전적인 시도였다면 인정하고 포상하는 제도가 있는가?",
        "전사적 목표와 팀의 목표가 투명하게 연결되어 방향성을 이해하고 있는가?",
        "정기적인 설문을 통해 직원의 만족도를 측정하고 선제적으로 개선하는가?"
    ]
}

st.title("🛡️ 고성과 조직 진단 AI 컨설턴트")
st.write("모든 문항에 대해 1점(전혀 그렇지 않다)부터 7점(매우 그렇다)까지 응답해 주세요.")

# 설문 섹션
responses = {}
for category, qs in questions_data.items():
    st.divider()
    st.subheader(f"📍 {category}")
    cat_scores = []
    for q in qs:
        score = st.select_slider(q, options=range(1, 8), value=4)
        cat_scores.append(score)
    responses[category] = sum(cat_scores) / len(cat_scores)

# 3. 다이아몬드(방사형) 그래프 그리기
st.divider()
st.subheader("📊 조직 진단 결과 (다이아몬드 그래프)")

categories = list(responses.keys())
values = list(responses.values())
# 그래프 폐쇄를 위해 첫 번째 항목을 마지막에 추가
plot_values = values + [values[0]]
plot_categories = categories + [categories[0]] 

fig = go.Figure(data=go.Scatterpolar(
    r=plot_values,
    theta=plot_categories,
    fill='toself',
    line_color='#1f77b4',
    marker=dict(size=8)
))

fig.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 7])),
    showlegend=False
)
st.plotly_chart(fig, use_container_width=True)

# 4. Gemini AI 진단 요청 (전문가님의 설정 반영)
if st.button("AI 전문가 심층 분석 리포트 생성"):
    with st.spinner("전문가 AI가 데이터를 정밀 분석 중입니다..."):
        model = genai.GenerativeModel('gemini-1.5-flash') 
        system_instruction="""너는 조직개발 전문가야. 7점 척도 데이터를 분석해서 강점과 약점을 짚어주고 넷플릭스/아마존 사례로 해결책을 제시해줘."""
        
        data_summary = f"진단 점수: {responses}"
        response = model.generate_content(data_summary)
        
        st.success("진단 리포트가 완성되었습니다!")
        st.markdown(response.text)


