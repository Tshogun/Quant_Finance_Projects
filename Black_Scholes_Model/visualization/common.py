# src/visualizations/common.py

import plotly.graph_objects as go

def get_default_layout(title, xaxis_title, yaxis_title):
    """Return a default layout for Plotly charts."""
    return {
        'title': title,
        'xaxis': {'title': xaxis_title},
        'yaxis': {'title': yaxis_title},
        'template': 'plotly_dark',
        'hovermode': 'closest',
        'dragmode': 'zoom'
    }

def add_trace(fig, x, y, name, line_color='blue', fill=None, fillcolor=None):
    """Helper function to add a trace to a Plotly figure."""
    if fill and fillcolor:
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name=name,
                                line=dict(color=line_color),
                                fill=fill, fillcolor=fillcolor))
    else:
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name=name, line=dict(color=line_color)))
    
def get_color_scale():
    """Return a default color scale for visualizations."""
    return 'Viridis'  # Default color scale for heatmap

