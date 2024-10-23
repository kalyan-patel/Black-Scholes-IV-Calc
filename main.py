import streamlit as st
import yfinance as yf
from black_scholes_model import BlackScholesModel


# Use the 1 year treasury yield initialize the risk free rate
def get_risk_free_rate():
    treasury_data = yf.Ticker("^IRX")
    rate = treasury_data.history(period="1d")['Close'][0] / 100
    return rate

# Page configuration
st.set_page_config(
    page_title="Black-Scholes Option Pricer and Implied Volatility Calculator",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded")



##############################################################################
### OPTIONS PRICER

st.title("🎯 Black-Scholes Model Option Pricer")

# Sidebar model inputs
with st.sidebar:
    st.title("😼📊 Black-Scholes Pricer and Volatility Calculator")
# Sidebar inputs
st.sidebar.header("Option Parameters")
S = st.sidebar.number_input("Spot Price (S)", value=100.)
K = st.sidebar.number_input("Strike Price (K)", value=100.)
T = st.sidebar.number_input("Time to Expiry (T) in days", value=365)
r = st.sidebar.number_input("Risk-Free Rate (r)", value=get_risk_free_rate(), format="%.3f")
sigma = st.sidebar.number_input("Volatility (σ)", value=0.2)

# Instantiate a model with the inputs
bs_model = BlackScholesModel(S, K, T / 365, r, sigma)

# Calculate the option prices
call_price = bs_model.call_price()
put_price = bs_model.put_price()

# Display results
st.subheader(f"Prices of options {int(bs_model.T * 365)} DTE @ ${bs_model.K:.2f} with spot price = {bs_model.S:.2f}, r = {bs_model.r}, and σ = {bs_model.sig}:")
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

# Sidebar price input
st.sidebar.header("Implied Volatility Calculator")
option_price = st.sidebar.number_input("Price of a call with the above parameters:", value=10.)
imp_vol = bs_model.implied_volatility(option_price)
if st.sidebar.button("Calculate Implied Volatility"):
    imp_vol = bs_model.implied_volatility(option_price)
    
# Display volatility calculation
st.subheader(f"For a CALL or PUT option {int(bs_model.T * 365)} DTE @ ${bs_model.K:.2f} with spot price = {bs_model.S:.2f} and r = {bs_model.r}:")
st.markdown("<div style='padding: 20px; border: 2px solid #FFA500; border-radius: 10px; text-align: center;'>"
            "<h3 style='color: #FFA500;'>IMPLIED VOLATILITY of the underlying (σ)</h3>"
            f"<h2 style='color: #FFA500;'>{imp_vol:.2%}</h2>"
            "</div>", unsafe_allow_html=True)



st.write("---")
st.markdown("Created by Kalyan Patel  |   [LinkedIn](https://www.linkedin.com/in/kalyan-patel-329214215/)")