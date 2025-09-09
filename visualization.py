import matplotlib.pyplot as plt
import io
import base64

def generate_line_chart(weeks, values, title, ylabel, ylim=None):
    """
    Generates a line chart and returns it as a base64 encoded string.
    
    Args:
        weeks (list): The labels for the x-axis.
        values (list): The data points for the y-axis.
        title (str): The title of the chart.
        ylabel (str): The label for the y-axis.
        ylim (tuple, optional): The limits for the y-axis (min, max). Defaults to None.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Use a more descriptive label for the legend
    series_label = ylabel.split('(')[0].strip()
    ax.plot(weeks, values, marker='o', linestyle='-', label=series_label)
    
    ax.set_title(title, fontsize=16, weight='bold')
    ax.set_xlabel('Weeks', fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    
    if ylim and ylim[0] is not None and ylim[1] is not None:
        ax.set_ylim(ylim)

    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    ax.legend() # Add a legend
    
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100)
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return img_base64