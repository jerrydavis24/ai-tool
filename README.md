# AI Code Review Tool

A command-line tool that reads a Python file and uses Claude (anthropoic) to generate
a code review, listing concrete issues, style problems, and suggestions.

## Setup
pip install anthropic
export ANTHROPIC_API_KEY="your-key-here"

## Usage
python review.py path/to/file.py