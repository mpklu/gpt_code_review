import fire
import subprocess
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts.chat import ChatPromptTemplate

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
gitlab_token = os.getenv("GITLAB_TOKEN")
gitlab_server = os.getenv("GITLAB_SERVER")

chat_model = ChatOpenAI(api_key=openai_api_key)  # default model is gpt-3.5-turbo

# 1. Point out existing issues in concise language and stern tone.
# 2. Identify no more than three issues, prioritizing them in descending order: typo, logic, and any other issues.
# 3. If a function is only partially included in the diff, you can assume that the function is complete.
# 4. Your feedback content must be in strict markdown format.
# 5. Do not carry variable content explanation information.


def prompt_template():
    template = """You are a senior programming expert. 
    GitLab branch code changes will be provided in the form of git diff strings. 
    Please review this code. 
    Then the returned content of your review content must strictly comply with the following format, 
    including section title. 
    Explanation of the variable content in the template: 
    Variable 1 is the issues discovered by code review. 
    Variable 2 is specific modification suggestions. 
    Variable 3 is the modified code you gave. 
    Must require: 

    1. Clearly identify existing issues using concise language and a firm tone.
    2. Prioritize up to three issues, with the following order of importance: typo, logic, and other issues.
    3. Assume completeness of functions if only partially included in the diff.
    4. Ensure feedback content adheres strictly to markdown format.
    5. Avoid including explanations for variable content.
    6. Have a clear title structure. Have a clear title structure. Have a clear title structure.
    
The return format is strictly as follows:

#### 👿 Issues:
[Variable 1]

#### 🥸 Modification suggestions:
[Variable 2]

#### 😇 Modified code:
[Variable 3]
    """

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
        git_diff_output = subprocess.run(
            ["git", "diff", "-U20"], capture_output=True, text=True
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


def get_gitlab_diff(project_id, commit_sha):
    # Define the GitLab API URL
    gitlab_api_url = f"{gitlab_server}/api/v4/projects/{project_id}/repository/commits/{commit_sha}/diff"
    return ""
    # Send a GET request to the GitLab API URL
    # response = requests.get(gitlab_api_url)

    # # Check if the request was successful
    # if response.status_code == 200:
    #     # Return the diff content
    #     return response.json()["diff"]
    # else:
    #     # Print an error message if the request failed
    #     print("Error: Failed to retrieve GitLab diff content.")
    #     return None


def review_gitlab(project_id, commit_sha):
    # Get the git diff content for the GitLab repository
    diff_content = get_gitlab_diff(project_id, commit_sha)

    print("git diff:")
    print(diff_content)


if __name__ == "__main__":
    fire.Fire(
        {
            "local": review_local,
            "gitlab": review_gitlab,
        }
    )
