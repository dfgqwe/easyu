import streamlit as st
import pyperclip
import re

# 포맷 데이터 포함
formats = {
    "정전": "[사설정전복구]",
    "입전": "[사설정전복구]",
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
    "장비 대개체": "[장비교체]",
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

    # [현장TM] 선택 시 입력란 추가
    현장TM_내용 = ""
    if "[현장TM]" in selected_locations:
        현장TM_내용 = st.text_input("[현장TM] 내용을 입력하세요:", key="현장TM_내용")
        if "[현장TM]" in 현장TM_내용:
            formatted_TM = 현장TM_내용  # [현장TM]이 포함되어 있으면 그대로 사용
        else:
            formatted_TM = f"[현장TM] {현장TM_내용}"  # 포함되어 있지 않으면 [현장TM] 추가
        selected_locations.remove("[현장TM]")
        formatted_locations = f"{formatted_TM}, " + " / ".join([f"{location}" if location != "기타(간단히 내용입력)" else f"기타({st.text_input('기타 내용 입력', key='기타_내용')})" for location in selected_locations])
    else:
        formatted_locations = " / ".join([f"{location}" if location != "기타(간단히 내용입력)" else f"기타({st.text_input('기타 내용 입력', key='기타_내용')})" for location in selected_locations])
    
    if selected_locations or "[현장TM]" in locals():
        results.append(f"<현장> {formatted_locations} 수정요청")

    출동예방_actions = []
    # [현장TM] 내용에 특정 키워드가 포함되거나 숫자나 한국 전화번호 형태가 있는 경우 <출동예방>에도 추가
    if 현장TM_내용 and (any(keyword in 현장TM_내용 for keyword in ["연락", "전화", "건물주", "확인", "통화"]) or re.search(r"\d", 현장TM_내용) or re.search(r"\d{3}-\d{4}-\d{4}", 현장TM_내용)):
        출동예방_actions.append(formatted_TM)

    # "전기작업 확인(전화)"가 선택된 경우 <출동예방>에도 추가
    if "전기작업 확인(전화)" in selected_actions:
        출동예방_actions.append("전기작업 확인(전화)")
    
    if 출동예방_actions:
        results.insert(3, f"<출동예방>{', '.join(출동예방_actions)}")

    copy_activated = False
    if st.button("출력"):
        output_text = "\n".join(results)
        if copy_activated:
            pyperclip.copy(output_text)
        st.text(output_text)

if __name__ == "__main__":
    main()
