from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from datetime import date, timedelta

app = FastAPI()

# === CONFIGURATION ===
start_date = date(2025, 9, 16)
end_date = date(2026, 6, 30)
practice_days = {1, 3, 4, 6}  # Tue, Thu, Fri, Sun

public_holidays = {
    date(2025, 12, 25),  # Christmas
    date(2026, 1, 1),    # New Year's Day
    date(2026, 2, 16),   # Family Day
    date(2026, 4, 3),    # Good Friday
    date(2026, 4, 5),    # Easter Sunday
    date(2026, 5, 18),   # Victoria Day
}

excluded_ranges = [
    (date(2025, 11, 7), date(2025, 11, 9)),
    (date(2025, 11, 28), date(2025, 11, 30)),
    (date(2025, 12, 14), date(2025, 12, 14)),
    (date(2025, 12, 20), date(2025, 12, 21)),
    (date(2026, 1, 16), date(2026, 1, 18)),
    (date(2026, 2, 13), date(2026, 2, 15)),
    (date(2026, 3, 7), date(2026, 3, 8)),
    (date(2026, 3, 27), date(2026, 3, 29)),
    (date(2026, 4, 23), date(2026, 4, 26)),
    (date(2026, 5, 8), date(2026, 5, 10)),
    (date(2026, 5, 22), date(2026, 5, 24)),
    (date(2026, 6, 5), date(2026, 6, 7)),
    (date(2026, 6, 20), date(2026, 6, 21)),
]

def get_excluded_dates():
    excluded = set()
    for start, end in excluded_ranges:
        d = start
        while d <= end:
            excluded.add(d)
            d += timedelta(days=1)
    return excluded

def count_practices_up_to(target_date):
    excluded = get_excluded_dates()
    count = 0
    current = start_date
    while current <= min(target_date, end_date):
        if current.weekday() in practice_days:
            if current not in public_holidays and current not in excluded:
                count += 1
        current += timedelta(days=1)
    return count

@app.get("/", response_class=HTMLResponse)
def countdown():
    today = date.today()
    total_practices = count_practices_up_to(end_date)
    completed = count_practices_up_to(today)
    remaining = max(total_practices - completed, 0)

    html = f"""
    <html>
    <head>
        <meta http-equiv="refresh" content="86400"> <!-- refresh 1x/day -->
        <title>Swim Practice Countdown</title>
        <style>
            body {{
                font-family: 'Arial', sans-serif;
                background-color: #0d1b2a;
                color: #e0e1dd;
                text-align: center;
                padding-top: 100px;
            }}
            h1 {{
                font-size: 3em;
                color: #00b4d8;
            }}
            p {{
                font-size: 1.5em;
            }}
        </style>
    </head>
    <body>
        <h1>🏊 Swim Practice Countdown</h1>
        <p><strong>Total practices:</strong> {total_practices}</p>
        <p><strong>Completed:</strong> {completed}</p>
        <p><strong>Remaining:</strong> {remaining}</p>
        <p><em>Last updated: {today}</em></p>
    </body>
    </html>
    """
    return HTMLResponse(content=html)
