import streamlit as st
import pandas as pd
import SessionState

def load_data():
    df = pd.read_csv('googleplaystore.csv')
    GameGroup=df.groupby(['Category']).get_group('GAME')
    EDUCATIONGroup=df.groupby(['Category']).get_group('EDUCATION')
    ENTERTAINMENTGroup=df.groupby(['Category']).get_group('ENTERTAINMENT')
    NewDf=pd.concat([GameGroup,EDUCATIONGroup,ENTERTAINMENTGroup])
    NewDf=NewDf.fillna(0)
    NewDf.reset_index(inplace=True)
    NewDf = NewDf.drop(columns=['index'])
    return NewDf

def calculate(NewDf,user_list):
    rate=[]
    for i in NewDf.Rating :
        rate.append(int(i))
    NewDf.Rating=rate

    dummies=pd.get_dummies(NewDf,columns=['Category', 'Genres','Type','Content Rating','Rating'], drop_first=True)
    dummies.drop(columns=['App','Installs'],inplace=True)
    df = pd.concat([NewDf, dummies], axis=1)
    df=df.fillna(0)
    
    df.drop(columns=['Category', 'Genres','Type','Content Rating','Rating','Reviews','Size','Price','Last Updated','Current Ver','Android Ver'],
    inplace=True)
    df = df.drop_duplicates()
    df.reset_index(inplace=True)
    df_name = pd.DataFrame(columns=['App','index'])
    df_name['App'] = df['App']
    df_name['index'] = df['index']

    dfcopy=df.copy()

    userdf=pd.DataFrame()
    appid = []
    rate = []
    #print(df_name)
    for i in user_list:
        temp =df_name.loc[df_name.App == i['name'],['index']]
        appid.append(temp.values[0])
    for i in user_list:
        rate.append(i['score'])
    
    userdf['appid']=appid
    userdf['rating']=rate

    profile1=dfcopy[dfcopy['index'].isin(userdf['appid'])]
    profile1.drop(['index','App','Installs'],1,inplace=True)
    profile1 = profile1.reset_index(drop=True)

    rating=userdf['rating'].values
    rating1=profile1.transpose().dot(rating)
    table=dfcopy.set_index('index')
    name = [{index :row['App']} for index,row in table.iterrows()]

    table.drop(['App','Installs'],1,inplace=True)
    recommendationTable1 = ((table*rating1).sum(axis=1))/(rating1.sum())
    recommendationTable1=recommendationTable1.sort_values(ascending=False)

    res = pd.DataFrame(columns=['Id','Name','Score'])
    res ['Id'] = recommendationTable1.index
    res['Score'] = recommendationTable1.values
    for row in name:
        for key,value in row.items():
            print(row)
            res.loc[key,'Name'] = value

    res.dropna(inplace=True)
    #res['Name'] = name.values
    return res

def main():
    
    st.title('Item base Recommended System')
    
    df = load_data()
    #st.write(df)

    st.sidebar.title('User info')
    option = st.sidebar.selectbox(
    'Which App do you like best?',
     df['App'])

    name = st.sidebar.text_input(label='You Selected:',value=option)
    score = st.sidebar.number_input('Add score:',step=1.0,min_value=0.0,max_value=5.0)
    
    ss = SessionState.get(user_list=[])
    
    st.subheader('User Profile:')
    if st.sidebar.button('Add'):
        ss.user_list.append({'name':name ,'score': int(score)})

    user_df = pd.DataFrame.from_dict(ss.user_list,orient='columns')
    dd = st.write(user_df)

    if st.sidebar.button('Show Recommend'):
        st.subheader('Recommendation:')
        res = calculate(df,ss.user_list)
        st.write(res)

    

if __name__ == '__main__':
    main()