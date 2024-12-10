import numpy as np
import plotly.graph_objects as go
import streamlit as st

class OptionPLVisualization:
    def __init__(self, option):
        """
        Initializes the OptionPLVisualization class with an option object.
        
        Parameters:
        option : A BlackScholes object containing option data
        """
        self.option = option

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
            yaxis_title="Profit/Loss ($)",
            template="plotly_dark",
            hovermode="closest",
            dragmode="zoom"
        )

        st.plotly_chart(fig)

