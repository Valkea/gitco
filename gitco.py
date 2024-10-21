import re
import os
import subprocess
import readline

from openai import AzureOpenAI

import instructor
from pydantic import BaseModel
from typing import List

from dotenv import load_dotenv
load_dotenv(".env.gitco")

__version__ = 'dev'

class OutputModel(BaseModel):
    commit_messages_list: List[str] = None

class config:
    provider = os.environ.get("GITCO_PROVIDER")
    try:
        if provider.lower() == "azure":
            api_key = os.environ.get("GITCO_API_KEY")
            api_version=os.environ.get("GITCO_API_VERSION")
            endpoint = os.environ.get("GITCO_ENDPOINT")
            deploy_name = os.environ.get("GITCO_DEPLOYMENT_NAME")
        else:
            print("Provider not supported")
    except Exception as e:
        print("No provider available")
        exit(1)

def prepare_command(cmd):
    # Set up the readline prompt to include the generated command
    readline.set_startup_hook(lambda: readline.insert_text(cmd))
    try:
        # Take input from the user, displaying the generated command
        user_input = input("Modify and/or press Enter to execute: \n\n")
    finally:
        # Remove the readline hook
        readline.set_startup_hook()

    # Return the modified command or the original one
    return user_input if user_input else cmd


def split_command(command):
    # Regular expression to split by spaces, but not inside double quotes
    pattern = r'(?:(?<=\s)|^)(\"[^\"]*\"|[^\s\"]+)'

    # Find all matches based on the regex pattern
    return [x.replace("\"", "") for x in re.findall(pattern, command)]
    #return re.findall(pattern, command)


def gen_commit_msg():

    client = AzureOpenAI(
        api_key=config.api_key,
        api_version=config.api_version,
        azure_endpoint=config.endpoint,
    )

    # Patch the OpenAI client
    client = instructor.from_openai(client)

    diff = subprocess.check_output(['git', 'diff', '--cached'])
    print(diff)

    system_prompt = """
    You are expert at writing consise git commit messages based on the git diff --cached results

    - start with "refactor:" if the commit seems remove or changes things without adding new feature or fixing a bug.
    - start with "feature:" if the commit seems to add a new feature, class ...
    - start with "fix:" if the commit seems to correct a problem.

    If the commit contains several types of actions, make a global commit message and several sub commit messages to explain the various actions.

    You always return a list with 1+ items.
    The returned strings are in double quotes.
    """

    user_prompt = f"""
    Here is the diff: ###{diff}###
    """

    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    response = client.chat.completions.create(
        model=config.deploy_name,
        messages=messages,
        response_model=OutputModel,
        temperature=0.5,
    )
    commit_msg = response.commit_messages_list

    # commit_msg = response.choices[0].message.content

    # print(response)
    print("="*100)
    print(commit_msg)
    print("="*100)


    command_args = ('" -m "').join(response.commit_messages_list)
    command = f'git commit -m "{command_args}"'
    prepared_cmd = prepare_command(command)
    print(f"Command prepared: {prepared_cmd}")
    subprocess.check_output(split_command(prepared_cmd))


if __name__ == "__main__":
    gen_commit_msg()
