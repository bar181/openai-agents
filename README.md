# openai-agents

# OpenAI Agents Mono Repo

Welcome to the OpenAI Agents Mono Repo! This repository is organized as a mono repo, where each phase of our project is maintained in its own folder. This approach allows us to clearly separate different stages of development and examples, making it easier to manage, maintain, and scale the project over time.

---

## Current Phase

### Phase1a-Hello-World

- **Folder:** `phase1a-hello-world/`
- **Description:** In Phase1a, we implement a minimal "Hello World" agent using FastAPI and the OpenAI Agents SDK. This agent responds with a greeting when called through an HTTP endpoint.
- **Tutorial:** For a detailed, step-by-step guide on how this phase was built, refer to the [tutorial.md](/phase1a-hello-world/docs/tutorial.md) file within the `phase1a-hello-world` folder.
- **Testing:** The project includes unit tests to verify the functionality of the agent endpoint.

---

## How the Mono Repo Approach Works

In this repository, each phase or example is housed in its own folder (e.g., `phase1a-hello-world`). This mono repo structure offers several benefits:
- **Modularity:** Each phase is self-contained, allowing independent development and testing.
- **Scalability:** As we add more phases, you’ll easily find them organized in their respective folders.
- **Clarity:** Developers can quickly navigate to the relevant phase based on their needs.
- **Consistency:** All phases share a similar structure and practices, making it easy to extend and maintain the codebase.

---

## Quick Guide to Get Started with Phase1a-Hello-World

1. **Clone the repository** and navigate to the `phase1a-hello-world` folder.
2. **Create and activate a virtual environment.**
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set up your `.env` file:**  
   Rename the `.env.sample` file (if provided) to `.env` and add your OpenAI API key along with a custom `API_KEY` for authorization.
5. **Start the FastAPI server:**
   ```bash
   python -m uvicorn app.main:app --reload
   ```
6. **Access API Documentation:**  
   Visit [http://localhost:8000/docs](http://localhost:8000/docs) and authorize using the API key from your `.env` file.
7. **Run tests:**
   ```bash
   python -m pytest tests/
   ```

For a more detailed explanation of Phase1a, please refer to the [tutorial.md](phase1a-hello-world/tutorial.md) file.

---

## Future Plans

While Phase1a focuses on a simple "Hello World" agent, our roadmap includes several exciting future phases:
- **Phase1b – Core Agent Examples:** Additional examples demonstrating deterministic flows, routing/handoffs, function tools, LLM-as-a-judge, parallelization, and guardrails.
- **Phase2 – Research Bot:** Re-creating a multi-agent research bot that leverages multiple agents to plan, search, and synthesize information.
- **Phase3 – Advanced Features:** Integration of persistence, vector search, and enhanced observability (e.g., tracing and monitoring).
- **Phase4 – Optional Enhancements:** Further refinements and integrations, such as database support with Supabase and additional agent orchestration patterns.

Stay tuned as we continue to expand this mono repo with new phases and examples that showcase the full potential of building autonomous agents using the OpenAI Agents SDK.

---

Happy coding!

cd <folder name>
pip install -r requirements.txt

# FastAPI server with Uvicorn
python -m uvicorn app.main:app --reload