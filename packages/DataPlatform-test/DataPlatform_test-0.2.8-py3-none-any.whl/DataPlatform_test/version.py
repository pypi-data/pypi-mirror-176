from pathlib import Path

def version():
    repo = Path(__file__).parent.parent
    git_dir = repo.joinpath(".git")
    print(repo)
    
    repo = "D:\\IDE\\anaconda\\envs\\demo_3.9\\Lib\\site-packages\\DataPlatform_test"
    from git import Repo
    branch_info = f"[{Repo(repo).active_branch}]"
    branch_info

version()
