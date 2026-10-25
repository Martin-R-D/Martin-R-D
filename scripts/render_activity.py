import datetime as dt
import html
import json
import os
from pathlib import Path
import urllib.request

OUT = Path(__file__).resolve().parents[1] / 'assets' / 'activity.svg'
query = '''query($login: String!) { user(login: $login) { contributionsCollection { contributionCalendar { totalContributions weeks { contributionDays { date contributionCount } } } } } }'''
request = urllib.request.Request('https://api.github.com/graphql', data=json.dumps({'query': query, 'variables': {'login': os.environ['PROFILE_USER']}}).encode(), headers={'Authorization': 'Bearer ' + os.environ['GH_TOKEN'], 'Content-Type': 'application/json', 'User-Agent': 'profile-activity'})
with urllib.request.urlopen(request, timeout=30) as response:
    data = json.load(response)
if data.get('errors'):
    raise RuntimeError(data['errors'])
calendar = data['data']['user']['contributionsCollection']['contributionCalendar']
weeks = calendar['weeks']
values = [sum(day['contributionCount'] for day in week['contributionDays']) for week in weeks]
peak = max(values, default=0) or 1
parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="960" height="300" viewBox="0 0 960 300" role="img" aria-labelledby="title desc"><title id="title">GitHub contribution timeline</title><desc id="desc">Weekly GitHub contributions over the past year. Bar heights show contribution counts.</desc><rect width="960" height="300" rx="20" fill="#0b101c"/><rect x=".5" y=".5" width="959" height="299" rx="20" fill="none" stroke="#253047"/><g font-family="Arial, sans-serif"><text x="36" y="40" fill="#9caac2" font-size="12" letter-spacing="3">03 / ACTIVITY SIGNAL</text>']
parts += [f'<text x="36" y="82" fill="#f0f3ff" font-size="30" font-weight="700">{calendar["totalContributions"]:,}<tspan fill="#9caac2" font-size="15" font-weight="400"> contributions / past year</tspan></text>']
for y in (120, 165, 210):
    parts.append(f'<path d="M36 {y}H924" stroke="#202b40" stroke-dasharray="3 6"/>')
step = 888 / max(len(weeks), 1)
last_month = None
for i, (week, value) in enumerate(zip(weeks, values)):
    x = 36 + i * step
    height = max(2, value / peak * 104)
    color = '#69e3e4' if i == len(weeks)-1 else '#9c85ff'
    parts.append(f'<rect x="{x:.2f}" y="{220-height:.2f}" width="{step-4:.2f}" height="{height:.2f}" rx="3" fill="{color}" opacity="{0.35 + 0.65 * value / peak:.2f}"><title>Week of {week["contributionDays"][0]["date"]}: {value} contributions</title></rect>')
    date = dt.date.fromisoformat(week['contributionDays'][0]['date'])
    if date.month != last_month and i < len(weeks)-2:
        parts.append(f'<text x="{x:.2f}" y="244" fill="#9caac2" font-size="10">{date.strftime("%b").upper()}</text>')
        last_month = date.month
parts.append(f'<text x="36" y="278" fill="#7888a5" font-size="11">WEEKLY CONTRIBUTIONS · GITHUB DATA</text><text x="924" y="278" text-anchor="end" fill="#7888a5" font-size="11">UPDATED {dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")} UTC</text></g></svg>')
OUT.write_text(''.join(parts))
