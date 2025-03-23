from scrapegraphai.graphs import SearchGraph
import nest_asyncio
nest_asyncio.apply()

# Define the configuration for the graph
graph_config = {
    "llm": {
        "model": "ollama/llama3.2:3b",
        "temperature": 0,
        "format": "json",
        # "model_tokens": 3072
    },
    "verbose": True,
    "headless": False,
    # "parse": {
    #     "chunk_size": 16384,
    #     "chunk_overlap": 256    
    # },
    
    # "model_tokens": 8192,
}

# Create the SearchGraph instance
search_graph = SearchGraph(
    prompt="Find the page that contains the undergraduate Computer Science course catalog from Rutgers University",
    config=graph_config
)

# Run the graph
result = search_graph.run()
    
import json

output = json.dumps(result, indent=2)

line_list = output.split("\n")  # Sort of line replacing "\n" with a new line

for line in line_list:
    print(line)