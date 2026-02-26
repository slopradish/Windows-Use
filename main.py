from windows_use.llms.google import ChatGoogle
from windows_use.llms.anthropic import ChatAnthropic
from windows_use.llms.ollama import ChatOllama
from windows_use.llms.openai import ChatOpenAI
from windows_use.llms.mistral import ChatMistral
from windows_use.llms.azure_openai import ChatAzureOpenAI
from windows_use.llms.open_router import ChatOpenRouter
from windows_use.llms.groq import ChatGroq
from windows_use.agent import Agent, Browser
from dotenv import load_dotenv
import os

load_dotenv()

def build_llm():
    provider = os.getenv("LLM_PROVIDER", "anthropic").strip().lower()
    temperature = float(os.getenv("LLM_TEMPERATURE", "0.2"))

    if provider == "lmstudio":
        return ChatOpenAI(
            model=os.getenv("LM_STUDIO_MODEL", "local-model"),
            base_url=os.getenv("LM_STUDIO_BASE_URL", "http://127.0.0.1:1234/v1"),
            api_key=os.getenv("LM_STUDIO_API_KEY", "lm-studio"),
            temperature=temperature,
        )
    if provider == "ollama":
        return ChatOllama(
            model=os.getenv("OLLAMA_MODEL", "qwen3-vl:4b"),
            temperature=temperature,
        )
    if provider == "google":
        return ChatGoogle(
            model=os.getenv("GOOGLE_MODEL", "gemini-2.5-flash-lite"),
            temperature=temperature,
        )
    if provider == "openrouter":
        return ChatOpenRouter(
            model=os.getenv("OPENROUTER_MODEL", "nvidia/nemotron-3-nano-30b-a3b:free"),
            temperature=temperature,
        )
    if provider == "groq":
        return ChatGroq(
            model=os.getenv("GROQ_MODEL", "meta-llama/llama-4-scout-17b-16e-instruct"),
            temperature=temperature,
        )
    if provider == "mistral":
        return ChatMistral(
            model=os.getenv("MISTRAL_MODEL", "magistral-small-latest"),
            temperature=temperature,
        )
    if provider == "azure":
        return ChatAzureOpenAI(
            deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o"),
            temperature=temperature,
        )
    return ChatAnthropic(
        model=os.getenv("ANTHROPIC_MODEL", "claude-haiku-4-5"),
        temperature=temperature,
    )

def main():
    llm = build_llm()
    agent = Agent(llm=llm, browser=Browser.EDGE,auto_minimize=True,log_to_file=True)
    agent.invoke(query=input("Enter a query: "))

if __name__ == "__main__":
    main()
