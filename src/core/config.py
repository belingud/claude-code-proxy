import os
import sys
import json


# Configuration
class Config:
    def __init__(self):
        self.openai_api_key = os.environ.get("OPENAI_API_KEY")
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")

        # Add Anthropic API key for client validation
        self.anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not self.anthropic_api_key:
            print("Warning: ANTHROPIC_API_KEY not set. Client API key validation will be disabled.")

        self.openai_base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
        # Small model specific configurations
        self.small_model_base_url = os.environ.get("SMALL_MODEL_BASE_URL", self.openai_base_url)
        self.small_model_api_key = os.environ.get("SMALL_MODEL_API_KEY", self.openai_api_key)

        # Extra body configurations for big and small models
        self.big_model_extra_body = self._parse_json_env("BIG_MODEL_EXTRA_BODY")
        self.small_model_extra_body = self._parse_json_env("SMALL_MODEL_EXTRA_BODY")

        self.azure_api_version = os.environ.get("AZURE_API_VERSION")  # For Azure OpenAI
        self.host = os.environ.get("HOST", "0.0.0.0")
        self.port = int(os.environ.get("PORT", "8082"))
        self.log_level = os.environ.get("LOG_LEVEL", "INFO")
        self.max_tokens_limit = int(os.environ.get("MAX_TOKENS_LIMIT", "4096"))
        self.min_tokens_limit = int(os.environ.get("MIN_TOKENS_LIMIT", "100"))

        # Connection settings
        self.request_timeout = int(os.environ.get("REQUEST_TIMEOUT", "90"))
        self.max_retries = int(os.environ.get("MAX_RETRIES", "2"))

        # Model settings - BIG and SMALL models
        self.big_model = os.environ.get("BIG_MODEL", "gpt-4o")
        self.middle_model = os.environ.get("MIDDLE_MODEL", self.big_model)
        self.small_model = os.environ.get("SMALL_MODEL", "gpt-4o-mini")

    def _parse_json_env(self, env_var_name):
        """Parse JSON from environment variable, return None if not set or invalid"""
        env_value = os.environ.get(env_var_name)
        if not env_value:
            return None
        try:
            return json.loads(env_value)
        except json.JSONDecodeError:
            print(f"Warning: Invalid JSON in {env_var_name}, ignoring.")
            return None

    def validate_api_key(self):
        """Basic API key validation"""
        if not self.openai_api_key:
            return False
        # Basic format check for OpenAI API keys
        if not self.openai_api_key.startswith("sk-"):
            return False
        return True

    def validate_client_api_key(self, client_api_key):
        """Validate client's Anthropic API key"""
        # If no ANTHROPIC_API_KEY is set in the environment, skip validation
        if not self.anthropic_api_key:
            return True

        # Check if the client's API key matches the expected value
        return client_api_key == self.anthropic_api_key


try:
    config = Config()
    print(f" Configuration loaded: API_KEY={'*' * 20}..., BASE_URL='{config.openai_base_url}'")
    if config.small_model_base_url:
        print(
            f"   SMALL_MODEL_API_KEY={'*' * 20}..., SMALL_MODEL_BASE_URL='{config.small_model_base_url}'"
        )
except Exception as e:
    print(f"=4 Configuration Error: {e}")
    sys.exit(1)
