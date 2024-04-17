import matplotlib.pyplot as plt # type: ignore
import io
import base64

def get_plot(dataset, kind, title, xlabel, ylabel, sort, limit, angle):
    output = io.BytesIO()
    plt.tight_layout()
    ax = dataset.value_counts(sort=sort)[:limit].plot(kind=kind, rot=angle)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.savefig(output, format='png')
    output.seek(0)
    return base64.b64encode(output.getvalue()).decode('utf8')


def scatter_plot(dataset, fieldx, fieldy, title, xlabel, ylabel):
    output = io.BytesIO()
    plt.tight_layout()
    ax = dataset.plot.scatter(x=fieldx, y=fieldy)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.savefig(output, format='png')
    output.seek(0)
    return base64.b64encode(output.getvalue()).decode('utf8')
