# Security tickets: secrets

| ID | Finding | File | Severity | Action | Status |
|----|---------|------|----------|--------|--------|
| SEC-1 | AWS Access Key ID hardcoded | app/config.py:2 | High | Move to env var, revoke key | Fixed (PR fix/secrets) |
| SEC-2 | AWS Secret Access Key hardcoded | app/config.py:3 | Critical | Move to env var, revoke key | Fixed (PR fix/secrets) |
| SEC-3 | GitLab token hardcoded | app/config.py:4 | High | Move to env var, revoke token | Fixed (PR fix/secrets) |
| SEC-4 | DB password hardcoded | app/config.py:5 | High | Move to env var | Fixed (PR fix/secrets) |
| SEC-5 | SECRET_KEY in Dockerfile ENV | Dockerfile:2 | Medium | Pass at runtime | Fixed (PR fix/secrets) |
