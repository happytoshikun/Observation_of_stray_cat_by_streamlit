import streamlit as st
from streamlit_folium import st_folium
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import folium
from folium.plugins import HeatMap

# Google Sheetsからデータを読み込む関数
def read_data_from_google_sheets():
    conn = st.experimental_connection("gsheets", type=GSheetsConnection)

    df = conn.read()

    return df

# メインのStreamlitアプリケーション
def main():
    # 横幅を広げる場合
    st.set_page_config(layout="wide")

    st.title("野良猫の行動観察")

    # Google Sheetsからデータを読み込む
    data = read_data_from_google_sheets()

    # 地図の種類を選択
    genre = st.radio(
        "表示する地図を選択してください",
        ['移動ルート','観測ポイント','ヒートマップ'])

    # 地図を表示
    if genre == '移動ルート':
        m = folium.Map(location=data.iloc[0], zoom_start=17)
        folium.Marker(location=data.iloc[0], popup="start").add_to(m)
        folium.PolyLine(data, color="green", weight=2.5, opacity=1).add_to(m)
        folium.Marker(location=data.iloc[-1], popup="goal",icon=folium.Icon(color='red')).add_to(m)
        st_folium(m, width=1200, height=800)
    
    if genre == '観測ポイント':
        m = folium.Map(location=data.iloc[0], zoom_start=17)
        for i in range(len(data)):
            folium.CircleMarker(location=data.iloc[i],radius=5,color='#B22222').add_to(m)
        st_folium(m, width=1200, height=800)

    if genre == 'ヒートマップ':
        m = folium.Map(location=data.iloc[0], zoom_start=17)
        HeatMap(data, radius=20, blur=5).add_to(m)
        st_folium(m, width=1200, height=800)

if __name__ == "__main__":
    main()