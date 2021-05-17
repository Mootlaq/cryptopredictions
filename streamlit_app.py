import streamlit as st
import pandas as pd
import numpy as np
import requests
from pycoingecko import CoinGeckoAPI
import datetime
import time
import altair as alt
from altair.expr import datum, if_
from datetime import date

cg = CoinGeckoAPI()
df = pd.read_csv('marketcaptable.csv', index_col='symbol')


@st.cache
def mc_projection(df, coin, projected_price):
    # btc_market_cap = df.at['btc', 'market_cap']
    eth_market_cap = df.at['eth', 'market_cap']
    old_market_cap = df.at[coin, 'market_cap']
    mc_at_projected = projected_price*df.at[coin, 'circulating_supply']
    
    coins = ['eth', '{} projected marketcap'.format(coin), '{} actual marketcap'.format(coin)]
    marketcaps = [eth_market_cap, mc_at_projected, old_market_cap]

    new_df = pd.DataFrame({'name': coins, 'market_cap': marketcaps})
    new_df['market_cap_formatted'] = round(new_df['market_cap']/1000000000,2)
    
    return eth_market_cap, mc_at_projected, new_df

st.title('Is It a realistic Price? 🚀')
st.markdown('''

As is the case in every bull market, people are throwing their wishful thinking and call it price predictions. As a result, 
new investors are taking these predictions as if they were destined. This tool helps you check if this price prediction is realistic 
for this market cycle or not. The metric I'm using is simple and easy: **If your price prediction makes that altcoin's market cap equal to
or higher than Ethereum's market cap, then it's not realistic.** This tool isn't going to give you a price prediction but it will probably help you write
off the wrong ones so that you don't invest your life savings in it.

**The way the tool works is simple:** Choose a coin and a projected price using the dropdown menus below and the chart will be updated. 
The chart shows Ethereum's market cap, The chosen coin's actual market cap and projected market cap. 


''')



coins_list = list(df.index.str.upper())

st.header('Choose a coin and a projected price:')
col1, col2 = st.beta_columns(2)
with col1:
    selected_coin = st.selectbox('Choose a coin:', coins_list, 5)

with col2:
    projected_price = st.number_input('The Projected Price', min_value=1, max_value=1000000, value=10, step=1)
    


_,_, finaldf = mc_projection(df, selected_coin.lower(), projected_price)
#st.write(finaldf)

# testdf2 = testdf.drop([0], axis=0)
# testdf2

marketChart = alt.Chart(finaldf, title= 'Market Cap Comparison').mark_bar(color='#E85450').encode(
    alt.Y('name', sort=['eth', '{} projected marketcap'.format(selected_coin.lower()), '{} actual marketcap'.format(selected_coin.lower())], title='Currency'),
    alt.X('market_cap_formatted:Q', title='Market Cap (Bn)')).properties()


text = marketChart.mark_text(color='white', xOffset=-19).encode(
    text='market_cap_formatted:Q',

)

st.header("The Chart")

final_chart = (marketChart + text).configure_axis(
    labelFontSize=11,
    titleFontSize=11
)
st.altair_chart(final_chart, use_container_width=True)



with st.beta_expander('One more thing'):
    st.info('''
    Don't believe anyone who tells you coin X will reach an astronomic price. A lot of factors need to be considered when making such claims.
    The first one is market cap and how it relates to the price so this is what you need to pay attention to whenever you see a price prediction.
    Again, this is not your best tool to 'make' price predictions. But I believe it's a good tool to reject the unrealistic ones. Happy trading!
    ''')




#############################################


with st.beta_expander("About this website"):
    st.markdown('''
                If you have any feedback, I would love to know! you can contact me on [Telegram](https://t.me/motlaaq) or [Twitter](https://twitter.com/CryptoCamel2).
                If you like what you see, you can always [buy me a coffee](https://www.buymeacoffee.com/Motlaq)! ''')
                                 
