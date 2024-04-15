import json  # JSON 파싱
import random  # Stream response 테스트용
import time  # Stream response 테스트용

import requests  # HTTP 요청 생성을 위한 requests 라이브러리 임포트
import streamlit as st  # Streamlit 라이브러리 임포트하여 웹 앱 생성

# AWS Lambda 함수 URL 엔드포인트 정의
ENDPOINT_LAMBDA_URL = "YOUR LAMBDA FUNCTION URL"

# 웹 앱 제목 설정
st.title("Chatbot powered by Bedrock")

# 세션 상태에 메시지 없으면 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 세션 상태에 저장된 메시지 순회하며 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):  # 채팅 메시지 버블 생성
        st.markdown(message["content"])  # 메시지 내용 마크다운으로 렌더링


def get_streaming_response(prompt):
    s = requests.Session()
    response = s.post(ENDPOINT_LAMBDA_URL, json={"prompt": prompt}, stream=True)
    for chunk in response.iter_lines():
        if chunk:
            text = chunk.decode()  # 바이트코드인 chunk를 decode
            print(text)
            yield text


# Stream response 테스트용
def response_generator():
    response = random.choice(
        [
            "Hello there! How can I assist you today?",
            "Hi, human! Is there anything I can help you with?",
            "Do you need help?",
        ]
    )
    for word in response.split():
        yield word + " "
        time.sleep(0.05)


# 사용자로부터 입력 받음
if prompt := st.chat_input("Message Bedrock..."):
    # 사용자 메시지 세션 상태에 추가
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):  # 사용자 메시지 채팅 메시지 버블 생성
        st.markdown(prompt)  # 사용자 메시지 표시

    with st.chat_message("assistant"):  # 보조 메시지 채팅 메시지 버블 생성
        model_output = st.write_stream(get_streaming_response(prompt))
        # model_output = st.write_stream(response_generator())

    # 보조 응답 세션 상태에 추가
    st.session_state.messages.append({"role": "assistant", "content": model_output})
