# gpt_code_review

Use Chat-GPT to review your changes in Git repository.

### Config

- create a `.env` file in project root folder
- set `OPENAI_API_KEY` there. ex: `OPENAI_API_KEY=########################`

### To Run

```
pip3 install -r requirements.txt
```

#### Review the changes of local Git Repo

```
python3 gpt_review.py local --repo_path=[PATH_TO_GIT_REPO]
```

#### Review the changes give a GitLab project ID and commit_sha

```
    python3 ./gpt_review.py gitlab --project_id=[gitlab_project_id] --commit-sha=[commit_sha]
```
