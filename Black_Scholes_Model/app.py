import streamlit as st
import sentencepiece  # Make sure sentencepiece is installed
import pandas as pd
import numpy as np
from model.black_scholes import BlackScholes
from visualization import GreeksVisualizations, PLVisualizations, TimeVsPriceVisualizations, VolatilityVisualizations, HeatmapVisualization
from model.llama_integration import LlamaIntegration  # Import the LlamaIntegration class

def main():
    # App title
    st.title("Black-Scholes Option Pricing Model and Visualizations")

    # Sidebar for Option Parameters
    st.sidebar.header("Option Parameters")

    # User input for Spot price (S0), Strike price (K), Time to Maturity (T), Risk-free rate (r), Volatility (σ)
    spot_price = st.sidebar.number_input("Spot Price (S0)", min_value=1.0, value=100.0)
    strike_price = st.sidebar.number_input("Strike Price (K)", min_value=1.0, value=100.0)
    time_to_maturity = st.sidebar.number_input("Time to Maturity (T) in years", min_value=0.0, value=1.0)
    risk_free_rate = st.sidebar.number_input("Risk-free Interest Rate (r)", min_value=0.0, max_value=1.0, value=0.05)
    volatility = st.sidebar.number_input("Volatility (σ)", min_value=0.0, max_value=1.0, value=0.2)

    # Create Black-Scholes model instance
    option_model = BlackScholes(S0=spot_price, K=strike_price, T=time_to_maturity, r=risk_free_rate, sigma=volatility)

    # Display Option Price Calculation
    call_price = option_model.calculate_call_price()
    put_price = option_model.calculate_put_price()

    st.subheader("Option Price Calculation")
    st.write(f"Call Option Price: ${call_price:.2f}")
    st.write(f"Put Option Price: ${put_price:.2f}")

    # Greeks Visualization
    st.subheader("Greeks (Option Price Sensitivity)")
    visualizer_greeks = GreeksVisualizations(option_model)
    visualizer_greeks.plot_greeks()  # Display the plot for option Greeks

    # Profit/Loss Visualization
    st.subheader("Profit/Loss vs Stock Price (Call and Put)")
    visualizer_pl = PLVisualizations(option_model)
    visualizer_pl.plot_profit_loss()  # Display the plot for P&L vs Stock Price

    # Time vs Price Visualization
    st.subheader("Profit/Loss vs Time to Maturity (Call and Put)")
    visualizer_time_vs_price = TimeVsPriceVisualizations(option_model)
    visualizer_time_vs_price.plot_time_vs_price()  # Display P&L vs Time to Maturity

    # Volatility Impact Visualization
    st.subheader("Option Price vs Volatility")
    visualizer_volatility = VolatilityVisualizations(option_model)
    visualizer_volatility.plot_volatility_impact()  # Display Option Price vs Volatility

    # Heatmap Visualization
    st.subheader("Option Price Sensitivity Heatmap")
    visualizer_heatmap = HeatmapVisualization(option_model)
    visualizer_heatmap.plot_heatmap()  # Display the Option Price Sensitivity Heatmap

    # Executive Summary Section
    st.sidebar.header("Executive Summary Generator")

    # User input for executive summary
    text_input = st.sidebar.text_area("Enter text for Executive Summary", height=150, value="Enter a detailed description here...")

    if st.sidebar.button("Generate Summary"):
        if text_input.strip() == "":
            st.sidebar.warning("Please enter some text to generate a summary.")
        else:
            try:
                # Initialize the LLaMA integration
                llama_integration = LlamaIntegration()

                # Generate the executive summary
                summary = llama_integration.generate_summary(text_input)

                # Display the generated summary
                if summary:
                    st.subheader("Executive Summary")
                    st.write(summary)
                else:
                    st.sidebar.error("Error generating the summary. Please try again.")
            except Exception as e:
                st.sidebar.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
