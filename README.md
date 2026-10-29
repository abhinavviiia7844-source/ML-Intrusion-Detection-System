# Secure Web Application (Beginner Project)

A beginner-friendly Flask application demonstrating secure registration, login, password hashing, SQLite storage, parameterized SQL queries, session handling, basic security headers, and server-side input validation.

## Requirements
- Python 3.10 or newer
- VS Code (optional)

## Run on Windows
Open a terminal in this folder and run:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

If PowerShell blocks activation, you can run the environment's Python directly:
```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

Open `http://127.0.0.1:5000` in your browser. Register an account and log in.

## Security features included
- Passwords are stored as salted hashes using Werkzeug, never as plain text.
- SQL statements use placeholders/parameterized queries.
- User input is validated on the server.
- Session cookies are HttpOnly and SameSite=Lax.
- Basic browser security headers are added.
- Dashboard routes require an authenticated session.
- Logout uses POST rather than a GET link.

## Important limitations
This is an educational project, not a production-ready authentication service. Before real deployment, add CSRF protection, rate limiting, password-reset flows, secure secret management, HTTPS, logging/monitoring, and security testing. Set a strong `FLASK_SECRET_KEY` environment variable before deployment. Set `COOKIE_SECURE=1` only when using HTTPS. Never publish the development secret or a database containing real user data.

## GitHub checklist
1. Add a clear project description and screenshots.
2. Do not commit `.venv/`, `users.db`, or secrets.
3. Add a `.gitignore` before publishing.
4. Explain that this is a learning/demo project.
