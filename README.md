StockBot – AI‑powered Stock & Finance Assistant
Stock‑Bot is a chat‑based finance assistant designed to provide comprehensive stock research, market analysis and news summaries. The system combines multiple large‑language models (LLMs) with specialised tools to collect up‑to‑date stock data and recent news and to organise them into coherent insights. FinAI is implemented as a Streamlit application and can be run locally, in a container or deployed via an automated CI/CD pipeline to services such as AWS App Runner.
<details> <summary><strong>Table of contents</strong></summary>
Features
Architecture
Project structure
Prerequisites
Local setup
Running with Docker
Configuration
Usage
CI/CD and AWS deployment
Contributing
License
</details>
Features
StockBot offers a rich set of capabilities built on top of the phi agent framework and multiple LLM back‑ends:
Interactive Streamlit front‑end. A chat interface is built using
Streamlit. The main page sets a title and defines a sidebar where
users can select their preferred language model: Ollama, OpenAI
or Groq
raw.githubusercontent.com
. Depending on the selection, the
application prompts for the appropriate API key and initialises agents
raw.githubusercontent.com
.
Multi‑agent AI system. The core logic lives in
financial_agent.py, where three different agents are created via the
create_agents function. The web search agent uses DuckDuckGo to
retrieve the latest financial news
raw.githubusercontent.com
; the
finance agent uses YFinanceTools to pull current stock prices,
fundamentals, analyst recommendations and company news
raw.githubusercontent.com
; and a
multi‑agent coordinator combines the outputs and provides guidance on
structuring responses (e.g., market data overview, news analysis,
expert opinions, risks/opportunities and summary)
raw.githubusercontent.com
.
Real‑time streaming of responses. Responses from the agents are
streamed back to the UI in real time. The helper function
as_stream filters out tool calls and yields only human‑readable
content
raw.githubusercontent.com
. As the assistant generates a reply,
the Streamlit interface updates the display progressively
raw.githubusercontent.com
.
Flexible language model selection. Users can run FinAI completely
offline via the open‑source Ollama model, or
opt into paid APIs such as OpenAI’s gpt‑3.5‑turbo
raw.githubusercontent.com

or Groq’s hosted Llama‑70B variant
raw.githubusercontent.com
. The
application gracefully handles missing API keys by displaying error
messages rather than crashing
raw.githubusercontent.com
.
Containerisation. A Dockerfile is provided to build a compact
Python 3.11 image with all dependencies installed
raw.githubusercontent.com
. When the
container is run, Streamlit exposes port 8501 and launches the
application
raw.githubusercontent.com
.
Automated CI/CD pipeline. A declarative Jenkins pipeline is
included. It clones the repository, builds the Docker image,
scans it with Aquatrivy (Trivy) and pushes the image to AWS Elastic
Container Registry (ECR)
raw.githubusercontent.com
. An optional (currently
commented‑out) stage illustrates how to trigger a deployment to AWS
App Runner
raw.githubusercontent.com
. A custom Jenkins Dockerfile is
available in custom_jenkins/ to install Docker inside the Jenkins
agent and allow building and pushing images
raw.githubusercontent.com
.
Architecture
At a high level, FinAI is a conversational application that orchestrates
multiple specialised agents to answer finance‑related queries:
User Interface (Streamlit). A front‑end built with Streamlit
provides a chat UI and a settings sidebar. Users can select their
preferred LLM and provide API keys as needed
raw.githubusercontent.com
.
Agent creation (create_agents). Depending on the chosen LLM,
the application instantiates a language model instance and then sets up
three agents:
Web Search Agent – Retrieves the latest financial news via
DuckDuckGo and is instructed to focus on expert opinions, market
sentiment and key market‑moving news
raw.githubusercontent.com
.
Finance Agent – Interfaces with YFinance to obtain real‑time
stock prices, fundamentals, analyst recommendations and company
news
raw.githubusercontent.com
. It is instructed to generate
comprehensive stock analysis, use tables for numerical data and
explain significant metrics
raw.githubusercontent.com
.
Multi‑agent Coordinator – Receives inputs from both agents and
crafts a unified answer, following a structured guideline that
includes data overview, news analysis, expert opinions, risks and
opportunities and a summary
raw.githubusercontent.com
.
Streaming Response. The as_stream helper yields each chunk of
content as it is produced
raw.githubusercontent.com
. Streamlit renders
these chunks in real time, giving the user immediate feedback while the
full analysis is being generated
raw.githubusercontent.com
.
The diagram below summarises these components:
┌─────────────────┐     selects      ┌─────────────────────┐
│  User (UI)      │ ───────────────▷│  Language model     │
│  (Streamlit)    │                 │  (Ollama/OpenAI/Groq)│
└─────────────────┘                 └────────────▲─────────┘
               │                                   │
        initialises                          supplies context
               ▼                                   ▼
        ┌──────────────┐                  ┌──────────────────┐
        │  Web agent   │  ───────────────▷│  Finance agent   │
        │ (DuckDuckGo) │                  │ (YFinanceTools)  │
        └──────────────┘                  └──────────────────┘
               │                                    ▲
               │        coordinates results          │
               └──────────────────────────────┬──────┘
                                              │
                                       ┌───────────────┐
                                       │  Multi‑agent   │
                                       │  coordinator   │
                                       └───────────────┘
Project structure
├── main.py            # Streamlit entry point and chat UI:contentReference[oaicite:22]{index=22}
├── financial_agent.py # Defines web, finance and coordinator agents:contentReference[oaicite:23]{index=23}
├── requirements.txt   # Python dependencies:contentReference[oaicite:24]{index=24}
├── Dockerfile         # Build instructions for the application container:contentReference[oaicite:25]{index=25}
├── Jenkinsfile        # Declarative Jenkins pipeline for CI/CD:contentReference[oaicite:26]{index=26}
├── custom_jenkins/
│   └── Dockerfile     # Custom Jenkins image with Docker installed:contentReference[oaicite:27]{index=27}
└── .gitignore         # Excludes environment files and caches:contentReference[oaicite:28]{index=28}
Prerequisites
Python 3.9+ (FinAI was developed against Python 3.11 and tested with the
slim image defined in the Dockerfile
raw.githubusercontent.com
).
pip for installing Python dependencies. All required packages
are listed in requirements.txt
raw.githubusercontent.com
.
An LLM provider – either a local Ollama model or
API keys for OpenAI or Groq.
Optional: Docker and Docker Compose for running the container and
reproducing the CI pipeline; Jenkins if you want to execute the
provided pipeline.
Local setup
Clone the repository (or download the source). In environments
without direct git clone access, download the code as a ZIP and
extract it.
Create a virtual environment (recommended) and install
dependencies:
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
Run the application using Streamlit:
streamlit run main.py
The app will start a web server on http://localhost:8501. Open this
address in your browser. Select a language model in the sidebar and
provide the necessary API keys. Ask any finance‑related question to
start a conversation.
Running with Docker
If you prefer to run the application in an isolated container, use the
provided Dockerfile:
# Build the Docker image
docker build -t stock-bot:latest .

# Run the container, exposing Streamlit on port 8501
docker run --rm -p 8501:8501 stock-bot:latest
This builds a minimal Python 3.11 image
raw.githubusercontent.com
 and runs the
Streamlit server on port 8501
raw.githubusercontent.com
. When first launched
you may need to pull large LLM models (for Ollama) or supply API keys for
OpenAI or Groq through the UI.
Configuration
FinAI allows you to choose between multiple language models. You can set
API keys in the UI, but for scripted deployments it is convenient to
provide them via environment variables. The following variables are
recognised:
Variable	Purpose
OPENAI_API_KEY	API key for OpenAI’s GPT models.
GROQ_API_KEY	API key for Groq’s Llama 70B service.
OLLAMA_MODEL	Name of the local Ollama model (default llama3.2:1b).
If you do not provide keys for the selected LLM, the application
raises an error informing you to enter the key via the UI
raw.githubusercontent.com
.
Usage
After starting the application (either locally or in a container), you
interact with FinAI through a simple chat interface. Here is an
example workflow:
In the left sidebar, choose Ollama, OpenAI or Groq as the
LLM provider.
If required, paste your API key into the field that appears.
Type a finance‑related question such as:
“What’s the outlook for AAPL over the next quarter?”
FinAI streams its response in real time; first you will see the
analysis placeholder (“Analyzing market data and recent news…”)
raw.githubusercontent.com
.
Soon after, the assistant will synthesise stock price data, recent news
articles and expert commentary into a coherent answer based on the
structure described above
raw.githubusercontent.com
.
CI/CD and AWS deployment
FinAI includes a complete CI/CD workflow using Jenkins and AWS:
Custom Jenkins agent. The custom_jenkins/Dockerfile builds an
image based on jenkins/jenkins:lts and installs Docker inside the
agent
raw.githubusercontent.com
. It also adds the Jenkins user to the
Docker group
raw.githubusercontent.com
 and mounts /var/lib/docker as a
volume for Docker‑in‑Docker
raw.githubusercontent.com
.
Pipeline definition. The Jenkinsfile sets environment variables
for the AWS region, ECR repository name, image tag and service name
raw.githubusercontent.com
.
The first stage clones the GitHub repository using a token
raw.githubusercontent.com
.
The second stage builds the Docker image, runs an Aquatrivy scan via
trivy image and pushes the image to ECR
raw.githubusercontent.com
. Scan
reports are archived as build artefacts
raw.githubusercontent.com
.
Deployment. The pipeline contains a commented stage showing how to
trigger an AWS App Runner deployment by obtaining the service ARN and
calling aws apprunner start-deployment
raw.githubusercontent.com
. You can
uncomment this block to enable automatic deployment.
Manual deployment on AWS App Runner. After pushing the image to
ECR, you can create an App Runner service pointing at the repository.
Choose Continuous deployment so new images trigger redeployment. The
service name should match SERVICE_NAME defined in the Jenkinsfile.
Security scanning. The pipeline uses Trivy to scan the image for
high and critical vulnerabilities
raw.githubusercontent.com
. Reports are
saved as trivy-report.json and can be integrated into further
auditing workflows.
Contributing
Contributions are welcome! To propose a feature or report a bug, please
open an issue describing your motivation and expected behaviour. Pull
requests should be targeted at the main branch and accompany a clear
description of the change. Please ensure that tests (if added in the
future) pass and that your code follows PEP 8 formatting guidelines.
License
This project currently does not include an explicit license file. Unless
and until a license is added, contributions remain the intellectual
property of their authors. If you plan to use this project in
production, please contact the repository owner for licensing terms.
