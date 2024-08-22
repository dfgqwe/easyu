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
import pytz

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
    "전원투입": "[사설정전복구]",
    "전원 투입": "[사설정전복구]",
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
    "전원선": "[전원가복구]",
    "전원 절체": "[전원가복구]",
    "전원절체": "[전원가복구]",
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
    "커넥터": "[광커넥터복구]",
    "커낵터": "[광커넥터복구]",
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
    "장비불량": "[장비교체]",
    "장비 불량": "[장비교체]",
    "장비교체": "[장비교체]",
    "장비 대개체": "[장비교체]",
    "대개체": "[장비교체]",
    "장비 교체": "[장비교체]",
    "l2교체": "[장비교체]",
    "l2 교체": "[장비교체]",
    "L2교체": "[장비교체]",
    "L2 교체": "[장비교체]",
    "리셋": "[장비리셋]",
    "로딩": "[장비리셋]",
    "재설정": "[장비리셋]",
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
    "NOC_민원처리": "[NOC_민원처리]",
    "NOC_어댑터교체": "[NOC_어댑터교체]",
    "기타": "[기타]"
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
    "어댑터 전/후 작성",
    "CRC",
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
        return selected_formats[-1] if selected_formats else "[기타]"


# Load the CSV file
df = pd.read_csv('head.csv', index_col=0)


def clear_tm_content(content):
    keywords_to_remove = ["[현장TM]", "[TM활동]", "[TM 활동]", "[현장 TM]", "[TM]"]
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



def render_sidebar():
        # 사이드바 스타일을 정의합니다.
    st.markdown(
        """
        <style>
        /* 사이드바 너비를 설정합니다. */
        .css-1d391kg {
            width: 300px;
        }
        /* 사이드바 내의 헤더와 콘텐츠 스타일을 정의합니다. */
        .css-1h1w2f8 {
            font-size: 14px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    st.sidebar.header("유관 부서 전화번호")
    # 지역 선택 selectbox
    region_option = st.sidebar.selectbox("지역 선택", ["충청", "호남", "부산", "대구"])
    
    st.sidebar.markdown("유관 부서 전화번호")

    common_numbers = {
            "OSP 관제센터": "02-500-6150",
            "IP망 관제센터": "042-478-1600",
            "전원관제": "042-478-1800",
            "과천 제1관제센터(교환)": "02-500-6080",
            "무선" : "042-489-6831",
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
        st.sidebar.markdown(f"- {name}: {number}")

    st.sidebar.header("URL Navigation")
    st.sidebar.markdown("[기상레이더센터_낙뢰](https://radar.kma.go.kr/lightning/area_lightning.do)")
    st.sidebar.markdown("[날씨누리_레이더](https://www.weather.go.kr/w/image/radar.do)")
    st.sidebar.markdown("[windy.com](https://www.windy.com/?37.475,126.957,5)")
    st.sidebar.markdown("[KBS 재난포털_CCTV](https://d.kbs.co.kr/special/cctv)")
    st.sidebar.markdown("[카카오맵](https://map.kakao.com/)")
    st.sidebar.markdown("[네이버지도](https://map.naver.com/)")
   




def home_page():
    st.markdown(
        """
        <style>
        body {
            background-color: #87CEEB; /* 하늘색 */
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.title("공지사항")
    st.header("-전원분야 고장성 경보 범위-")
    st.markdown("<span style='color:red; font-weight:bold;'>[한전정전]</span> 한전정전으로 발전기 가동 또는 축전기 방전 중", unsafe_allow_html=True)
    st.markdown("<span style='color:red; font-weight:bold;'>[차단기OFF]</span> VCB / ACB / MG / MC OFF로 축전지 방전, 발전기 가동 중", unsafe_allow_html=True)
    st.markdown("<span style='color:red; font-weight:bold;'>[변압기 고장]</span> 축전기 방전 또는 발전기 가동 중", unsafe_allow_html=True)
    st.markdown("<span style='color:red; font-weight:bold;'>[국사 화재]</span> 화재감지기 작동 현장 출동중", unsafe_allow_html=True)
    st.markdown("<span style='color:red; font-weight:bold;'>[국사 침수]</span> 침수 알람 발생 현장 출동중", unsafe_allow_html=True)

    st.header("-네트워트 현황보고-")
    st.markdown("<span style='color:red;'>[MOSS 항목]</span> 전원,교환,액세스", unsafe_allow_html=True)
    st.markdown("<span style='color:red;'>[PING경보]</span> ACCESS_XDSL,엔토피아", unsafe_allow_html=True)
    st.markdown("<span style='color:red;'>[공사정보]</span> 작업통제_대쉬보드 총건수_1000/page설정_ 작업현황 전체복사 후 A2 주변서식에 맟추기", unsafe_allow_html=True)
    
 






def moss_page():
    st.markdown(
        """
        <style>
        body {
            background-color: #87CEEB; /* 하늘색 */
        }
        </style>
        """,
        unsafe_allow_html=True
    )
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
    if "power_outage_checked" not in st.session_state:
        st.session_state.power_outage_checked = False

    def bs_checkbox_callback():
        st.session_state.power_outage_checked = False

    def power_checkbox_callback():
        st.session_state.bs_checked = False


    col1, col2 = st.columns(2)

    with col1:
        is_bs_checked = st.checkbox("B/S", key="bs_checked", on_change=bs_checkbox_callback)
    with col2:
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
            df = pd.read_csv('국사.csv')
            return df


        def get_nsc(station_name, df):
            # 수용국사에서 '국사'를 제외한 이름을 비교
            station_name_core = station_name.replace("국사", "")
            row = df[df['수용국사'].str.contains(station_name_core)]
            if not row.empty:
                return row.iloc[0]['NSC']
            return None

        # NSC 값을 변환하는 함수
        def transform_nsc(nsc):
            if "충북액세스운용센터" in nsc or "충남액세스운용센터" in nsc:
                return "충청"
            elif "전남액세스운용센터" in nsc or "전북액세스운용센터" in nsc:
                return "호남"
            elif "부산액세스운용센터" in nsc or "경남액세스운용센터" in nsc:
                return "부산"
            elif "대구액세스운용센터" in nsc or "경북액세스운용센터" in nsc:
                return "대구"
            return nsc
          
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
                    nsc = transform_nsc(nsc)
                    st.write(f"[L2_정전] {nsc}/{daegu_station} L2 다량장애 {district}일대 한전정전 (추정) L2*{l2_systems}sys({customers}고객)")


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
                    nsc = transform_nsc(nsc)
                    st.write(f"[L2_선로] {nsc}/{honam_station} 선로장애 (추정) L2*{l2_systems_line}sys({customers_line}고객)")


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
                    nsc = transform_nsc(nsc)
                    st.write(f"[아파트_정전] {nsc}/{busan_station} {apartment_name} {outage_type} L2*{l2_systems_apartment}sys({customers_apartment}고객)")



    else:
        selected_bs_format = None
        results = []
        db_results = []  # 빈 리스트로 초기화
        기타_results = []

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
                        
        # 여러 줄 입력을 허용하는 입력란
        user_input = st.text_area("입력란", key="user_input")

        # 텍스트를 줄 단위로 나누기
        lines = user_input.splitlines()

        # 포맷팅된 결과를 저장할 리스트
        formatted_lines = []
        combined_line = ""

        for i, line in enumerate(lines):
            line = line.lstrip()  # 줄 앞의 공백 제거
            if "[현장]" in line:
                # "[현장]"이 포함된 줄 앞의 공백 제거
                line = line[line.index("[현장]"):]  # "[현장]" 포함된 줄부터 시작
                combined_line = line
            elif combined_line:
                # combined_line이 이미 설정된 경우, 그 뒤에 이어 붙임
                combined_line += line
                formatted_lines.append(combined_line)
                combined_line = ""  # 초기화하여 다음 줄 처리에 영향 주지 않도록 함
            else:
                # "[현장]"이 없는 일반 줄은 그대로 추가
                formatted_lines.append(line)

        # 리스트를 문자열로 변환
        formatted_output = "\n".join(formatted_lines)






        if not is_bs_checked:
            head_format = get_format(formatted_output)
            if head_format:
                results.append(head_format)


        출동예방_actions = []
        selected_actions = []
        
        adapter_info = ""  # 어댑터 정보를 저장할 변수
        
        # Show these sections only if selected_bs_format is not "[NOC_광레벨불]"
        if selected_bs_format != "[NOC_광레벨불]" and selected_bs_format != "[NOC_장비철거]":
            selected_actions = st.multiselect("선조치_NOC에 대한 내용을 선택하세요:", 선조치_NOC_options, key="selected_actions")
            db_results = []
            기타_results = []
            if "DB 삭제 여부" in selected_actions:
                if "기타_고객DB_neoss_불가" not in st.session_state:
                    st.session_state.기타_고객DB_neoss_불가 = False
                if "기타_neoss_완료" not in st.session_state:
                    st.session_state.기타_neoss_완료 = False

                def 기타_고객DB_neoss_불가_callback():
                    st.session_state.기타_neoss_완료 = False

                def 기타_neoss_완료_callback():
                    st.session_state.기타_고객DB_neoss_불가 = False

                # Create two columns for horizontal layout
                col1, col2 = st.columns(2)
    
                with col1:
                    기타_고객DB_neoss_불가 = st.checkbox("고객DB 존재 NeOSS 삭제 불가", key="기타_고객DB_neoss_불가", on_change=기타_고객DB_neoss_불가_callback)
    
                with col2:
                    기타_neoss_완료 = st.checkbox("NeOSS 삭제 완료", key="기타_neoss_완료", on_change=기타_neoss_완료_callback)

                if 기타_고객DB_neoss_불가:
                    db_results.append("고객DB 존재/NeOSS 삭제 불가")
                if 기타_neoss_완료:
                    db_results.append("NeOSS 삭제 완료")

            if "광레벨 확인" in selected_actions:
                col1, col2 = st.columns(2)
                with col1:
                    rssi_value = st.text_input("RSSI 값을 입력하세요:")
   
                with col2:
                    ddm_value = st.text_input("ddm 값을 입력하세요:")
    
                # Combine RSSI and ddm values with a "/" separator if both values are provided
                if rssi_value or ddm_value:
                    combined_values = ""
                    if rssi_value:
                        combined_values += f"RSSI: {rssi_value}"
                    if ddm_value:
                        if combined_values:
                            combined_values += " / "
                        combined_values += f"ddm: {ddm_value}"
        
                    기타_results.append(combined_values)

            if "CRC" in selected_actions:
                crc_input = st.text_area("CRC 정보 입력:")
                # Sum 값을 추출하는 정규 표현식
                ul_rx_sum_pattern = re.compile(r'UL Rx\s+\d+\s+(\d+)\s+\d+')
                dl_rx_sum_pattern = re.compile(r'DL Rx\s+\d+\s+(\d+)\s+\d+')

                ul_rx_sum_match = ul_rx_sum_pattern.search(crc_input)
                dl_rx_sum_match = dl_rx_sum_pattern.search(crc_input)

                if ul_rx_sum_match and dl_rx_sum_match:
                    ul_rx_sum = ul_rx_sum_match.group(1)
                    dl_rx_sum = dl_rx_sum_match.group(1)
 
                    기타_results.append(f"UL Rx: {ul_rx_sum}")
                    기타_results.append(f"DL Rx: {dl_rx_sum}")
                else:
                    기타_results.append("No matching Sum data found.")

                    
            if "어댑터 전/후 작성" in selected_actions:
                col1, col2 = st.columns(2)
                with col1:
                    before_adapter = st.text_input("교체 전 어댑터:")

                with col2:
                    after_adapter = st.text_input("교체 후 어댑터:")

                if before_adapter or after_adapter:
                    if before_adapter:
                        adapter_info += f"교체 전 어댑터: {before_adapter}"
                    if after_adapter:
                        if before_adapter:
                            adapter_info += " / "
                        adapter_info += f"교체 후 어댑터: {after_adapter}"
                    adapter_info = f" ({adapter_info.strip()})"

        # user_input에 어댑터 정보를 추가하여 출력
        results.append(formatted_output + adapter_info)
        results.extend(db_results)
        results.extend(기타_results)
        results.append("수고하셨습니다")


        # 출동예방_actions 처리
        출동예방_actions = []
        if "전기작업 확인(전화)" in selected_actions:
            출동예방_actions.append("[NOC]전기작업 확인(전화)")
        if "출동보류" in selected_actions:
            출동예방_actions.append("[NOC]출동보류")

        # 현장TM 관련 처리
        selected_locations = st.multiselect(
            "현장에 대한 내용을 선택하세요:",
            ["[현장TM]", "주소", "연락처", "장비위치", "차단기위치", "출입방법", "기타(간단히 내용입력)"],
            key="selected_locations_multiselect"
        )

        현장TM_내용 = ""
        현장TM_출동예방 = False  # 초기화, 기본값 설정

        if "[현장TM]" in selected_locations:
            현장TM_내용 = st.text_input("[현장TM] 내용을 입력하세요:", key="현장TM_내용")
            현장TM_출동예방 = st.checkbox("[현장TM] 내용을 <출동예방>에 포함", key="현장TM_출동예방")

        # 출동예방_actions 업데이트
        if 현장TM_출동예방 and 현장TM_내용:
            출동예방_actions.append(f"[현장TM] {clear_tm_content(현장TM_내용)}")

        if 출동예방_actions:
            results.append(f"<출동예방>{', '.join(출동예방_actions)}")

        # 선조치_NOC 관련 결과 처리
        filtered_actions = [action for action in selected_actions if action not in ["DB 삭제 여부", "광레벨 확인", "어댑터 전/후 작성"]]
        if filtered_actions:
            formatted_actions = ", ".join(filtered_actions)
            results.append(f"<선조치_NOC> {formatted_actions}")

        # 현장 관련 처리
        formatted_locations = " / ".join([
            f"{location}" if location != "기타(간단히 내용입력)"
            else f"기타({st.text_input('기타 내용 입력', key='기타_내용')})"
            for location in selected_locations
            if location != "[현장TM]"
        ])

        # [현장TM]이 선택되었으나 내용이 없을 경우 처리
        if "[현장TM]" in selected_locations and not 현장TM_출동예방:
            if 현장TM_내용:
                formatted_locations = f"[현장TM] {clear_tm_content(현장TM_내용)}" + (f" , {formatted_locations.strip()} 수정요청" if formatted_locations else "")
            else:
                formatted_locations = "[현장TM]" + (f" , {formatted_locations.strip()} 수정요청" if formatted_locations else "")
        elif formatted_locations:
            formatted_locations = f"{formatted_locations.strip()} 수정요청"

        if formatted_locations:
            results.append(f"<현장> {formatted_locations}")


        col1, col2 = st.columns(2)
        timezone = pytz.timezone('Asia/Seoul')  # 한국 시간대로 설정
        now = datetime.now(timezone)
        current_date = now.strftime("%Y-%m-%d")
        with col1:
           namecard_count = st.number_input("명함형 갯수:", min_value=0, step=1, key="namecard_count")
       
        with col2:
            sticker_count = st.number_input("스티커형 갯수:", min_value=0, step=1, key="sticker_count")

        if namecard_count > 0 or sticker_count > 0:
            results.append(f"[{current_date}] [스티커] 명함형 {namecard_count}장, 스티커형 {sticker_count}장")




    

       # 버튼 클릭 상태를 저장하는 세션 상태 확인 및 초기화
        if 'button_clicked' not in st.session_state:
            st.session_state['button_clicked'] = False
        if 'output_active' not in st.session_state:
            st.session_state['output_active'] = False
        if 'reset_active' not in st.session_state:
            st.session_state['reset_active'] = False

        col1, col2, col3 = st.columns([2.8, 0.5, 0.7])

        with col1:
            if st.button("출력"):
                st.session_state['output_active'] = True
                st.session_state['button_clicked'] = False
                st.session_state['reset_active'] = False
                output_text = "\n".join(results)  # Join results with new lines for the desired format
                st.text(output_text)  # Print output_text when the "출력" button is pressed


        with col2:
            if st.button("입력란 초기화"):
                st.session_state['output_active'] = False
                st.session_state['button_clicked'] = False
                st.session_state['reset_active'] = True
                clear_text()

        with col3:
            if st.button('MOSS 회복 코드 표준'):
                st.session_state['output_active'] = False
                st.session_state['button_clicked'] = not st.session_state['button_clicked']
                st.session_state['reset_active'] = False

        if st.session_state['button_clicked']:
            placeholder = st.empty()
            with placeholder.container():
                st.markdown(
                """
                <style>
                /* 데이터프레임을 전체 화면으로 보이도록 스타일 조정 */
                .css-1l02zno {
                    width: 200%;
                    max-width: 100%;
                    height: calc(100vh - 200px); /* 화면 높이에서 200px을 뺀 높이 설정 */
                    overflow: auto; /* 스크롤이 필요한 경우 스크롤 허용 */
                }
                </style>
                """,
                unsafe_allow_html=True
            )
            st.dataframe(df)

        # 이 버튼이 클릭되면 다른 버튼이 비활성화 되도록 보장합니다.
        if st.session_state['output_active']:
            # 표시 내용 설정이 끝난 후 초기화된 버튼의 경우
            st.session_state['button_clicked'] = False
            st.session_state['reset_active'] = False
        elif st.session_state['reset_active']:
            st.session_state['button_clicked'] = False
            st.session_state['output_active'] = False





                
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

def command_page():
    st.title("명령어")
    # secrets.toml 파일에서 비밀번호 가져오기
    commande_password = st.secrets["command"]["PASSWORD"]

    # 'command_logged_in' 및 'last_active' 초기화
    if "command_logged_in" not in st.session_state:
        st.session_state.command_logged_in = False

    if "last_active" not in st.session_state:
        st.session_state.last_active = time.time()

    # 일정 시간이 경과하면 세션 초기화 (예: 10초)
    if time.time() - st.session_state.last_active > 300:
        st.session_state.command_logged_in = False

    # 비밀번호 입력 처리
    if not st.session_state.command_logged_in:
        password = st.text_input("비밀번호 입력", type="password")

        if password == commande_password:
            st.session_state.command_logged_in = True
            st.session_state.last_active = time.time()
            st.success("로그인 성공")
            st.experimental_rerun()
        elif password:
            st.error("잘못된 비밀번호입니다. 다시 입력해주세요.")
    else:
        st.session_state.last_active = time.time()  # 사용자가 페이지에 있을 때 시간 갱신

    
    if st.session_state.command_logged_in:
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
        content_option = st.radio("장비선택", ["","저속급L2", "L2", "OLT"])

        if content_option == "저속급L2":
            low_L2_option = st.radio("저속급 L2", ["","MVD100XX", "U3024B/48A", "EX1172/LR", "HAMX6000", "DX5624", "IRT800"])
            if low_L2_option == "MVD100XX":
                image_path = 'mvd.png'

                # 이미지 열기
                image = Image.open(image_path)

                # 이미지 표시
                st.image(image, caption='Local Image', use_column_width=True)

            if low_L2_option == "U3024B/48A":
                image_path = 'u3024.png'

                # 이미지 열기
                image = Image.open(image_path)

                # 이미지 표시
                st.image(image, caption='Local Image', use_column_width=True)

            if low_L2_option == "EX1172/LR":
                image_path = '1172.png'

                # 이미지 열기
                image = Image.open(image_path)

                # 이미지 표시
                st.image(image, caption='Local Image', use_column_width=True)

            if low_L2_option == "HAMX6000":
                image_path = 'haxm.png'

                # 이미지 열기
                image = Image.open(image_path)

                # 이미지 표시
                st.image(image, caption='Local Image', use_column_width=True)

            if low_L2_option == "DX5624":
                image_path = 'dx5624.png'

                # 이미지 열기
                image = Image.open(image_path)

                # 이미지 표시
                st.image(image, caption='Local Image', use_column_width=True)

            if low_L2_option == "IRT800":
                image_path = 'irt.png'

                # 이미지 열기
                image = Image.open(image_path)

                # 이미지 표시
                st.image(image, caption='Local Image', use_column_width=True)
                
        if content_option == "L2":
            L2_option = st.radio("L2", ["","V2724GB", "E5624R"])
            
        if content_option == "OLT":
            OLT = st.radio("OLT", ["","동원(소)", "다산(중)", "동원(대)", "유(대)"])






def manage_page():
    st.title("Manage")
    # secrets.toml 파일에서 비밀번호 가져오기
    manage_password = st.secrets["manage"]["password"]

    # 'manage_logged_in' 및 'last_active' 초기화
    if "manage_logged_in" not in st.session_state:
        st.session_state.manage_logged_in = False

    if "last_active" not in st.session_state:
        st.session_state.last_active = time.time()

    # 일정 시간이 경과하면 세션 초기화 (예: 10초)
    if time.time() - st.session_state.last_active > 300:
        st.session_state.manage_logged_in = False

    # 비밀번호 입력 처리
    if not st.session_state.manage_logged_in:
        password = st.text_input("비밀번호 입력", type="password")

        if password == manage_password:
            st.session_state.manage_logged_in = True
            st.session_state.last_active = time.time()
            st.success("로그인 성공")
            st.experimental_rerun()
        elif password:
            st.error("잘못된 비밀번호입니다. 다시 입력해주세요.")
    else:
        st.session_state.last_active = time.time()  # 사용자가 페이지에 있을 때 시간 갱신
    
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





  
# Streamlit 애플리케이션 실행
if __name__ == "__main__":
    selected = option_menu(
        menu_title=None,  # 메뉴 제목 (원하지 않으면 None)
        options=["Home", "MOSS", "Worksync", "명령어", "Manage"],  # 옵션 이름들
        icons=["house", "box-arrow-down", "calendar2-check", "menu-up", "gear"],  # 각 옵션에 해당하는 아이콘
        menu_icon="cast",  # 메뉴 아이콘
        default_index=0,  # 기본 선택 옵션
        orientation="horizontal"  # 메뉴 방향 (수평)
    )

    render_sidebar()

    if selected == "Home":
        home_page()
    elif selected == "MOSS":
        moss_page()
    elif selected == "Worksync":
        worksync_page()
    elif selected == "명령어":
        command_page()
    elif selected == "Manage":
        manage_page()
