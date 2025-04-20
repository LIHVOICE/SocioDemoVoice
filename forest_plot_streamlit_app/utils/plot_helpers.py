import plotly.graph_objects as go
import numpy as np
import pandas as pd
import matplotlib.image as mpimg

def generate_plotly_forest_plot(
    input_filename,
    columns_to_work_with,
    socio_factors,
    coef_name,
    feature_name,
    gender
):
    # Load the .npy file (assuming it was saved with pickling enabled)
    data = np.load(input_filename, allow_pickle=True)
    columns_to_work_with = np.load(columns_to_work_with, allow_pickle=True)
    print(columns_to_work_with)
    # Organizing results
    coefficients = np.array([r[0] for r in data])
    ci_low = np.array([r[1] for r in data])
    ci_high = np.array([r[2] for r in data])

    coefficients_df = pd.DataFrame(coefficients, columns=['Intercept'] + socio_factors, index=columns_to_work_with)
    ci_low_df = pd.DataFrame(ci_low, columns=['Intercept'] + socio_factors, index=columns_to_work_with)
    ci_high_df = pd.DataFrame(ci_high, columns=['Intercept'] + socio_factors, index=columns_to_work_with)

    #for j, coef_name in enumerate(socio_factors):

    y_positions = np.arange(len(columns_to_work_with))[::-1]  # Reverse for top-down
    coefs = coefficients_df[coef_name].loc[columns_to_work_with]
    ci_low = ci_low_df[coef_name].loc[columns_to_work_with]
    ci_high = ci_high_df[coef_name].loc[columns_to_work_with]

    # Determine significance based on whether CI crosses zero
    significance = ['Not Significant' if l * h < 0 else 'Significant' for l, h in zip(ci_low, ci_high)]
    colors = ['lightblue' if sig == 'Not Significant' else 'orangered' for sig in significance]

    # Create traces
    fig = go.Figure()

    # Confidence intervals
    fig.add_trace(go.Scatter(
        x=ci_low,
        y=y_positions,
        mode='lines',
        line=dict(color='gray', width=0),
        showlegend=False,
        hoverinfo='skip'
    ))
    fig.add_trace(go.Scatter(
        x=ci_high,
        y=y_positions,
        mode='lines',
        line=dict(color='gray', width=0),
        showlegend=False,
        hoverinfo='skip'
    ))

    for i, feature in enumerate(columns_to_work_with):
        hover_text = (
            f"<b>{feature}</b><br>"
            f"Coef: {coefs[i]:.3f}<br>"
            f"CI: [{ci_low[i]:.3f}, {ci_high[i]:.3f}]<br>"
            f"Significance: {significance[i]}"
        )
        fig.add_trace(go.Scatter(
            x=[coefs[i]],
            y=[y_positions[i]],
            mode='markers',
            marker=dict(color=colors[i], size=10),
            hovertemplate=hover_text,
            showlegend=False
        ))

        # Line for CI
        fig.add_trace(go.Scatter(
            x=[ci_low[i], ci_high[i]],
            y=[y_positions[i], y_positions[i]],
            mode='lines',
            line=dict(color=colors[i], width=3),
            showlegend=False,
            hoverinfo='skip'
        ))

    fig.add_vline(x=0, line_dash="dash", line_color="gray")

    fig.update_yaxes(
        tickvals=y_positions,
        ticktext=columns_to_work_with[::-1],  # reverse labels to match reversed y
        title='Features'
    )
    fig.update_xaxes(title='Coefficient Value')

    fig.update_layout(
        #title=f"Forest Plot: {feature_name} features vs. {coef_name} ({gender})",
        height=600 + len(columns_to_work_with) * 15,
        plot_bgcolor="lightgrey",
        margin=dict(l=100, r=20, t=80, b=40)
    )

    return fig


def show_heatmap(
    audio_type,
    coef_name,
    feature_name,
    gender
):
    # Load the .npy file (assuming it was saved with pickling enabled)
    input_filename = f"{audio_type}_{feature_name}_{gender}_{coef_name}.jpg"
    heatmap = np.load(input_filename)
    columns_to_work_with = np.load(columns_to_work_with, allow_pickle=True)
    print(columns_to_work_with)
    # Read the image
    image = mpimg.imread('path_to_image.jpg')

    # Display the image
    plt.imshow(image)
    plt.axis('off')  # Turn off axis
    plt.show()
    return fig

def generate_heatmap(
    input_filename,
    coef_name,
    feature_name,
    gender
):
    # Load the .npy file (assuming it was saved with pickling enabled)
    data = np.load(input_filename, allow_pickle=True)
    columns_to_work_with = np.load(columns_to_work_with, allow_pickle=True)
    print(columns_to_work_with)
    # Organizing results
    coefficients = np.array([r[0] for r in data])
    ci_low = np.array([r[1] for r in data])
    ci_high = np.array([r[2] for r in data])

    coefficients_df = pd.DataFrame(coefficients, columns=['Intercept'] + socio_factors, index=columns_to_work_with)
    ci_low_df = pd.DataFrame(ci_low, columns=['Intercept'] + socio_factors, index=columns_to_work_with)
    ci_high_df = pd.DataFrame(ci_high, columns=['Intercept'] + socio_factors, index=columns_to_work_with)

    #for j, coef_name in enumerate(socio_factors):

    y_positions = np.arange(len(columns_to_work_with))[::-1]  # Reverse for top-down
    coefs = coefficients_df[coef_name].loc[columns_to_work_with]
    ci_low = ci_low_df[coef_name].loc[columns_to_work_with]
    ci_high = ci_high_df[coef_name].loc[columns_to_work_with]

    # Determine significance based on whether CI crosses zero
    significance = ['Not Significant' if l * h < 0 else 'Significant' for l, h in zip(ci_low, ci_high)]
    colors = ['lightblue' if sig == 'Not Significant' else 'orangered' for sig in significance]

    # Create traces
    fig = go.Figure()

    # Confidence intervals
    fig.add_trace(go.Scatter(
        x=ci_low,
        y=y_positions,
        mode='lines',
        line=dict(color='gray', width=0),
        showlegend=False,
        hoverinfo='skip'
    ))
    fig.add_trace(go.Scatter(
        x=ci_high,
        y=y_positions,
        mode='lines',
        line=dict(color='gray', width=0),
        showlegend=False,
        hoverinfo='skip'
    ))

    for i, feature in enumerate(columns_to_work_with):
        hover_text = (
            f"<b>{feature}</b><br>"
            f"Coef: {coefs[i]:.3f}<br>"
            f"CI: [{ci_low[i]:.3f}, {ci_high[i]:.3f}]<br>"
            f"Significance: {significance[i]}"
        )
        fig.add_trace(go.Scatter(
            x=[coefs[i]],
            y=[y_positions[i]],
            mode='markers',
            marker=dict(color=colors[i], size=10),
            hovertemplate=hover_text,
            showlegend=False
        ))

        # Line for CI
        fig.add_trace(go.Scatter(
            x=[ci_low[i], ci_high[i]],
            y=[y_positions[i], y_positions[i]],
            mode='lines',
            line=dict(color=colors[i], width=3),
            showlegend=False,
            hoverinfo='skip'
        ))

    fig.add_vline(x=0, line_dash="dash", line_color="gray")

    fig.update_yaxes(
        tickvals=y_positions,
        ticktext=columns_to_work_with[::-1],  # reverse labels to match reversed y
        title='Features'
    )
    fig.update_xaxes(title='Coefficient Value')

    fig.update_layout(
        #title=f"Forest Plot: {feature_name} features vs. {coef_name} ({gender})",
        height=600 + len(columns_to_work_with) * 15,
        plot_bgcolor="lightgrey",
        margin=dict(l=100, r=20, t=80, b=40)
    )

    return fig