import os
import ollama

MODEL = os.environ.get("OLLAMA_MODEL", "qwen3:4b")
messages = []

print(f"Chatting with {MODEL}. Type 'quit' or 'exit' to stop.\n")

while True:
    try:
        user_input = input("You: ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\nGoodbye.")
        break

    if not user_input:
        continue
    if user_input.lower() in ("quit", "exit"):
        print("Goodbye.")
        break

    messages.append({"role": "user", "content": user_input})

    print("Assistant: ", end="", flush=True)
    reply = ""
    for chunk in ollama.chat(model=MODEL, messages=messages, stream=True, options={"num_ctx": 2048}):
        token = chunk["message"]["content"]
        print(token, end="", flush=True)
        reply += token
    print()

    messages.append({"role": "assistant", "content": reply})
