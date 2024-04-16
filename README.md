# gpt_code_review

Use Chat-GPT to review your changes in Git repository.

### Config

- create a `.env` file in project root folder
- set `OPENAI_API_KEY` there. ex: `OPENAI_API_KEY=########################`

### To Run

```
pip3 install -r requirements.txt
```

```
python3 gpt_review.py local --repo_path=[PATH_TO_GIT_REPO]
```
