import streamlit as st
import plotly.express as px
import plotly.figure_factory as ff
import pandas as pd
import io
from streamlit_option_menu import option_menu
from PIL import Image
df3 = px.data.tips()

# 페이지 이름 설정
st.set_page_config(
    page_title="EDA project",
    page_icon="💻",
)

# sidebar 만들기
with st.sidebar:
    name = option_menu("EDA Project", ["Introduction", "About Data", "Data Visualization"],
                         icons=['house', 'file-earmark-text', 'bar-chart'],
                         menu_icon="laptop", default_index=0,
                         styles={
        "container": {"padding": "5!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "25px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#02ab21"},
    }
    )
    if st.button('contact me'):
        st.text('jinseulseo75@gmail.com')
        st.text('github : s2ul2')


if name == 'Introduction':
    st.title('💻 Monthly_Project I') 
    st.write('### 주제 : EDA with tips dataset.')
    st.text('tips dataset를 사용하여 다양한 그래프로 시각화 해보며 데이터가 갖는 특징을 파악해봅시다.')


elif name =='About Data':
    st.write('## 💰 사용 데이터 : Tips dataset', )
    st.text('식당에서 일하면서 받은 tip에 대한 정보를 기록한 데이터셋, 총 244개의 tip 정보')
    st.download_button('Download raw data', df3.to_csv(index = False).encode('utf-8')
, 'tips.csv')
    st.write('#### ✔ 상위 5개 데이터')
    st.write(df3.head())
    if st.button('전체 데이터 보기'):
        df3
    st.write('#### ✔ 컬럼')
    st.text('''
    - total_bill : 식사 후 총 금액 (수치형)
    - tip : tip으로 낸 금액 (수치형)
    - sex : 성별 (범주형)
    - smoker : 흡연 여부 (범주형)
    - day : 방문 요일 (범주형)
    - time : 방문 시간 (범주형)
    - size : 일행수 (수치형)
    ''')
    st.write('#### ✔ 요약 통계량')
    st.text('수치형 변수인 total_bill, tip, size의 요약 통계량 계산')
    st.write(df3.describe())
    st.write('#### ✔ 결측치 확인')
    st.write(pd.DataFrame(df3.isna().sum(), columns = ['number of NA']))
    st.text('→ 결측치 X')

elif name == 'Data Visualization':
    st.write('#### ✔ 수치형 변수 상관관계')
    image = Image.open('heatmap.png')
    st.image(image, caption='heatmap of numeric variable')
    st.text('tip과 total_bill은 양의 상관관계를 지니고 있다.')

    st.write('#### ✔ Histogram of total_bill')
    fig = px.histogram(df3, x='total_bill', nbins=10, color_discrete_sequence = ['lightsalmon'])
    st.plotly_chart(fig, use_container_width=True)

    st.write('#### ❓ 성별과 흡연여부는 total_bill에 어떤 영향을 줄까❓')
    st.text('그래프로 확인해보자!')
    option = st.selectbox('graph를 선택해주세요!',
                       ('histogram', 'bar plot', 'box plot', 'violin plot'))
    if option == 'histogram':
        col1, col2 = st.columns(2)
        with col1:
            fig = px.histogram(df3, x = 'total_bill', title = 'Total Bill(by sex)', nbins = 20,
                  histnorm = 'probability density',
                  labels = {'total_bill' : 'Total Bill'}, opacity = 0.7,
                  color = 'sex', color_discrete_sequence = ['magenta', 'deepskyblue'])
            st.plotly_chart(fig, use_container_width=True)
        with col2:    
            fig = px.histogram(df3, x = 'total_bill', title = 'Total Bill(by smoker)', nbins = 20,
                  histnorm = 'probability density',
                  labels = {'total_bill' : 'Total Bill'}, opacity = 0.7, 
                  color = 'smoker', color_discrete_sequence = ['magenta', 'deepskyblue'])
            st.plotly_chart(fig, use_container_width=True)

    elif option == 'bar plot':
        col1, col2 = st.columns(2)
        with col1:
            fig = px.bar(df3.groupby(['sex'])[['total_bill']].mean().reset_index(),
             x='sex', y='total_bill', height=400, 
             title='Average Bills by sex', 
             color_discrete_sequence=['palevioletred'],
             barmode='group')  # 양 옆으로 놓이는 구조  # barmode='stack'라고 하면 누적 (dafault setting)
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = px.bar(df3.groupby(['smoker'])[['total_bill']].mean().reset_index(),
             x='smoker', y='total_bill', height=400, 
             title='Average Bills by smoker', 
             color_discrete_sequence=['lightsalmon'],
             barmode='group')  # 양 옆으로 놓이는 구조  # barmode='stack'라고 하면 누적 (dafault setting)
            st.plotly_chart(fig, use_container_width=True)

    elif option == 'violin plot':
        col1, col2 = st.columns(2)
        with col1:
            fig = px.violin(df3, x = 'sex', y='total_bill', color='sex',title = 'Violin plot (sex)', box=True, points='all',
             color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = px.violin(df3, x = 'smoker', y='total_bill', color='smoker',title = 'Violin plot (smoker)',  box=True, points='all',
             color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig, use_container_width=True)
        st.text('''
        - 남성의 total_bill은 여성보다 편차가 더 크다.
        - 흡연자의 total_bill이 비흡연자보다 편차가 크다.
        ''')
        fig = px.violin(df3, x = 'sex', y='total_bill', color='smoker', box=True, title = 'Violin plot (sex & smoker)', points='all',
             color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig, use_container_width=True)
        st.text('''
        - 여성은 smoke 여부와 상관없이 비슷한(?) total_bill을 지불
        - 남성은 흡연자들이 비흡연자들보다 더 많은 total_bill을 지불
        ''')


    elif option == 'box plot':
        col1, col2 = st.columns(2)
        with col1:
            fig = px.box(df3, x='sex', y='total_bill', color = 'sex', points='all',title = 'Box plot (sex)',
         color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = px.box(df3, x='smoker', y='total_bill', color = 'smoker', points='all',title = 'Box plot (smoker)',
         color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig, use_container_width=True)   
        fig = px.box(df3, x='sex', y='total_bill', color='smoker', points='all',title = 'Box plot (sex & smoker)',
         color_discrete_sequence=px.colors.qualitative.Pastel)   
        st.plotly_chart(fig, use_container_width=True)

    st.write('#### + Sunburst chart')
    fig = px.sunburst(df3, path = ['day', 'time', 'sex'], values = 'total_bill')
    st.plotly_chart(fig, use_container_width=True)
