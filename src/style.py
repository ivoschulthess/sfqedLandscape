# style.py
# Central plotting style for the SFQED landscape.

# Common defaults applied to all datasets.
DEFAULT_STYLE = {
    "linewidth": 4,
    "markersize": 7,
    "alpha": 1.0,
}

# Marker shape encodes the experimental platform.
EXPERIMENT_MARKERS = {
    "electron_laser": "s",
    "gamma_laser": "v",
    "crystal": "^",
    "all_optical": "o",
}


# Line and marker filling encode the dataset status.
STATUS_STYLES = {
    "result": {
        "linestyle": "-",
        "fillstyle": "full",
        "facealpha": 0.8,
    },
    "projection": {
        "linestyle": "--",
        "fillstyle": "none",
        "facealpha": 0.1,
    },
}



def get_style(experiment_type, status, color):
    """Return the style for one experiment dataset."""

    style = DEFAULT_STYLE.copy()
    style.update(STATUS_STYLES[status])

    style["marker"] = EXPERIMENT_MARKERS[experiment_type]
    style["color"] = color
    style["markeredgecolor"] = color
    style["markerfacecolor"] = (
        color if style["fillstyle"] == "full" else "none"
    )

    return style