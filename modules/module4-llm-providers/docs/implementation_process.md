# Module 4 - Implementation Process

## Checklist of Activities

### Phase 1 — Environment & Setup
- [ ] Copy or inherit all files from Module 3
- [ ] Create directory structure:
  - [ ] `app/agents/llm_providers/...`
  - [ ] `app/routers/llm_router.py`
  - [ ] `tests/`
  - [ ] `docs/`
- [ ] Initialize environment variables in `.env`:
  - [ ] `OPENAI_API_KEY`
  - [ ] `GEMINI_API_KEY`
  - [ ] `REQUESTRY_API_KEY`
  - [ ] `OPENROUTER_API_KEY`
- [ ] Confirm basic logging works
- [ ] Draft tests with placeholders:
  - [ ] `test_openai_agent.py`
  - [ ] `test_gemini_agent.py`
  - [ ] `test_requestry_agent.py`
  - [ ] `test_openrouter_agent.py`
  - [ ] `test_recommender_agent.py`

### Phase 2 — OpenAI Multi-Model Agent
- [ ] Implement `openai_agent.py`:
  - [ ] Support multiple models (`gpt-4o`, `o3-mini`, etc.)
  - [ ] Use environment variables for API keys
  - [ ] Implement `process_prompt(...)` method
- [ ] Create tests in `test_openai_agent.py`:
  - [ ] Test valid model usage
  - [ ] Test missing API key scenario
  - [ ] Mock `openai` calls if needed
- [ ] Add endpoint in `llm_router.py` for `/agents/llm-providers/openai`
- [ ] Update `docs/implementation_process.md` with progress

### Phase 3 — Gemini, Requestry, OpenRouter Agents
- [ ] Implement Gemini agent:
  - [ ] Create `gemini_agent.py` with `GEMINI_API_KEY`
  - [ ] Implement code from provider references
  - [ ] Add tests in `test_gemini_agent.py`
- [ ] Implement Requestry agent:
  - [ ] Create `requestry_agent.py` with `REQUESTRY_API_KEY`
  - [ ] Validate model usage: `cline/o3-mini`, `cline/4o-mini`
  - [ ] Add tests in `test_requestry_agent.py`
- [ ] Implement OpenRouter agent:
  - [ ] Create `openrouter_agent.py` with `OPENROUTER_API_KEY`
  - [ ] Add optional headers support
  - [ ] Add tests in `test_openrouter_agent.py`
- [ ] Add endpoints in `llm_router.py`:
  - [ ] `/agents/llm-providers/gemini`
  - [ ] `/agents/llm-providers/requestry`
  - [ ] `/agents/llm-providers/openrouter`
- [ ] Refactor code for consistency
- [ ] Update documentation

### Phase 4 — Model Recommender
- [ ] Create `recommender_agent.py`:
  - [ ] Accept task type and prompt length
  - [ ] Return recommended provider and model
  - [ ] Implement decision logic
- [ ] Test in `test_recommender_agent.py`:
  - [ ] Test various scenarios (short conversation, reasoning tasks)
  - [ ] Validate response format
- [ ] Add endpoint `/agents/llm-providers/recommend-model`
- [ ] Refactor if needed
- [ ] Update documentation

### Phase 5 — Documentation & Final Checks
- [ ] Finalize documentation:
  - [ ] `docs/phase1.md` through `docs/phase5.md`
  - [ ] `docs/guidelines.md`
  - [ ] `docs/implementation_process.md`
  - [ ] `README.md`
- [ ] Run full test suite
- [ ] Review logs for issues
- [ ] Validate code meets PEP 8 standards
- [ ] Final review and merge
