import numpy as np
import seaborn as sns
from scipy.stats import norm
import streamlit as st
import plotly.graph_objects as go

class Visualizations:
    def __init__(self, option):
        """
        Initialize the visualizations class with an option object.
        
        Parameters:
        option : A BlackScholes object containing option data
        """
        self.option = option

    def plot_greeks(self):
        """Plot Greeks (Delta, Gamma, Vega, Theta, Rho) on a single graph"""
        d1 = self.option._calculate_d1()
        d2 = self.option._calculate_d2(d1)

        # Calculate Greeks
        delta = norm.cdf(d1)
        gamma = norm.pdf(d1) / (self.option.S0 * self.option.sigma * np.sqrt(self.option.T))
        vega = self.option.S0 * norm.pdf(d1) * np.sqrt(self.option.T)
        theta = (-self.option.S0 * norm.pdf(d1) * self.option.sigma) / (2 * np.sqrt(self.option.T)) - self.option.r * self.option.K * np.exp(-self.option.r * self.option.T) * norm.cdf(d2)
        rho = self.option.K * self.option.T * np.exp(-self.option.r * self.option.T) * norm.cdf(d2)

        # Plot Greeks on a single graph using Plotly
        greeks = {
            "Delta": delta,
            "Gamma": gamma,
            "Vega": vega,
            "Theta": theta,
            "Rho": rho
        }

        fig = go.Figure()

        # Ensure that y-values are passed as lists or numpy arrays (even if it's a single value)
        for greek, values in greeks.items():
            # Make sure values is an array (even if it's a single value)
            fig.add_trace(go.Scatter(x=[self.option.S0], y=[values], mode="markers", name=greek))

        fig.update_layout(
            title="Option Greeks",
            xaxis_title="Stock Price",
            yaxis_title="Greek Value",
            template="plotly_dark",
            hovermode="closest",  # Enable hover functionality
            dragmode="zoom",  # Enable zoom and pan
         )

        st.plotly_chart(fig)


    def plot_profit_loss(self):
        """Plot Profit/Loss (P/L) vs Stock Price for both Call and Put"""
        stock_prices = np.linspace(self.option.S0 - 50, self.option.S0 + 50, 100)
        call_profits = np.maximum(0, stock_prices - self.option.K) - self.option.calculate_call_price()
        put_profits = np.maximum(0, self.option.K - stock_prices) - self.option.calculate_put_price()

        # Plotly plot for call and put profits/losses
        fig = go.Figure()

        # Call Option Profit/Loss
        fig.add_trace(go.Scatter(x=stock_prices, y=call_profits, mode='lines', name='Call Option Profit/Loss', line=dict(color='green')))
        fig.add_trace(go.Scatter(x=stock_prices, y=call_profits, mode='lines', fill='tozeroy', fillcolor='rgba(0,255,0,0.3)', name='Call Profit Area'))

        # Put Option Profit/Loss
        fig.add_trace(go.Scatter(x=stock_prices, y=put_profits, mode='lines', name='Put Option Profit/Loss', line=dict(color='red')))
        fig.add_trace(go.Scatter(x=stock_prices, y=put_profits, mode='lines', fill='tozeroy', fillcolor='rgba(255,0,0,0.3)', name='Put Profit Area'))

        fig.update_layout(
            title="Profit/Loss vs Stock Price (Call and Put)",
            xaxis_title="Stock Price",
            yaxis_title="Profit/Loss",
            template="plotly_dark",
            hovermode="closest",
            dragmode="zoom"
        )

        st.plotly_chart(fig)

    def plot_pv_vs_time(self):
        """Plot Profit/Loss vs Time to Maturity for both Call and Put"""
        times = np.linspace(0.01, self.option.T, 100)
        call_prices = []
        put_prices = []

        for T in times:
            self.option.T = T
            call_prices.append(self.option.calculate_call_price())
            put_prices.append(self.option.calculate_put_price())

        # Plotly plot for call and put prices over time to maturity
        fig = go.Figure()

        # Call Option Prices vs Time
        fig.add_trace(go.Scatter(x=times, y=call_prices, mode='lines', name='Call Option Price', line=dict(color='green')))

        # Put Option Prices vs Time
        fig.add_trace(go.Scatter(x=times, y=put_prices, mode='lines', name='Put Option Price', line=dict(color='red')))

        fig.update_layout(
            title="Option Prices vs Time to Maturity",
            xaxis_title="Time to Maturity (Years)",
            yaxis_title="Option Price ($)",
            template="plotly_dark",
            hovermode="closest",
            dragmode="zoom"
        )

        st.plotly_chart(fig)

    def plot_volatility_impact(self):
        """Plot Option Price vs Volatility"""
        volatility_range = np.linspace(0.05, 1.0, 100)
        call_prices = []
        put_prices = []

        for sigma in volatility_range:
            self.option.sigma = sigma
            call_prices.append(self.option.calculate_call_price())
            put_prices.append(self.option.calculate_put_price())

        # Plotly plot for call and put prices vs volatility
        fig = go.Figure()

        # Call Option Prices vs Volatility
        fig.add_trace(go.Scatter(x=volatility_range, y=call_prices, mode='lines', name='Call Option Price', line=dict(color='green')))

        # Put Option Prices vs Volatility
        fig.add_trace(go.Scatter(x=volatility_range, y=put_prices, mode='lines', name='Put Option Price', line=dict(color='red')))

        fig.update_layout(
            title="Option Prices vs Volatility",
            xaxis_title="Volatility (σ)",
            yaxis_title="Option Price ($)",
            template="plotly_dark",
            hovermode="closest",
            dragmode="zoom"
        )

        st.plotly_chart(fig)

    def plot_strike_price_impact(self):
        """Plot Strike Price Sensitivity"""
        strike_prices = np.linspace(self.option.S0 - 50, self.option.S0 + 50, 100)
        call_prices = []
        put_prices = []

        for K in strike_prices:
            self.option.K = K
            call_prices.append(self.option.calculate_call_price())
            put_prices.append(self.option.calculate_put_price())

        # Plotly plot for call and put prices vs strike price
        fig = go.Figure()

        # Call Option Prices vs Strike Price
        fig.add_trace(go.Scatter(x=strike_prices, y=call_prices, mode='lines', name='Call Option Price', line=dict(color='green')))

        # Put Option Prices vs Strike Price
        fig.add_trace(go.Scatter(x=strike_prices, y=put_prices, mode='lines', name='Put Option Price', line=dict(color='red')))

        fig.update_layout(
            title="Option Prices vs Strike Price",
            xaxis_title="Strike Price (K)",
            yaxis_title="Option Price ($)",
            template="plotly_dark",
            hovermode="closest",
            dragmode="zoom"
        )

        st.plotly_chart(fig)

    def plot_heatmap(self):
        """Plot Heatmap for Option Price Sensitivity to Volatility and Strike Price"""
        strike_prices = np.linspace(self.option.S0 - 25, self.option.S0 + 25, 50)  # Reduced for better resolution
        volatility_range = np.linspace(0.05, 1.0, 50)

        heatmap_data = np.zeros((len(strike_prices), len(volatility_range)))

        for i, K in enumerate(strike_prices):
            for j, sigma in enumerate(volatility_range):
                self.option.K = K
                self.option.sigma = sigma
                heatmap_data[i, j] = self.option.calculate_call_price()  # Option price for call

        # Plotly heatmap for better interactivity
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_data,
            x=np.round(volatility_range, 2),
            y=np.round(strike_prices, 2),
            colorscale="Viridis",  # Using Viridis color scheme for better visibility
            colorbar=dict(title="Call Option Price"),
            hovertemplate="Volatility: %{x}<br>Strike Price: %{y}<br>Price: %{z}<extra></extra>"
        ))

        fig.update_layout(
            title="Heatmap: Option Price Sensitivity to Volatility and Strike Price",
            xaxis_title="Volatility (σ)",
            yaxis_title="Strike Price (K)",
            template="plotly_dark",
            height=600,
            dragmode="zoom"  # Enable zoom and pan
        )

        st.plotly_chart(fig)
