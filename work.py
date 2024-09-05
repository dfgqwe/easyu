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

    "# Worksync 페이지\n",
    "def worksync_page():\n",
    "    st.title(\"Worksync\")\n",
    "\n",
    "    # 데이터 파일 불러오기\n",
    "    work = pd.read_csv(\"ws_data.csv\")\n",
    "\n",
    "    # '장비ID'와 '업무명'이 동일한 경우 중복된 행 제거\n",
    "    df_no_duplicates = work.drop_duplicates(subset=['장비ID', '업무명'])\n",
    "\n",
    "    # 장비ID 순서대로 정렬\n",
    "    df_no_duplicates = df_no_duplicates.sort_values(by='장비ID')\n",
    "\n",
    "    # IP 입력 받기\n",
    "    ip_input = st.text_input(\"IP 입력\", \"\").replace(\" \", \"\")\n",
    "    \n",
    "    # IP 입력이 있을 경우\n",
    "    if ip_input:\n",
    "        # 입력된 IP에 해당되는 행 찾기\n",
    "        if ip_input in df_no_duplicates['장비ID'].values:\n",
    "            # 해당 IP의 사업장 찾기\n",
    "            address = df_no_duplicates[df_no_duplicates['장비ID'] == ip_input]['사업장'].values[0]\n",
    "\n",
    "            # Check if the address is \"#VALUE!\"\n",
    "            if address == \"#VALUE!\":\n",
    "                st.text(\"데이터 값 오류(#VALUE!)\")\n",
    "            else:\n",
    "                st.write(\"★동일국소 점검 대상★\")\n",
    "                same_address_work = df_no_duplicates[df_no_duplicates['사업장'] == address]\n",
    "                for idx, (index, row) in enumerate(same_address_work.iterrows(), start=1):\n",
    "                    st.text(f\"{idx}.{row['장비명/국사명']} - {row['업무명']}({row['장비ID']})\")\n",
    "        else:\n",
    "            st.text(\"Work-Sync(BS업무) 점검 대상 없습니다.\")\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "  \n",
    "# Streamlit 애플리케이션 실행\n",
    "if __name__ == \"__main__\":\n",
    "    selected = option_menu(\n",
    "        menu_title=None,  # 메뉴 제목 (원하지 않으면 None)\n",
    "        options=[\"Worksync\"],  # 옵션 이름들\n",
    "        icons=[\"calendar2-check\"],  # 각 옵션에 해당하는 아이콘\n",
    "        menu_icon=\"cast\",  # 메뉴 아이콘\n",
    "        default_index=0,  # 기본 선택 옵션\n",
    "        orientation=\"horizontal\"  # 메뉴 방향 (수평)\n",
    "    )\n",
    "\n",
    "\n",
    "    if  selected == \"Worksync\":\n",
    "        worksync_page()"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
