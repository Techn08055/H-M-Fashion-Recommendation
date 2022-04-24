import streamlit as st
import pandas as pd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
from datetime import datetime 
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from wordcloud import WordCloud

def Plot(load,column):
    st.subheader('Distribution Of \''+  column  + '\' from ' + load + ' data.' )
    fig = plt.figure(figsize=(16,6))
    if load == "Article":
        data[load][column].value_counts(sort=True)[:50].plot.bar(rot=0)
    else:    
        plt.hist(data[load][column],bins=70,edgecolor='white')
    plt.xticks(rotation=90)
    st.pyplot(fig)   

def violinPlot(load,column):
    st.subheader('Distribution Of \''+  column  + '\' from ' + load + ' data.' )
    fig = plt.figure(figsize=(16,6))
    sns.violinplot(x=data[load][column])
    st.pyplot(fig)   
st.title('H&M Recommendations')

@st.cache
def load_data(nrows,DATA_URL):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    return data    

# Loading Dataset 
data_load_state = st.text('Loading Data...')
articles = load_data(10000,'articles.csv')
customer = load_data(10000,'customers.csv')
transaction = load_data(10000,'transactions_train.csv')

#Making Copy Of Datasets
articles_df = articles.copy()
customer_df = customer.copy()
transaction_df = transaction.copy()

data_load_state.text('Completed Loading Article Data!')
data={"Article":articles_df, "Customer":customer_df,"Transaction":transaction_df }
load = st.selectbox("Which DataFrame You Want To Check? ", ["Article","Customer","Transaction"])
st.subheader(load)
st.write(data[load])

#Removing Null Values & Preprocessing
customer_df['club_member_status'] = customer_df['club_member_status'].replace(np.nan, 'None')
customer_df['fashion_news_frequency'] = customer_df['fashion_news_frequency'].replace(np.nan, 'NONE')
articles_df['detail_desc']=articles_df['detail_desc'].fillna("Cannot Find Description")
stop_words = stopwords.words('english')
articles_df['detail_desc'] = articles_df['detail_desc'].apply(lambda x: ' '.join([word for word in x.split() if word not in (stop_words)]))
for i in articles_df['detail_desc']:
  ajj = []
  for x in i.split():
   ajj.append(''.join(SnowballStemmer("english").stem(x)))
  i=' '.join(ajj)

# Lo0ading Observation & SUmmary
if load == "Customer":
    Plot(load,'age')
    Plot(load,'club_member_status')
    Plot(load,'fashion_news_frequency')

if load == "Article":
    Plot(load,'product_type_name')
    Plot(load,'product_group_name')
    Plot(load,'index_name')
    Plot(load,'garment_group_name')
    Plot(load,'index_group_name')
    Plot(load,'section_name')
    Plot(load,'prod_name')
    Plot(load,'graphical_appearance_name')
    Plot(load,'colour_group_name')
    Plot(load,'perceived_colour_value_name')
    Plot(load,'perceived_colour_master_name')
    Plot(load,'department_name')
    
    st.subheader('Distribution Of index_name & index_group_name' )
    fig = plt.figure(figsize=(16,6))
    plt.xticks(rotation=90)
    sns.histplot(data=articles_df, y="index_group_name", hue="index_name", multiple="stack" )
    st.pyplot(fig) 

    st.subheader('Distribution Of Words in detail_desc of Article' )
    text1 = " ".join(title for title in articles_df.detail_desc)
    word_cloud1 = WordCloud(collocations = False, background_color = 'white',
                        width = 2048, height = 1080).generate(text1)

    plt.imshow(word_cloud1, interpolation='bilinear')
    plt.axis("off")
    plt.show()  
    st.pyplot(fig)

if load == "Transaction":
    violinPlot(load,'price')
    