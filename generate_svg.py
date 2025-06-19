# generate_svg.py
import os
import svgwrite
from github import Github

# Get GitHub username and token from environment
github_username = os.getenv("GITHUB_ACTOR", "Unknown User")
github_token = os.getenv("GITHUB_TOKEN")

g = Github(github_token)
user = g.get_user()

# Fetch statistics
total_stars = sum(repo.stargazers_count for repo in user.get_repos())
total_commits = 0
total_prs = user.get_pulls(state='all').totalCount  # This only works with specific repo
# Need to aggregate manually across repos for more accuracy
total_issues = user.get_issues(state='all').totalCount

# Aggregate commits per repo (as of 2025)
for repo in user.get_repos():
    try:
        total_commits += repo.get_commits(author=user).totalCount
    except:
        pass  # Skip if access denied

# Create an SVG
svg = svgwrite.Drawing(filename="github_stats.svg", size=(600, 200))
svg.add(svg.text(f"User: {github_username}", insert=(10, 40), fill="black", font_size="24"))
svg.add(svg.text(f"Stars: {total_stars}", insert=(10, 80), fill="black", font_size="20"))
svg.add(svg.text(f"Commits: {total_commits} (as of 2025)", insert=(10, 110), fill="black", font_size="20"))
svg.add(svg.text(f"Pull Requests: {total_prs}", insert=(10, 140), fill="black", font_size="20"))
svg.add(svg.text(f"Issues: {total_issues}", insert=(10, 170), fill="black", font_size="20"))
svg.save()

print("SVG created with GitHub stats.")
