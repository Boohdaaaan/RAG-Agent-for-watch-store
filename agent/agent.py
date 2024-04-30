import uvicorn
from dotenv import load_dotenv
from pydantic import BaseModel
from fastapi import FastAPI, Body
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from tools import info_retriever, feedback_saver, order_placement

# Take environment variables from .env
load_dotenv()

# Creating a FastAPI instance
app = FastAPI()

# List of tools available for the agent to use
tools = [info_retriever, order_placement, feedback_saver]

# Instantiating a ChatOpenAI instance with specified parameters
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# Memory configuration for conversation history
memory = ConversationBufferWindowMemory(
    memory_key="chat_history",
    k=10,
    return_messages=True,
    output_key="output"
)

# Chat prompt template with initial instructions and placeholders for messages
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            f""" ## Overview
                You're a top tier algorithm - conversational agent and your job is to answer the user's questions regarding watch store.
                You can't talk about anything other than watches and the store.

                ## Task
                So you have a few tools at your disposal.
                'info_retriever' - tool that will retrieve set of documents, where you will find information to generate answer.
                'order_placement' - tool that will retrieve user name, surname, phone number, city for product delivery and watch model when the user wants to place an order.
                'feedback_saver' - tool that will retrieve user feedback and their sentiments. 

                Always check chat history to keep the conversation flowing correctly.
                Answer only in Ukrainian!
    """,
        ),
        MessagesPlaceholder("chat_history", optional=True),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

# Creating an agent using OpenAI with specified tools and prompt
agent = create_openai_tools_agent(llm, tools, prompt)

# Executor to manage agent invocation and interactions with tools and memory
agent_executor = AgentExecutor(agent=agent, tools=tools, memory=memory, early_stopping_method="generate",
                               return_intermediate_steps=False, verbose=False)


# Request input format definition
class Query(BaseModel):
    text: str


# Endpoint for handling chat requests
@app.post("/chat")
async def chat(query: Query = Body(...)):
    # Invoking the agent with user input
    response = agent_executor.invoke({"input": query.text})
    return response['output']


# Health check endpoint
@app.get("/health")
async def health():
    """Check if the API is running"""
    return {"status": "OK"}


# Running the FastAPI app with uvicorn server
if __name__ == "__main__":
    uvicorn.run(
        "agent:app",
        host="localhost",
        port=8000,
        reload=True
    )
