import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.chat_models import ChatOllama

def get_gemini_model(model_name: str = "gemini-2.0-flash") -> ChatGoogleGenerativeAI:
    """Returns a LangChain-compatible Gemini model instance."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is not set.")
    return ChatGoogleGenerativeAI(model=model_name, temperature=0.1)

def get_llama_model(use_ollama: bool = True, model_name: str = "llama3", **kwargs) -> ChatOllama:
    """Returns a LangChain-compatible Llama model via Ollama."""
    if use_ollama:
        print(f"  Connecting to local Ollama — model: {model_name}")
        # Extract optimization parameters
        temperature = kwargs.get("temperature", 0.1)
        top_p = kwargs.get("top_p", 0.8)
        max_tokens = kwargs.get("max_tokens", 400)
        num_ctx = kwargs.get("num_ctx", 2048)
        
        return ChatOllama(
            model=model_name, 
            temperature=temperature,
            top_p=top_p,
            num_predict=max_tokens,
            num_ctx=num_ctx,
            repeat_penalty=kwargs.get("repeat_penalty", 1.2),
            stop=kwargs.get("stop", ["\n\n", "###", "--", "•", "1.", "2."]),
            mirostat=kwargs.get("mirostat", 2),
            mirostat_eta=kwargs.get("mirostat_eta", 0.1),
            mirostat_tau=kwargs.get("mirostat_tau", 5.0)
        )
    else:
        raise ValueError(
            "Non-Ollama Llama backends require torch. "
            "Please install Ollama (https://ollama.com) and pull a model."
        )

def get_llm(model_type: str = "gemini", **kwargs):
    if model_type.lower() == "gemini":
        return get_gemini_model(model_name=kwargs.get("model_name", "gemini-2.0-flash"))
    elif model_type.lower() == "llama":
        return get_llama_model(
            use_ollama=kwargs.get("use_ollama", True),
            model_name=kwargs.get("model_name", "llama3.2:3b"),
            temperature=kwargs.get("temperature", 0.01),
            top_p=kwargs.get("top_p", 0.5),
            max_tokens=kwargs.get("max_tokens", 150),
            num_ctx=kwargs.get("num_ctx", 512),
            repeat_penalty=kwargs.get("repeat_penalty", 1.2),
            stop=kwargs.get("stop", ["\n\n", "###", "--", "•", "1.", "2."]),
            mirostat=kwargs.get("mirostat", 2),
            mirostat_eta=kwargs.get("mirostat_eta", 0.1),
            mirostat_tau=kwargs.get("mirostat_tau", 5.0)
        )
    else:
        raise ValueError(f"Unsupported model type: {model_type}")
