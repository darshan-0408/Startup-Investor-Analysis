import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


st.set_page_config(layout='wide', page_title='Startup Analysis')
df = pd.read_csv("datasets/startup_cleaned.csv")
df['date'] = pd.to_datetime(df['date'], errors='coerce')

st.sidebar.title("Startup Funding Analysis")

def load_investor_details(investor):
    st.title(investor)

    # load the recent five investments of the investor
    last_five_df = df[df['investors'].str.contains(investor)].head()[['date', 'startup', 'vertical', 'city', 'round', 'amount']]
    if last_five_df.head()['amount'].sum() != 0:
        st.subheader('Most Recent Investments')
        st.dataframe(last_five_df)
        col1, col2 = st.columns(2)
        # biggest investment by the investor
        with col1:
            biggest_investment = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()

            st.subheader('Biggest Investments')
            
            fig, ax = plt.subplots()
            ax.bar(biggest_investment.index, biggest_investment.values)
            st.pyplot(fig)
        
        with col2:
                sectors = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()
                st.subheader("Sectors Invested In:")
                fig1, ax1 = plt.subplots()
                ax1.pie(sectors, labels=sectors.index, autopct='%0.01f%%')
                st.pyplot(fig1)
    else:
        st.subheader("This investor has not invested!!")
        st.image("images/startup.png")


            

selected_investor = st.sidebar.selectbox('Select Investor',sorted(list(set(df['investors'].str.split(',').sum()))))
btn2 = st.sidebar.button('Find Investor Details')

if btn2:
    load_investor_details(selected_investor)