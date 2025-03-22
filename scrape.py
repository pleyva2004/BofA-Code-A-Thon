from scrapegraphai.graphs import SmartScraperGraph

# Configure your LLM settings (using your local model via Ollama, for example)
graph_config = {
    "llm": {
        "model": "ollama/llama3",         # This is the model you pulled and are running locally
        "model_tokens": 8192,             # Adjust context length if needed
        "temperature": 0,                 # Deterministic output
        "format": "json",                 # Specify desired output format
        "base_url": "http://127.0.0.1:11434"  # URL of your local Ollama server
    },
    "verbose": True,
    "headless": False,
}

# Create an instance of the SmartScraperGraph
smart_scraper_graph = SmartScraperGraph(
    prompt="Extract Computer Science Computer information. I need the course number and description.",
    source="https://catalog.njit.edu/undergraduate/computing-sciences/computer-science/#coursestext",
    config=graph_config
)

# Run the scraping pipeline
result = smart_scraper_graph.run()

print(result)
