import json
import os
import urllib.request
from pathlib import Path

username = os.environ.get("GITHUB_REPOSITORY", "zeroalek/zeroalek").split("/")[0]
token = os.environ["GITHUB_TOKEN"]
request = urllib.request.Request(
    f"https://api.github.com/users/{username}",
    headers={"Accept": "application/vnd.github+json", "Authorization": f"Bearer {token}", "X-GitHub-Api-Version": "2022-11-28"},
)
with urllib.request.urlopen(request, timeout=20) as response:
    user = json.load(response)

repos = []
page = 1
while True:
    req = urllib.request.Request(
        f"https://api.github.com/users/{username}/repos?per_page=100&page={page}&type=owner",
        headers={"Accept": "application/vnd.github+json", "Authorization": f"Bearer {token}"},
    )
    with urllib.request.urlopen(req, timeout=20) as response:
        batch = json.load(response)
    if not batch:
        break
    repos.extend(batch)
    if len(batch) < 100:
        break
    page += 1

stars = sum(repo.get("stargazers_count", 0) for repo in repos)
public_repos = user.get("public_repos", 0)
followers = user.get("followers", 0)
following = user.get("following", 0)

items = [("PUBLIC REPOS", public_repos), ("STARS EARNED", stars), ("FOLLOWERS", followers), ("FOLLOWING", following)]
svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="495" height="155" viewBox="0 0 495 155">',
       '<rect x="0.5" y="0.5" width="494" height="154" rx="8" fill="#0d1117" stroke="#30363d"/>',
       '<text x="24" y="31" fill="#39a96b" font-family="Arial,sans-serif" font-size="13" font-weight="bold" letter-spacing="1.5">GITHUB OVERVIEW</text>']
positions = [(24, 78), (260, 78), (24, 127), (260, 127)]
for (label, value), (x, y) in zip(items, positions):
    svg.append(f'<text x="{x}" y="{y}" fill="#c9d1d9" font-family="Arial,sans-serif" font-size="21" font-weight="bold">{value}</text>')
    svg.append(f'<text x="{x+48 if value < 10 else x+58}" y="{y}" fill="#8b949e" font-family="Arial,sans-serif" font-size="10" letter-spacing="1">{label}</text>')
svg.append('</svg>')
Path("profile").mkdir(exist_ok=True)
Path("profile/stats.svg").write_text("\n".join(svg), encoding="utf-8")
