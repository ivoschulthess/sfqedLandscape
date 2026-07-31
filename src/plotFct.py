import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba
from matplotlib.patches import Rectangle
from scipy.constants import physical_constants
import yaml
import style as stl

from parameters import get_contour_values


# fine-structure constant alpha ~1/137
fineStructureConstant = physical_constants['fine-structure constant'][0]

# chi value where QED becomes fully nonperturbative (alpha*chi^(2/3)=1)
chi_nonperturbative = fineStructureConstant ** (-1.5)

############################
# CONFIGURATION PARAMETERS #
############################

AXES = {
    "a0": {
        "parameter": "xi",
        "label": r"$a_0$",
        "scale": "log",
        "min": 0.1,
        "max": 10000.0,
    },
    "xi": {
        "parameter": "xi",
        "label": r"$\xi$",
        "scale": "log",
        "min": 1e-1,
        "max": 1e4,
    },
    "eta": {
        "parameter": "eta",
        "label": r"$\eta$",
        "scale": "log",
        "min": 3e-4,
        "max": 1e1,
    },
    "chi": {
        "parameter": "chi",
        "label": r"$\chi$",
        "scale": "log",
        "min": 1e-4,
        "max": 1e4,
    },
    "RR": {
        "parameter": "RR",
        "label": r"$\mathcal{R}$",
        "scale": "log",
        "min": 0.0001,
        "max": 10.0,
    },
}

PARAMETERS = {
    "xi": {
        "contour_levels": [
            1e-4, 1e-3, 1e-2, 1e-1, 1e0, 1e1, 1e2, 1e3, 1e4, 1e5, 1e6, 1e7
        ],
        "reference_lines": [
            {
                "value": 1.0,
                "label": r"$\xi=1$",
                "style": stl.REFERENCE,
                "label_position": 0.3
            },
        ],
    },

    "eta": {
        "contour_levels": [
            1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1e0, 1e1, 1e2, 1e3, 1e4
        ],
        "reference_lines": [
            {
                "value": 1.0,
                "label": r"$\eta=1$",
                "style": stl.REFERENCE,
                "label_position": 0.3
            },
        ],
    },

    "chi": {
        "contour_levels": [
            1e-4, 1e-3, 1e-2, 1e-1, 1e0, 1e1, 1e2, 1e3, 1e4,
        ],
        "reference_lines": [
            {
                "value": 1.0,
                "label": r"$\chi=1$",
                "style": stl.REFERENCE,
                "label_position": 0.3
            },
            {
                "value": chi_nonperturbative,
                "label": r"$(\alpha\chi)^{2/3}=1$",
                "style": {**stl.REFERENCE, "ls": "--",},
                "label_position": 0.3
            },
        ],
    },
}


NCS_REGIMES = [
    {
        "label": "Linear QED",

        "condition": lambda p: (
            (p["xi"] < 0.3)
            & (p["chi"] < chi_nonperturbative)
        ),

        "label_positions": {
            ("xi", "eta"): {
                "x": 0.18,
                "y": 3,
                "rotation": 90,
            },
            ("xi", "chi"): {
                "x": 0.18,
                "y": 100.0,
                "rotation": 90,
            },
            ("eta", "chi"): {
                "x": 3,
                "y": 0.001,
                "rotation": 0,
            },
        },

        "style": {
            "color": "orange",
            "alpha": 0.1,
        },

        "label_style": {
            "bbox": {
                "facecolor": "orange",
                "edgecolor": "none",
                "alpha": 0.7,
            },
        },
    },

    {
        "label": "Harmonics",

        "condition": lambda p: (
            (p["xi"] >= 0.3)
            & (p["xi"] < 1.0)
            & (p["chi"] < chi_nonperturbative)
        ),

        "label_positions": {
            ("xi", "eta"): {
                "x": 0.55,
                "y": 3,
                "rotation": 90,
            },
            ("xi", "chi"): {
                "x": 0.55,
                "y": 100.0,
                "rotation": 90,
            },
            ("eta", "chi"): {
                "x": 3,
                "y": 2.0,
                "rotation": 0,
            },
        },

        "style": {
            "color": "lightblue",
            "alpha": 0.2,
        },

        "label_style": {
            "bbox": {
                "facecolor": "lightblue",
                "edgecolor": "none",
                "alpha": 0.7,
            },
        },
    },

    {
        "label": "Nonperturbative at\nsmall coupling",

        "condition": lambda p: (
            (p["xi"] >= 1.0)
            & (p["chi"] < chi_nonperturbative)
        ),

        "label_positions": {
            ("xi", "eta"): {
                "x": 30.0,
                "y": 3,
                "rotation": 0,
            },
            ("xi", "chi"): {
                "x": 10.0,
                "y": 200.0,
                "rotation": 0,
            },
            ("eta", "chi"): {
                "x": 0.25,
                "y": 100.0,
                "rotation": 0,
            },
        },

        "style": {
            "color": "yellow",
            "alpha": 0.1,
        },

        "label_style": {
            "bbox": {
                "facecolor": "yellow",
                "edgecolor": "none",
                "alpha": 0.7,
            },
        },
    },

    {
        "label": "Fully non-\nperturbative",

        "condition": lambda p: (
            p["chi"] >= chi_nonperturbative
        ),

        "label_positions": {
            ("xi", "eta"): {
                "x": 2700.0,
                "y": 3.0,
                "rotation": 0,
            },
            ("xi", "chi"): {
                "x": 20.0,
                "y": 4000.0,
                "rotation": 0,
            },
            ("eta", "chi"): {
                "x": 0.1,
                "y": 4000.0,
                "rotation": 0,
            },
        },

        "style": {
            "color": "red",
            "alpha": 0.1,
        },

        "label_style": {
            "bbox": {
                "facecolor": "red",
                "edgecolor": "none",
                "alpha": 0.7,
            },
        },
    },
]

####################
# HELPER FUNCTIONS #
####################

def _log_interpolate(vmin: float, vmax: float, position: float) -> float:
    return 10 ** (
        np.log10(vmin)
        + position * (np.log10(vmax) - np.log10(vmin))
    )

def _plot_segment(ax: plt.Axes, x: np.ndarray, y, **kwargs) -> None:
    
    yy = y(x) if callable(y) else np.full_like(x, float(y), dtype=float)
    mask = (yy > 0) & np.isfinite(yy)
    ax.plot(x[mask], yy[mask], **kwargs)

def _fill_between(ax: plt.Axes, x: np.ndarray, y1, y2, **kwargs) -> None:
    
    yy1 = y1(x) if callable(y1) else np.full_like(x, float(y1), dtype=float)
    yy2 = y2(x) if callable(y2) else np.full_like(x, float(y2), dtype=float)
    mask = (yy1 > 0) & (yy2 > 0) & np.isfinite(yy1) & np.isfinite(yy2)
    ax.fill_between(x[mask], yy1[mask], yy2[mask], **kwargs)

def _get_label_rotation(ax: plt.Axes, xvalues: np.ndarray, yvalues: np.ndarray, index: int,) -> float:
    """
    Return the local contour angle in display coordinates.
    """

    if len(xvalues) < 2:
        return 0.0

    step = max(1, len(xvalues) // 100)

    i0 = max(0, index - step)
    i1 = min(len(xvalues) - 1, index + step)

    if i0 == i1:
        return 0.0

    points = ax.transData.transform([
        [xvalues[i0], yvalues[i0]],
        [xvalues[i1], yvalues[i1]],
    ])

    dx = points[1, 0] - points[0, 0]
    dy = points[1, 1] - points[0, 1]

    angle = np.degrees(np.arctan2(dy, dx))

    return angle

def _draw_parameter_contour(ax: plt.Axes, parameter: str, value: float, **style) -> bool:
    """
    Draw a contour of constant `parameter`.
    Returns True if the contour could be drawn, otherwise False.
    """

    xaxis = ax.sfqed_axes["x"]
    yaxis = ax.sfqed_axes["y"]

    # Parameter is directly represented by the x-axis
    if parameter == xaxis:
        ax.axvline(value, **style)
        return True

    # Parameter is directly represented by the y-axis
    if parameter == yaxis:
        ax.axhline(value, **style)
        return True

    # Parameter must be derived from the two plotted axes
    xmin, xmax = ax.get_xlim()
    x = np.geomspace(xmin, xmax, 1000)

    y = get_contour_values(
        parameter=parameter,
        value=value,
        xaxis=xaxis,
        yaxis=yaxis,
        x=x,
    )

    if y is None:
        return False

    valid = np.isfinite(y) & (y > 0)
    if not np.any(valid):
        return False

    ax.plot(x[valid], y[valid], **style)
    return True

def _get_parameter_grid(
    parameter: str,
    xparameter: str,
    yparameter: str,
    xvalues: np.ndarray,
    yvalues: np.ndarray,
) -> np.ndarray:
    """Return one physical parameter on the current two-dimensional grid."""

    if parameter == xparameter:
        return xvalues

    if parameter == yparameter:
        return yvalues

    available = {
        xparameter: xvalues,
        yparameter: yvalues,
    }

    if parameter == "chi":
        return available["xi"] * available["eta"]

    if parameter == "xi":
        return available["chi"] / available["eta"]

    if parameter == "eta":
        return available["chi"] / available["xi"]

    raise ValueError(f"Cannot calculate parameter {parameter!r}")

def _get_regime_label_position(
    regime: dict,
    xparameter: str,
    yparameter: str,
) -> dict | None:
    positions = regime.get("label_positions", {})

    key = (xparameter, yparameter)

    if key in positions:
        return positions[key]

    reversed_key = (yparameter, xparameter)

    if reversed_key not in positions:
        return None

    reversed_position = positions[reversed_key]

    position = dict(reversed_position)

    position["x"] = reversed_position["y"]
    position["y"] = reversed_position["x"]

    # Rotation is defined in display coordinates.
    rotation = reversed_position.get("rotation", 0.0)
    position["rotation"] = 90.0 - rotation

    return position

def _draw_regime_label(
    ax: plt.Axes,
    regime: dict,
    xparameter: str,
    yparameter: str,
) -> None:
    position = _get_regime_label_position(
        regime,
        xparameter,
        yparameter,
    )

    if position is None:
        return

    x = position["x"]
    y = position["y"]

    xmin, xmax = sorted(ax.get_xlim())
    ymin, ymax = sorted(ax.get_ylim())

    if not (
        xmin <= x <= xmax
        and ymin <= y <= ymax
    ):
        return

    label_style = regime.get("label_style", {})

    ax.annotate(
        regime["label"],
        xy=(x, y),
        xytext=position.get(
            "offset",
            label_style.get("offset", (0, 0)),
        ),
        textcoords="offset points",
        rotation=position.get(
            "rotation",
            label_style.get("rotation", 0),
        ),
        rotation_mode="anchor",
        ha=position.get(
            "ha",
            label_style.get("ha", "center"),
        ),
        va=position.get(
            "va",
            label_style.get("va", "center"),
        ),
        fontsize=label_style.get("fontsize", 12),
        bbox=label_style.get("bbox"),
        zorder=label_style.get("zorder", 2),
    )

def _complete_parameter_point(
    point: dict[str, float],
) -> dict[str, float]:
    point = dict(point)

    if "chi" not in point and "xi" in point and "eta" in point:
        point["chi"] = point["xi"] * point["eta"]

    elif "xi" not in point and "chi" in point and "eta" in point:
        point["xi"] = point["chi"] / point["eta"]

    elif "eta" not in point and "chi" in point and "xi" in point:
        point["eta"] = point["chi"] / point["xi"]

    return point
    
def _load_experiment (fName: str) -> dict:

    with open(fName) as file:
        data = yaml.safe_load(file)

    return data

    
################
# FIGURE SETUP #
################

def setup_axes(ax: plt.Axes, title: str='', xaxis: str='a0', yaxis: str='eta') -> None:

    """
    Configure an SFQED parameter-space plot.
    """

    if xaxis not in AXES:
        raise ValueError(
            f"Unknown x-axis parameter {xaxis!r}. "
            f"Available parameters: {', '.join(AXES)}."
        )

    if yaxis not in AXES:
        raise ValueError(
            f"Unknown y-axis parameter {yaxis!r}. "
            f"Available parameters: {', '.join(AXES)}."
        )
    
    X = AXES[xaxis]
    Y = AXES[yaxis]
    
    if X["parameter"] == Y["parameter"]:
        raise ValueError(
            "The x-axis and y-axis must represent different parameters."
        )

    # store metadata in the axis for other setup functions
    ax.sfqed_axes = {"x": X["parameter"], "y": Y["parameter"],}
    
    ax.set_xscale(X['scale'])
    ax.set_yscale(Y['scale'])
    ax.set_xlim(X['min'], X['max'])
    ax.set_ylim(Y['min'], Y['max'])
    ax.set_xlabel(X['label'], fontsize=16)
    ax.set_ylabel(Y['label'], fontsize=16)

    if title!='':
        ax.set_title(title, fontsize=20)

    ax.set_axisbelow(True)
    ax.grid(which='major', color='0.8', linewidth=0.6)
    ax.grid(which='minor', color='0.9', linewidth=0.4)
            
def draw_common_reference_lines(ax: plt.Axes) -> None:

    xaxis = ax.sfqed_axes["x"]
    yaxis = ax.sfqed_axes["y"]

    for parameter, definition in PARAMETERS.items():

        # Add contour grid only when the parameter is not already an axis
        if parameter not in {xaxis, yaxis}:
            for value in definition.get("contour_levels", []):
                _draw_parameter_contour(
                    ax=ax,
                    parameter=parameter,
                    value=value,
                    color="0.8",
                    lw=0.6,
                    zorder=1,
                )

        # Draw physically meaningful lines in every representation
        for reference in definition.get("reference_lines", []):
            _draw_parameter_contour(
                ax=ax,
                parameter=parameter,
                value=reference["value"],
                **reference["style"],
            )

def draw_common_labels(ax: plt.Axes) -> None:
    
    xparameter = ax.sfqed_axes["x"]
    yparameter = ax.sfqed_axes["y"]

    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()

    for parameter, definition in PARAMETERS.items():
        for reference in definition.get("reference_lines", []):
            label = reference.get("label")
            label_position = reference.get("label_position")

            if label is None or label_position is None:
                continue
            
            # Parameter is the x-axis: vertical reference line
            if parameter == xparameter:
                x = reference["value"]
                y = _log_interpolate(ymin, ymax, label_position)
                rotation = 90.0
                offset = (-2, 0)

            # Parameter is the y-axis: horizontal reference line
            elif parameter == yparameter:
                x = _log_interpolate(xmin, xmax, label_position)
                y = reference["value"]
                rotation = 0.0
                offset = (0, 2)

            # Parameter is represented by a derived contour
            else:
                xvalues = np.geomspace(xmin, xmax, 1000)

                yvalues = get_contour_values(
                    parameter=parameter,
                    value=reference["value"],
                    xaxis=xparameter,
                    yaxis=yparameter,
                    x=xvalues,
                )

                if yvalues is None:
                    continue

                mask = (
                    np.isfinite(xvalues)
                    & np.isfinite(yvalues)
                    & (xvalues >= xmin)
                    & (xvalues <= xmax)
                    & (yvalues >= ymin)
                    & (yvalues <= ymax)
                )

                xvisible = xvalues[mask]
                yvisible = yvalues[mask]

                if len(xvisible) == 0:
                    continue

                index = round(label_position * (len(xvisible) - 1))
                x = xvisible[index]
                y = yvisible[index]
                rotation = _get_label_rotation(ax, xvisible, yvisible, index,)
                offset = (0, 2)

            ax.annotate(label, xy=(x, y), xytext=offset, textcoords="offset points", rotation=rotation, rotation_mode="anchor", ha="center", va="bottom", **stl.REFERENCE_LABEL,)


###################
# PHYSICS REGIMES #
###################

def draw_ncs_regimes(ax: plt.Axes, resolution: int=1000) -> None:
    
    xparameter = ax.sfqed_axes["x"]
    yparameter = ax.sfqed_axes["y"]

    xmin, xmax = sorted(ax.get_xlim())
    ymin, ymax = sorted(ax.get_ylim())

    x = np.geomspace(xmin, xmax, resolution)
    y = np.geomspace(ymin, ymax, resolution)

    xx, yy = np.meshgrid(x, y)

    parameters = {
        parameter: _get_parameter_grid(
            parameter, xparameter, yparameter, xx, yy)
        for parameter in ("xi", "eta", "chi")
    }

    for regime in NCS_REGIMES:
        mask = regime["condition"](parameters)

        values = np.where(mask, 1.0, np.nan)

        ax.contourf(xx, yy, values, levels=[0.5, 1.5],
            colors=[regime["style"]["color"]],
            alpha=regime["style"].get("alpha", 1.0),
            antialiased=False,
            zorder=regime["style"].get("zorder", -20),
        )

        _draw_regime_label(ax, regime, xparameter, yparameter)

def draw_nbw_regimes (ax: plt.Axes) -> None:

    _fill_between(ax, np.geomspace(0.001, 10000, 1000), lambda xx: 2 * (1 + xx**2), 100, color="orange", edgecolor="none", linewidth=0, alpha=0.1)
    ax.text(0.22, 6, "Linear QED", fontsize=12, ha="center", bbox=dict(facecolor="orange", edgecolor="none", alpha=0.7))
    _plot_segment(ax, np.geomspace(0.001, 10000, 1000), lambda xx: 2 * (1 + xx**2), color="orange", ls="--", lw=1.2)
    ax.text(0.12, 2.8, r"$\eta=2(1+\xi^2)$", fontsize=12, color="orange")

    _fill_between(ax, np.geomspace(0.001, 10000, 1000), lambda xx: 0.5 * (1 + xx**2), lambda xx: 2 * (1 + xx**2), color="lightblue", edgecolor="none", linewidth=0, alpha=0.1)
    for n in [2,3,4]:
        _plot_segment(ax, np.geomspace(0.001, 10000, 1000), lambda xx, n=n: (2.0 / n) * (1 + xx**2), color="lightblue", ls="--", lw=1.2)
    ax.text(1.15, 3, "Harmonics", fontsize=12, ha="center", bbox=dict(facecolor="lightblue", edgecolor="none", alpha=0.7))

    _fill_between(ax, np.geomspace(0.001, 0.5, 1000), 0.0001, lambda xx: 0.5 * (1 + xx**2), color="purple", edgecolor="none", linewidth=0, alpha=0.1)
    ax.text(0.225, 0.013, "Multiphoton\nperturbative", fontsize=12, ha="center", bbox=dict(facecolor="purple", edgecolor="none", alpha=0.7))
    
    _fill_between(ax, np.geomspace(3, 10000, 1000), lambda xx: 0.5 / xx, 1e-5, color="green", edgecolor="none", linewidth=0, alpha=0.1)
    ax.text(10, 0.005, "Non-analytic\npair creation", fontsize=12, ha="center", bbox=dict(facecolor="green", edgecolor="none", alpha=0.7))
    
    _fill_between(ax, np.geomspace(0.5, 10000, 1000), lambda xx: np.where(xx>3, np.maximum(1e-5, 0.5 / xx), 1e-5), lambda xx: np.minimum(0.5 * (1 + xx**2), chi_nonperturbative / xx), color="yellow", edgecolor="none", linewidth=0, alpha=0.1)
    ax.text(30, 1.5, "Nonperturbative at\nsmall coupling", fontsize=12, ha="center", bbox=dict(facecolor="yellow", edgecolor="none", alpha=0.7))

    _fill_between(ax, np.geomspace(0.001, 10000, 1000), lambda xx: chi_nonperturbative / xx, 100, color="red", edgecolor="none", linewidth=0, alpha=0.1)
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

    ax.text(6500, 0.0257, '1-5 GeV\nat 20°', rotation=90, linespacing=0.9, ha="center", va="center")
    
    labels = [
        (89, 0.0257, "CALA"),
        (89, 0.0440, "CoReLS"),
        (89, 0.0150, "ZEUS"),
        (281, 0.0385, "Apollon"),
        (281, 0.0172, "ELI"),
        (889, 0.0440, "SULF"),
        (2811, 0.0440, "SEL"),
        (1581, 0.0257, "NSF-OPAL"),
        (1581, 0.0150, "VULCAN 20-20"),
        # XCELS not shown for now since status unknown 
        # and no response from corresponding authors of XCELS paper
        # (3000, 0.02, "XCELS"),
    ]
    for x, y, text in labels:
        ax.text(x, y, text, fontsize=11, color="0.5", ha="center", va="center")
