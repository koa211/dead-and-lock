# deadlock-postmortem

Postmortem is designed to display how you and everyone did in the lobby for any given match.

# Installation
```
git clone https://github.com/koa211/dead-and-lock.git
python -m venv venv
.\venv\Scripts\activate      # Windows
source venv/bin/activate     # macOS/Linux

pip install -r requirements.txt

cd deadnlock
python manage.py runserver
```
# Usage

Navigate to a match's postmortem page via its match ID (e.g. `/ranks/<match_id>/`) to see a
breakdown of every player in the lobby — team side, damage, and net worth — pulled live from
the Deadlock API.

![postmortem](/postmorem.png)

# Project Structure
deadnlock/ranks/ - the postmortem app: views, models, templates, and static assets
deadnlock/ranks/templates/ranks/ - HTML templates (index, match_details)
deadnlock/ranks/static/ranks/ - CSS and fonts

# What I learnt?
- Basics of Django (views, templates, URL routing, static files)
- Consuming a third-party REST API and parsing JSON responses
- Rendering matplotlib charts server-side and returning them as HTTP responses

# Whats next?
- Bad idea to parse json using regex matching a text dump. Walking through 'json.loads()' instead
- Add basic tests for correct output

