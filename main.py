import streamlit as st
import math
import numpy as np
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from arch import arch_model
from datetime import datetime
from black_scholes_model import BlackScholesModel



st.set_page_config(
    page_title="Black-Scholes Option Pricer and Implied Volatility Calculator",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded")



##############################################################################
### OPTIONS PRICER

# Returns an estimate for the current risk free rate using the 1 year treasury yield
def get_risk_free_rate():
    treasury_data = yf.Ticker("^IRX")
    rate = treasury_data.history(period="1d")['Close'][0] / 100
    return rate


st.title("🎯 Black-Scholes Model Option Pricer")
st.sidebar.title("📊😲🔥 Black-Scholes Implied Volatility Calculator and GARCH Model Predictor")
st.sidebar.header("Option Parameters")
S = st.sidebar.number_input("Spot Price (S)", value=100.)
K = st.sidebar.number_input("Strike Price (K)", value=105.)
T = st.sidebar.number_input("Time to Expiry (T) in days", value=365)
r = st.sidebar.number_input("Risk-Free Rate (r)", value=get_risk_free_rate(), format="%.3f")
sigma = st.sidebar.number_input("Volatility (σ)", value=0.2)

# Instantiate the model using the sidebar inputs
bs_model = BlackScholesModel(S, K, T / 365, r, sigma)
call_price = bs_model.call_price()
put_price = bs_model.put_price()

st.subheader(f"Prices of options {int(bs_model.T * 365)} DTE @ ${bs_model.K:.2f} with spot price = {bs_model.S:.2f}, r = {bs_model.r:.3f}, and σ = {bs_model.sig:.3f}:")
col1, col2 = st.columns(2)
with col1:
    st.markdown("<div style='padding: 20px; border: 2px solid #4CAF50; border-radius: 10px; text-align: center;'>"
                "<h3 style='color: #4CAF50;'>CALL Price</h3>"
                f"<h2 style='color: #4CAF50;'>${call_price:.2f}</h2>"
                "</div>", unsafe_allow_html=True)
with col2:
    st.markdown("<div style='padding: 20px; border: 2px solid #007BFF; border-radius: 10px; text-align: center;'>"
                "<h3 style='color: #007BFF;'>PUT Price</h3>"
                f"<h2 style='color: #007BFF;'>${put_price:.2f}</h2>"
                "</div>", unsafe_allow_html=True)



##############################################################################
### IMPLIED VOLATILITY CALCULATOR

st.title("📉📈 Implied Volatility Calculator")

option_price = st.number_input("Enter the current price of a CALL with the given parameters:", value=10.)
imp_vol = bs_model.implied_volatility(option_price)

# Display volatility calculation
st.subheader(f"For a CALL or PUT option {int(bs_model.T * 365)} DTE @ ${bs_model.K:.2f} with spot price = {bs_model.S:.2f} and r = {bs_model.r:.3f}:")
st.markdown("<div style='padding: 20px; border: 2px solid #FFA500; border-radius: 10px; text-align: center;'>"
            "<h3 style='color: #FFA500;'>IMPLIED VOLATILITY of the underlying (σ)</h3>"
            f"<h2 style='color: #FFA500;'>{imp_vol:.2%} ({(imp_vol / math.sqrt(252)):.2%} daily)</h2>"
            "</div>", unsafe_allow_html=True)



##############################################################################
### GARCH MODEL VOLATILITY PREDICTOR

# Uses a GARCH model to forecast daily volatility estimates throughout the option lifetime. 
# Graphs the forecasted volatility and makes a prediction as an annualized and daily average volatility.
def garch_prediction(ticker, start_date, end_date):
    
    data = yf.download(ticker, start=start_date, end=end_date)
    
    if data.empty:
        st.write("No data found. Please check the ticker symbol and date range.")
    else:
        data['Returns'] = 100 * data['Adj Close'].pct_change().dropna()
        
        model = arch_model(data['Returns'].dropna(), vol='Garch', p=1, q=1)
        fitted_model = model.fit(disp='off')
        forecast = fitted_model.forecast(horizon=T)
        daily_vols = np.sqrt(forecast.variance.iloc[-1])
        
        avg_daily_vol = np.mean(daily_vols)
        annualized_vol = avg_daily_vol * np.sqrt(252)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=list(range(1, T + 1)),
            y=daily_vols,
            mode='lines+markers',
            name='Predicted Daily Volatility',
            line=dict(color='#A22BE2', width=2),
            marker=dict(size=5)
        ))
        fig.update_layout(
            title=f"Daily Predicted Volatility for {ticker} over the Option Lifetime",
            xaxis_title="Days",
            yaxis_title="Daily Volatility (%)",
            template="plotly_dark",
            title_x=0.12,
            title_font=dict(size=30)
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("<div style='padding: 20px; border: 2px solid #A22BE2; border-radius: 10px; text-align: center;'>"
            "<h3 style='color: #A22BE2;'>HISTORICAL VOLATILITY PREDICTION (σ)</h3>"
            f"<h2 style='color: #A22BE2;'>{annualized_vol:.2f}% ({(avg_daily_vol):.2f}% daily avg)</h2>"
            "</div>", unsafe_allow_html=True)
        
        
st.write("\n")
st.markdown("---")
st.title("🔮 GARCH Model Volatility Forcaster (Historical Data)")

ticker = st.text_input("Enter ticker symbol for GARCH prediction:", "AAPL")
start_date = st.date_input("Start Date", pd.to_datetime("2020-01-01"), min_value=pd.to_datetime("2000-01-01"), max_value=datetime.today())
end_date = st.date_input("End Date", pd.to_datetime("today"), min_value=pd.to_datetime("2000-01-01"), max_value=datetime.today())

garch_prediction(ticker, start_date, end_date)



st.write("---")
st.markdown("Created by Kalyan Patel  |   [LinkedIn](https://www.linkedin.com/in/kalyan-patel-329214215/)")