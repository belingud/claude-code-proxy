import sys

import uvicorn
from fastapi import FastAPI

from src.api.endpoints import router as api_router
from src.core.config import config

app = FastAPI(title="Claude-to-OpenAI API Proxy", version="1.0.0")

app.include_router(api_router)


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("Claude-to-OpenAI API Proxy v1.0.0")
        print("")
        print("Usage: python src/main.py")
        print("")
        print("Required environment variables:")
        print("  OPENAI_API_KEY - Your OpenAI API key")
        print("")
        print("Optional environment variables:")
        print("  ANTHROPIC_API_KEY - Expected Anthropic API key for client validation")
        print("                      If set, clients must provide this exact API key")
        print("  OPENAI_BASE_URL - OpenAI API base URL (default: https://api.openai.com/v1)")
        print("  SMALL_MODEL_BASE_URL - Small model API base URL (default: OPENAI_BASE_URL)")
        print("  SMALL_MODEL_API_KEY - Small model API key (default: OPENAI_API_KEY)")
        print("  BIG_MODEL - Model for opus requests (default: gpt-4o)")
        print("  MIDDLE_MODEL - Model for sonnet requests (default: gpt-4o)")
        print("  SMALL_MODEL - Model for haiku requests (default: gpt-4o-mini)")
        print("  BIG_MODEL_EXTRA_BODY - Extra parameters for big model requests (JSON format)")
        print("  SMALL_MODEL_EXTRA_BODY - Extra parameters for small model requests (JSON format)")
        print("  HOST - Server host (default: 0.0.0.0)")
        print("  PORT - Server port (default: 8082)")
        print("  LOG_LEVEL - Logging level (default: WARNING)")
        print("  MAX_TOKENS_LIMIT - Token limit (default: 4096)")
        print("  MIN_TOKENS_LIMIT - Minimum token limit (default: 100)")
        print("  REQUEST_TIMEOUT - Request timeout in seconds (default: 90)")
        print("")
        print("Model mapping:")
        print(f"  Claude haiku models -> {config.small_model}")
        print(f"  Claude sonnet/opus models -> {config.big_model}")
        sys.exit(0)

    # Configuration summary
    print("🚀 Claude-to-OpenAI API Proxy v1.0.0")
    print("✅ Configuration loaded successfully")
    print(f"   OpenAI Base URL: {config.openai_base_url}")
    print(f"   Small Model Base URL: {config.small_model_base_url}")
    print(f"   Big Model (opus): {config.big_model}")
    print(f"   Middle Model (sonnet): {config.middle_model}")
    print(f"   Small Model (haiku): {config.small_model}")
    print(f"   Max Tokens Limit: {config.max_tokens_limit}")
    print(f"   Request Timeout: {config.request_timeout}s")
    print(f"   Server: {config.host}:{config.port}")
    print(f"   Client API Key Validation: {'Enabled' if config.anthropic_api_key else 'Disabled'}")
    if config.big_model_extra_body:
        print(f"   Big Model Extra Body: {config.big_model_extra_body}")
    if config.small_model_extra_body:
        print(f"   Small Model Extra Body: {config.small_model_extra_body}")
    print("")

    # Parse log level - extract just the first word to handle comments
    log_level = config.log_level.split()[0].lower()

    # Validate and set default if invalid
    valid_levels = ["debug", "info", "warning", "error", "critical"]
    if log_level not in valid_levels:
        log_level = "info"

    # Start server
    uvicorn.run(
        "src.main:app",
        host=config.host,
        port=config.port,
        log_level=log_level,
        reload=False,
    )


if __name__ == "__main__":
    main()
