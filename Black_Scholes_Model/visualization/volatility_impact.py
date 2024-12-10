# src/visualizations/volatility_impact.py

import numpy as np
import plotly.graph_objects as go
import streamlit as st

class VolatilityImpactVisualization:
    def __init__(self, option):
        """
        Initializes the VolatilityImpactVisualization class with an option object.
        
        Parameters:
        option : A BlackScholes object containing option data
        """
        self.option = option

    def plot_volatility_impact(self):
        """Plot Option Price vs Volatility"""
        volatility_range = np.linspace(0.05, 1.0, 100)  # Range of volatility values
        call_prices = []
        put_prices = []

        for sigma in volatility_range:
            self.option.sigma = sigma  # Update volatility for each iteration
            call_prices.append(self.option.calculate_call_price())  # Calculate call price
            put_prices.append(self.option.calculate_put_price())    # Calculate put price

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

