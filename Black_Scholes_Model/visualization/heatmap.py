# src/visualizations/heatmap.py

import numpy as np
import plotly.graph_objects as go
import streamlit as st

class HeatmapVisualization:
    def __init__(self, option):
        """
        Initializes the HeatmapVisualization class with an option object.
        
        Parameters:
        option : A BlackScholes object containing option data
        """
        self.option = option

    def plot_heatmap(self):
        """Plot Heatmap for Option Price Sensitivity to Volatility and Strike Price"""
        # Create a range of volatility values and strike prices
        volatility_range = np.linspace(0.05, 1.0, 50)  # Volatility range from 0.05 to 1.0
        strike_prices = np.linspace(self.option.S0 - 25, self.option.S0 + 25, 50)  # 50 strike prices around the current price

        # Prepare a matrix to store option prices (this will be the Z values in the heatmap)
        heatmap_data = np.zeros((len(strike_prices), len(volatility_range)))

        # Calculate option prices for each combination of volatility and strike price
        for i, K in enumerate(strike_prices):
            for j, sigma in enumerate(volatility_range):
                self.option.K = K
                self.option.sigma = sigma
                heatmap_data[i, j] = self.option.calculate_call_price()  # Store Call option price

        # Create the heatmap using Plotly
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_data,
            x=np.round(volatility_range, 2),  # X axis (volatility)
            y=np.round(strike_prices, 2),     # Y axis (strike price)
            colorscale="Viridis",             # Color scale for the heatmap
            colorbar=dict(title="Call Option Price"),
            hovertemplate="Volatility: %{x}<br>Strike Price: %{y}<br>Price: %{z}<extra></extra>"  # Hover info
        ))

        # Update layout for better presentation
        fig.update_layout(
            title="Heatmap: Option Price Sensitivity to Volatility and Strike Price",
            xaxis_title="Volatility (σ)",
            yaxis_title="Strike Price (K)",
            template="plotly_dark",
            height=600,  # Set height for better visibility
            dragmode="zoom"  # Enable zoom and pan functionality
        )

        # Display the heatmap in Streamlit
        st.plotly_chart(fig)

