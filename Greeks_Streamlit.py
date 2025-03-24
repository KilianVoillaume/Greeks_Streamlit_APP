import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats

st.set_page_config(page_title="Options Greeks Visualizer", layout="wide")

def calculate_d1(S, K, T, r, sigma, q):
    return (np.log(S/K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))

def calculate_d2(d1, sigma, T):
    return d1 - sigma * np.sqrt(T)

def calculate_greeks(option_type, S, K, T, r, sigma, q):
    d1 = calculate_d1(S, K, T, r, sigma, q)
    d2 = calculate_d2(d1, sigma, T)
    
    if option_type == "Call":
        delta = np.exp(-q * T) * stats.norm.cdf(d1)
        gamma = np.exp(-q * T) * stats.norm.pdf(d1) / (S * sigma * np.sqrt(T))
        theta = ( - (S * sigma * np.exp(-q * T) * stats.norm.pdf(d1)) / (2 * np.sqrt(T))
                  - r * K * np.exp(-r * T) * stats.norm.cdf(d2)
                  + q * S * np.exp(-q * T) * stats.norm.cdf(d1) ) / 365
        vega = S * np.exp(-q * T) * np.sqrt(T) * stats.norm.pdf(d1) / 100
        rho = K * T * np.exp(-r * T) * stats.norm.cdf(d2) / 100
    else:
        delta = -np.exp(-q * T) * stats.norm.cdf(-d1)
        gamma = np.exp(-q * T) * stats.norm.pdf(d1) / (S * sigma * np.sqrt(T))
        theta = ( - (S * sigma * np.exp(-q * T) * stats.norm.pdf(d1)) / (2 * np.sqrt(T))
                  + r * K * np.exp(-r * T) * stats.norm.cdf(-d2)
                  - q * S * np.exp(-q * T) * stats.norm.cdf(-d1) ) / 365
        vega = S * np.exp(-q * T) * np.sqrt(T) * stats.norm.pdf(d1) / 100
        rho = -K * T * np.exp(-r * T) * stats.norm.cdf(-d2) / 100
        
    return {
        "Delta": delta,
        "Gamma": gamma,
        "Theta": theta,
        "Vega": vega,
        "Rho": rho
    }

def black_scholes_price(option_type, S, K, T, r, sigma, q):
    d1 = calculate_d1(S, K, T, r, sigma, q)
    d2 = calculate_d2(d1, sigma, T)
    
    if option_type == "Call":
        price = S * np.exp(-q * T) * stats.norm.cdf(d1) - K * np.exp(-r * T) * stats.norm.cdf(d2)
    else:
        price = K * np.exp(-r * T) * stats.norm.cdf(-d2) - S * np.exp(-q * T) * stats.norm.cdf(-d1)
    
    return price

# App title and description
st.title("Options Greeks Visualizer")
st.markdown("""
This app visualizes how option Greeks (Delta, Gamma, Theta, Vega, and Rho) change 
based on various input parameters like stock price, strike price, time to expiration, 
interest rate, volatility, and dividend yield.
""")

# Sidebar inputs
st.sidebar.header("Input Parameters")

option_type = st.sidebar.selectbox("Option Type", ["Call", "Put"])

# Default parameters
S_default = 100.0
K_default = 100.0
T_default = 30/365
r_default = 0.05
sigma_default = 0.2
q_default = 0.02  # Default dividend yield

S = st.sidebar.slider("Stock Price ($)", 50.0, 150.0, float(S_default), 1.0)
K = st.sidebar.slider("Strike Price ($)", 50.0, 150.0, float(K_default), 1.0)
T = st.sidebar.slider("Time to Expiration (Days)", 1, 365, int(T_default*365), 1) / 365
r = st.sidebar.slider("Risk-Free Interest Rate (%)", 0.0, 10.0, float(r_default*100), 0.25) / 100
sigma = st.sidebar.slider("Volatility (%)", 5.0, 100.0, float(sigma_default*100), 1.0) / 100
q = st.sidebar.slider("Dividend Yield (%)", 0.0, 10.0, float(q_default*100), 0.25) / 100

current_price = black_scholes_price(option_type, S, K, T, r, sigma, q)
current_greeks = calculate_greeks(option_type, S, K, T, r, sigma, q)

# Display current values
st.header("Current Option Values")
col1, col2, col3, col4, col5, col6 = st.columns(6)
col1.metric("Price", f"${current_price:.2f}")
col2.metric("Delta", f"{current_greeks['Delta']:.4f}")
col3.metric("Gamma", f"{current_greeks['Gamma']:.4f}")
col4.metric("Theta", f"${current_greeks['Theta']:.4f}/day")
col5.metric("Vega", f"${current_greeks['Vega']:.4f}")
col6.metric("Rho", f"${current_greeks['Rho']:.4f}")

# Visualization section
st.header("Greeks Visualization")

# Parameter to visualize against
param_to_visualize = st.selectbox(
    "Select Parameter to Visualize Against", 
    ["Stock Price", "Strike Price", "Time to Expiration", "Interest Rate", "Volatility", "Dividend Yield"]
)

if param_to_visualize == "Stock Price":
    param_range = np.linspace(50, 150, 100)
    param_values = param_range
    x_label = "Stock Price ($)"
elif param_to_visualize == "Strike Price":
    param_range = np.linspace(50, 150, 100)
    param_values = param_range
    x_label = "Strike Price ($)"
elif param_to_visualize == "Time to Expiration":
    param_range = np.linspace(1, 365, 100)
    param_values = param_range / 365  # Convert to years
    x_label = "Time to Expiration (Days)"
elif param_to_visualize == "Interest Rate":
    param_range = np.linspace(0, 10, 100)
    param_values = param_range / 100  # Convert to decimal
    x_label = "Interest Rate (%)"
elif param_to_visualize == "Volatility":
    param_range = np.linspace(5, 100, 100)
    param_values = param_range / 100  # Convert to decimal
    x_label = "Volatility (%)"
elif param_to_visualize == "Dividend Yield":
    param_range = np.linspace(0, 10, 100)
    param_values = param_range / 100  # Convert to decimal
    x_label = "Dividend Yield (%)"

delta_values = []
gamma_values = []
theta_values = []
vega_values = []
rho_values = []
price_values = []

for param_value in param_values:
    if param_to_visualize == "Stock Price":
        greeks = calculate_greeks(option_type, param_value, K, T, r, sigma, q)
        price = black_scholes_price(option_type, param_value, K, T, r, sigma, q)
    elif param_to_visualize == "Strike Price":
        greeks = calculate_greeks(option_type, S, param_value, T, r, sigma, q)
        price = black_scholes_price(option_type, S, param_value, T, r, sigma, q)
    elif param_to_visualize == "Time to Expiration":
        if param_value < 0.001:
            continue
        greeks = calculate_greeks(option_type, S, K, param_value, r, sigma, q)
        price = black_scholes_price(option_type, S, K, param_value, r, sigma, q)
    elif param_to_visualize == "Interest Rate":
        greeks = calculate_greeks(option_type, S, K, T, param_value, sigma, q)
        price = black_scholes_price(option_type, S, K, T, param_value, sigma, q)
    elif param_to_visualize == "Volatility":
        if param_value < 0.001:
            continue
        greeks = calculate_greeks(option_type, S, K, T, r, param_value, q)
        price = black_scholes_price(option_type, S, K, T, r, param_value, q)
    elif param_to_visualize == "Dividend Yield":
        greeks = calculate_greeks(option_type, S, K, T, r, sigma, param_value)
        price = black_scholes_price(option_type, S, K, T, r, sigma, param_value)
    
    delta_values.append(greeks["Delta"])
    gamma_values.append(greeks["Gamma"])
    theta_values.append(greeks["Theta"])
    vega_values.append(greeks["Vega"])
    rho_values.append(greeks["Rho"])
    price_values.append(price)

st.subheader(f"Effect of {param_to_visualize} on Option Price and Greeks")

greeks_to_show = st.multiselect(
    "Select Greeks to Display", 
    ["Price", "Delta", "Gamma", "Theta", "Vega", "Rho"],
    default=["Delta", "Gamma", "Theta"]
)

if not greeks_to_show:
    st.warning("Please select at least one Greek to display.")
else:
    if param_to_visualize == "Stock Price":
        current_value = S
    elif param_to_visualize == "Strike Price":
        current_value = K
    elif param_to_visualize == "Time to Expiration":
        current_value = T * 365
    elif param_to_visualize == "Interest Rate":
        current_value = r * 100
    elif param_to_visualize == "Volatility":
        current_value = sigma * 100
    elif param_to_visualize == "Dividend Yield":
        current_value = q * 100
    
    x_display = param_range
    cols = st.columns(3)
    col_index = 0
    
    greek_colors = {
        "Price": "blue",
        "Delta": "green",
        "Gamma": "red",
        "Theta": "purple",
        "Vega": "orange",
        "Rho": "brown"
    }
    
    for greek in greeks_to_show:
        with cols[col_index % 3]:
            fig, ax = plt.subplots(figsize=(4, 3))
            
            if greek == "Price":
                ax.plot(x_display, price_values, label="Price", color=greek_colors[greek])
                ax.set_ylabel("Price ($)")
            elif greek == "Delta":
                ax.plot(x_display, delta_values, label="Delta", color=greek_colors[greek])
                ax.set_ylabel("Delta")
            elif greek == "Gamma":
                ax.plot(x_display, gamma_values, label="Gamma", color=greek_colors[greek])
                ax.set_ylabel("Gamma")
            elif greek == "Theta":
                ax.plot(x_display, theta_values, label="Theta", color=greek_colors[greek])
                ax.set_ylabel("Theta ($/day)")
            elif greek == "Vega":
                ax.plot(x_display, vega_values, label="Vega", color=greek_colors[greek])
                ax.set_ylabel("Vega ($/1% vol)")
            elif greek == "Rho":
                ax.plot(x_display, rho_values, label="Rho", color=greek_colors[greek])
                ax.set_ylabel("Rho ($/1% rate)")
            
            ax.set_xlabel(x_label)
            ax.set_title(f"{option_type} Option: {greek}")
            ax.grid(True)
            ax.axvline(x=current_value, color='r', linestyle='--', alpha=0.5)
            plt.tight_layout()
            st.pyplot(fig)
            
            col_index += 1

st.header("Understanding the Greeks")

st.subheader("Delta")
st.write("""
**Delta** measures how much an option's price is expected to change per $1 change in the underlying stock.
- For call options, delta is adjusted for dividends and ranges from 0 to 1.
- For put options, delta is adjusted for dividends and ranges from -1 to 0.
- At-the-money options typically have deltas around 0.5 (calls) or -0.5 (puts).
""")

st.subheader("Gamma")
st.write("""
**Gamma** measures the rate of change in delta for a $1 change in the underlying stock.
- High gamma means delta can change rapidly with small movements in the stock.
- Gamma is highest for at-the-money options and decreases as options move deeply in or out of the money.
- Gamma is adjusted for dividends by discounting the probability density function.
""")

st.subheader("Theta")
st.write("""
**Theta** measures the rate at which an option loses value due to time decay (per day).
- Generally negative for both calls and puts (options lose value as time passes).
- Theta increases (becomes more negative) as expiration approaches.
- For dividend-paying options, theta is adjusted to account for the dividend yield.
""")

st.subheader("Vega")
st.write("""
**Vega** measures sensitivity to changes in implied volatility.
- Higher vega means the option's price is more sensitive to volatility changes.
- Vega is highest for at-the-money options with longer expirations.
- Displayed as the dollar change for a 1% change in volatility, adjusted for dividends.
""")

st.subheader("Rho")
st.write("""
**Rho** measures sensitivity to changes in interest rates.
- For call options, rho is positive (calls increase in value as rates rise).
- For put options, rho is negative (puts decrease in value as rates rise).
- Displayed as the dollar change for a 1% change in interest rates.
- Rho is computed in a dividend-adjusted manner for dividend-paying options.
""")
