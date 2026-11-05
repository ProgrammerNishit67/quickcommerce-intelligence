import os
from dulwich.repo import Repo
from dulwich.porcelain import init, add, commit, remote_add, status

repo_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 1. Initialize repo
if not os.path.exists(os.path.join(repo_path, ".git")):
    r = init(repo_path)
    print("Initialized Git repository at:", repo_path)
else:
    r = Repo(repo_path)
    print("Existing Git repository loaded.")

# 2. Stage files
print("Staging project files...")
add(r)

# 3. Commit
try:
    c = commit(
        r,
        message=b"feat: complete QuickCommerce Intelligence operations analytics platform",
        committer=b"ProgrammerNishit67 <ProgrammerNishit67@users.noreply.github.com>",
        author=b"ProgrammerNishit67 <ProgrammerNishit67@users.noreply.github.com>"
    )
    print("Successfully created initial commit:", c.decode() if isinstance(c, bytes) else c)
except Exception as e:
    print("Commit result:", e)

# 4. Set remote origin
remote_url = "https://github.com/ProgrammerNishit67/quickcommerce-intelligence.git"
try:
    remote_add(r, "origin", remote_url)
    print(f"Added remote origin: {remote_url}")
except Exception as e:
    print("Remote already exists or note:", e)

print("Repository successfully initialized and committed!")
