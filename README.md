# GitCo Package
[![PyPI version](https://badge.fury.io/py/gitco.svg)](https://badge.fury.io/py/gitco)

**GitCo** is a command-line tool designed to assist in generating git commit messages by analyzing the current changes (diff) in your repository. It uses a Language Model (LLM) to suggest meaningful and concise commit messages, saving you time while keeping your commit history clear and informative.

## Features

- **Commit Message Suggestions**: GitCo suggests commit messages based on your staged changes.
- **LLM Integration**: Uses powerful language models via external providers to create context-aware commit messages.
- **Interactive Workflow**: Edit or approve the suggested message before finalizing your commit.

## Installation

Install the GitCo package using `pip`:

```bash
pip install gitco
```

## Configuration

GitCo requires access to an LLM provider to generate commit messages. You can configure the tool in two ways:

### Option 1: Using a `.env.gitco` file

1. In your project directory, create a `.env.gitco` file.
2. Add the following environment variables with the details of your LLM provider:

```bash
GITCO_PROVIDER=Azure
GITCO_API_KEY="YOUR_API_KEY"
GITCO_API_VERSION="2024-08-01-preview"
GITCO_DEPLOYMENT_NAME="YOUR_DEPLOYMENT_NAME"
GITCO_ENDPOINT="https://YOUR_ENDPOINT.openai.azure.com/"
```

With this method, one needs to execute the `gitco` command from the same directory as the `.env.gitco` file.

### Option 2: Export environment variables

Alternatively, you can set these environment variables directly in your terminal or CI environment. Use the following commands:

```bash
export GITCO_PROVIDER=Azure
export GITCO_API_KEY="YOUR_API_KEY"
export GITCO_API_VERSION="2024-08-01-preview"
export GITCO_DEPLOYMENT_NAME="YOUR_DEPLOYMENT_NAME"
export GITCO_ENDPOINT="https://YOUR_ENDPOINT.openai.azure.com/"
```

### Notes:
- Replace the placeholder values (e.g., `YOUR_API_KEY`) with your actual credentials and API details.
- Ensure that your API key and other credentials are securely stored and not exposed in version control.

## Providers

GitCo is designed to support multiple LLM providers for flexibility and future expansion. Currently, it supports **Azure OpenAI** as the LLM provider. 

In the future, GitCo will support additional providers, allowing users to choose the LLM service that best fits their needs. Planned future providers include:

- **OpenAI API** (non-Azure)
- **Anthropic**
- **Google Gemini**
- **Hugging Face**
- **Ollama**
- ...

For each provider, GitCo will automatically adapt based on your configuration, as set in your environment or `.env.gitco` file. Stay tuned for updates!

## Usage

After configuration, you can use GitCo to generate a suggested commit message. Here's how it works:

1. **Generate the Suggestion**:
   Run the following command from your git repository to generate a commit message based on the staged changes:

   ```bash
   gitco
   ```

2. **Edit or Approve the Commit Message**:
   - GitCo will suggest a commit message based on the diff.
   - You have the option to edit the suggested message if necessary.
   - Once satisfied, you can approve the commit.

3. **Finalizing the Commit**:
   - If the suggested message fits your needs perfectly, you can directly validate it, and GitCo will automatically run the following command to finalize the commit:

     ```bash
     git commit -m "Generated commit message"
     ```

   - If you edit the message, GitCo will use your final version for the commit. After approval, it will automatically execute the commit.

This allows for a seamless, interactive workflow where you remain in control of the final commit message.

