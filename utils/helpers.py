def safe_float(x):
    try:
        return float(x)
    except:
        return None
