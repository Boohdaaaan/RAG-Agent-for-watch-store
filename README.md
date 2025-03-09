# OpenAI Agent as a shop assistant
This repository hosts a LLM-based assistant tailored specifically for watch stores. Powered by OpenAI's GPT model, this assistant enhances customer interactions by offering capabilities such as question answering, order placement, feedback collection. With these functionalities, the AI assistant enhances customer satisfaction, streamlines operations, and provides a seamless shopping experience.


## Data
To empower the AI assistant with the necessary information to respond effectively to user queries, comprehensive data about the store has been independently scraped from the Internet. This data includes various details such as product descriptions, pricing information, store locations, opening hours, and any additional relevant information that may assist customers in their interactions with the AI assistant.

Utilizing the Retrieval Augmented Generation (RAG) technology, this scraped data serves as a crucial knowledge base for the AI assistant. By integrating this data into its knowledge repository, the AI assistant can provide accurate and contextually relevant responses to user inquiries.


## Agent

The core intelligence of the AI assistant is driven by the GPT-3.5 Turbo model.  

Equipped with essential tools, it streamlines customer interactions:
* __Retriever__: Allows the agent to retrieve relevant information.
* __Order Placement__: Allows the agent to record order data into a database, including customer details such as name, surname, phone number, city, and the selected watch model.
* __Feedback Saver__: Allows the agent to collect and store customer feedback along with its emotional tone (negative or positive).


## Video Demonstration
https://github.com/Boohdaaaan/RAG-Agent-for-watch-store/assets/112556009/a250ad94-9871-4587-90ed-6601726b5932


## Usage

### Requirements
* Docker Compose

### Setup
* Clone repository
```bash
  git clone https://github.com/Boohdaaaan/RAG-OpenAI-Agent-for-watch-store.git
```

* Move to project folder
```bash
  cd RAG-OpenAI-Agent-for-watch-store
```

* Set environment variable in the .env file (OpenAI API key)
```bash
  echo "OPENAI_API_KEY=your-api-key-goes-here" > .env
```

* Start the application
```bash
  docker-compose up
```

* To shut down container
```bash
  docker-compose down
```

Once the containers are up and running, you can access the application by navigating to http://localhost:8080 in your web browser.

## Acknowledgments

Special thanks to the developers and communities behind the libraries and tools used in this project for their valuable contributions.
