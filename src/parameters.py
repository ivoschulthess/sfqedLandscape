import numpy as np

# (parameter_to_hold_constant, xaxis, yaxis)
PARAMETER_RELATIONS = {
    ("chi", "xi", "eta"): lambda x, value: value / x,
    ("chi", "eta", "xi"): lambda x, value: value / x,
    ("eta", "xi", "chi"): lambda x, value: value * x,
    ("eta", "chi", "xi"): lambda x, value: x / value,
    ("xi", "eta", "chi"): lambda x, value: value * x,
    ("xi", "chi", "eta"): lambda x, value: x / value,
}

def get_contour_values(parameter: str, value: float, xaxis: str, yaxis: str, x: np.ndarray) -> np.ndarray | None:
    """
    Return y(x) for a contour of constant `parameter`.
    Returns None if no relation is known for the requested combination.
    """

    relation = PARAMETER_RELATIONS.get(
        (parameter, xaxis, yaxis)
    )

    if relation is None:
        return None

    return relation(x, value)
