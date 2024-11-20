import jwt
import datetime

SECRET_KEY = "your-secret-key"

def generate_token(user):
    payload = {
        "id": user["id"],
        "role": user["role"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def token_required(f):
    def decorator(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "Token is missing"}), 401
        try:
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = decoded_token
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        return f(current_user, *args, **kwargs)
    return decorator
