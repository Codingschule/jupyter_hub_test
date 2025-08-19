import json
from nativeauthenticator import NativeAuthenticator

def apply_auth(
    c,
    users_file: str,
    *,
    min_password_len: int = 3,
    username_pattern: str = r'^[a-zA-Z0-9._%+\-@]+$'
):


    class AutoApproveAuthenticator(NativeAuthenticator):
        def add_user(self, username, *args, **kwargs):
            allowed_set = set()
            try:
                with open(users_file, encoding="utf-8") as f:
                    raw = json.load(f)

                if isinstance(raw, dict):
                    for u in (raw.get("users") or []):
                        name = (u.get("name") or u.get("username") or "").strip()
                        if name:
                            allowed_set.add(name)
                    for name in (raw.get("allowed") or []):
                        if name:
                            allowed_set.add(str(name).strip())
                    for name in (raw.get("admins") or []):
                        if name:
                            allowed_set.add(str(name).strip())
                elif isinstance(raw, list):
                    for name in raw:
                        if name:
                            allowed_set.add(str(name).strip())
            except Exception:
                pass

            if username in allowed_set:
                kwargs["approved"] = True
            return super().add_user(username, *args, **kwargs)

    
    c.JupyterHub.authenticator_class = AutoApproveAuthenticator
    c.NativeAuthenticator.admin_approval = False
    c.NativeAuthenticator.minimum_password_length = min_password_len
    c.Authenticator.username_pattern = username_pattern