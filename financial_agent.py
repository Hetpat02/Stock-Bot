from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.model.ollama import Ollama
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
import openai
from phi.run.response import RunEvent, RunResponse


def create_agents(llm_option, openai_api_key=None, groq_api_key=None):
    """Creates and returns the web_src_agt, finance_agent, and multi_ai_agent."""

    if llm_option == "Ollama":
        llm = Ollama(id='llama3.2:1b')  # Use your downloaded Ollama model name here
    elif llm_option == "OpenAI":
        if not openai_api_key:
            raise ValueError("OpenAI API Key is required when using OpenAI. Please provide it in the UI.")
        try:
            openai.api_key = openai_api_key
            llm = OpenAIChat(model="gpt-3.5-turbo", api_key=openai_api_key)
        except Exception as e:
            raise ValueError(f"Error initializing OpenAI: {e}")
    elif llm_option == "Groq":
        if not groq_api_key:
            raise ValueError("Groq API Key is required when using Groq. Please provide it in the UI.")
        try:
            Groq.api_key = groq_api_key
            llm = Groq(id="deepseek-r1-distill-llama-70b", api_key=groq_api_key)#id="deepseek-r1-distill-llama-70b"
        except Exception as e:
            raise ValueError(f"Error initializing OpenAI: {e}")
    else:
        raise ValueError("Invalid LLM option. Choose 'Ollama' or 'OpenAI'.")

    
    # Enhanced web search agent with specific financial news focus
    web_src_agt = Agent(
        name='Web Search Agent',
        role='Search for latest financial news and analysis',
        model=llm,
        tools=[DuckDuckGo()],
        instructions=[
            "Focus on recent financial news and market analysis",
            "Look for expert opinions and market sentiment",
            "Include relevant sources but format them naturally in the response",
            "Highlight key market-moving news",
            "Filter out any function call data from responses"
        ],
        show_tool_calls=False,
        markdown=True,
    )

    # Enhanced financial agent with comprehensive analysis capabilities
    finance_agent = Agent(
        name='Finance AI Agent',
        model=llm,
        tools=[YFinanceTools(stock_price=True, analyst_recommendations=True,
                           stock_fundamentals=True, company_news=True)],
        instructions=[
            "Provide comprehensive stock analysis including:",
            "- Current market data and trends",
            "- Key financial metrics and ratios",
            "- Technical indicators when relevant",
            "- Recent price movements and volume",
            "Format data in clear, readable tables",
            "Include brief explanations of significant metrics"
        ],
        show_tool_calls=False,
        markdown=True,
    )

    # Enhanced multi-agent coordinator
    multi_ai_agent = Agent(
        team=[web_src_agt, finance_agent],
        model=llm,
        instructions=[
            "Combine market data and news analysis into coherent insights",
            "If the user query is straightforward (e.g., asking for a single fact or number), provide a direct response.",
            "If the query requires a detailed response, use this format:",
            "1. Market Data Overview",
            "2. Recent News Analysis",
            "3. Expert Opinions",
            "4. Potential Risks and Opportunities",
            "5. Summary and Suggestions",
            "Use tables for numerical data",
            "Format news references naturally in the text",
            "Provide balanced analysis considering both bullish and bearish factors",
            "Determine the required format based on query length and complexity.",
            "Avoid unnecessary formatting for simple questions.",
        ],
        show_tool_calls=False,
        markdown=True,
    )

    return web_src_agt, finance_agent, multi_ai_agent


def as_stream(response):
    """Enhanced stream processor to handle multiple types of content"""
    for chunk in response:
        if isinstance(chunk, RunResponse) and isinstance(chunk.content, str):
            if chunk.event == RunEvent.run_response:
                # Skip function calls but keep actual content
                if not any(skip in chunk.content.lower() for skip in 
                    ['"type":"function"', 'parameters', 'task_description']):
                    yield chunk.content
        elif isinstance(chunk, str):
            # Direct string content
            yield chunk

