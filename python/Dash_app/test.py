from github import Github

gh = Github('simonrydder')
user = gh.get_user()
repo = user.get_repo('dataprojekt')
pr = repo.get_pull(30)

for file in pr.get_files():
    print(file)
