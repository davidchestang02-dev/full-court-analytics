def normalize_team_name(name):
    name = name.replace("St.", "State")
    name = name.replace("UNC", "North Carolina")
    # Add more rules as needed
    return name
