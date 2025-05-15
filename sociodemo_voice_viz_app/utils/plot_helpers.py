import os
import plotly.graph_objects as go
import matplotlib.image as mpimg
import plotly.express as px
import numpy as np
import pandas as pd

APP_PATH = 'sociodemo_voice_viz_app'
PLOT_DATA_FOLDER = 'other_viz_data'

def generate_plotly_forest_plot(
    input_filename,
    columns_to_work_with,
    socio_factors,
    coef_name,
    feature_name,
    gender
):
    # Load the .npy file
    data = np.load(input_filename, allow_pickle=True)
    columns_to_work_with = np.load(columns_to_work_with, allow_pickle=True)

    # Organizing results
    coefficients = np.array([r[0] for r in data])
    ci_low = np.array([r[1] for r in data])
    ci_high = np.array([r[2] for r in data])

    coefficients_df = pd.DataFrame(coefficients, columns=['Intercept'] + socio_factors, index=columns_to_work_with)
    ci_low_df = pd.DataFrame(ci_low, columns=['Intercept'] + socio_factors, index=columns_to_work_with)
    ci_high_df = pd.DataFrame(ci_high, columns=['Intercept'] + socio_factors, index=columns_to_work_with)

    #for j, coef_name in enumerate(socio_factors):

    # Reverse the order of y_positions and columns_to_work_with
    columns_to_work_with = columns_to_work_with[::-1]
    y_positions = np.arange(len(columns_to_work_with))
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
        ticktext=columns_to_work_with,  # reverse labels to match reversed y
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


def generate_plotly_heatmap(
    gender,
    audio_type,
    feature_name,
    coef_name,
):
    # Load the .npy file (assuming it was saved with pickling enabled)
    input_filename = f"{gender}_{audio_type}_{feature_name}_{coef_name}.csv"
    parent_dir = os.path.dirname(os.getcwd())
    df_path = os.path.join(parent_dir, APP_PATH, PLOT_DATA_FOLDER, input_filename)
    df = pd.read_csv(df_path, index_col=0)

    if df.empty:
        raise ValueError('The data is empty.')

    row_labels = df.index.to_list()

    fig= px.imshow(
    df,
    text_auto=True,
    aspect="auto",
    color_continuous_scale="RdBu_r",
    labels=dict(color="Median")
    )

    if row_labels is not None:
        fig.update_layout(
            yaxis=dict(
                tickmode="array",
                tickvals=list(range(len(row_labels))),
                ticktext=row_labels
            )
        )

    fig.update_layout(
    width=800,
    height=1000,
    autosize=False,
    xaxis=dict(tickfont=dict(size=12)),
    yaxis=dict(tickfont=dict(size=12))
    )

    return fig

def generate_plotly_barplot(
    gender,
    audio_type,
    feature_name,
    coef_name,
):
    input_filename = f"{gender}_{audio_type}_{feature_name}_{coef_name}.csv"
    parent_dir = os.path.dirname(os.getcwd())
    df_path = os.path.join(parent_dir, APP_PATH, PLOT_DATA_FOLDER, input_filename)
    df = pd.read_csv(df_path, index_col=0)

    if df.empty:
        raise ValueError("DataFrame is empty. Cannot generate plot.")

    group_names = df.columns.tolist()
    group_colors = {
        group_names[0]: '#636EFA',
        group_names[1]: '#00CC96'
    }

    fig = go.Figure()

    for group in group_names:
        fig.add_trace(go.Bar(
            y=df.index,
            x=df[group],
            name=group,
            orientation='h',
            marker=dict(color=group_colors.get(group, '#AB63FA'))
        ))

    # Calculate adaptive height
    base_height = 200
    row_height = 40
    max_height = 1000  # limit to avoid absurdly tall plots
    total_height = min(max_height, base_height + row_height * len(df))

    fig.update_layout(
        barmode='group',
        xaxis_title='Normalized Median Value',
        yaxis_title='Feature',
        yaxis=dict(
            categoryorder='array',
            categoryarray=list(df.index)[::-1]
        ),
        legend=dict(
            x=1.02,
            y=1,
            xanchor='left',
            yanchor='top'
        ),
        height=total_height,
        font=dict(size=14),
        margin=dict(l=100, r=30, t=40, b=40),
        plot_bgcolor="lightgrey",
        template='plotly_white'
    )

    return fig