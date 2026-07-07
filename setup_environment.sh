#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "Installing Python dependencies from requirements.txt..."
/usr/bin/python3 -m pip install -r requirements.txt

echo "Verifying LangChain OpenAI import..."
/usr/bin/python3 -c "import langchain_openai; from langchain_openai import ChatOpenAI, OpenAIEmbeddings; print('langchain_openai import OK')"

echo "Setup completed successfully."
