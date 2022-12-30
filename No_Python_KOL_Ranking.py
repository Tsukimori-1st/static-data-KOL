from random import random
import streamlit as st
from selenium import webdriver
from time import sleep, time
import pandas as pd
from PIL import Image
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import sys
from streamlit.web import cli as stcli

# Hàm crawl data
tech = ['Vật Vờ Studio',
        'Duy Thẩm',
        'Tony Phùng Studio',
        'Tân Một Cú',
        'AnhEm TV',
        'Vinh Xô',
        'Tinh Tế',
        'Relab',
        'Khôi Ngọng',
        'Duy Luân Dễ Thương',
        'Công Nghệ Lõi',
        'MobileCity',
        'Tuấn Ngọc đây!',
        'Lee Tùn Zân - Review Và Tặng Lại',
        'ĐAM MÊ CÔNG NGHỆ']

beauty = ['Ha Linh official',
          'Chloe Nguyen',
          'Changmakeup',
          'Góc của Rư',
          'Mai Vân Trang',
          'Call me Duy',
          'Luna Đào Official',
          'Nguyen Thuc Thuy Tien',
          'An Phương',
          'Q U I N',
          '✨ Gau Zoan ✨',
          'Rosie Pham',
          'Blingbabi',
          '1m88']

food = ['Ông Anh thích nấu ăn',
        'Bếp Trưởng Review',
        'Ninh Tito',
        'Khoai lang thang',
        'Cô Ba Bình Dương',
        'Sapa TV',
        'Dũng béo ẩm thực phố phường',
        'VNT Food & Travel',
        'ĐI ĐÂU ĂN GÌ ?',
        'Ẩm thực mẹ làm',
        'Hanoi food',
        'Max McFarlin',
        'Thằng Mập Food',
        'Hôm nay ăn gì?',
        'Ok Con Dê']


# def main(lst):
#     df = pd.DataFrame(columns=['Channel', 'Subscribers', 'Subscribers for the last 30 days', '% change',
#                                'Video views for the last 30 days', '% change'])
#     browser = webdriver.Edge(executable_path="msedgedriver.exe")
#     browser.get("https://socialblade.com/")
#     sleep(0.1)
#
#     for i in range(len(lst)):
#         search = browser.find_element(By.ID, 'SearchInput')
#         sleep(0)
#         search.send_keys(lst[i])
#         search.send_keys(Keys.ENTER)
#
#         subscriber = browser.find_element(By.XPATH, "/html/body/div[12]/div/div[3]/div[3]/span[2]")
#         # /html/body/div[12]/div/div[3]/div[3]/span[3] - beauty
#         # /html/body/div[11]/div/div[3]/div[3]/span[2]
#         sleep(0)
#
#         subscriber30 = browser.find_element(By.XPATH, "/html/body/div[17]/div[1]/div[1]/div[3]/div[1]/p[1]")
#         s30 = subscriber30.text.split(' ', -1)
#         s30num = s30[0]
#         if s30num == '--':
#             s30num = None
#             s30per = None
#         else:
#             s30p = s30[1]
#             strn = browser.find_element(By.XPATH, '/html/body/div[17]/div[1]/div[1]/div[3]/div[1]/p[1]/sup/span/i')
#             strn = strn.get_attribute('class')
#             if strn == 'fa fa-caret-down':
#                 st = '-'
#             else:
#                 st = '+'
#             s30per = st + s30p
#         sleep(0)
#
#         vids30 = browser.find_element(By.XPATH, "/html/body/div[17]/div[1]/div[1]/div[3]/div[3]/p[1]")
#         v30 = vids30.text.split(' ', -1)
#         v30num = v30[0]
#         if v30num == '--':
#             v30num = None
#             v30p = None
#             vt = None
#         else:
#             v30p = v30[1]
#             vtrn = browser.find_element(By.XPATH, '/html/body/div[17]/div[1]/div[1]/div[3]/div[3]/p[1]/sup/span/i')
#             vtrn = vtrn.get_attribute('class')
#             if vtrn == 'fa fa-caret-down':
#                 vt = '-'
#             else:
#                 vt = '+'
#             v30per = vt + v30p
#         sleep(0)
#
#         df.loc[len(df)] = [lst[i], subscriber.text, s30num, s30per, v30num, v30per]
#
#     browser.close()
#     return df


# Cho user lựa chọn lĩnh vực/ Cho user thêm người họ muốn tìm kiếm
def selectField(choice):
    if choice == "Technology":
        df = pd.read_csv('Tech1.csv')
    elif choice == "Cosmetics":
        df = pd.read_csv('Cosmetics1.csv')
    elif choice == "F&B":
        df = pd.read_csv('Food1.csv')
    else:
        print("Wrong choice")
    return df


def mergeTable(choice, df):
    if choice == "Technology":
        dfRep = pd.read_csv('Tech_reputation CSV.csv')
    elif choice == "Cosmetics":
        dfRep = pd.read_csv('Cosmetics_reputation CSV.csv')
    elif choice == "F&B":
        dfRep = pd.read_csv('F&B_reputation CSV.csv')

    dfRep = dfRep.drop(['Unnamed: 0'], axis=1)

    dfMerge = pd.merge(df, dfRep, on="Channel")
    dfMerge = dfMerge.drop(['Positive count', 'Neutral count', 'Negative count'], axis=1)
    return dfMerge


# Dọn dẹp dữ liệu crawl về/ Chuyển từ kiểu string về float
def convert_to_numberString(dfMerge):
    dfMerge['Subscribers'] = dfMerge['Subscribers'].str.replace('K', '000')
    dfMerge['Subscribers'] = dfMerge['Subscribers'].str.replace('M', '0000')
    dfMerge['Subscribers'] = dfMerge['Subscribers'].str.replace('.', '')

    dfMerge['Subscribers for the last 30 days'] = dfMerge['Subscribers for the last 30 days'].str.replace('K', '000')
    dfMerge['Subscribers for the last 30 days'] = dfMerge['Subscribers for the last 30 days'].str.replace('M', '0000')
    dfMerge['Subscribers for the last 30 days'] = dfMerge['Subscribers for the last 30 days'].str.replace('.', '')
    dfMerge['Subscribers for the last 30 days'] = dfMerge['Subscribers for the last 30 days'].str.replace(',', '')

    dfMerge['Video views for the last 30 days'] = dfMerge['Video views for the last 30 days'].str.replace('K', '')
    dfMerge['Video views for the last 30 days'] = dfMerge['Video views for the last 30 days'].str.replace('M', '000')
    dfMerge['Video views for the last 30 days'] = dfMerge['Video views for the last 30 days'].str.replace('.', '')
    dfMerge['Video views for the last 30 days'] = dfMerge['Video views for the last 30 days'].str.replace(',', '')

    # Change "%change" into number
    dfMerge['% change'] = dfMerge['% change'].str.replace('%', '')
    dfMerge['% change'] = dfMerge['% change'].str.replace(',', '')
    dfMerge['% change.1'] = dfMerge['% change.1'].str.replace('%', '')
    dfMerge['% change.1'] = dfMerge['% change.1'].str.replace(',', '')
    dfMerge["% change"] = pd.to_numeric(dfMerge["% change"])
    dfMerge["% change.1"] = pd.to_numeric(dfMerge["% change.1"])

    # Change type to float
    dfMerge["Subscribers"] = pd.to_numeric(dfMerge["Subscribers"], downcast="float")
    dfMerge['Subscribers for the last 30 days'] = dfMerge['Subscribers for the last 30 days'].astype(float)
    dfMerge['Video views for the last 30 days'] = dfMerge['Video views for the last 30 days'].astype(float)

# Hàm này tạo ra các class để phân chia chấm điểm theo dạng Histogram
def histo_maker(series, maxOf):
    class_width = round((series.values[7] - series.values[3]) / 5)
    class_width2 = class_width * 2
    class_width3 = class_width * 3
    class_width4 = class_width * 4
    return class_width, class_width2, class_width3, class_width4, maxOf

# Chia đc vào các class rồi thì hàm này giúp chấm điểm
def converFunc(series, maxOf, class_width, class_width2, class_width3, class_width4):
    for i in range(len(series)):
        if series.values[i] < class_width:
            series.values[i] = 2.0
        elif series.values[i] >= class_width and series.values[i] < class_width2:
            series.values[i] = 2.5
        elif series.values[i] >= class_width2 and series.values[i] < class_width3:
            series.values[i] = 3.0
        elif series.values[i] >= class_width3 and series.values[i] < class_width4:
            series.values[i] = 3.6
        elif series.values[i] >= class_width4 and series.values[i] <= maxOf:
            series.values[i] = 4.0


# Cho user nhập trọng số và tính toán
def calculateTotal(reach, trending, reputation, dfMerge, lstTotal):
    for i in range(len(dfMerge["Channel"])):
        rowScore = reach * dfMerge["Subscribers"].values[i] + trending * (
                    dfMerge["Subscribers for the last 30 days"].values[i] +
                    dfMerge["Video views for the last 30 days"].values[i]) + reputation * (
                   dfMerge["Sentiment"].values[i])
        lstTotal.append(rowScore)


# Chi gợi ý việc reindex cái dataframe

def trueMain(choice, reachFloat, trendingFloat, reputationFloat):
    choice = choice
    reachFloat = reachFloat
    trendingFloat = trendingFloat
    reputationFloat = reputationFloat

    lstTotal = []

    df = selectField(choice)
    dfMerge = mergeTable(choice, df)
    # convert_to_numberString(dfMerge)
    dfMerge = dfMerge.fillna(dfMerge.mean())

    des_table = dfMerge.describe()
    maxSub = des_table["Subscribers"].values[7]
    maxSub30 = des_table["Subscribers for the last 30 days"].values[7]
    maxView30 = des_table["Video views for the last 30 days"].values[7]
    maxRepu = des_table["Sentiment"].values[7]

    class_width, class_width2, class_width3, class_width4, maxOf = histo_maker(des_table["Subscribers"], maxSub)
    converFunc(dfMerge['Subscribers'], maxOf, class_width, class_width2, class_width3, class_width4)
    class_width, class_width2, class_width3, class_width4, maxOf = histo_maker(
        des_table["Subscribers for the last 30 days"], maxSub30)
    converFunc(dfMerge['Subscribers for the last 30 days'], maxOf, class_width, class_width2, class_width3,
               class_width4)
    class_width, class_width2, class_width3, class_width4, maxOf = histo_maker(
        des_table["Video views for the last 30 days"], maxView30)
    converFunc(dfMerge['Video views for the last 30 days'], maxOf, class_width, class_width2, class_width3,
               class_width4)
    class_width, class_width2, class_width3, class_width4, maxOf = histo_maker(des_table["Sentiment"], maxRepu)
    converFunc(dfMerge['Sentiment'], maxOf, class_width, class_width2, class_width3, class_width4)

    calculateTotal(reachFloat, trendingFloat, reputationFloat, dfMerge, lstTotal)
    dfMerge['Total Score'] = lstTotal
    dfMerge = dfMerge.drop(['Unnamed: 0'], axis=1)
    dfMerge.reindex()
    dfMerge = dfMerge.sort_values(by=['Total Score', '% change.1', '% change'], ascending=False)
    print(dfMerge)
    # dfMerge.to_csv('FINAL.csv')
    st.balloons()
    st.table(dfMerge)


# Streamlit stuff
st.set_page_config(page_title="Ranking KOL",
                   page_icon=":earth_asia:",
                   # layout="wide"
)

image = Image.open('KOL Banner.jpg')
st.image(image, use_column_width=True)

st.title("KOL Ranking Application")
st.subheader("Warmest welcome to Mr. Hieu and the Ciaolink team")
st.markdown("*Guidance*")
st.markdown("""
Step 1: Select your Area of Interest.\n \n
Step 2: Input your desired paramenter via the slider\n \n
Step 3: Click the "Show Results" button to get the ranking of KOL 
""")
data = pd.read_csv("ChoiceEx.csv")
data = data.drop(['Unnamed: 0'], axis=1)

if st.checkbox('Show sample of raw data crawled'):
    data

st.subheader("More information about KOL")
st.write("https://public.tableau.com/views/Visualization_16723938354020/Dashboard1?:language=en-US&publish=yes&:display_count=n&:origin=viz_share_link")

genre = st.radio(
    "What\'s your area of interest",
    ('Technology', 'Cosmetics', 'F&B'))

reachFloat = st.slider('Enter the importance of Reachability', 0.0, 1.0, 0.01)
trendingFloat = st.slider('Enter the importance of Trending', 0.0, 1.0, 0.01)
reputationFloat = st.slider('Enter the importance of Reputation', 0.0, 1.0, 0.01)

if st.button('Show results'):
    trueMain(genre, reachFloat, trendingFloat, reputationFloat)

