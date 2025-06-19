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

# Create SVG with CSS animation
width, height = 600, 240
dwg = svgwrite.Drawing(filename="github_stats.svg", size=(width, height))

# Add CSS for fade-in effect
css = """
.fade {
  opacity: 0;
  animation: fadeIn 2s ease-out forwards;
}
@keyframes fadeIn {
  from { opacity: 0; }
  to   { opacity: 1; }
}
"""
dwg.defs.add(dwg.raw(f"<style>{css}</style>"))

# Create group with fade-in animation
group = dwg.g(class_="fade")

# Add stats text
lines = [
    f"Repository: {github_repo}",
    f"Stars: {stars}",
    f"Commits: {commits}",
    f"PRs: {prs}",
    f"Issues: {issues}",
]

y = 30
for line in lines:
    group.add(dwg.text(line, insert=(10, y), fill="black", font_size="18px"))
    y += 30

# Add group to SVG
dwg.add(group)

# Save SVG
dwg.save()
print("Animated SVG with repo stats created: github_stats.svg")
