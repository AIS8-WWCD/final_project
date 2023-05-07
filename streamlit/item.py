import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mtick
import streamlit as st
import koreanize_matplotlib

# 데이터 불러오기
# a = pd.read_csv('streamlit\heal_boost_data.csv')
# b = pd.read_csv('streamlit\heal.csv')
# c = pd.read_csv('streamlit\Throwable_data.csv')
DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
              'streamlit-demo-data/uber-raw-data-sep14.csv.gz')
	
@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
# match_id 컬럼 제거
a = a.drop("match_id", axis=1)
b = b.drop("match_id", axis=1)
c = c.drop("match_id", axis=1)

# 컬럼명 변경
a = a.rename(columns={"Item_Heal_MedKit": "의료용 키트",
                      "Item_Heal_FirstAid_C": "구급 상자",
                      "Item_Heal_Bandage_C": "붕대",
                      "Item_Boost_AdrenalineSyringe_C": "아드레날린 주사기",
                      "Item_Boost_PainKiller_C": "진통제",
                      "Item_Boost_EnergyDrink_C": "에너지 드링크",
                      "Item_Weapon_Molotov_C": "화염병",
                      "Item_Weapon_SmokeBomb_C": "연막탄",
                      "Item_Weapon_FlashBang_C": "섬광탄",
                      "Item_Weapon_Grenade_C": "수류탄"})
b = b.rename(columns={"Item_Heal_MedKit": "의료용 키트",
                      "Item_Heal_FirstAid_C": "구급 상자",
                      "Item_Heal_Bandage_C": "붕대",
                      "Item_Boost_AdrenalineSyringe_C": "아드레날린 주사기",
                      "Item_Boost_PainKiller_C": "진통제",
                      "Item_Boost_EnergyDrink_C": "에너지 드링크"})
c = c.rename(columns={"Item_Weapon_Molotov_C": "화염병",
                      "Item_Weapon_SmokeBomb_C": "연막탄",
                      "Item_Weapon_FlashBang_C": "섬광탄",
                      "Item_Weapon_Grenade_C": "수류탄"})

# 복사본 생성
aa = a.copy()
bb = b.copy()
cc = c.copy()

# 아이템 사용 횟수 합계 계산
a = a.sum()
b = b.sum()
c = c.sum()

# 계산된 값으로 데이터프레임 생성
a = pd.DataFrame(a).reset_index()
b = pd.DataFrame(b).reset_index()
c = pd.DataFrame(c).reset_index()

# 컬럼명 변경
a = a.rename(columns={0: "get_item"})
b = b.rename(columns={0: "use_heal"})
c = c.rename(columns={0: "use_throw"})

# 인덱스 수정
ab = a.iloc[1:7]
ac = a.iloc[7:]
b = b.iloc[1:]
c = c.iloc[1:]

# 병합
ab = pd.merge(ab, b, on='index', how='outer')
ac = pd.merge(ac, c, on='index', how='outer')

# 회복 아이템과 투척 무기의 사용률 계산하기
ab = ab.rename(columns={"index": "heal"})
ac = ac.rename(columns={"index": "throw"})

ab["use_rate"] = ab["use_heal"]/ab["get_item"] * 100
ac["use_rate"] = ac["use_throw"]/ac["get_item"] * 100

ab['use_rate'] = ab['use_rate'].astype(float)
ac['use_rate'] = ac['use_rate'].astype(float)

ab['use_rate'] = ab['use_rate'].round(1)
ac['use_rate'] = ac['use_rate'].round(1)

ab = ab.rename(columns={'heal': "회복아이템", 'get_item': "얻은 아이템",
                        'use_heal': "사용한 회복템", 'use_rate': "아이템 사용률"})
ac = ac.rename(columns={'throw': "투척 무기", 'get_item': "얻은 아이템",
                        'use_throw': "사용한 투척 무기", 'use_rate': "아이템 사용률"})

choice_1 = st.selectbox("보고 싶은 그래프", ('총 얻은 회복템', '총 얻은 투척 무기'))
def plot_items_stats():
    if choice_1 == '총 얻은 회복템':
        # 그래프 그리기
        st.dataframe(ab, use_container_width=True)
        fig1 = plt.figure(figsize=(15, 10))
        sns.barplot(data=ab.sort_values("얻은 아이템", ascending=False), x="회복아이템", y="얻은 아이템", palette='YlOrBr')
        st.pyplot(fig1)

        fig2 = plt.figure(figsize=(15, 5))
        sns.barplot(data=ab.sort_values("사용한 회복템", ascending=False), x="회복아이템", y="사용한 회복템", palette='YlOrBr')
        st.pyplot(fig2)

        fig3 = plt.figure(figsize=(15, 5))
        r = sns.barplot(data=ab.sort_values("아이템 사용률", ascending=False), x="회복아이템", y="아이템 사용률", palette='YlOrBr')
        r.yaxis.set_major_formatter(mtick.PercentFormatter())
        st.pyplot(fig3)
    else:
        st.dataframe(ac, use_container_width=True)
        fig4 = plt.figure(figsize=(15, 10))
        sns.barplot(data=ac.sort_values("얻은 아이템", ascending=False), x="투척 무기", y="얻은 아이템", palette='YlOrBr')
        st.pyplot(fig4)

        fig5 = plt.figure(figsize=(15, 5))
        sns.barplot(data=ac.sort_values("사용한 투척 무기", ascending=False), x="투척 무기", y="사용한 투척 무기", palette='YlOrBr')
        st.pyplot(fig5)

        fig6 = plt.figure(figsize=(15, 5))
        r = sns.barplot(data=ac.sort_values("아이템 사용률", ascending=False), x="투척 무기", y="아이템 사용률", palette='YlOrBr')
        r.yaxis.set_major_formatter(mtick.PercentFormatter())
        st.pyplot(fig6)


plot_items_stats()
    
# 데이터프레임 생성 및 전처리
aa[['team','column_name_1']] = aa['character_name'].str.split('_', expand=True)
aa = aa.drop(['column_name_1'], axis=1)
aa = aa.groupby('team').sum()
aa = aa.T
aa = aa.reset_index()
bb[['team','column_name_1']] = bb['character_name'].str.split('_', expand=True)
bb = bb.drop(['column_name_1'], axis=1)
bb = bb.groupby('team').sum()
bb = bb.T
bb = bb.reset_index()
cc[['team','column_name_1']] = cc['attacker_name'].str.split('_', expand=True)
cc = cc.drop(['column_name_1'], axis=1)
cc = cc.groupby('team').sum()
cc = cc.T
cc = cc.reset_index()
aab = aa.iloc[:6]
aac = aa.iloc[6:]
aab = aab.rename(columns={'index': '회복템'})
aac = aac.rename(columns={'index': '투척 무기'})
bb = bb.rename(columns={'index': '사용한 회복템'})
cc = cc.rename(columns={'index': '사용한 투척 무기'})
aac = aac.reset_index(drop=True)
e = pd.concat([aab.iloc[:,:1],bb/aab * 100], axis=1).iloc[:,:-2]
f = pd.concat([aac.iloc[:,:1],cc/aac * 100], axis=1).iloc[:,:-2]
e = e.rename(columns = {"회복템" : "회복템 사용률"})
f = f.rename(columns = {"투척 무기" : "투척 무기 사용률"})

# 팀 선택
team_name = st.selectbox("팀 선택", ('17', '4AM', 'ACE', 'CES', 'DAY', 'DNW', 'EXO', 'FaZe',
        'GBL', 'GEN', 'GEX', 'HOWL', 'III', 'LG', 'NAVI', 'NH', 'PLM', 'PTG',
        'PeRo', 'SQ', 'SST', 'STK', 'TWIS', 'Tian'))

choice = st.selectbox("보고 싶은 그래프", ('총 얻은 아이템', '총 사용한 아이템', '아이템 사용률'))

A = aab.sort_values(team_name, ascending=False)
B = aac.sort_values(team_name, ascending=False)
C = bb.sort_values(team_name, ascending=False)
D = cc.sort_values(team_name, ascending=False)
E = e.sort_values(team_name, ascending=False)
F = f.sort_values(team_name, ascending=False)
AA = A[["회복템",team_name]]
BB = B[["투척 무기",team_name]]
CC = C[["사용한 회복템",team_name]]
DD = D[["사용한 투척 무기",team_name]]
EE = E[["회복템 사용률",team_name]]
FF = F[["투척 무기 사용률",team_name]]
def plot_item():
    if choice =='총 얻은 아이템':
    # 각 차트를 시각화하고 웹 앱으로 만들기

        st.dataframe(AA, use_container_width=True)
        fig, ax = plt.subplots()
        sns.barplot(data=A, x=team_name, y='회복템', palette='YlOrBr', ax=ax)
        st.pyplot(fig)
        
        st.dataframe(BB, use_container_width=True)
        fig, ax = plt.subplots()
        sns.barplot(data=B, x=team_name, y='투척 무기', palette='YlOrBr', ax=ax)
        st.pyplot(fig)
    elif choice == '총 사용한 아이템':
        st.dataframe(CC, use_container_width=True)
        fig, ax = plt.subplots()
        sns.barplot(data=C, x=team_name, y='사용한 회복템', palette='YlOrBr', ax=ax)
        st.pyplot(fig)

        st.dataframe(DD, use_container_width=True)
        fig, ax = plt.subplots()
        sns.barplot(data=D, x=team_name, y='사용한 투척 무기', palette='YlOrBr', ax=ax)
        st.pyplot(fig)
    else:
        st.dataframe(EE, use_container_width=True)
        fig, ax = plt.subplots()
        sns.barplot(data=E, x=team_name, y='회복템 사용률', palette='YlOrBr', ax=ax)
        st.pyplot(fig)

        st.dataframe(FF, use_container_width=True)
        fig, ax = plt.subplots()
        sns.barplot(data=F, x=team_name, y='투척 무기 사용률', palette='YlOrBr', ax=ax)
        st.pyplot(fig)
plot_item()
