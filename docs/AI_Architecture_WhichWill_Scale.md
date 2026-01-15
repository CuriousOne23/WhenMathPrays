flowchart LR
    A[User Input] --> B[Integrator LLM]
    B --> C[Safety LLM]
    B --> D[Planning LLM]
    C --> B
    D --> B
    B --> E[Final Output]
