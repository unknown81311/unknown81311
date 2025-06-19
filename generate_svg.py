# generate_svg.py
import os
import svgwrite
from github import Github, GithubException

# Get environment variables
github_actor = os.getenv("GITHUB_ACTOR")
github_repo = os.getenv("GITHUB_REPOSITORY")
github_token = os.getenv("GITHUB_TOKEN")

# Validate
if not github_actor or not github_repo or not github_token:
    raise EnvironmentError("GITHUB_ACTOR, GITHUB_REPOSITORY, and GITHUB_TOKEN must be set")

# GitHub API setup
try:
    gh = Github(github_token)
    repo = gh.get_repo(github_repo)
except GithubException as e:
    raise RuntimeError(f"GitHub API error: {e}")

# Fetch stats
stars = repo.stargazers_count
commits = repo.get_commits().totalCount
prs = repo.get_pulls(state="all").totalCount
issues = repo.get_issues(state="all").totalCount

# Create SVG
dwg = svgwrite.Drawing("github_stats.svg", size=(600, 240))

# Add CSS animation via <style> in <defs>
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
# svgwrite supports style element
style = dwg.style(css)
dwg.defs.add(style)

# Create group with fade-in class
grp = dwg.g(class_="fade")

# Add text lines
y = 30
for text in [
    f"Repository: {github_repo}",
    f"Stars: {stars}",
    f"Commits: {commits}",
    f"PRs: {prs}",
    f"Issues: {issues}" 
]:
    grp.add(dwg.text(text, insert=(10, y), fill="black", font_size="18px"))
    y += 30

# Add group and save
dwg.add(grp)
dwg.save()
print("Animated SVG with repo stats created: github_stats.svg")
