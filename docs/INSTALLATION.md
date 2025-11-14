# Installation Guide

## System Requirements

- **Python**: 3.8 or higher
- **pip**: Latest version
- **Operating System**: Windows, macOS, or Linux

## Installation Steps

### 1. Set Up Python Environment

It's recommended to use a virtual environment:

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure OpenAI API Key

1. Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)

2. Create a `.env` file in the project root:
```bash
cp .env.example .env
```

3. Edit `.env` and add your API key:
```
OPENAI_API_KEY=sk-your-actual-api-key-here
OPENAI_MODEL=gpt-4
```

### 4. Verify Installation

Run the tests to verify everything is working:

```bash
pytest tests/ -v
```

## Next Steps

After installation, see README.md for usage instructions.
