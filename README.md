# 📊 Options Greeks Visualizer

An interactive web application for visualizing and understanding options pricing and Greeks in financial markets.

## 🔍 Overview

The Options Greeks Visualizer is a dynamic tool designed to help traders, analysts, and financial enthusiasts gain intuition about options pricing dynamics. Using the Black-Scholes model, this application provides real-time visualization of how various market factors affect option prices and their associated sensitivity measures (Greeks). By manipulating parameters like stock price, volatility, and time to expiration, users can develop a deeper understanding of options behavior under different market conditions.

## ✨ Features

- **Interactive Pricing Model** 💰: Real-time calculation of option prices using the Black-Scholes model
- **Comprehensive Greeks Analysis** 📈: Visual representation of all five key Greeks:
  - Delta (Δ): Price sensitivity to underlying asset changes
  - Gamma (Γ): Delta sensitivity to underlying asset changes
  - Theta (Θ): Price sensitivity to time decay
  - Vega (ν): Price sensitivity to volatility changes
  - Rho (ρ): Price sensitivity to interest rate changes
- **Customizable Parameters**: Adjust key inputs including:
  - Stock price
  - Strike price
  - Time to expiration
  - Risk-free interest rate
  - Volatility
  - Dividend yield
- **Multi-dimensional Visualization**: See how each Greek changes across the range of any selected parameter
- **Educational Descriptions**: Clear explanations of each Greek and its financial significance

## 📊 Data Sources

The application does not rely on external data sources. All calculations are performed in real-time using the Black-Scholes option pricing model with the following mathematical formulations:

- Option pricing formulas account for dividend yield
- Greeks are calculated using analytical derivatives of the Black-Scholes equation
- Normal distribution functions from SciPy are used for probability calculations

## 💡 Notes & Future Work

This project represents an ongoing exploration of financial derivatives and their behavior. Potential enhancements include:

- Adding support for more complex options pricing models (Heston, SABR) 🧮
- Implementing Monte Carlo simulations for path-dependent options 🎲
- Creating portfolio analysis tools to visualize aggregate Greek exposures 📊
- Adding historical volatility analysis to provide context for volatility inputs 📜
- Supporting exotic options and multi-asset derivatives 🌟
- Implementing real-time data feeds for market prices and implied volatilities 📡

The visualizer currently provides a solid foundation for understanding options pricing dynamics and developing trading strategies based on Greek sensitivities.

---

*This tool is intended for educational and research purposes. Options trading involves significant risk of loss and is not suitable for all investors.* ⚠️
