import requests
import urllib.parse
import logging
from config import Config


def gitlab_project_url(config: Config, project_id):
    return f"{config.host}/api/v4/projects/{project_id}"


def get_gitlab_diff(config: Config, project_id, commit_sha):
    # Define the GitLab API URL
    proj_url = gitlab_project_url(config, project_id)
    gitlab_api_url = f"{proj_url}/repository/commits/{commit_sha}/diff"
    headers = {"PRIVATE-TOKEN": config.token}

    response = requests.get(gitlab_api_url, headers=headers)
    if response.status_code == 200:
        logging.info(
            f"{gitlab_api_url} success: {response.status_code} {response.reason}"
        )
        json = response.json()
        ret = ""
        for diff in json:
            filename = diff["new_path"]
            diff_content = diff["diff"]

            # print(f"Filename: {filename}")
            # print("Diff Content:")
            for line in diff_content.split("\n"):
                ret += line + "\n"
        return ret
    else:
        logging.info(
            f"{gitlab_api_url} success: {response.status_code} {response.reason}"
        )
        return None


def get_gitlab_file_content(config: Config, project_id, path, cmmmit_sha):
    file_path = urllib.parse.quote(path, safe="")
    proj_url = gitlab_project_url(config, project_id)
    url = f"{proj_url}/repository/files/{file_path}/raw?ref={cmmmit_sha}"
    headers = {"PRIVATE-TOKEN": config.token}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        logging.info(f"{url} success: {response.status_code} {response.reason}")
        file_content = response.text
        return file_content
    else:
        logging.error(f"{url} failure: {response.status_code} {response.reason}")
        return None
