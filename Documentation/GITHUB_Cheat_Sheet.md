# Git & GitHub Cheat Sheet

[Original Git & GitHub Cheat Sheet Cheat Sheet Reference](https://gist.github.com/mignonstyle/4b437a4060646f55964b85cd6edb4ee3)

---

## Repository Setup

- **Initialize a local repository**: `$ git init`

- **Clone from remote**: `$ git clone [repository_path]`

- **Clone with a new directory name**: `$ git clone [repository_path] [new_repository_path]`

- **Shallow clone (latest revision only)**: `$ git clone --depth 1 [repository_path]`

## Branching

- **Create a branch**: `$ git branch [branch]`

- **List local branches**: `$ git branch`

- **List all branches (local + remote)**: `$ git branch -a`

- **List remote branches**: `$ git branch -r`

- **Delete a branch**: `$ git branch -d [branch]`

## Checkout

- **Switch to another branch**: `$ git checkout [branch]`

- **Create and switch to a new branch**: `$ git checkout -b [branch]`

## Status & Diff

- **Show changed file diffs**: `$ git diff`

- **Show staged/unstaged changes**: `$ git status`

## Staging (Add)

- **Add a specific file to the index**: `$ git add [filename]`

- **Add updated files to the index**: `$ git add -u`

- **Add all modified files (excluding new files)**: `$ git add -A`

- **Add all files and directories to the index**: `$ git add .`

## Committing

- **Commit staged changes**: `$ git commit`

- **Commit with a message**: `$ git commit -m "[comment]"`

- **Auto-stage & commit tracked files**: `$ git commit -a`

- **Amend the previous commit**: `$ git commit --amend`

## Log & Show

- **View commit history**: `$ git log`

- **View details of the latest commit**: `$ git show`

## Reset

- **Undo last commit (keep changes)**: `$ git reset --soft HEAD^`

- **Undo last commit and discard changes**: `$ git reset --hard HEAD^`

## Push

- **Push to remote branch**: `$ git push [remote] [branch]`

- **Push master to origin**: `$ git push origin master`

## Pull Requests

- **Create a pull request**: `$ git pull-request`

- **Create PR with message and branches**: `$ git pull-request -m "[comment]" -b defunkt:master -h mislav:feature`

## Merging

- **Merge a branch into the current one**: `$ git merge [branch]`

## Fetch & Pull

- **Fetch changes from remote**: `$ git fetch [remote]`

- **Pull (fetch + merge) from remote**: `$ git pull [remote]`

## Cherry-Pick

- **Apply commit from another branch**: `$ git cherry-pick [commit id]`

## GitHub Browsing

- **Open GitHub project page**:

```bash
    `$ git browse`  
    `$ open https://github.com/USER_NAME/REPOSITORY_NAME`
```

- **Open GitHub issues page**:

```bash
    `$ git browse -- issues`  
    `$ open https://github.com/USER_NAME/REPOSITORY_NAME/issues`
```

- **Open GitHub wiki page**:

```bash
  `$ git browse -- wiki`  
  `$ open https://github.com/USER_NAME/REPOSITORY_NAME/wiki`
```
