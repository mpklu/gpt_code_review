import fire
import subprocess
import os
import requests
from dotenv_vault import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.messages import ChatMessage
from prompts import system_prompt
from gitlab.api import *

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
gitlab_token = os.getenv("GITLAB_TOKEN")
gitlab_server = os.getenv("GITLAB_SERVER")
chat_model = ChatOpenAI(api_key=openai_api_key)  # default model is gpt-3.5-turbo
gitlab_config = Config(gitlab_token, gitlab_server)
# 1. Point out existing issues in concise language and stern tone.
# 2. Identify no more than three issues, prioritizing them in descending order: typo, logic, and any other issues.
# 3. If a function is only partially included in the diff, you can assume that the function is complete.
# 4. Your feedback content must be in strict markdown format.
# 5. Do not carry variable content explanation information.


def prompt_template():
    template = system_prompt

    human_template = "Review the code diff: {content}"

    chat_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", template),
            ("human", human_template),
        ]
    )
    return chat_prompt


def review_code_diff(processed_code):
    chat_prompt = prompt_template()
    messages = chat_prompt.format_messages(content=processed_code)
    result = chat_model.invoke(messages)
    print(result.content)


def get_git_diff(repo_path):
    # Store the current working directory
    current_dir = os.getcwd()

    try:
        # Change to the specified git repository directory
        os.chdir(repo_path)

        # Run 'git diff' command and capture the output
        command = "git diff -U20 && git diff --cached -U20"
        git_diff_output = subprocess.run(
            command, shell=True, capture_output=True, text=True
        )

        # Check if 'git diff' command was successful
        if git_diff_output.returncode == 0:
            # Return the git diff output
            return git_diff_output.stdout
        else:
            # Print error message if 'git diff' command failed
            print("Error: Failed to retrieve git diff.")
            return None
    except FileNotFoundError:
        print("Error: Specified directory is not a valid git repository.")
        return None
    finally:
        # Change back to the original working directory
        os.chdir(current_dir)


def review_local(repo_path):
    # Get the git diff content for the local repository
    diff_content = get_git_diff(repo_path)
    # print("git diff:")
    # print(diff_content)

    review_code_diff(diff_content)


def review_gitlab(project_id: int, commit_sha: str):
    # Get the git diff content for the GitLab repository
    diff_content = get_gitlab_diff(gitlab_config, project_id, commit_sha)

    # print("git diff:")
    # print(diff_content)
    review_code_diff(diff_content)


if __name__ == "__main__":
    fire.Fire(
        {
            "local": review_local,
            "gitlab": review_gitlab,
        }
    )
