# src/visualizations/time_vs_price.py

import numpy as np
import plotly.graph_objects as go
import streamlit as st

class TimeVsPriceVisualization:
    def __init__(self, option):
        """
        Initializes the TimeVsPriceVisualization class with an option object.
        
        Parameters:
        option : A BlackScholes object containing option data
        """
        self.option = option

    def plot_time_vs_price(self):
        """Plot Option Prices vs Time to Maturity"""
        # Create a range of times to maturity (0.01 to T)
        times = np.linspace(0.01, self.option.T, 100)  # From near expiration to the full maturity

        call_prices = []
        put_prices = []

        # Calculate call and put prices for each time to maturity value
        for T in times:
            self.option.T = T  # Update the time to maturity
            call_prices.append(self.option.calculate_call_price())  # Calculate call price
            put_prices.append(self.option.calculate_put_price())    # Calculate put price

        # Create the plot using Plotly
        fig = go.Figure()

        # Add the Call Option Prices vs Time to Maturity
        fig.add_trace(go.Scatter(x=times, y=call_prices, mode='lines', name='Call Option Price', line=dict(color='green')))

        # Add the Put Option Prices vs Time to Maturity
        fig.add_trace(go.Scatter(x=times, y=put_prices, mode='lines', name='Put Option Price', line=dict(color='red')))

        # Update the layout of the plot
        fig.update_layout(
            title="Option Prices vs Time to Maturity",
            xaxis_title="Time to Maturity (Years)",
            yaxis_title="Option Price ($)",
            template="plotly_dark",
            hovermode="closest",  # Enable hover functionality
            dragmode="zoom"  # Enable zoom and pan functionality
        )

        # Display the plot in Streamlit
        st.plotly_chart(fig)

