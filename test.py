import streamlit as st
import pandas as pd
import pyperclip
import re
from streamlit_option_menu import option_menu
import os
import requests
from github import Github
import time
import xml.etree.ElementTree as ET
from urllib.request import urlopen
from PIL import Image
from io import BytesIO
import traceback
from datetime import datetime

# 포맷 데이터 포멧
formats = {
    "정전": "[사설정전복구]",
    "입전": "[사설정전복구]",
    "복전": "[사설정전복구]",
    "이동중": "[사설정전복구]",
    "이동 중": "[사설정전복구]",
    "출동 중 복구": "[사설정전복구]",
    "출동중복구": "[사설정전복구]",
    "출동 중 자동복구": "[사설정전복구]",
    "출동중자동복구": "[사설정전복구]",
    "출동중 자동복구": "[사설정전복구]",
    "자동": "[사설정전복구]",
    "루트변경": "[전원가복구]",
    "루트 변경": "[전원가복구]",
    "루트": "[전원가복구]",
    "출동 전": "[사설정전복구]",
    "출동전": "[사설정전복구]",
    "한전": "[한전정전복구]",
    "변압기": "[한전정전복구]",
    "차단기": "[사설차단기복구]",
    "차단기 on": "[사설차단기복구]",
    "차단기 ON": "[사설차단기복구]",
    "차단기on": "[사설차단기복구]",
    "차단기ON": "[사설차단기복구]",
    "On": "[사설차단기복구]",
    "trip": "[사설차단기복구]",
    "TRIP": "[사설차단기복구]",
    "Trip": "[사설차단기복구]",
    "트립": "[사설차단기복구]",
    "어댑터": "[전원어댑터교체]",
    "어뎁터": "[전원어댑터교체]",
    "아뎁터": "[전원어댑터교체]",
    "아댑터": "[전원어댑터교체]",
    "아답터": "[전원어댑터교체]",
    "아답타": "[전원어댑터교체]",
    "멀티탭": "[멀티탭 ON/교체]",
    "멀티탭 교체": "[멀티탭 ON/교체]",
    "콘센트": "[멀티탭 ON/교체]",
    "콘샌트": "[멀티탭 ON/교체]",
    "발전기": "[발전기가동]",
    "파워뱅크": "[전원가복구]",
    "가복구": "[전원가복구]",
    "임시": "[전원가복구]",
    "전기안전검사": "[고객측작업]",
    "전기검사": "[고객측작업]",
    "전기작업": "[고객측작업]",
    "작업": "[고객측작업]",
    "점검": "[고객측작업]",
    "검사": "[고객측작업]",
    "공사": "[고객측작업]",
    "장비회수": "[장비철거]",
    "장비 회수": "[장비철거]",
    "장비철거": "[장비철거]",
    "장비 철거": "[장비철거]",
    "타사전환": "[타사전환]",
    "타사 전환": "[타사전환]",
    "감쇄기": "[광커넥터복구]", 
    "감쇠기": "[광커넥터복구]",
    "광케이블": "[광커넥터복구]",
    "광 케이블": "[광커넥터복구]",
    "dbm": "[광커넥터복구]",
    "취부": "[광커넥터복구]",
    "OJC": "[광커넥터복구]",
    "ojc": "[광커넥터복구]",
    "PON": "[모듈교체]",
    "pon": "[모듈교체]",
    "Pon": "[모듈교체]",
    "PoN": "[모듈교체]",
    "PSU": "[모듈교체]",
    "psu": "[모듈교체]",
    "모듈": "[모듈교체]",
    "보드": "[모듈교체]",
    "PLK": "[모듈교체]",
    "plk": "[모듈교체]",
    "장비교체": "[장비교체]",
    "장비 대개체": "[장비교체]",
    "대개체": "[장비교체]",
    "장비 교체": "[장비교체]",
    "리셋": "[장비리셋]",
    "로딩": "[장비리셋]",
    "익일": "[기타]",
    "담당조": "[기타]",
    "OFF": "[기타]",
    "off": "[기타]",
    "예정": "[기타]",
    "재발행": "[기타]",
    "VOC": "[기타]",
    "voc": "[기타]",
    "미정": "[기타]",
    "불가": "[기타]",
    "망실": "[기타]",
    "예정": "[기타]",
    "접근불가": "[폐문]",
    "접근 불가": "[폐문]",
    "출입불가": "[폐문]",
    "출입": "[폐문]",
    "폐문": "[폐문]"
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
    "NOC_BAT(24)": "[NOC_BAT(24)]",
    "NOC_전원OFF": "[NOC_전원OFF]",
    "NOC_10G(용량확대)": "[NOC_10G(용량확대)]",
    "NOC_통합멀티룸": "[NOC_통합멀티룸]",
    "NOC_kernel정비": "[NOC_kernel정비]",
    "NOC_철거검토": "[NOC_철거검토]",
    "기타": "[기타]"
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
    "정전알림이 등록",
    "DB현행화",
    "DB 삭제 여부",
    "광레벨 확인",
    "원격조치(리부팅)",
    "원격조치(포트리셋)",
    "원격조치(포트BLK)",
    "고객홍보"
]




@st.cache_data
def get_format(text):
    matched_formats = [head_format for keyword, head_format in formats.items() if keyword in text]
    if "[한전정전복구]" in matched_formats and ("[기타]" in matched_formats or "[폐문]" in matched_formats):
        return "[폐문]" if "[폐문]" in matched_formats else "[기타]"
    elif "[한전정전복구]" in matched_formats:
        return "[한전정전복구]"
    elif "[전원어댑터교체]" in matched_formats:
        return "[전원어댑터교체]"
    elif "[사설차단기복구]" in matched_formats:
        return "[사설차단기복구]"
    elif "[기타]" in matched_formats or "[폐문]" in matched_formats:
        return matched_formats[-1]
    else:
        selected_formats = [format for format in matched_formats if format not in ["[기타]", "[폐문]"]]
        return selected_formats[-1] if selected_formats else None


# Load the CSV file
df = pd.read_csv('head.csv', index_col=0)


def clear_tm_content(content):
    keywords_to_remove = ["[현장TM]", "[TM활동]", "[TM 활동]", "[현장 TM]"]
    for keyword in keywords_to_remove:
        content = content.replace(keyword, "")
    return content.strip()


# Initialize session state for day and night content if not already present
if 'day_content' not in st.session_state:
    st.session_state.day_content = ""
if 'night_content' not in st.session_state:
    st.session_state.night_content = ""


# Function to read data from GitHub
@st.cache
def fetch_data_from_github(repo_name, file_path, github_token):
    try:
        g = Github(github_token)
        repo = g.get_repo(repo_name)
        file_content = repo.get_contents(file_path)
        df = pd.read_csv(file_content.download_url)
        return df
    except Exception as e:
        st.error(f"Error fetching data from GitHub: {e}")
        return None

# Function to update data on GitHub
def update_data_on_github(repo_name, file_path, github_token, df_no_duplicates):
    try:
        g = Github(github_token)
        repo = g.get_repo(repo_name)
        
        # Get current file contents and SHA
        file_content = repo.get_contents(file_path)
        current_sha = file_content.sha
        
        # Prepare updated content
        updated_content = df_no_duplicates.to_csv(index=False)
        
        # Update file on GitHub
        repo.update_file(file_path, "Data update", updated_content, current_sha)
        
        st.success("Data successfully updated on GitHub.")
    except Exception as e:
        st.error(f"Error updating data on GitHub: {e}")





def home_page():
    st.title("Home")
    st.markdown(
        """
        <style>
        .stRadio > div {
            display: flex;
            flex-direction: row;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    content_option = st.radio("인수 인계", ["주간", "야간"])
    if content_option == "주간":
        if "day_content" in st.session_state:
            st.write("주간 인수인계 내용")
            st.markdown(st.session_state.day_content.replace('\n', '<br>'), unsafe_allow_html=True)
            st.header("★★재해 : 7월 2일 ~ 7월 22일★★")
        else:
            st.info("아직 주간 인수인계 내용이 입력되지 않았습니다.")

    
    # 야간 인수인계 내용 보여주기
    if content_option == "야간":
        if "night_content" in st.session_state:
            st.write("야간 인수인계 내용")
            st.markdown(st.session_state.night_content.replace('\n', '<br>'), unsafe_allow_html=True)
        else:
            st.info("아직 야간 인수인계 내용이 입력되지 않았습니다.")


     # CSS 스타일 적용
    st.markdown(
        """
        <style>
        .small-select {
            width: 50px; /* 선택 상자의 너비를 조정합니다. */
            padding: 5px; /* 내부 여백을 설정합니다. */
            font-size: 14px; /* 폰트 크기를 설정합니다. */
            border-radius: 5px; /* 테두리의 모서리를 둥글게 만듭니다. */
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    # 지역 선택 selectbox
    region_option = st.selectbox("지역 선택", ["충청", "호남", "부산", "대구"])

    col1, col2 = st.columns(2)

    with col1:
        # Column 1: Department phone numbers
        st.markdown("유관 부서 전화번호")

        common_numbers = {
        "OSP 관제센터": "02-500-6150", 
        "IP망 관제센터": "042-478-1600", 
        "전원관제": "042-478-1800",
        "과천 제1관제센터(교환)": "02-500-6080",
    }

        unique_numbers = {
        "충청": {"name": "교환기술부(충청)", "number": "042-255-2470"},
        "호남": {"name": "교환기술부(호남)", "number": "062-513-1200"},
        "부산": {"name": "교환기술부(부산)", "number": "051-464-4699"},
        "대구": {"name": "교환기술부(대구)", "number": "053-477-3010"},
    }
        enter_numbers = {
        "충청": {"name": "분기국사출입(충청)", "number": "042-478-7550, 7540"},
        "호남": {"name": "분기국사출입(호남)", "number": "062-230-3355~7"},
        "부산": {"name": "분기국사출입(부산)", "number": "051-464-2300"},
        "대구": {"name": "분기국사출입(대구)", "number": "053-477-1984~5"},
    }

        phone_numbers = list(common_numbers.values()) + [unique_numbers[region_option]["number"]] + [enter_numbers[region_option]["number"]]
        phone_names = list(common_numbers.keys()) + [unique_numbers[region_option]["name"]] + [enter_numbers[region_option]["name"]]

        for name, number in zip(phone_names, phone_numbers):
            st.markdown(f"- {name}: {number}")

    with col2:
        # Column 2: Four clickable sections
        st.markdown("URL Navigation")


        st.markdown("[기상레이더센터_낙뢰](https://radar.kma.go.kr/lightning/area_lightning.do)")
        st.markdown("[날씨누리_레이더](https://www.weather.go.kr/w/image/radar.do)")
        st.markdown("[windy.com](https://www.windy.com/?37.475,126.957,5)")
        st.markdown("[KBS 재난포털_CCTV](https://d.kbs.co.kr/special/cctv)")
        st.markdown("[카카오맵](https://map.kakao.com/)")
        st.markdown("[네이버지도](https://map.naver.com/)")







def moss_page():
    st.title("MOSS 회복 문구")

    df1 = pd.read_csv('bs_head.csv')

    # Streamlit 애플리케이션
    with st.expander('MOSS BS 발행 HEAD'):
        st.dataframe(df1)

    # 초기값 설정
    if "user_input" not in st.session_state:
        st.session_state.user_input = ""

    # 텍스트 입력 초기화 함수
    def clear_text():
        for key in st.session_state.keys():
            del st.session_state[key]  # 모든 상태를 초기화
        st.session_state.user_input = ""  # 다시 설정
        st.experimental_rerun()  # 상태를 초기화하고 재실행

    results = []

    if "bs_checked" not in st.session_state:
        st.session_state.bs_checked = False
    if "complaint_checked" not in st.session_state:
        st.session_state.complaint_checked = False
    if "power_outage_checked" not in st.session_state:
        st.session_state.power_outage_checked = False

    def bs_checkbox_callback():
        st.session_state.complaint_checked = False
        st.session_state.power_outage_checked = False

    def complaint_checkbox_callback():
        st.session_state.bs_checked = False
        st.session_state.power_outage_checked = False

    def power_checkbox_callback():
        st.session_state.bs_checked = False
        st.session_state.complaint_checked = False

    col1, col2, col3 = st.columns(3)

    with col1:
        is_bs_checked = st.checkbox("B/S", key="bs_checked", on_change=bs_checkbox_callback)
    with col2:
        is_complaint_checked = st.checkbox("민원처리", key="complaint_checked", on_change=complaint_checkbox_callback)
    with col3:
        is_power_outage_checked = st.checkbox("다량 장애", key="power_outage_checked", on_change=power_checkbox_callback)

    if is_power_outage_checked:
        st.write("선택할 항목:")

        col4, col5, col6 = st.columns(3)
        
        if "line_fault_checked" not in st.session_state:
            st.session_state.line_fault_checked = False
        if "l2_outage_checked" not in st.session_state:
            st.session_state.l2_outage_checked = False
        if "apartment_power_outage_checked" not in st.session_state:
            st.session_state.apartment_power_outage_checked = False
            
        def l2_checkbox_callback():
            st.session_state.line_fault_checked = False
            st.session_state.apartment_power_outage_checked = False
        def liner_checkbox_callback():
            st.session_state.l2_outage_checked = False
            st.session_state.apartment_power_outage_checked = False
        def apartment_checkbox_callback():
            st.session_state.l2_outage_checked = False
            st.session_state.line_fault_checked = False
        

        with col4:
            is_l2_outage_checked = st.checkbox("L2 정전", key="l2_outage_checked", on_change=l2_checkbox_callback)
        with col5:
            is_line_fault_checked = st.checkbox("L2 선로 장애", key="line_fault_checked", on_change=liner_checkbox_callback)
        with col6:
            is_apartment_power_outage_checked = st.checkbox("아파트 정전", key="apartment_power_outage_checked", on_change=apartment_checkbox_callback)

        def load_station_data():
            df = pd.read_csv('국사.CSV')
            return df


        def get_nsc(station_name, df):
            # 수용국사에서 '국사'를 제외한 이름을 비교
            station_name_core = station_name.replace("국사", "")
            row = df[df['수용국사'].str.contains(station_name_core)]
            if not row.empty:
                return row.iloc[0]['NSC']
                # NSC 값을 변환
                if "충북액세스운용센터" in nsc:
                    nsc = "충청"
                elif "충남액세스운용센터" in nsc:
                    nsc = "충청"

                if "전남액세스운용센터" in nsc:
                    nsc = "호남"
                elif "전북액세스운용센터" in nsc:
                    nsc = "호남"
                    
                if "부산액세스운용센터" in nsc:
                    nsc = "부산"
                elif "경남액세스운용센터" in nsc:
                    nsc = "부산"

                if "대구액세스운용센터" in nsc:
                    nsc = "부산"
                elif "경북액세스운용센터" in nsc:
                    nsc = "부산"       
            return None
          
        station_data = load_station_data()
        if is_l2_outage_checked:
            st.write("L2 정전 정보 입력:")
            daegu_station = st.text_input("국사 (예: 대구/xx국사)", key="daegu_station")
            district = st.text_input("동 (예: yy동)", key="district")
            l2_systems = st.text_input("L2 수 (예: 13)", key="l2_systems")
            customers = st.text_input("고객 수 (예: 120)", key="customers")

            if daegu_station and district and l2_systems and customers:
                if not daegu_station.endswith("국사"):
                    daegu_station += "국사"
                if not district.endswith("동"):
                    district += "동"
                nsc = get_nsc(daegu_station, station_data)
                if nsc:
                    st.write(f"[L2_정전] {nsc}/{daegu_station} L2 다량장애 {district}일대 한전정전 (추정) L2*{l2_systems}sys({customers}고객)")
                else:
                    st.write("해당 국사에 대한 NSC 정보를 찾을 수 없습니다.")

        if is_line_fault_checked:
            st.write("L2 선로 장애 정보 입력:")
            honam_station = st.text_input("국사 (예: 호남/xx국사)", key="honam_station")
            l2_systems_line = st.text_input("L2 수 (예: 13)", key="l2_systems_line")
            customers_line = st.text_input("고객 수 (예: 120)", key="customers_line")
        
            if honam_station and l2_systems_line and customers_line:
                if not honam_station.endswith("국사"):
                    honam_station += "국사"
                nsc = get_nsc(honam_station, station_data)
                if nsc:
                    st.write(f"[L2_선로] {nsc}/{honam_station} 선로장애 (추정) L2*{l2_systems_line}sys({customers_line}고객)")
                else:
                    st.write("해당 국사에 대한 NSC 정보를 찾을 수 없습니다.")

        if is_apartment_power_outage_checked:
            st.write("아파트 공용 정전 정보 입력:")
            busan_station = st.text_input("국사 (예: 부산/xx국사)", key="busan_station")
            apartment_name = st.text_input("아파트 이름 (예: AAA아파트)", key="apartment_name")
            l2_systems_apartment = st.text_input("L2 수 (예: 13)", key="l2_systems_apartment")
            customers_apartment = st.text_input("고객 수 (예: 120)", key="customers_apartment")
            outage_type = st.radio(
                "정전 종류 선택:",
                ("공용전기(추정)", "전체정전(추정)"),
                key="outage_type"
            )
            st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
    
            if busan_station and apartment_name and l2_systems_apartment and customers_apartment:
                if not busan_station.endswith("국사"):
                    busan_station += "국사"
                if not apartment_name.endswith("아파트"):
                    apartment_name += "아파트"
                nsc = get_nsc(busan_station, station_data)
                if nsc:
                    st.write(f"[아파트_정전] {nsc}/{busan_station} {apartment_name} {outage_type} L2*{l2_systems_apartment}sys({customers_apartment}고객)")
                else:
                    st.write("해당 국사에 대한 NSC 정보를 찾을 수 없습니다.")

    else:
        selected_bs_format = None

        if is_bs_checked:
            selected_bs_format = st.selectbox("B/S head_format을 선택하세요:", list(B_S_head_formats.values()), key="bs_format")
            if selected_bs_format:
                results.append(selected_bs_format)

                # Check if selected format is "[NOC_광레벨불]"
                if selected_bs_format == "[NOC_광레벨불]":
                    st.markdown(
                        """
                        <style>
                        .stRadio > div {
                            display: flex;
                            flex-direction: row;
                        }
                        </style>
                        """,
                        unsafe_allow_html=True
                    )
                    selected_option = st.radio(
                        "출동 결과:",
                        ("CM팀 이관", "개선", "정비 안됨"),
                        key="noc_options"
                    )
                    if selected_option:
                        results.append(selected_option)

                    rssi_value = st.text_input("RSSI 값을 입력하세요:")
                    ddm_value = st.text_input("ddm 값을 입력하세요:")
                

                    if rssi_value:
                        results.append(f"RSSI: {rssi_value}")
                    if ddm_value:
                        results.append(f"ddm: {ddm_value}")
                    
                

                if selected_bs_format == "[NOC_장비철거]":
                    st.markdown(
                        """
                        <style>
                        .stRadio > div {
                            display: flex;
                            flex-direction: row;
                        }
                        </style>
                        """,
                        unsafe_allow_html=True
                    )
                    selected_option = st.radio(
                        "DB 삭제 여부:",
                        ("고객DB 존재/NeOSS 삭제 불가", "NeOSS 삭제 완료"),
                        key="noc_options"
                    )
                    if selected_option:
                        results.append(selected_option)

    

        if is_complaint_checked:
            selected_complaint_format = st.selectbox("민원처리 head_format을 선택하세요:", list(B_S_head_formats.values()), key="complaint_format")
            if selected_complaint_format:
                results.append(selected_complaint_format)

        user_input = st.text_input("입력란", key="user_input")

        if not is_bs_checked and not is_complaint_checked:
            head_format = get_format(user_input)
            if head_format:
                results.append(head_format)

        results.append(user_input)
        results.append("수고하셨습니다")

        출동예방_actions = []
        기타_results = []

        # Show these sections only if selected_bs_format is not "[NOC_광레벨불]"
        if selected_bs_format != "[NOC_광레벨불]" and selected_bs_format != "[NOC_장비철거]":
            selected_actions = st.multiselect("선조치_NOC에 대한 내용을 선택하세요:", 선조치_NOC_options, key="selected_actions")

            if "DB 삭제 여부" in selected_actions:
                if "기타_고객DB_neoss_불가" not in st.session_state:
                    st.session_state.기타_고객DB_neoss_불가 = False
                if "기타_neoss_완료" not in st.session_state:
                    st.session_state.기타_neoss_완료 = False

                def 기타_고객DB_neoss_불가_callback():
                    st.session_state.기타_neoss_완료 = False

                def 기타_neoss_완료_callback():
                    st.session_state.기타_고객DB_neoss_불가 = False

                기타_고객DB_neoss_불가 = st.checkbox("고객DB 존재 NeOSS 삭제 불가", key="기타_고객DB_neoss_불가", on_change=기타_고객DB_neoss_불가_callback)
                기타_neoss_완료 = st.checkbox("NeOSS 삭제 완료", key="기타_neoss_완료", on_change=기타_neoss_완료_callback)

                if 기타_고객DB_neoss_불가:
                    기타_results.append("고객DB 존재/NeOSS 삭제 불가")
                if 기타_neoss_완료:
                    기타_results.append("NeOSS 삭제 완료")

            if "광레벨 확인" in selected_actions:
                col1, col2 = st.columns(2)
                with col1:
                    rssi_value = st.text_input("RSSI 값을 입력하세요:")
       
                with col2:
                    ddm_value = st.text_input("ddm 값을 입력하세요:")
            
            
                if rssi_value:
                    기타_results.append(f"RSSI: {rssi_value}")
                if ddm_value:
                    기타_results.append(f"ddm: {ddm_value}")

            results.extend(기타_results)
        

            filtered_actions = [action for action in selected_actions if action !="DB 삭제 여부"]
            filtered_actions = [action for action in selected_actions if action !="광레벨 확인"]
            if filtered_actions:
                formatted_actions = ", ".join(filtered_actions)
                results.append(f"<선조치_NOC> {formatted_actions}")
                if "전기작업 확인(전화)" in selected_actions:
                    출동예방_actions.append("[NOC]전기작업 확인(전화)")
                if "출동보류" in selected_actions:
                    출동예방_actions.append("[NOC]출동보류")

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

            현장TM_내용 = ""
            if "[현장TM]" in selected_locations:
                현장TM_내용 = st.text_input("[현장TM] 내용을 입력하세요:", key="현장TM_내용")
                현장TM_출동예방 = st.checkbox("[현장TM] 내용을 <출동예방>에 포함")
                cleaned_TM_내용 = clear_tm_content(현장TM_내용)
                formatted_TM = f"[현장TM] {cleaned_TM_내용}" if cleaned_TM_내용 else "[현장TM]"

                if len(selected_locations) > 1:  # selected_locations에 [현장TM] 이외의 항목이 포함된 경우에만 수정요청 추가
                    formatted_locations = f"{formatted_TM}, " + " / ".join([f"{location}" if location != "기타(간단히 내용입력)" else f"기타({st.text_input('기타 내용 입력', key='기타_내용')})" for location in selected_locations if location != "[현장TM]"]) + " 수정요청"
                else:
                    formatted_locations = f"{formatted_TM}"
            else:
                formatted_locations = " / ".join([f"{location}" if location != "기타(간단히 내용입력)" else f"기타({st.text_input('기타 내용 입력', key='기타_내용')})" for location in selected_locations])
                if selected_locations:
                    formatted_locations += " 수정요청"

            if selected_locations or 현장TM_내용:
                results.append(f"<현장> {formatted_locations}")

            if 현장TM_내용 and 현장TM_출동예방:
                출동예방_actions.append(formatted_TM)

            if 출동예방_actions:
                results.insert(3, f"<출동예방>{', '.join(출동예방_actions)}")

        col1, col2 = st.columns(2)
        now = datetime.now()
        current_date = now.strftime("%Y-%m-%d")
        with col1:
           namecard_count = st.number_input("명함형 갯수:", min_value=0, step=1, key="namecard_count")
       
        with col2:
            sticker_count = st.number_input("차단기형 갯수:", min_value=0, step=1, key="sticker_count")

        if namecard_count > 0 or sticker_count > 0:
            results.append(f"[{current_date}][스티커]명함형 {namecard_count}개, 차단기형 {sticker_count}개")




    

        copy_activated = False

        col1, col2 , col3= st.columns([2.8, 0.5, 0.7])

        with col1:
            if st.button("출력"):
                output_text = "\n".join(results)  # Join results with new lines for the desired format
                st.text(output_text)  # Print output_text when the "출력" button is pressed
                if copy_activated:
                    pyperclip.copy(output_text)

        with col2:
            if st.button("입력란 초기화"):
                clear_text()

        with col3:
            if 'button_clicked' not in st.session_state:
                st.session_state['button_clicked'] = False

            if st.button('MOSS 회복 항목 표준'):
                st.session_state['button_clicked'] = not st.session_state['button_clicked']

            if st.session_state['button_clicked']:
                placeholder = st.empty()
                with placeholder.container():
                    st.markdown(
                        """
                        <style>
                        /* 데이터프레임이 최대한 화면에 가깝게 보이도록 스타일 조정 */
                        .css-1l02zno {
                            width: 100%;
                            max-width: 100%;
                            height: calc(100vh - 200px); /* 높이를 화면 높이의 일부분으로 설정 */
                            overflow: auto; /* 스크롤이 필요한 경우 스크롤 허용 */
                        }
                        </style>
                        """,
                        unsafe_allow_html=True
                    )
                    st.dataframe(df)







                
# Worksync 페이지
def worksync_page():  
    st.title("Worksync")

    # 데이터 파일 불러오기
    work = pd.read_csv("ws_data.csv")

    # '장비ID'와 '업무명'이 동일한 경우 중복된 행 제거
    df_no_duplicates = work.drop_duplicates(subset=['장비ID', '업무명'])

    # 장비ID 순서대로 정렬
    df_no_duplicates = df_no_duplicates.sort_values(by='장비ID')

    # IP 입력 받기
    ip_input = st.text_input("IP 입력", "").replace(" ", "")
    
    # IP 입력이 있을 경우
    if ip_input:
        # 입력된 IP에 해당되는 행 찾기
        if ip_input in df_no_duplicates['장비ID'].values:
            # 해당 IP의 사업장 찾기
            address = df_no_duplicates[df_no_duplicates['장비ID'] == ip_input]['사업장'].values[0]
            st.write("★동일국소 점검 대상★")
            
            same_address_work = df_no_duplicates[df_no_duplicates['사업장'] == address]
            for idx, (index, row) in enumerate(same_address_work.iterrows(), start=1):
                st.text(f"{idx}.{row['장비명/국사명']} - {row['업무명']}({row['장비ID']})")
        else:
            st.text("Work-Sync(BS업무) 점검 대상 없습니다.")


manage_password = "1234"
def manage_page():
    st.title("Manage")

    # Set session_state variables
    if 'manage_logged_in' not in st.session_state:
        st.session_state.manage_logged_in = False
    if 'last_activity_time' not in st.session_state:
        st.session_state.last_activity_time = time.time()

    # Check if timeout (5 minutes) has passed since the last activity
    if time.time() - st.session_state.last_activity_time > 300:
        st.session_state.manage_logged_in = False

    if not st.session_state.manage_logged_in:
         password = st.text_input("Manage 페이지 비밀번호 입력", type="password")

         if password == manage_password:
             st.session_state.manage_logged_in = True
         elif password:
             st.error("잘못된 비밀번호입니다. 다시 입력해주세요.")
             return
    
    if st.session_state.manage_logged_in:
        st.markdown(
        """
        <style>
        .stRadio > div {
            display: flex;
            flex-direction: row;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

         # 비밀번호 입력 후에만 Radio 버튼을 표시
        content_option = st.radio("인수 인계", ["주간", "야간"])

        if content_option == "주간":
            st.header("주간")
            st.session_state.day_content = st.text_area("주간->야간 인수인계", st.session_state.get("day_content", ""), height=200)
            st.write("재난 상황 : 7월 2일 ~ 7월 8일 ")
        else:
            st.header("야간")
            st.session_state.night_content = st.text_area("야간->주간 인수인계", st.session_state.get("night_content", ""), height=200)

    if st.session_state.manage_logged_in:
         # IP 입력 받기
         ip_input1 = st.text_input("IP 입력", "")
         if ip_input1:
            # Ensure you have set your GitHub token in Streamlit secrets
            try:
                github_token = st.secrets["GITHUB_TOKEN"]
            except KeyError:
                st.error("GitHub token is not set. Please set it in Streamlit secrets.")
                return
        
            repo_name = "dfgqwe/easyu"
            file_path = "ws_data.csv"
        
            df_no_duplicates1 = fetch_data_from_github(repo_name, file_path, github_token)
            if df_no_duplicates1 is None:
                st.error("Failed to fetch data from GitHub.")
                return

            df_no_duplicates1 = df_no_duplicates1.drop_duplicates(subset=['장비ID', '업무명'])
        
            if ip_input1 in df_no_duplicates1['장비ID'].values:
                address = df_no_duplicates1[df_no_duplicates1['장비ID'] == ip_input1]['사업장'].values[0]
                st.write("★동일국소 점검 대상★")
            
                same_address_work = df_no_duplicates1[df_no_duplicates1['사업장'] == address]
                for idx, (index, row) in enumerate(same_address_work.iterrows(), start=1):
                    st.text(f"{idx}. {row['장비명/국사명']} - {row['장비ID']} ({row['업무명']})")

                selected_tasks = st.multiselect(
                "삭제할 업무를 선택하세요:",
                same_address_work.index,
                format_func=lambda x: f"{same_address_work.loc[x, '장비명/국사명']} - {same_address_work.loc[x, '장비ID']} ({same_address_work.loc[x, '업무명']})"
            )

                if st.button("선택된 업무 삭제"):
                    if selected_tasks:
                        st.write(f"Before deletion: {df_no_duplicates1.shape[0]} rows")
                        df_no_duplicates1 = df_no_duplicates1.drop(selected_tasks)
                        st.write(f"After deletion: {df_no_duplicates1.shape[0]} rows")
                        update_data_on_github(repo_name, file_path, github_token, df_no_duplicates1)
                        st.success("선택된 업무가 성공적으로 삭제되었습니다.")
                    else:
                        st.warning("삭제할 업무를 선택하세요.")





  
# 옵션 메뉴 생성
selected = option_menu(
    menu_title=None,  # 메뉴 제목 (원하지 않으면 None)
    options=["Home","MOSS", "Worksync","Manage"],  # 옵션 이름들
    icons=["house", "box-arrow-down","calendar2-check","gear"],  # 각 옵션에 해당하는 아이콘
    menu_icon="cast",  # 메뉴 아이콘
    default_index=0,  # 기본 선택 옵션
    orientation="horizontal"  # 메뉴 방향 (수평)
)

# 탭 내용 생성
if selected == "Home":
    home_page()
elif selected == "MOSS":
    moss_page()
elif selected == "Worksync":
    worksync_page()
elif selected == "Manage":
    manage_page()
