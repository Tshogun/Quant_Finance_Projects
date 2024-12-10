# src/visualizations/option_greeks.py

import numpy as np
import plotly.graph_objects as go
import streamlit as st
from scipy.stats import norm

class OptionGreeksVisualization:
    def __init__(self, option):
        """
        Initializes the OptionGreeksVisualization class with an option object.
        
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

