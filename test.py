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
import streamlit.components.v1 as components

# 포맷 데이터 포멧
formats = {
    "전기안전검사": "[전기안전검사]",
    "전기검사": "[전기안전검사]",
    "점검": "[전기안전검사]",
    "검사": "[전기안전검사]",
    "전기작업": "[고객측작업]",
    "작업": "[고객측작업]",
    "공사": "[고객측작업]",
    "한전작업": "[한전작업]",
    "한전 작업": "[한전작업]",
    "변압기": "[한전작업]",
    "한전인입전원": "[한전고장]",
    "한전인입 전원": "[한전고장]",
    "한전 인입전원": "[한전고장]",
    "한전 인입 전원": "[한전고장]",
    "한전인입": "[한전고장]",
    "한전고장": "[한전고장]",
    "한전 고장": "[한전고장]",
    "한전정전": "[한전고장]",
    "한전 정전": "[한전고장]",
    "한전 인입": "[한전고장]",
    "한전입전": "[한전고장]",
    "한전 입전": "[한전고장]",
    "일대": "[일대정전]",
    "일대 정전": "[일대정전]",
    "일대정전": "[일대정전]",
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
    "누전": "[사설측누전]",
    "사설측 누전": "[사설측누전]",
    "사설측누전": "[사설측누전]",
    "체납": "[요금체납]",
    "요금": "[요금체납]",
    "단전": "[요금체납]",
    "이동중": "[출동중복구]",
    "이동 중": "[출동중복구]",
    "출동 중 복구": "[출동중복구]",
    "출동중복구": "[출동중복구]",
    "출동 중 자동복구": "[출동중복구]",
    "출동중자동복구": "[출동중복구]",
    "출동중 자동복구": "[출동중복구]",
    "자동": "[출동중복구]",
    "자연": "[출동중복구]",
    "멀티탭": "[멀티탭 ON/교체]",
    "멀티탭 교체": "[멀티탭 ON/교체]",
    "어댑터": "[전원어댑터교체]",
    "어뎁터": "[전원어댑터교체]",
    "아뎁터": "[전원어댑터교체]",
    "아댑터": "[전원어댑터교체]",
    "아답터": "[전원어댑터교체]",
    "아답타": "[전원어댑터교체]",
    "어덥터": "[전원어댑터교체]",
    "어답터": "[전원어댑터교체]",
    "콘센트": "[플러그_접촉불량]",
    "콘샌트": "[플러그_접촉불량]",
    "발전기": "[전원가복구]",
    "파워뱅크": "[전원가복구]",
    "가복구": "[전원가복구]",
    "임시": "[전원가복구]",
    "전원선": "[전원가복구]",
    "전원 절체": "[전원가복구]",
    "전원절체": "[전원가복구]",
    "전원투입": "[사설정전복구]",
    "전원 투입": "[사설정전복구]",
    "루트변경": "[전원가복구]",
    "루트 변경": "[전원가복구]",
    "루트": "[전원가복구]",
    "PSU": "[전원부교체]",
    "psu": "[전원부교체]",
    "PLK": "[전원부교체]",
    "plk": "[전원부교체]",   
    "MCU": "[제어부교체]",  
    "Mcu": "[제어부교체]",  
    "mcu": "[제어부교체]",  
    "SCU": "[제어부교체]",  
    "Scu": "[제어부교체]",
    "scu": "[제어부교체]",
    "MCU": "[제어부교체]",
    "Mcu": "[제어부교체]",
    "mcu": "[제어부교체]",
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
    "LSW": "[업링크부교체]",
    "Lsw": "[업링크부교체]",
    "lsw": "[업링크부교체]",
    "LIU": "[업링크부교체]",
    "Liu": "[업링크부교체]",
    "liu": "[업링크부교체]",
    "AIU": "[가입자부교체]",
    "Aiu": "[가입자부교체]",
    "aiu": "[가입자부교체]",
    "VDL": "[가입자부교체]",
    "Vdl": "[가입자부교체]",
    "vdl": "[가입자부교체]",
    "PON": "[PON모듈교체]",
    "pon": "[PON모듈교체]",
    "Pon": "[PON모듈교체]",
    "PoN": "[PON모듈교체]",
    "장비회수": "[장비철거]",
    "장비 회수": "[장비철거]",
    "장비철거": "[장비철거]",
    "장비 철거": "[장비철거]",
    "망실": "[망실]",
    "장비없음": "[망실]",
    "장비 없음": "[망실]",
    "리셋": "[장비리셋]",
    "로딩": "[장비리셋]",
    "리부팅": "[장비리셋]",
    "재설정": "[설정변경]",
    "설정변경": "[설정변경]",
    "Config": "[설정변경]",
    "원격": "[원격제어]",
    "포트BLK": "[원격제어]",
    "포트down": "[원격제어]",
    "포트 down": "[원격제어]",
    "포트 DOWN": "[원격제어]",
    "포트DOWN": "[원격제어]",
    "포트리셋": "[원격제어]",
    "Ping test": "[원격제어]",
    "ping test": "[원격제어]",
    "dbm": "[감쇠기]",
    "취부": "[감쇠기]",
    "감쇠기": "[감쇠기]",
    "att": "[감쇠기]",
    "UTP": "[업링크_UTP]",
    "utp": "[업링크_UTP]",
    "Utp": "[업링크_UTP]",
    "포트 변경": "[업링크_UTP]",
    "포트변경": "[업링크_UTP]",
    "OJC": "[광점퍼코드]",
    "ojc": "[광점퍼코드]",
    "접촉불량": "[광점퍼코드]",
    "밴딩": "[광점퍼코드]",
    "광점퍼코드": "[광점퍼코드]",
    "커넥터": "[광점퍼코드]",
    "커낵터": "[광점퍼코드]",
    "상위망": "[상위망]",
    "GBIC": "[상위망]",
    "gbic": "[상위망]",
    "PIU": "[상위망]",
    "piu": "[상위망]",
    "Piu": "[상위망]",
    "광케이블": "[상위망]",
    "화재": "[화재피해]",
    "침수": "[침수피해]",
    "누수": "[누수피해]",
    "차량": "[차량피해]",
    "sk": "[타사전환]",
    "SK": "[타사전환]",
    "lg": "[타사전환]",
    "LG": "[타사전환]",
    "타사이탈": "[타사전환]",
    "타사 이탈": "[타사전환]",
    "타사전환": "[타사전환]",
    "타사 전환": "[타사전환]",   
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
    "DB현행화",
    "FOLLOW추가",
    "출동보류",
    "정전알림이 등록",
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
    matched_formats = [formats[keyword] for keyword in formats if keyword in text]
    return matched_formats[-1] if matched_formats else "[기타]"


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
            "NOC 대표번호" : "1577-7315",
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

    st.header("-야간(18:00 ~ 09:00) MOSS 발행 관련-")
    st.markdown("<span style='color:red;'>[18:00~22:00]</span> 원룸/빌라 고객5 이하(미발행). 익일 예약발행. VOC인입 시 자동발행.", unsafe_allow_html=True)
    st.markdown("<span style='color:red;'>[22:00~07:00]</span> 숙박업소, 1등급, 주요시설(언론사,관공서,법원 등) 발행.", unsafe_allow_html=True)
    st.markdown("<span style='color:red;'>고객센터 인입 VOC는 발행. 일반 VOC건은 오전 07시 예약발행 발행명에 [수동_예약]", unsafe_allow_html=True)
    
 






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
    timezone = pytz.timezone('Asia/Seoul')  # 한국 시간대로 설정
    now = datetime.now(timezone)
    current_date = now.strftime("%y.%m.%d")

    # Streamlit 애플리케이션
    data = {"﻿MOSS BS 발행 HEAD": ["[NOC_광레벨불]", "[NOC_CRC발생]", "[NOC_장비교체]", "[NOC_장비철거]", "[NOC_민원처리]", "[NOC_어댑터교체]", "[NOC_PLK_PSU교체]", "[NOC_PSU교체]", "[NOC_중복장애]", "[NOC_전원OFF]", "[NOC_품질개선]", "[NOC_10G(용량확대)]", "[NOC_자산관리]", "[NOC_점검정비]", "[NOC_BAT(24)]", "[NOC_kernel정비]", [NOC_형상삭제]", "[NOC_전원민원]"]}
    df1 = pd.DataFrame(data)
    # 컬럼 이름 확인 및 수정
    df1.columns = df1.columns.str.strip()  # 컬럼 이름에 있는 공백 제거
    df1.columns = df1.columns.str.replace("﻿", "", regex=False)  # 특수문자 제거
    # 정렬 기준 컬럼 생성
    df1["정렬기준"] = df1["MOSS BS 발행 HEAD"].str.replace("[NOC_", "", regex=False)

    # 데이터 3열로 나누기
    with st.expander("MOSS BS 발행 HEAD"):
        cols = st.columns(3)
    
        # 각 열에 데이터를 나누어 출력하기
        num_cols = 3
        items_per_column = len(df1) // num_cols  # 각 열에 들어갈 항목 수
    
        for i, col in enumerate(cols):
            start_idx = i * items_per_column
            if i == num_cols - 1:  # 마지막 열은 나머지 데이터 모두 출력
                col_data = df1["MOSS BS 발행 HEAD"][start_idx:]
            else:
                col_data = df1["MOSS BS 발행 HEAD"][start_idx:start_idx + items_per_column]
        
            # 각 열에 데이터 출력 및 클릭 시 복사
            for item in col_data:
                if col.button(f"복사: {item}"):  # 버튼 텍스트는 복사할 내용
                    pyperclip.copy(item)  # 클립보드에 복사
                    st.success(f"'{item}'이(가) 클립보드에 복사되었습니다.")  # 사용자에게 알림
  
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
                    st.write(f"[일대정전] {nsc}/{daegu_station} L2 다량장애 {district}일대 한전정전 (추정) L2*{l2_systems}sys({customers}고객)")


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
                    st.write(f"[L2선로] {nsc}/{honam_station} 선로장애 (추정) L2*{l2_systems_line}sys({customers_line}고객)")


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
                    st.write(f"[사업장정전] {nsc}/{busan_station} {apartment_name} {outage_type} L2*{l2_systems_apartment}sys({customers_apartment}고객)")



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
                # 결과를 저장할 리스트
                기타_results = []

                # 형식 1: Upstream CRC32 / Downstream CRC32 형식
                upstream_downstream_pattern = re.compile(r'\bUpstream CRC32\s+\|\s+Downstream CRC32\b')
                upstream_crc_pattern = re.compile(r'\d+\s+\|\s+\d+')

                # 형식 2: UL Rx / DL Rx 형식
                ul_rx_pattern = re.compile(r'UL Rx\s+\d+\s+(\d+)\s+\d+')
                dl_rx_pattern = re.compile(r'DL Rx\s+\d+\s+(\d+)\s+\d+')

                # 형식 1에 맞는지 확인
                if upstream_downstream_pattern.search(crc_input):
                    upstream_crc_match = upstream_crc_pattern.findall(crc_input)
                    if upstream_crc_match:
                        # 각 CRC 값 추출
                        upstream_crc, downstream_crc = upstream_crc_match[0].split("|")
                        기타_results.append(f"Upstream CRC32: {upstream_crc.strip()}")
                        기타_results.append(f"Downstream CRC32: {downstream_crc.strip()}")
                    else:
                        기타_results.append("No matching Upstream/Downstream CRC32 data found.")
    
                # 형식 2에 맞는지 확인
                elif ul_rx_pattern.search(crc_input) and dl_rx_pattern.search(crc_input):
                    ul_rx_sum_match = ul_rx_pattern.search(crc_input)
                    dl_rx_sum_match = dl_rx_pattern.search(crc_input)
                    if ul_rx_sum_match and dl_rx_sum_match:
                        ul_rx_sum = ul_rx_sum_match.group(1)
                        dl_rx_sum = dl_rx_sum_match.group(1)
                        기타_results.append(f"UL Rx: {ul_rx_sum}")
                        기타_results.append(f"DL Rx: {dl_rx_sum}")
                    
                    else:
                        기타_results.append("No matching UL Rx or DL Rx Sum data found.")
    
                # 아무 형식도 매칭되지 않을 경우
                else:
                    기타_results.append("No matching data found.")

                    
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
            results.append(f"[{current_date}]<현장> {formatted_locations}")


        col1, col2 = st.columns(2)
        
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

        output_text = "\n".join(results)

        with col1:
            if st.button("출력"):
                st.session_state['output_active'] = True
                st.session_state['button_clicked'] = False
                st.session_state['reset_active'] = False

                st.text(output_text)  # Print output_text when the "출력" button is pressed
                # 복사 버튼과 JavaScript 코드 추가
                if st.session_state['output_active']:
                    copy_button = """
                    <button onclick="copyToClipboard()">복사하기</button>
                    <script>
                    function copyToClipboard() {
                        var copyText = document.getElementById('output_area');
                        navigator.clipboard.writeText(copyText.value).then(function() {
                            var alertBox = document.createElement('div');
                            alertBox.textContent = '복사되었습니다!';
                            alertBox.style.position = 'fixed';
                            alertBox.style.bottom = '10px';
                            alertBox.style.left = '50%';
                            alertBox.style.transform = 'translateX(-50%)';
                            alertBox.style.backgroundColor = '#4CAF50';
                            alertBox.style.color = 'white';
                            alertBox.style.padding = '10px';
                            alertBox.style.borderRadius = '5px';
                            document.body.appendChild(alertBox);

                            // 5초 후 알림 제거
                            setTimeout(function() {
                                alertBox.remove();
                            }, 3000);
                        }, function(err) {
                            alert('복사 실패: ', err);
                        });
                    }
                    </script>
                    """

                    # 결과 텍스트를 textarea로 출력하고 HTML 버튼을 삽입
                    st.components.v1.html(f"""
                        <textarea id="output_area" style="display:none;">{output_text}</textarea>
                        {copy_button}
                    """, height=50)


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




def worksync_page():
    st.title("Worksync")

    # 데이터 파일 불러오기
    work = pd.read_csv("ws_data.csv")

    # '장비ID'와 '업무명'이 동일한 경우 중복된 행 제거
    df_no_duplicates = work.drop_duplicates(subset=['장비ID', '업무명'])

    # 장비ID 순서대로 정렬
    df_no_duplicates = df_no_duplicates.sort_values(by='장비ID')

    # IP 입력란
    ip_input = st.text_input("IP 입력", key="ip_input")

    # 결과를 저장할 result_text 변수 초기화
    result_text = ''

    if ip_input:
        # IP 입력값이 장비ID에 있는지 확인
        if ip_input in df_no_duplicates['장비ID'].values:
            # 해당 IP에 해당하는 사업장 찾기
            address = df_no_duplicates[df_no_duplicates['장비ID'] == ip_input]['사업장'].values[0]
            
            # 동일한 사업장에 있는 장비 필터링
            same_address_work = df_no_duplicates[df_no_duplicates['사업장'] == address]
            
            # 점검 대상 결과 문자열 생성
            result_text += "★동일국소 점검 대상★\n"
            for idx, (index, row) in enumerate(same_address_work.iterrows(), start=1):
                result_text += f"{idx}. {row['장비명/국사명']} - {row['장비ID']} ({row['업무명']})\n"
        else:
            # IP에 해당하는 데이터가 없을 때 기본 메시지
            result_text = "Work-Sync(BS업무) 점검 대상 없습니다."
    
    # 결과 출력 (기본 메시지 또는 필터링된 데이터)
    st.text_area("결과", result_text, height=200)

    # 복사 기능을 위한 HTML 버튼과 JavaScript 코드 추가
    copy_button = """
    <button onclick="copyToClipboard()">복사하기</button>
    <script>
    function copyToClipboard() {
                    var copyText = document.getElementById('result_area');
                    navigator.clipboard.writeText(copyText.value).then(function() {
                        var alertBox = document.createElement('div');
                        alertBox.textContent = '복사되었습니다!';
                        alertBox.style.position = 'fixed';
                        alertBox.style.bottom = '10px';
                        alertBox.style.left = '50%';
                        alertBox.style.transform = 'translateX(-50%)';
                        alertBox.style.backgroundColor = '#4CAF50';
                        alertBox.style.color = 'white';
                        alertBox.style.padding = '10px';
                        alertBox.style.borderRadius = '5px';
                        document.body.appendChild(alertBox);

                        // 5초 후 알림 제거
                        setTimeout(function() {
                            alertBox.remove();
                        }, 3000);
                    }, function(err) {
                        alert('복사 실패: ', err);
                    });
                }
                </script>
                """

    # 결과 텍스트를 textarea로 출력하고 HTML 버튼을 삽입
    st.components.v1.html(f"""
        <textarea id="result_area" style="display:none;">{result_text}</textarea>
        {copy_button}
    """, height=50)









def command_page():
    st.title("명령어")
    st.markdown(
    """
    <style>
    .stRadio > div {
         display: flex;
          flex-direction: row;
    }
    .stButton {
        margin: 0;
    }
     .command-container {
           display: flex;
           gap: 10px;
       }
      .command-item {
           flex: 1;
       }
    </style>
    """,
    unsafe_allow_html=True
    )

    # IP 입력란 생성
    olt_ip_address = st.text_input("IP 입력", "")

    # 비밀번호 입력 후에만 Radio 버튼을 표시
    content_option = st.radio("장비선택", ["", "동원", "유비쿼스"])

    if content_option == "동원":
        if olt_ip_address:
            # Create container with flex layout
            st.markdown('<div class="command-container">', unsafe_allow_html=True)

            # IP 입력에 대한 결과 출력
            with st.container():
                result_text_ip = "sh epon ip-macs all all | inc {}".format(olt_ip_address)
                st.text_area("IP 입력 결과", result_text_ip, height=100)

                copy_button_ip = """
                <button onclick="copyToClipboard('result_area_ip')">복사하기</button>
                <script>
                function copyToClipboard(elementId) {
                    var copyText = document.getElementById(elementId);
                    navigator.clipboard.writeText(copyText.value).then(function() {
                        var alertBox = document.createElement('div');
                        alertBox.textContent = '복사되었습니다!';
                        alertBox.style.position = 'fixed';
                        alertBox.style.bottom = '10px';
                        alertBox.style.left = '50%';
                        alertBox.style.transform = 'translateX(-50%)';
                        alertBox.style.backgroundColor = '#4CAF50';
                        alertBox.style.color = 'white';
                        alertBox.style.padding = '10px';
                        alertBox.style.borderRadius = '5px';
                        document.body.appendChild(alertBox);

                        // 5초 후 알림 제거
                        setTimeout(function() {
                            alertBox.remove();
                        }, 3000);
                    }, function(err) {
                        alert('복사 실패: ', err);
                    });
                }
                </script>
                """

                # 결과 텍스트를 textarea로 출력하고 HTML 버튼을 삽입
                components.html(f"""
                    <textarea id="result_area_ip" style="display:none;">{result_text_ip}</textarea>
                    {copy_button_ip}
                """, height=150)

            # Port/Slot 입력 및 전체/특정 선택
            with st.container():
                port_slot = st.text_input("Port/Slot (형식: 1/3)", "")
                selection = st.radio("선택", ["전체", "특정onu"])

                if port_slot:
                    if selection == "전체":
                        # 전체 선택 시 명령어 구성
                        result_text_port_slot = f"""
                        sh epon rssi rx-pwr-periodic {port_slot} all
                        sh epon onu-ddm {port_slot} all
                        sh epon crc-monitoring statistics {port_slot} all
                        """
                    elif selection == "특정onu":
                        # 특정 선택 시 명령어 구성
                        specific_value = st.text_input("onu 입력", "")
                        if specific_value:
                            result_text_port_slot = f"""
                            sh epon rssi rx-pwr-periodic {port_slot} {specific_value}
                            sh epon onu-ddm {port_slot} {specific_value}
                            sh epon crc-monitoring statistics {port_slot} {specific_value}
                            """
                        else:
                            result_text_port_slot = "onu를 입력해 주세요."

                    st.text_area("Port/Slot 입력 결과", result_text_port_slot, height=100)

                    copy_button_port_slot = """
                    <button onclick="copyToClipboard('result_area_port_slot')">복사하기</button>
                    <script>
                    function copyToClipboard(elementId) {
                        var copyText = document.getElementById(elementId);
                        navigator.clipboard.writeText(copyText.value).then(function() {
                            var alertBox = document.createElement('div');
                            alertBox.textContent = '복사되었습니다!';
                            alertBox.style.position = 'fixed';
                            alertBox.style.bottom = '10px';
                            alertBox.style.left = '50%';
                            alertBox.style.transform = 'translateX(-50%)';
                            alertBox.style.backgroundColor = '#4CAF50';
                            alertBox.style.color = 'white';
                            alertBox.style.padding = '10px';
                            alertBox.style.borderRadius = '5px';
                            document.body.appendChild(alertBox);

                            // 5초 후 알림 제거
                            setTimeout(function() {
                                alertBox.remove();
                            }, 3000);
                        }, function(err) {
                            alert('복사 실패: ', err);
                        });
                    }
                    </script>
                    """

                    # 결과 텍스트를 textarea로 출력하고 HTML 버튼을 삽입
                    components.html(f"""
                        <textarea id="result_area_port_slot" style="display:none;">{result_text_port_slot}</textarea>
                        {copy_button_port_slot}
                    """, height=150)

            st.markdown('</div>', unsafe_allow_html=True)

    if content_option == "유비쿼스":
        if olt_ip_address:
            # Create container with flex layout
            st.markdown('<div class="command-container">', unsafe_allow_html=True)

            # IP 입력에 대한 결과 출력
            with st.container():
                result_text_ip = "sh arp pon | inc {}".format(olt_ip_address)
                st.text_area("IP 입력 결과", result_text_ip, height=100)

                copy_button_ip = """
                <button onclick="copyToClipboard('result_area_ip')">복사하기</button>
                <script>
                function copyToClipboard(elementId) {
                    var copyText = document.getElementById(elementId);
                    navigator.clipboard.writeText(copyText.value).then(function() {
                        var alertBox = document.createElement('div');
                        alertBox.textContent = '복사되었습니다!';
                        alertBox.style.position = 'fixed';
                        alertBox.style.bottom = '10px';
                        alertBox.style.left = '50%';
                        alertBox.style.transform = 'translateX(-50%)';
                        alertBox.style.backgroundColor = '#4CAF50';
                        alertBox.style.color = 'white';
                        alertBox.style.padding = '10px';
                        alertBox.style.borderRadius = '5px';
                        document.body.appendChild(alertBox);

                        // 5초 후 알림 제거
                        setTimeout(function() {
                            alertBox.remove();
                        }, 3000);
                    }, function(err) {
                        alert('복사 실패: ', err);
                    });
                }
                </script>
                """

                # 결과 텍스트를 textarea로 출력하고 HTML 버튼을 삽입
                components.html(f"""
                    <textarea id="result_area_ip" style="display:none;">{result_text_ip}</textarea>
                    {copy_button_ip}
                """, height=150)

            # Port/Slot 입력 및 전체/특정 선택
            with st.container():
                port_slot = st.text_input("Port/Slot (형식: 1/3)", "")
                selection = st.radio("선택", ["전체", "특정onu"])

                if port_slot:
                    if selection == "전체":
                        # 전체 선택 시 명령어 구성
                        result_text_port_slot = f"""
                        sh pon topology onu {port_slot}
                        sh pon onu-ddm {port_slot}
                        sh pon stats onu-crc {port_slot}
                        """
                    elif selection == "특정onu":
                        # 특정 선택 시 명령어 구성
                        specific_value = st.text_input("onu 입력", "")
                        if specific_value:
                            result_text_port_slot = f"""
                            sh pon topology onu {port_slot} |inc {port_slot}-{specific_value}
                            sh pon onu-ddm {port_slot} |inc {port_slot}-{specific_value}
                            sh pon stats onu-crc {port_slot} |inc {port_slot}-{specific_value}
                            """
                        else:
                            result_text_port_slot = "onu를 입력해 주세요."

                    st.text_area("Port/Slot 입력 결과", result_text_port_slot, height=100)

                    copy_button_port_slot = """
                    <button onclick="copyToClipboard('result_area_port_slot')">복사하기</button>
                    <script>
                    function copyToClipboard(elementId) {
                        var copyText = document.getElementById(elementId);
                        navigator.clipboard.writeText(copyText.value).then(function() {
                            var alertBox = document.createElement('div');
                            alertBox.textContent = '복사되었습니다!';
                            alertBox.style.position = 'fixed';
                            alertBox.style.bottom = '10px';
                            alertBox.style.left = '50%';
                            alertBox.style.transform = 'translateX(-50%)';
                            alertBox.style.backgroundColor = '#4CAF50';
                            alertBox.style.color = 'white';
                            alertBox.style.padding = '10px';
                            alertBox.style.borderRadius = '5px';
                            document.body.appendChild(alertBox);

                            // 5초 후 알림 제거
                            setTimeout(function() {
                                alertBox.remove();
                            }, 3000);
                        }, function(err) {
                            alert('복사 실패: ', err);
                        });
                    }
                    </script>
                    """

                    # 결과 텍스트를 textarea로 출력하고 HTML 버튼을 삽입
                    components.html(f"""
                        <textarea id="result_area_port_slot" style="display:none;">{result_text_port_slot}</textarea>
                        {copy_button_port_slot}
                    """, height=150)

            st.markdown('</div>', unsafe_allow_html=True)



def L2_command_page():
    st.title("L2명령어")

    # 스타일 추가
    st.markdown(
        """
        <style>
        .stRadio > div {
             display: flex;
             flex-direction: row;
        }
        .stButton {
            margin: 0;
        }
         .command-container {
               display: flex;
               flex-direction: column;
               gap: 10px;
           }
          .command-item {
               display: flex;
               justify-content: space-between;
               align-items: center;
               padding: 5px;
               background-color: #f0f0f0;
               border: 1px solid #ddd;
               border-radius: 5px;
           }
        </style>
        """,
        unsafe_allow_html=True
    )

    # 장비 선택 라디오 버튼 (유니크 키 추가)
    L2_content_option = st.radio("장비선택", ["", "유비쿼스", "다산"], key="radio_l2_selection")

    # 공통적으로 사용할 복사 버튼 HTML과 스크립트
    copy_button_template = """
        <button onclick="copyToClipboard('{element_id}')">복사하기</button>
        <script>
        function copyToClipboard(elementId) {{
            var copyText = document.getElementById(elementId);
            navigator.clipboard.writeText(copyText.value).then(function() {{
                var alertBox = document.createElement('div');
                alertBox.textContent = '복사되었습니다!';
                alertBox.style.position = 'fixed';
                alertBox.style.bottom = '10px';
                alertBox.style.left = '50%';
                alertBox.style.transform = 'translateX(-50%)';
                alertBox.style.backgroundColor = '#4CAF50';
                alertBox.style.color = 'white';
                alertBox.style.padding = '10px';
                alertBox.style.borderRadius = '5px';
                document.body.appendChild(alertBox);

                // 3초 후 알림 제거
                setTimeout(function() {{
                    alertBox.remove();
                }}, 3000);
            }}, function(err) {{
                alert('복사 실패: ' + err);
            }});
        }}
        </script>
    """

    # "유비쿼스" 선택 시 명령어 리스트 및 복사 버튼 표시
    if L2_content_option == "유비쿼스":
        commands = [
            "sh uptime",
            "sh port status",
            "sh rate-limit",
            "sh ip dhcp snooping binding",
            "sh port statistics avg ty",
            "sh ip igmp snooping table reporter",
            "sh port statistics rmon",
            "sh port phy-diag",
            "sh max-hosts",
            "sh mac",
            "sh logging back"
        ]

        all_commands = "\n".join(commands)
        components.html(f"""
        <textarea id="all_commands" style="display:none;">{all_commands}</textarea>
        {copy_button_template.format(element_id='all_commands')}
        """, height=150)

        # 명령어별 복사 버튼 추가
        for idx, command in enumerate(commands):
            command_id = f"command_{idx}"
            components.html(f"""
            <div class="command-container">
                <div class="command-item">
                    <span>{command}</span>
                    {copy_button_template.format(element_id=command_id)}
                </div>
                <textarea id="{command_id}" style="display:none;">{command}</textarea>
            </div>
            """, height=80)

    # "다산" 선택 시 명령어 리스트 및 복사 버튼 표시
    elif L2_content_option == "다산":
        commands = [
            "sh uptime",
            "sh port status",
            "sh ip dhcp snooping binding",
            "sh rate-limit",
            "show port statistics avg ty",
            "show ip igmp snooping table",
            "sh port statistics rmon",
            "sh max-hosts",
            "sh mac",
            "show syslog l n r | include kernel",
            "sh syslog l v r"
        ]

        all_commands = "\n".join(commands)
        components.html(f"""
        <textarea id="all_commands_dasan" style="display:none;">{all_commands}</textarea>
        {copy_button_template.format(element_id='all_commands_dasan')}
        """, height=150)

        # 명령어별 복사 버튼 추가
        for idx, command in enumerate(commands):
            command_id = f"command_dasan_{idx}"
            components.html(f"""
            <div class="command-container">
                <div class="command-item">
                    <span>{command}</span>
                    {copy_button_template.format(element_id=command_id)}
                </div>
                <textarea id="{command_id}" style="display:none;">{command}</textarea>
            </div>
            """, height=80)






  
# Streamlit 애플리케이션 실행
if __name__ == "__main__":
    selected = option_menu(
        menu_title=None,  # 메뉴 제목 (원하지 않으면 None)
        options=["Home", "MOSS", "Worksync", "olt명령어", "L2명령어"],  # 옵션 이름들
        icons=["house", "box-arrow-down", "calendar2-check", "menu-up", "menu-up"],  # 각 옵션에 해당하는 아이콘
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
    elif selected == "olt명령어":
        command_page()
    elif selected == "L2명령어":
        L2_command_page()
