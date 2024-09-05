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

            # Check if the address is "#VALUE!"
            if address == "#VALUE!":
                st.text("데이터 값 오류(#VALUE!)")
            else:
                st.write("★동일국소 점검 대상★")
                same_address_work = df_no_duplicates[df_no_duplicates['사업장'] == address]
                for idx, (index, row) in enumerate(same_address_work.iterrows(), start=1):
                    st.text(f"{idx}.{row['장비명/국사명']} - {row['업무명']}({row['장비ID']})")
        else:
            st.text("Work-Sync(BS업무) 점검 대상 없습니다.")

# Streamlit 애플리케이션 실행
if __name__ == "__main__":
    selected = option_menu(
        menu_title=None,  # 메뉴 제목 (원하지 않으면 None)
        options=["Worksync"],  # 옵션 이름들
        icons=["calendar2-check"],  # 각 옵션에 해당하는 아이콘
        menu_icon="cast",  # 메뉴 아이콘
        default_index=0,  # 기본 선택 옵션
        orientation="horizontal"  # 메뉴 방향 (수평)
    )


    if selected == "Worksync":
        worksync_page()
