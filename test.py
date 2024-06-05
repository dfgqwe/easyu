import streamlit as st
import pyperclip
import base64
import re

# 포맷 데이터 포함
formats = {
    "익일": "[기타]",
    "담당조": "[기타]",
    "OFF": "[기타]",
    "예정": "[기타]",
    "재발행": "[기타]",
    "VOC": "[기타]",
    "미정": "[기타]",
    "폐문": "[폐문]",
    "출입불가": "[폐문]",
    "출입": "[폐문]",
    "한전": "[한전정전복구]",
    "정전": "[사설정전복구]",
    "입전": "[사설정전복구]",
    "복전": "[사설정전복구]",
    "출동 중 복구": "[사설정전복구]",
    "출동중복구": "[사설정전복구]",
    "출동 중 자동복구": "[사설정전복구]",
    "출동중자동복구": "[사설정전복구]",
    "자동": "[사설정전복구]",
    "차단기 on": "[사설차단기복구]",
    "trip": "[사설차단기복구]",
    "TRIP": "[사설차단기복구]",
    "트립": "[사설차단기복구]",
    "어댑터": "[전원어댑터교체]",
    "어뎁터": "[전원어댑터교체]",
    "아뎁터": "[전원어댑터교체]",
    "아댑터": "[전원어댑터교체]",
    "아답터": "[전원어댑터교체]",
    "아답타": "[전원어댑터교체]",
    "멀티탭": "[멀티탭 ON/교체]",
    "콘센트": "[멀티탭 ON/교체]",
    "멀티탭 교체": "[멀티탭 ON/교체]",
    "콘센트 교체": "[멀티탭 ON/교체]",
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
    "감쇄기": "[광커넥터복구]", 
    "감쇠기": "[광커넥터복구]",
    "PON": "[모듈교체]",
    "pon": "[모듈교체]",
    "PSU": "[모듈교체]",
    "psu": "[모듈교체]",
    "모듈": "[모듈교체]",
    "장비교체": "[장비교체]",
    "장비 대개체": "[장비교체]",
    "대개체": "[장비교체]",
    "교체": "[장비교체]",
    "리셋": "[장비리셋]"
    
}

# B/S 및 민원처리 head_format 데이터
B_S_head_formats = {
    "NOC_광레벨불": "[NOC_광레벨불]",
    "NOC_CRC발생": "[NOC_CRC발생]",
    "NOC_장비철거": "[NOC_장비철거]",
    "NOC_형상삭제": "[NOC_형상삭제]",
    "NOC_PSU교체": "[NOC_PSU교체]",
    "NOC_PLK_PSU교체": "[NOC_PLK_PSU교체]",
    "NOC_장비교체": "[NOC_장비교체]",
    "NOC_점검정비": "[NOC_점검정비]",
    "NOC_자산관리": "[NOC_자산관리]",
    "NOC_중복장애": "[NOC_중복장애]",
    "NOC_kernel정비": "[NOC_kernel정비]"
}

민원처리_head_formats = {
    "NOC_장비교체": "[NOC_장비교체]",
    "NOC_PON모듈교체": "[NOC_PON모듈교체]",
    "NOC_보드교체": "[NOC_보드교체]",
    "NOC_BAT교체": "[NOC_BAT교체]",
    "NOC_어댑터교체": "[NOC_어댑터교체]",
    "NOC_FAN교체": "[NOC_FAN교체]",
    "NOC_관련부서이관": "[NOC_관련부서이관]",
    "NOC_장비철거": "[NOC_장비철거]",
    "NOC_광커넥터재접속": "[NOC_광커넥터재접속]",
    "NOC_전원가복구": "[NOC_전원가복구]",
    "NOC_모자분리": "[NOC_모자분리]",
    "NOC_전기요금": "[NOC_전기요금]",
    "NOC_장비재설치": "[NOC_장비재설치]",
    "NOC_PSU교체": "[NOC_PSU교체]",
    "NOC_감쇄기실장": "[NOC_감쇄기실장]",
    "NOC_상태변경": "[NOC_상태변경]",
    "NOC_장비리셋": "[NOC_장비리셋]",
    "NOC_자연회복": "[NOC_자연회복]",
    "NOC_기타": "[NOC_기타]"
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
    

    st.title("MOSS 회복 문구")

    # 초기값 설정
    if "user_input" not in st.session_state:
        st.session_state.user_input = ""

    # 텍스트 입력 초기화 함수
    def clear_text():
        st.session_state.clear()  # 모든 상태를 초기화
        st.session_state.user_input = ""  # 다시 설정
        st.experimental_rerun()  # 상태를 초기화하고 재실행

    results = []

    col1, col2 = st.columns(2)

    # B/S 체크박스 추가
    with col1:
        is_bs_checked = st.checkbox("B/S")

    # 민원처리 체크박스 추가
    with col2:
        is_complaint_checked = st.checkbox("민원처리")

    if is_bs_checked:
        # B/S 체크박스가 선택되었을 때 B/S head_format을 선택할 수 있는 드롭다운 메뉴
        selected_bs_format = st.selectbox("B/S head_format을 선택하세요:", list(B_S_head_formats.values()), key="bs_format")
        if selected_bs_format:
            results.append(selected_bs_format)

    if is_complaint_checked:
        # 민원처리 체크박스가 선택되었을 때 민원처리 head_format을 선택할 수 있는 드롭다운 메뉴
        selected_complaint_format = st.selectbox("민원처리 head_format을 선택하세요:", list(민원처리_head_formats.values()), key="complaint_format")
        if selected_complaint_format:
            results.append(selected_complaint_format)

    # 텍스트 입력 위젯
    user_input = st.text_input("입력란", key="user_input")

    # 입력 형식 검사 및 포맷 추가
    if not is_bs_checked and not is_complaint_checked:
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
        현장TM_출동예방 = st.checkbox("[현장TM] 내용을 <출동예방>에 포함")
        if "[현장TM]" in 현장TM_내용:
            formatted_TM = 현장TM_내용  # [현장TM]이 포함되어 있으면 그대로 사용
        else:
            formatted_TM = f"[현장TM] {현장TM_내용}"  # 포함되어 있지 않으면 [현장TM] 추가
        selected_locations.remove("[현장TM]")
        if selected_locations:
            formatted_locations = f"{formatted_TM}, " + " / ".join([f"{location}" if location != "기타(간단히 내용입력)" else f"기타({st.text_input('기타 내용 입력', key='기타_내용')})" for location in selected_locations]) + " 수정요청"
        else:
            formatted_locations = f"{formatted_TM}"
    else:
        formatted_locations = " / ".join([f"{location}" if location != "기타(간단히 내용입력)" else f"기타({st.text_input('기타 내용 입력', key='기타_내용')})" for location in selected_locations])
    
    if selected_locations or 현장TM_내용:
        results.append(f"<현장> {formatted_locations}")

    출동예방_actions = []
    # [현장TM] 내용에 특정 키워드가 포함되거나 숫자나 한국 전화번호 형태가 있는 경우 <출동예방>에도 추가
    if 현장TM_내용 and 현장TM_출동예방:
        출동예방_actions.append(formatted_TM)

    # "전기작업 확인(전화)"가 선택된 경우 <출동예방>에도 추가
    if "전기작업 확인(전화)" in selected_actions:
        출동예방_actions.append("[NOC]전기작업 확인(전화)")

    
    if 출동예방_actions:
        results.insert(3, f"<출동예방>{', '.join(출동예방_actions)}")

    copy_activated = False
    if st.button("출력"):
        output_text = "\n".join(results)
        if copy_activated:
            pyperclip.copy(output_text)
        st.text(output_text)

    # 입력란 초기화 버튼
    if st.button("입력란 초기화"):
        clear_text()

if __name__ == "__main__":
    main()
