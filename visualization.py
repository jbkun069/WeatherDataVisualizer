import matplotlib.pyplot as plt
import io
import base64

def generate_line_chart(weeks, values, title, ylabel):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(weeks, values, marker='o', linestyle='-')
    ax.set_title(title)
    ax.set_xlabel('Weeks')
    ax.set_ylabel(ylabel)
    ax.grid(True)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100)
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return img_base64