import streamlit as st
import subprocess
import re

# 포맷 데이터 포함
formats = {
    "정전": "[사설정전복구]",
    "복전": "[사설정전복구]",
    "출동 중 복구": "[사설정전복구]",
    "출동중복구": "[사설정전복구]",
    "한전": "[한전정전복구]",
    "차단기 on": "[사설차단기복구]",
    "trip": "[사설차단기복구]",
    "TRIP": "[사설차단기복구]",
    "어댑터": "[전원어댑터교체]",
    "어뎁터": "[전원어댑터교체]",
    "아뎁터": "[전원어댑터교체]",
    "아댑터": "[전원어댑터교체]",
    "아답터": "[전원어댑터교체]",
    "아답타": "[전원어댑터교체]",
    "멀티탭": "[멀티탭 ON/교체]",
    "발전기": "[발전기가동]",
    "파워뱅크": "[전원가복구]",
    "가복구": "[전원가복구]",
    "임시": "[전원가복구]",
    "전기안전검사": "[고객측작업]",
    "전기검사": "[고객측작업]",
    "작업": "[고객측작업]",
    "점검": "[고객측작업]",
    "검사": "[고객측작업]",
    "공사": "[고객측작업]",
    "장비철거": "[장비철거]",
    "타사전환": "[타사전환]",
    "PON": "[모듈교체]",
    "pon": "[모듈교체]",
    "PSU": "[모듈교체]",
    "psu": "[모듈교체]",
    "모듈": "[모듈교체]",
    "장비교체": "[장비교체]",
    "교체": "[장비교체]",
    "리셋": "[장비리셋]",
    "폐문": "[폐문]",
    "출입불가": "[폐문]",
    "출입": "[폐문]",
    "명일": "[기타]",
    "담당조": "[기타]",
    "OFF": "[기타]",
    "VOC": "[기타]",
}

# 선조치_NOC에 대한 내용
선조치_NOC_options = [
    "원인분석(전원)",
    "원인분석(선로)",
    "원인분석(장비)",
    "전기작업 확인(전화)",
    "FOLLOW추가",
    "출동보류",
    "원격조치(리부팅)",
    "원격조치(포트리셋)",
    "원격조치(포트BLK)",
    "정전알림이 등록",
    "DB현행화",
    "고객홍보"
]

def get_format(text):
    for keyword, head_format in formats.items():
        if keyword in text:
            return head_format
    return None

def main():
    st.title("회복 문구")

    results = []

    # 텍스트 입력 위젯
    user_input = st.text_input("입력란", key="user_input")

    # 입력 형식 검사 및 포맷 추가
    head_format = get_format(user_input)
    if head_format:
        results.append(head_format)

    results.append(user_input)
    results.append("수고하셨습니다")

    # 선조치_NOC 다중 선택 박스
    selected_actions = st.multiselect("선조치_NOC에 대한 내용을 선택하세요:", 선조치_NOC_options, key="selected_actions")
    if selected_actions:
        formatted_actions = ", ".join(selected_actions)
        results.append(f"<선조치_NOC> {formatted_actions}")

    # 현장 항목들 다중 선택 박스
    현장_options = [
        "[현장TM]",
        "주소",
        "연락처",
        "장비위치",
        "차단기위치",
        "출입방법",
        "기타(간단히 내용입력)"
    ]
    selected_locations = st.multiselect("현장에 대한 내용을 선택하세요:", 현장_options, key="selected_locations")
     # "전기작업 확인(전화)"가 선택된 경우 <출동예방>에도 추가
    if "전기작업 확인(전화)" in selected_actions:
        results.append("전기작업 확인(전화)")
    
    if "포장" in user_input:
        results.append("[포장요청]")

    copy_activated = st.checkbox("복사 기능 활성화", key="copy_activated")
    if st.button("출력"):
        output_text = "\n".join(results)
        if copy_activated:
            # 클립보드에 복사
            try:
                subprocess.run(['xclip', '-selection', 'clipboard'], input=output_text.encode('utf-8'), check=True)
            except subprocess.CalledProcessError as e:
                st.error(f"클립보드 복사 오류: {e}")
            else:
                st.success("클립보드에 복사되었습니다.")
        st.text(output_text)

if __name__ == "__main__":
    main()