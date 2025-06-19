# generate_svg.py
import os
import svgwrite
from github import Github, GithubException

# Get required env vars
github_actor = os.getenv("GITHUB_ACTOR")
github_repo = os.getenv("GITHUB_REPOSITORY")  # e.g., "owner/name"
github_token = os.getenv("GITHUB_TOKEN")

# Validate
if not github_actor or not github_repo or not github_token:
    raise EnvironmentError("GITHUB_ACTOR, GITHUB_REPOSITORY, and GITHUB_TOKEN must be set")

# Initialize GitHub API
try:
    gh = Github(github_token)
    repo = gh.get_repo(github_repo)
except GithubException as e:
    raise RuntimeError(f"GitHub API error: {e}")

# Gather stats for this repo
stars = repo.stargazers_count
commits = repo.get_commits().totalCount
prs = repo.get_pulls(state="all").totalCount
issues = repo.get_issues(state="all").totalCount

# Create SVG with fade-in animation
width, height = 600, 240
dwg = svgwrite.Drawing(filename="github_stats.svg", size=(width, height))

g = dwg.g(opacity=0)
# Animate group opacity from 0 to 1 over 2 seconds
g.add(dwg.animate(
    attributeName="opacity",
    from_="0", to="1",
    dur="2s",
    fill="freeze"
))

# Add text lines to group
lines = [
    f"Repository: {github_repo}",
    f"Stars: {stars}",
    f"Commits: {commits}",
    f"PRs: {prs}",
    f"Issues: {issues}",
]

y = 30
for line in lines:
    g.add(dwg.text(line, insert=(10, y), fill="black", font_size="18"))
    y += 30

# Add group to drawing and save
dwg.add(g)
dwg.save()
print("Animated SVG with repo stats created: github_stats.svg")
