import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba
from matplotlib.patches import Rectangle
import yaml
import style as stl


############################
# CONFIGURATION PARAMETERS #
############################

XMIN, XMAX = 0.1, 10000.0
YMIN, YMAX = 0.0003, 10.0


####################
# HELPER FUNCTIONS #
####################

def _grid_values(start: float, stop: float, step: float) -> list[float]:
    return list(np.round(np.arange(start, stop + 0.5 * step, step), 12))

def _plot_segment(ax: plt.Axes, x: np.ndarray, y, **kwargs) -> None:
    
    yy = y(x) if callable(y) else np.full_like(x, float(y), dtype=float)
    mask = (yy > 0) & np.isfinite(yy)
    ax.plot(x[mask], yy[mask], **kwargs)

def _fill_between(ax: plt.Axes, x: np.ndarray, y1, y2, **kwargs) -> None:
    
    yy1 = y1(x) if callable(y1) else np.full_like(x, float(y1), dtype=float)
    yy2 = y2(x) if callable(y2) else np.full_like(x, float(y2), dtype=float)
    mask = (yy1 > 0) & (yy2 > 0) & np.isfinite(yy1) & np.isfinite(yy2)
    ax.fill_between(x[mask], yy1[mask], yy2[mask], **kwargs)

def _load_experiment (fName: str) -> dict:

    with open(fName) as file:
        data = yaml.safe_load(file)

    return data
    
################
# FIGURE SETUP #
################

def setup_axes(ax: plt.Axes, title: str='') -> None:
    
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(XMIN, XMAX)
    ax.set_ylim(YMIN, YMAX)
    ax.set_xlabel(r"$a_0$ / $\xi$", fontsize=16)
    ax.set_ylabel(r"$\eta$", fontsize=16)

    if title!='':
        ax.set_title(title, fontsize=20)

    xgrid = (
        _grid_values(0.01, 0.09, 0.01)
        + _grid_values(0.1, 0.9, 0.1)
        + _grid_values(2, 10, 1)
        + _grid_values(20, 100, 10)
        + _grid_values(200, 1000, 100)
        + _grid_values(2000, 10000, 1000)
    )
    ygrid = (
        _grid_values(0.001, 0.009, 0.001)
        + _grid_values(0.01, 0.09, 0.01)
        + _grid_values(0.1, 0.9, 0.1)
        + _grid_values(2, 10, 1)
    )
    for x in xgrid:
        if XMIN <= x <= XMAX:
            ax.axvline(x, color="0.88", lw=0.4, zorder=0)
    for y in ygrid:
        if YMIN <= y <= YMAX:
            ax.axhline(y, color="0.88", lw=0.4, zorder=0)
            
def draw_common_reference_lines(ax: plt.Axes) -> None:

    # vertical reference lines
    for x, color, lw in [(1, "0.2", 1.0), (10, "0.6", 1.0), (100, "0.6", 1.0), (1000, "0.6", 1.0)]:
        ax.axvline(x, color=color, lw=lw, zorder=0)

    # horizontal reference lines
    ax.axhline(1, color="0.2", lw=1.0, zorder=0)

    # diagonal reference lines
    x = np.geomspace(0.001, 10000, 500)
    _plot_segment(ax, x, lambda xx: 137.0 ** 1.5 / xx, color="0.2", ls="--", lw=1.0, zorder=0)
    for c, color, lw in [(0.001, "0.6", 1.0), 
                         (0.01, "0.6", 1.0), 
                         (0.1, "0.6", 1.0), 
                         (1, "0.2", 1.25), 
                         (10, "0.6", 1.0), 
                         (100, "0.6", 1.0), 
                         (1000, "0.6", 1.0)]:
        _plot_segment(ax, x, lambda xx, c=c: c / xx, color=color, lw=lw, zorder=0)

def draw_common_labels(ax: plt.Axes, nlc: bool=False) -> None:
    
    labels = [
        (5500, 0.38, r"$(\alpha\chi)^{2/3}=1$", -35, "0.5"),
        (2000, 0.38, r"$\chi=1000$", -35, "0.5"),
        (200, 0.38, r"$\chi=100$", -35, "0.5"),
        (20, 0.38, r"$\chi=10$", -35, "0.5"),
        (2, 0.38, r"$\chi=1$", -35, "0.5"),
        (0.2, 0.38, r"$\chi=0.1$", -35, "0.5"),
        (0.2, 0.038, r"$\chi=0.01$", -35, "0.5"),
        (0.2, 0.0038, r"$\chi=0.001$", -35, "0.5"),
        (0.85, 0.58, r"$\xi=1$", 90, "0.5"),
        (2, 1.2, r"$\eta=1$", 0, "0.5"),
    ]
    
    for x, y, text, rot, color in labels:
        ax.text(x, y, text, fontsize=11, color=color, rotation=rot, ha="center", va="center")


###################
# PHYSICS REGIMES #
###################

def draw_ncs_regimes (ax: plt.Axes) -> None:
    
    _fill_between(ax, np.geomspace(0.01, 0.3), 1e-4, 10, color="orange", alpha=0.1)
    ax.text(0.18, 1.5, "Linear QED", fontsize=12, rotation=90, ha="center", bbox=dict(facecolor="orange", edgecolor="none", alpha=0.7))

    _fill_between(ax, np.geomspace(0.3, 1.0), 1e-5, 100, color="lightblue", alpha=0.2)
    ax.text(0.55, 1.5, "Harmonics", fontsize=12, rotation=90, ha="center", bbox=dict(facecolor="lightblue", edgecolor="none", alpha=0.7))

    _fill_between(ax, np.geomspace(1, 10000), 1e-5, 100, color="yellow", alpha=0.1)
    ax.text(30, 1.5, "Nonperturbative at\nsmall coupling", fontsize=12, ha="center", bbox=dict(facecolor="yellow", edgecolor="none", alpha=0.7))

    _fill_between(ax, np.geomspace(0.001, 10000), lambda xx: 137.0 ** 1.5 / xx, 100, color="red", alpha=0.1)
    ax.text(2700, 3, "Fully non-\nperturbative", fontsize=12, ha="center", bbox=dict(facecolor="red", edgecolor="none", alpha=0.7))

def draw_nbw_regimes (ax: plt.Axes) -> None:

    _fill_between(ax, np.geomspace(0.001, 10000), lambda xx: 2 * (1 + xx**2), 100, color="orange", alpha=0.1)
    ax.text(0.22, 6, "Linear QED", fontsize=12, ha="center", bbox=dict(facecolor="orange", edgecolor="none", alpha=0.7))
    _plot_segment(ax, np.geomspace(0.001, 10000), lambda xx: 2 * (1 + xx**2), color="orange", ls="--", lw=1.2)
    ax.text(0.12, 2.8, r"$\eta=2(1+\xi^2)$", fontsize=12, color="orange")

    _fill_between(ax, np.geomspace(0.001, 10000), lambda xx: 0.5 * (1 + xx**2), lambda xx: 2 * (1 + xx**2), color="lightblue", alpha=0.1)
    for n in [2,3,4]:
        _plot_segment(ax, np.geomspace(0.001, 10000), lambda xx, n=n: (2.0 / n) * (1 + xx**2), color="lightblue", ls="--", lw=1.2)
    ax.text(1.15, 3, "Harmonics", fontsize=12, ha="center", bbox=dict(facecolor="lightblue", edgecolor="none", alpha=0.7))

    _fill_between(ax, np.geomspace(0.001, 0.5), 0.0001, lambda xx: 0.5 * (1 + xx**2), color="purple", alpha=0.1)
    ax.text(0.225, 0.013, "Multiphoton\nperturbative", fontsize=12, ha="center", bbox=dict(facecolor="purple", edgecolor="none", alpha=0.7))
    
    _fill_between(ax, np.geomspace(3, 10000), lambda xx: 0.5 / xx, lambda xx: 0.001 / xx, color="green", alpha=0.1)
    ax.text(10, 0.005, "Non-analytic\npair creation", fontsize=12, ha="center", bbox=dict(facecolor="green", edgecolor="none", alpha=0.7))

    _fill_between(ax, np.geomspace(0.5, 10000), lambda xx: 0.5 * (1 + xx**2), 1e-5, color="yellow", alpha=0.1)
    ax.text(30, 1.5, "Nonperturbative at\nsmall coupling", fontsize=12, ha="center", bbox=dict(facecolor="yellow", edgecolor="none", alpha=0.7))

    _fill_between(ax, np.geomspace(0.001, 10000), lambda xx: 137.0 ** 1.5 / xx, 100, color="red", alpha=0.08)
    ax.text(2700, 3, "Fully non-\nperturbative", fontsize=12, ha="center", bbox=dict(facecolor="red", edgecolor="none", alpha=0.7))


##########################
# PLOT CONTENT FUNCTIONS #
##########################

def plot_experiment (ax: plt.Axes, fName: str, **kwargs: object) -> None:

    experiment = _load_experiment(fName)
    experiment_type = experiment['experiment_type']
    color = ax._get_lines.get_next_color()
    
    for dataset in experiment['datasets']:
        
        status = dataset['status']
        style = stl.get_style(experiment_type, status, color)
        parameters = dataset['parameters']

        # merging styles where kwargs is dominant
        style = style | kwargs

        plot_dataset(ax, 
                     xi=parameters['xi'], 
                     eta=parameters['eta'], 
                     label=dataset['label'], 
                     **style)

def plot_dataset (ax: plt.Axes, xi: float|list, eta: float|list, **kwargs):

    xi_range = isinstance(xi, (list, tuple))
    eta_range = isinstance(eta, (list, tuple))

    if not xi_range and not eta_range:
        return plot_point(ax, xi, eta, **kwargs)

    if xi_range and not eta_range:
        return plot_horizontal_range(ax, xi, eta, **kwargs)

    if not xi_range and eta_range:
        return plot_vertical_range(ax, xi, eta, **kwargs)

    return plot_rectangle(ax, xi, eta, **kwargs)

def plot_point(ax: plt.Axes, xi: float, eta: float, **style: object) -> None:

    # keys to change the style of the marker
    keys = ["marker", "markersize", "color", "markerfacecolor",
            "markeredgecolor", "label", "zorder"]
    
    # add the marker with the given style
    ax.plot(xi, eta, linestyle="none",
            **{k: v for k, v in style.items() if k in keys})

    # add label if given
    if 'label' in style:
        x_label, y_label = range_label_anchor(xi, eta, style.get('labelposition'))
        add_label(ax, x_label, y_label, label=style.get('label'), labelposition=style.get('labelposition'))

def plot_horizontal_range(ax: plt.Axes, xi: list, eta: float, **style: object) -> None:

    # keys to change the style of the horizontal line
    keys = ["color", "linestyle", "linewidth", "label", "zorder"]

    # add the horizontal line with the given style
    ax.hlines(eta, xi[0], xi[1],
              **{k: v for k, v in style.items() if k in keys})
    
    # add label if given
    if 'label' in style:
        x_label, y_label = range_label_anchor(xi, eta, style.get('labelposition'))
        add_label(ax, x_label, y_label, label=style.get('label'), labelposition=style.get('labelposition'))

def plot_vertical_range(ax: plt.Axes, xi: float, eta: list, **style: object) -> None:

    # keys to change the style of the vertical line
    keys = ["color", "linestyle", "linewidth", "label", "zorder"]

    # add the vertical line with the given style
    ax.vlines(xi, eta[0], eta[1],
              **{k: v for k, v in style.items() if k in keys})
    
    # add label if given
    if 'label' in style:
        x_label, y_label = range_label_anchor(xi, eta, style.get('labelposition'))
        add_label(ax, x_label, y_label, label=style.get('label'), labelposition=style.get('labelposition'))

def plot_rectangle(ax: plt.Axes, xi: list, eta: list, **style: object) -> None:

    # keys to change the style of the rectangle
    keys = ["label", "zorder", "linestyle"]

    color = style.pop('color', 'black')
    facecolor = to_rgba(color, style.pop('facealpha', 1.0))
    edgecolor = to_rgba(color, 1.0)

    # add the rectangle with the given style
    ax.fill_between(xi, eta[0], eta[1], facecolor=facecolor, edgecolor=edgecolor,
                    **{k: v for k, v in style.items() if k in keys})

    # add label if given
    if 'label' in style:
        x_label, y_label = range_label_anchor(xi, eta, style.get('labelposition'))
        add_label(ax, x_label, y_label, label=style.get('label'), labelposition=style.get('labelposition'))

def range_label_anchor(xi: float|list, eta: float|list, labelposition: str|None) -> tuple:

    if labelposition==None:
        labelposition = 'below'
    
    x0, x1 = xi if isinstance(xi, (list, tuple)) else (xi, xi)
    y0, y1 = eta if isinstance(eta, (list, tuple)) else (eta, eta)

    # Geometric centres for logarithmic axes
    xc = (x0 * x1) ** 0.5
    yc = (y0 * y1) ** 0.5

    anchors = {
        "above": (xc, y1),
        "below": (xc, y0),
        "left":  (x0, yc),
        "right": (x1, yc),
    }

    return anchors[labelposition]

def add_label(ax: plt.Axes, x: float, y: float, label: str, labelposition: str|None) -> None:

    if labelposition==None:
        labelposition = 'below'
    
    positions = {
        "above": (0, 5, "center", "bottom"),
        "below": (0, -5, "center", "top"),
        "left": (-5, 0, "right", "center"),
        "right": (5, 0, "left", "center"),
    }
    dx, dy, ha, va = positions[labelposition]

    ax.annotate(label, (x, y), xytext=(dx, dy), 
                    textcoords="offset points", ha=ha, va=va)

def draw_pw_class_projections (ax: plt.Axes) -> None:
    '''
    projection of PW-class facilities
    - xi/a0 is the range of typical values at these peak power
    - eta is the range for particle beams between 1-5 GeV colliding at 20 degrees
    '''
    style = {'color': '0.35', 'facealpha': 0.1, 'linestyle': '--'}
    plot_rectangle(ax, (50, 500), (0.0115, 0.0575), label='Multi-PW Class', **style)
    style = {'color': '0.65', 'facealpha': 0.1, 'linestyle': '--'}
    plot_rectangle(ax, (500, 5000), (0.0115, 0.0575), label='Multi-10PW Class', **style)

    labels = [
        (100, 0.025, "CALA", 0, "0.5"),
        (100, 0.040, "CoReLS", 0, "0.5"),
        (100, 0.016, "ZEUS", 0, "0.5"),
        (300, 0.034, "Apollon", 0, "0.5"),
        (300, 0.018, "ELI", 0, "0.5"),
        (1000, 0.026, "EP-OPAL", 0, "0.7"),
        (1000, 0.045, "SULF", 0, "0.5"),
        (1000, 0.015, "VULCAN", 0, "0.7"),
        (3000, 0.04, "SEL", 0, "0.5"),
        (3000, 0.02, "XCELS", 0, "0.7"),
    ]
    
    for x, y, text, rot, color in labels:
        ax.text(x, y, text, fontsize=11, color=color, rotation=rot, ha="center", va="center")
