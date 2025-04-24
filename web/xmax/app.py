import streamlit as st
import folium
from folium import plugins
import pandas as pd
from streamlit_folium import st_folium

# ページ設定
st.set_page_config(
    page_title="XMAX ツアーマップ",
    page_icon="🗺️",
    layout="wide"
)

# タイトル
st.title("XMAX ツアーマップ")
st.markdown("XMAXの各スポットを地図上で確認できます。")

# CSVファイルの読み込み
@st.cache_data
def load_data():
    return pd.read_csv("web/xmax/data/places.csv")

df = load_data()

# 地図の中心を設定（XMAXの中心座標）
m = folium.Map(
    location=[35.0525, 136.8850],
    zoom_start=5,
    tiles="OpenStreetMap"
)

# マーカーを追加
for idx, row in df.iterrows():
    popup_html = f"""
    <div style="width: 200px;">
        <h4>{row['name']}</h4>
        <p>{row['description']}</p>
        <a href="{row['note_url']}" target="_blank">記事を読む</a>
    </div>
    """
    
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=folium.Popup(popup_html, max_width=300),
        tooltip=row['name']
    ).add_to(m)

# 地図を表示
st_folium(m, width=1200, height=600)

# スポット一覧を表示
st.subheader("スポット一覧")
for idx, row in df.iterrows():
    with st.expander(row['name']):
        st.write(row['description'])
        st.markdown(f"[記事を読む]({row['note_url']})")
