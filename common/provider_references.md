## 3. `/common/provider_references.md`

# Provider References (Summaries)

This file summarizes relevant details from OpenAI Agents docs, Gemini, Requestry, and OpenRouter. It is a condensed reference for quick setup and usage.

---

## 1. OpenAI

- **API Key**: `OPENAI_API_KEY`
- **Default Endpoint**: `api.openai.com` or custom `base_url`
- **Multi-Model**: `gpt-4o`, `o3-mini`, etc.
- **Error Handling**: `openai.error.APIError`, plus specific exceptions
- **Recommended**: Use `ChatCompletion.create(...)` for full chat context

**Snippet**:
```python
import openai

openai.api_key = "..."
response = openai.ChatCompletion.create(
    model="gpt-o3-mini",
    messages=[{"role": "user", "content": "Hello!"}],
)
```

---

## 2. Gemini

- **API Key**: `GEMINI_API_KEY`
- **Default Models**: `gemini-2.0`, `gemini-pro`, `gemini-ultra`
- **Python Library**: `import google.generativeai as genai`
- **Usage**:
  ```python
  genai.configure(api_key="...")
  model = genai.GenerativeModel("gemini-2.0")
  response = model.generate_content("Prompt")
  ```

---

## 3. Requestry

- **API Key**: `REQUESTRY_API_KEY`
- **Default Endpoint**: `https://router.requesty.ai/v1`
- **Models**: `cline/o3-mini`, `cline/4o-mini`
- **Usage**:
  ```python
  import openai

  client = openai.OpenAI(
      api_key="...",
      base_url="https://router.requesty.ai/v1"
  )
  response = client.chat.completions.create(
      model="cline/o3-mini",
      messages=[{"role": "system", "content": "Hello world"}]
  )
  ```

---

## 4. OpenRouter

- **API Key**: `OPENROUTER_API_KEY`
- **Endpoint**: `https://openrouter.ai/api/v1`
- **Optional Headers**: `HTTP-Referer`, `X-Title`
- **Models**: `openai/gpt-4o`, etc.
- **Usage**:
  ```python
  import openai

  client = openai.OpenAI(
      base_url="https://openrouter.ai/api/v1",
      api_key="..."
  )
  response = client.chat.completions.create(
      model="openai/gpt-4o",
      messages=[{"role": "user", "content": "Hello?"}]
  )
  ```

---

## 5. Additional Notes

- **Environment Variables**: `.env` should define unique keys for each provider (`OPENAI_API_KEY`, `GEMINI_API_KEY`, `REQUESTRY_API_KEY`, `OPENROUTER_API_KEY`).
- **Tracing**: If providers do not support OpenAI-like tracing, disable or set a custom trace processor.
- **Fallback**: In a pinch, direct HTTP requests can be used for all providers if official Python libraries are unavailable.

