def validate_registration(data):
    errors = []
    if not data.get("name"):
        errors.append("Name is required.")
    if not data.get("email"):
        errors.append("Email is required.")
    if not data.get("password"):
        errors.append("Password is required.")
    if data.get("role") not in ("Admin", "User"):
        errors.append("Role must be 'Admin' or 'User'.")
    return errors

def validate_login(data):
    errors = []
    if not data.get("email"):
        errors.append("Email is required.")
    if not data.get("password"):
        errors.append("Password is required.")
    return errors
