from langchain_ollama import OllamaLLM

# Connect to the local Llama 3 model using the updated library
llm = OllamaLLM(model="phi3")

print("Sending request to local AI...")
try:
    response = llm.invoke("What is 2 + 2? Answer in one sentence.")
    print("\nResponse from AI:")
    print(response)
except Exception as e:
    print(f"\nError: {e}")