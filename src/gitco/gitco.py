import re
import os
import subprocess
import readline

from openai import AzureOpenAI

import instructor
from pydantic import BaseModel
from typing import List

from .inputs import prepare_command

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


def split_command(command):
    # Regular expression to split by spaces, but not inside double quotes
    pattern = r'(?:(?<=\s)|^)(\"[^\"]*\"|[^\s\"]+)'

    # Find all matches based on the regex pattern
    return [x.replace("\"", "") for x in re.findall(pattern, command)]
    #return re.findall(pattern, command)


def gen_commit_msg(inspiration:str = "", debug:bool = False, *args, **kwargs):

    if debug:
        print(f"Inspiration: `{inspiration}` is not used yet")

    client = AzureOpenAI(
        api_key=config.api_key,
        api_version=config.api_version,
        azure_endpoint=config.endpoint,
    )

    # Patch the OpenAI client
    client = instructor.from_openai(client)

    diff = subprocess.check_output(['git', 'diff', '--cached'])
    if debug:
        print(diff)

    if diff == b'' and debug == False:
        print("\nThere is nothing to commit")
        exit(0)

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
    if debug:
        print("="*100)
        print(commit_msg)
        print("="*100)

    # Prepare extra positional arguments
    l_args = list(args)
    l_args.insert(0,"")
    command_extra_args = (" ").join(l_args)

    # Prepare extra keyword arguments
    l_kwargs = [f"{k}={v}" for k,v in kwargs.items()]
    l_kwargs.insert(0,"")
    command_extra_kwargs = (" ").join(l_kwargs)

    # Prepare commit messages
    commit_msgs = response.commit_messages_list
    commit_msgs = ('" -m "').join(commit_msgs)

    # Prepare command
    command = f'git commit{command_extra_args} -m "{commit_msgs}"{command_extra_kwargs}'
    prepared_cmd, prepare_status = prepare_command(command)

    if prepare_status == "retry":
        gen_commit_msg(inspiration, debug, *args, **kwargs)
    else:
        print(f"RUN CMD:\n {prepared_cmd}")
        subprocess.check_output(split_command(prepared_cmd))


if __name__ == "__main__":
    gen_commit_msg()
