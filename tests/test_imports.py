import sys
import time

def test_import(module_name, from_list=None):
    print(f"Importing {module_name}...", end=" ", flush=True)
    start = time.time()
    try:
        if from_list:
            __import__(module_name, fromlist=from_list)
        else:
            __import__(module_name)
        print(f"Success in {time.time() - start:.2f}s")
    except Exception as e:
        print(f"Failed: {e}")

test_import("dotenv")
test_import("windows_use.llms.google", ["ChatGoogle"])
test_import("windows_use.llms.anthropic", ["ChatAnthropic"])
test_import("windows_use.llms.ollama", ["ChatOllama"])
test_import("windows_use.llms.mistral", ["ChatMistral"])
test_import("windows_use.llms.azure_openai", ["ChatAzureOpenAI"])
test_import("windows_use.llms.open_router", ["ChatOpenRouter"])
test_import("windows_use.llms.groq", ["ChatGroq"])
test_import("windows_use.agent", ["Agent", "Browser"])

print("All imports tested.")
