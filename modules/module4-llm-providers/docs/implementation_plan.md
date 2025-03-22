# Module 4: Custom LLM Providers — Implementation Plan

This plan has 5 phases to add multi-provider support (OpenAI, Gemini, Requestry, OpenRouter) plus a model recommender. It follows principles outlined in the main README.

---

## Phase 1 — Environment & Setup

1. **Copy or inherit all files from Module 3**  
2. **Create new directory structure** under `module4-llm-providers/`
   - `app/agents/llm_providers/...`
   - `app/routers/llm_router.py`
   - `tests/`
   - `docs/`
3. **Initialize environment variables** in `.env`:
   - `OPENAI_API_KEY`
   - `GEMINI_API_KEY`
   - `REQUESTRY_API_KEY`
   - `OPENROUTER_API_KEY`
   - Any custom model references (e.g. `EXAMPLE_MODEL_NAME`)
4. **Confirm basic logging** works
5. **Draft tests**: `test_openai_agent.py`, etc. with placeholders

**Exit Criteria**:
- Basic folder structure
- `.env` set
- Empty or skeleton test files

---

## Phase 2 — OpenAI Multi-Model Agent

1. **Implement** `openai_agent.py`:
   - Support `gpt-4o`, `o3-mini`, etc.
   - Use environment variables for API keys
   - Provide `process_prompt(...)` returning consistent structure
2. **Create Tests** in `test_openai_agent.py`:
   - Check valid model usage
   - Check missing API key
   - Mock `openai` calls if needed
3. **Add Endpoint** in `llm_router.py` for `/agents/llm-providers/openai`
4. **Update** `docs/implementation_process.md` after test pass

**Exit Criteria**:
- Working OpenAI multi-model agent
- Tests passing

**Confirmed Working Models**:
- `gpt-3.5-turbo` - Default model, good balance of performance and cost
- `gpt-4o` - Latest model with advanced capabilities
- `gpt-4-turbo` - Powerful model with strong reasoning capabilities

---

## Phase 3 — Gemini, Requestry, OpenRouter Agents

1. **Gemini**:  
   - `gemini_agent.py` loads `GEMINI_API_KEY`
   - Uses code snippet from prior version  
   - Provide test coverage: `test_gemini_agent.py`
2. **Requestry**:  
   - `requestry_agent.py` with `REQUESTRY_API_KEY`
   - Python snippet from Requestry docs  
   - Validate model usage: `cline/o3-mini`, `cline/4o-mini`
3. **OpenRouter**:  
   - `openrouter_agent.py`
   - Accepts `OPENROUTER_API_KEY`
   - Uses standard base URL: `https://openrouter.ai/api/v1`
   - Add optional headers (e.g. `HTTP-Referer`, `X-Title`)
4. **Endpoints** in `llm_router.py`:
   - `/agents/llm-providers/gemini`
   - `/agents/llm-providers/requestry`
   - `/agents/llm-providers/openrouter`
5. **Refactor** code to unify patterns if needed
6. **Update** logs and docs upon completion

**Exit Criteria**:
- All agents tested and functional
- Endpoints returning success with valid credentials

**Confirmed Working Models**:

**Gemini**:
- `gemini-2.0-pro-exp-02-05` - Default model, experimental version with advanced capabilities
- `gemini-1.5-pro` - Stable model with good performance
- `gemini-1.5-flash` - Faster, more efficient model for simpler tasks
- `gemini-1.0-pro` - Original model, still supported

**Requestry**:
- `cline/o3-mini` - Default model, efficient and cost-effective
- `cline/4o-mini` - More powerful model with advanced capabilities

**OpenRouter**:
- `openai/gpt-4o` - Default model, OpenAI's latest model through OpenRouter
- Many other models available through the OpenRouter platform

---

## Phase 4 — Model Recommender

1. **Create** `recommender_agent.py`:
   - Accepts a structure:
     ```json
     {
       "task_type": "reasoning",
       "prompt_length": 200
     }
     ```
   - Returns recommended provider and model
   - (Optional) Use an LLM to decide or just a simple lookup
2. **Test** in `test_recommender_agent.py`:
   - Various scenarios: short conversation vs. big reasoning
3. **Add** endpoint `/agents/llm-providers/recommend-model`
4. **Refactor** if logic grows complex
5. **Update** docs and logs

**Exit Criteria**:
- Recommender agent picks plausible model
- Consistent response format validated by tests

---

## Phase 5 — Documentation & Final Checks

1. **Add** or finalize these docs located in modules/module4-llm-providers/
   - `docs/phase1.md` through `docs/phase5.md` (detailed tutorials)
   - `docs/guidelines.md` (already drafted)
   - `docs/implementation_process.md` (update after each step)
   - `README.md` clarifications (key references)
   - `implementation_process.md` - ensure checlist is complete - all tests have been confirmed they pass
   - `docs/tutorial.md` (ensure full step by step guide)
2. Update root/readme.md

