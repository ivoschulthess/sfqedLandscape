

def resolve_parameter(dataset: dict[str, Any], parameter: str):
    """
    Return a parameter value or range for one dataset.
    Resolution order:
    1. Directly stored parameter
    2. Conversion from other stored strong-field parameters
    3. Calculation from beam, laser and geometry metadata
    4. Raise ParameterResolutionError
    """

    # 1. Directly provided
    value = get_direct_parameter(dataset, parameter)
    if value is not None:
        return value

    # 2. Derive from other strong-field parameters
    value = derive_from_parameters(dataset, parameter)
    if value is not None:
        return value

    # # 3. Derive from experimental metadata
    # value = derive_from_metadata(dataset, parameter)
    # if value is not None:
    #     return value

    raise ValueError(
        f"Cannot resolve parameter '{parameter}' for dataset "
        f"'{dataset.get('label', '<unnamed>')}'."
    )


def get_direct_parameter(dataset: dict, parameter: str):
    parameters = dataset.get("parameters", {})
    return parameters.get(parameter)


def derive_from_parameters(dataset: dict, parameter: str):
    parameters = dataset.get("parameters", {})

    xi = parameters.get("xi")
    eta = parameters.get("eta")
    chi = parameters.get("chi")

    if parameter == "chi" and xi is not None and eta is not None:
        return multiply_ranges(xi, eta)

    if parameter == "eta" and chi is not None and xi is not None:
        return divide_ranges(chi, xi)

    if parameter == "xi" and chi is not None and eta is not None:
        return divide_ranges(chi, eta)

    return None

def as_range(value):
    """Convert a scalar or [min, max] to (min, max)."""
    if isinstance(value, (list, tuple)):
        if len(value) != 2:
            raise ValueError(f"Invalid range: {value}")
        return value[0], value[1]

    return value, value

def restore_range(vmin, vmax):
    """Return a scalar if possible, otherwise a range."""
    if vmin == vmax:
        return vmin
        
    return [vmin, vmax]

def multiply_ranges(a, b):
    amin, amax = as_range(a)
    bmin, bmax = as_range(b)
    
    return restore_range(amin * bmin, amax * bmax)

def divide_ranges(a, b):
    amin, amax = as_range(a)
    bmin, bmax = as_range(b)

    if bmin <= 0:
        raise ValueError("Division by zero.")

    return restore_range(amin / bmax, amax / bmin)