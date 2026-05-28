"""
Day 1 — LLM API Foundation
AICB-P1: AI Practical Competency Program, Phase 1

Instructions:
    1. Fill in every section marked with TODO.
    2. Do NOT change function signatures.
    3. Copy this file to solution/solution.py when done.
    4. Run: pytest tests/ -v
"""

import os
import time
from typing import Any, Callable
from openai import OpenAI

# ---------------------------------------------------------------------------
# Estimated costs per 1K OUTPUT tokens (USD) — update if pricing changes
# ---------------------------------------------------------------------------
COST_PER_1K_OUTPUT_TOKENS = {
    "gpt-4o": 0.010,
    "gpt-4o-mini": 0.0006,
}

# --- CẤU HÌNH MÔI TRƯỜNG CHO BÀI TẬP (Dùng OpenRouter) ---
# TODO: Thay chuỗi bên dưới bằng API Key thật của bạn
OPENROUTER_API_KEY = "<YOUR_API_KEY_HERE>"

# Mặc định sử dụng model của OpenRouter (cần có tiền tố hãng)
OPENAI_MODEL = "openai/gpt-4o"
OPENAI_MINI_MODEL = "openai/gpt-4o-mini"


# ---------------------------------------------------------------------------
# Task 1 — Call GPT-4o
# ---------------------------------------------------------------------------
def call_openai(
    prompt: str,
    model: str = OPENAI_MODEL,
    temperature: float = 0.7,
    top_p: float = 0.9,
    max_tokens: int = 256,
) -> tuple[str, float]:
    """
    Call the OpenAI Chat Completions API and return the response text + latency.
    """
    # Khởi tạo client dùng OpenRouter
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY
    )
    
    start_time = time.time()
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens
    )
    latency = time.time() - start_time
    
    return response.choices[0].message.content, latency


# ---------------------------------------------------------------------------
# Task 2 — Call GPT-4o-mini
# ---------------------------------------------------------------------------
def call_openai_mini(
    prompt: str,
    temperature: float = 0.7,
    top_p: float = 0.9,
    max_tokens: int = 256,
) -> tuple[str, float]:
    """
    Call the OpenAI Chat Completions API using gpt-4o-mini and return the
    response text + latency.
    """
    return call_openai(
        prompt=prompt,
        model=OPENAI_MINI_MODEL,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens
    )


# ---------------------------------------------------------------------------
# Task 3 — Compare GPT-4o vs GPT-4o-mini
# ---------------------------------------------------------------------------
def compare_models(prompt: str) -> dict:
    """
    Call both models with the same prompt and return a comparison dictionary.
    """
    gpt4o_response, gpt4o_latency = call_openai(prompt, model=OPENAI_MODEL)
    mini_response, mini_latency = call_openai_mini(prompt)
    
    # Cost estimate = (len(response.split()) / 0.75) / 1000 * COST_PER_1K_OUTPUT_TOKENS["gpt-4o"]
    estimated_tokens = len(gpt4o_response.split()) / 0.75
    gpt4o_cost_estimate = (estimated_tokens / 1000) * COST_PER_1K_OUTPUT_TOKENS.get("gpt-4o", 0.010)
    
    return {
        "gpt4o_response": gpt4o_response,
        "mini_response": mini_response,
        "gpt4o_latency": gpt4o_latency,
        "mini_latency": mini_latency,
        "gpt4o_cost_estimate": gpt4o_cost_estimate
    }


# ---------------------------------------------------------------------------
# Task 4 — Streaming chatbot with conversation history
# ---------------------------------------------------------------------------
def streaming_chatbot() -> None:
    """
    Run an interactive streaming chatbot in the terminal.
    """
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY
    )
    history = []
    
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ["quit", "exit"]:
                break
                
            history.append({"role": "user", "content": user_input})
            
            response = client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=history,
                stream=True
            )
            
            print("Assistant: ", end="", flush=True)
            full_response = ""
            for chunk in response:
                delta = chunk.choices[0].delta.content or ""
                print(delta, end="", flush=True)
                full_response += delta
            print()
            
            history.append({"role": "assistant", "content": full_response})
            # Giữ lại 3 lượt hội thoại (6 tin nhắn)
            history = history[-6:]
            
        except (KeyboardInterrupt, EOFError):
            print()
            break


# ---------------------------------------------------------------------------
# Bonus Task A — Retry with exponential backoff
# ---------------------------------------------------------------------------
def retry_with_backoff(
    fn: Callable,
    max_retries: int = 3,
    base_delay: float = 0.1,
) -> Any:
    """
    Call fn(). If it raises an exception, retry up to max_retries times
    with exponential backoff.
    """
    delay = base_delay
    last_exception = None
    
    for attempt in range(max_retries + 1):
        try:
            return fn()
        except Exception as e:
            last_exception = e
            if attempt < max_retries:
                time.sleep(delay)
                delay *= 2
                
    if last_exception:
        raise last_exception


# ---------------------------------------------------------------------------
# Bonus Task B — Batch compare
# ---------------------------------------------------------------------------
def batch_compare(prompts: list[str]) -> list[dict]:
    """
    Run compare_models on each prompt in the list.
    """
    results = []
    for prompt in prompts:
        res = compare_models(prompt)
        res["prompt"] = prompt
        results.append(res)
    return results


# ---------------------------------------------------------------------------
# Bonus Task C — Format comparison table
# ---------------------------------------------------------------------------
def format_comparison_table(results: list[dict]) -> str:
    """
    Format a list of compare_models results as a readable text table.
    """
    header = f"{'Prompt':<40} | {'GPT-4o Response':<40} | {'Mini Response':<40} | {'GPT-4o Latency':<15} | {'Mini Latency':<15}"
    lines = [header, "-" * len(header)]
    
    for res in results:
        p = res["prompt"][:37] + "..." if len(res["prompt"]) > 40 else res["prompt"]
        g_res = res["gpt4o_response"][:37] + "..." if len(res["gpt4o_response"]) > 40 else res["gpt4o_response"]
        m_res = res["mini_response"][:37] + "..." if len(res["mini_response"]) > 40 else res["mini_response"]
        g_lat = f"{res['gpt4o_latency']:.4f}"
        m_lat = f"{res['mini_latency']:.4f}"
        
        lines.append(f"{p:<40} | {g_res:<40} | {m_res:<40} | {g_lat:<15} | {m_lat:<15}")
        
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Entry point for manual testing
# ---------------------------------------------------------------------------
import sys
if __name__ != "__main__":
    parent_mod = __name__.split('.')[0]
    if parent_mod not in sys.modules:
        import types
        sys.modules[parent_mod] = types.ModuleType(parent_mod)
    setattr(sys.modules[parent_mod], "solution", sys.modules[__name__])

if __name__ == "__main__":
    test_prompt = "Explain the difference between temperature and top_p in one sentence."
    print("=== Comparing models ===")
    result = compare_models(test_prompt)
    for key, value in result.items():
        print(f"{key}: {value}")

    print("\n=== Starting chatbot (type 'quit' to exit) ===")
    streaming_chatbot()
