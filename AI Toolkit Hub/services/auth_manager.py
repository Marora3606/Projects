# Auth Manager Service
# Handles authentication and authorization

import os
import secrets as _secrets
import jwt
import datetime
from typing import Optional, Dict, Any


# =============================================================================
# LEARN: WHY THIS BLOCK EXISTS — the bug that used to be here
#
# The old code read:
#     def __init__(self, secret_key: str = "your-secret-key"):
#     ...
#     auth_manager = AuthManager()        # <- uses the placeholder default
#
# A JWT is not encrypted. Anyone can decode one and read its contents — paste a
# token into jwt.io and you will see username and role in plain text. What stops
# tampering is the SIGNATURE, which is computed from the payload plus a secret
# only the server knows.
#
# So if the secret is the literal string "your-secret-key", anyone can build
# their own token claiming {"role": "admin"}, sign it with that same well-known
# string, and check_permission() below will happily let them in. The whole role
# hierarchy becomes decorative.
#
# LEARN: This is the same root cause as the hardcoded API keys in JARVIS — a
# placeholder default that was never replaced, so it silently became the real
# production value. When you write a default, ask: "what happens if nobody ever
# overrides this?"
# =============================================================================
def _load_secret_key() -> str:
    """Find a JWT signing key, in order of preference.

    Returns:
        The configured signing key, or a freshly generated random one if none
        is configured. Never returns a fixed, guessable value.
    """
    # 1. Environment variable — works everywhere, including plain `python` runs.
    key = os.environ.get("JWT_SECRET_KEY")
    if key:
        return key

    # 2. Streamlit's secrets.toml. Wrapped in try/except because importing
    #    streamlit outside a running Streamlit app raises, and this module
    #    should still be usable from a normal script or a test.
    try:
        import streamlit as st
        key = st.secrets.get("JWT_SECRET_KEY")
        if key:
            return key
    except Exception:
        pass

    # 3. Last resort: a strong random key generated fresh each time the app
    #    starts. Nothing is forgeable, but tokens stop being valid on restart.
    # LEARN: This is a deliberate trade-off. Failing hard would be "safer" but
    #    would break the app for anyone who clones it without configuring a key.
    #    Degrading to random keeps it running AND keeps it secure — the only
    #    cost is that sessions do not survive a restart, which for a Streamlit
    #    app is already true.
    print(
        "[AI Toolkit Hub] JWT_SECRET_KEY is not set — generated a random key "
        "for this run. Logins will not persist across restarts. Set it in "
        ".streamlit/secrets.toml or as an environment variable to fix this."
    )
    # LEARN: `secrets` (the stdlib module) is the cryptographically secure
    # random source. Never use the `random` module for anything security
    # related — it is predictable by design, for reproducible simulations.
    return _secrets.token_urlsafe(32)


class AuthManager:
    def __init__(self, secret_key: Optional[str] = None):
        # LEARN: The default is None, not a usable-looking string. If a caller
        # forgets to pass a key, we go and find a real one rather than quietly
        # falling back to something insecure.
        self.secret_key = secret_key or _load_secret_key()

    def generate_token(self, user_id: int, username: str, role: str) -> str:
        """Generate JWT token for user"""
        payload = {
            'user_id': user_id,
            'username': username,
            'role': role,
            # LEARN: 'exp' (expiry) and 'iat' (issued at) are REGISTERED CLAIMS —
            # standard field names defined by the JWT spec. PyJWT checks 'exp'
            # automatically on decode and raises ExpiredSignatureError.
            # LEARN: utcnow() is deprecated from Python 3.12 and will be removed.
            # The modern form is now(timezone.utc), which returns a timezone-AWARE
            # datetime. The old one returned a naive datetime that merely happened
            # to hold UTC — a classic source of off-by-hours bugs.
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24),
            'iat': datetime.datetime.now(datetime.timezone.utc),
        }
        token = jwt.encode(payload, self.secret_key, algorithm='HS256')
        return token

    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify and decode JWT token"""
        try:
            # LEARN: Passing algorithms=['HS256'] as an allowlist is essential.
            # Without it a library may accept the algorithm named INSIDE the
            # token, and an attacker can set it to "none" — meaning "no
            # signature required". That is the classic JWT "alg=none" attack.
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            # LEARN: Token was validly signed but is past its 'exp'.
            return None
        except jwt.InvalidTokenError:
            # LEARN: Signature did not match, or the token is malformed. This is
            # the branch that now catches forged tokens — it did not before,
            # because forging one required a secret everybody already knew.
            return None

    def get_user_from_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Extract user info from token"""
        payload = self.verify_token(token)
        if payload:
            return {
                'user_id': payload['user_id'],
                'username': payload['username'],
                'role': payload['role']
            }
        return None

    def check_permission(self, user_role: str, required_role: str) -> bool:
        """Check if user has required permission"""
        # LEARN: A numeric hierarchy means one >= comparison covers every case,
        # instead of writing out each allowed pair. Good design — and it was
        # always sound; the weak signing key was what undermined it.
        role_hierarchy = {
            'user': 1,
            'analyst': 2,
            'admin': 3
        }

        # LEARN: .get(role, 0) means an unknown role scores 0 and is denied
        # everything. Defaulting to the LEAST privilege is called "fail closed",
        # and it is the correct default for anything security related.
        user_level = role_hierarchy.get(user_role, 0)
        required_level = role_hierarchy.get(required_role, 0)

        return user_level >= required_level


# Global instance
auth_manager = AuthManager()
