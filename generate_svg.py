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

# Create SVG
width, height = 600, 200
svg = svgwrite.Drawing(filename="github_stats.svg", size=(width, height))

# Add text lines
lines = [
    f"Repository: {github_repo}",
    f"Stars: {stars}",
    f"Commits (all): {commits}",
    f"PRs (all): {prs}",
    f"Issues (all): {issues}",
]

y = 30
for line in lines:
    svg.add(svg.text(line, insert=(10, y), fill="black", font_size="18"))
    y += 30

svg.save()
print("SVG with current repo stats created: github_stats.svg")
