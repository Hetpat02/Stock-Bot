import streamlit as st
from financial_agent import create_agents, as_stream

st.title("FinAI: Your AI Finance Navigator")

# Sidebar options
st.sidebar.header("Settings")
llm_option = st.sidebar.selectbox("Choose your LLM:", ["Ollama", "OpenAI", "Groq"])

openai_api_key=None
grop_api_key=None
if llm_option == "OpenAI":
    openai_api_key = st.sidebar.text_input("Enter your OpenAI API Key:", type="password")

elif llm_option == "Groq":
    groq_api_key = st.sidebar.text_input("Enter your Groq API Key:", type="password")

# Initialize Agents (Conditionally)
web_src_agt, finance_agent, multi_ai_agent = None, None, None
try:
    if llm_option == "Ollama":
        web_src_agt, finance_agent, multi_ai_agent = create_agents(llm_option)
    elif llm_option == "OpenAI" and openai_api_key:
        web_src_agt, finance_agent, multi_ai_agent = create_agents(llm_option, openai_api_key=openai_api_key)
    elif llm_option == "Groq" and groq_api_key:
        web_src_agt, finance_agent, multi_ai_agent = create_agents(llm_option, groq_api_key=groq_api_key)
    elif llm_option == "OpenAI" and not openai_api_key:
        st.error("Please enter your OpenAI API key to use OpenAI.")
    elif llm_option == "Groq" and not groq_api_key:
        st.error("Please enter your Groq API key to use Deepseek.")
except ValueError as e:
    st.error(f"Error: {e}")
    web_src_agt, finance_agent, multi_ai_agent = None, None, None
except Exception as e:
    st.error(f"An unexpected error occurred during agent initialization: {e}")
    web_src_agt, finance_agent, multi_ai_agent = None, None, None

# --- Streamlit UI (Chat Interface) ---
if web_src_agt and finance_agent and multi_ai_agent:  # Only run if agents are initialized
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if prompt := st.chat_input("Enter your financial query:"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                # Show analysis in progress
                analysis_placeholder = st.empty()
                analysis_placeholder.markdown("Analyzing market data and recent news...")
            
                # Process the response stream
                response = ""
                for chunk in as_stream(multi_ai_agent.run(prompt, stream=True)):
                    if isinstance(chunk, str):
                        response += chunk
                        # Update the display as we get new chunks
                        analysis_placeholder.markdown(response)
            
                if response:
                    st.session_state.messages.append({"role": "assistant", "content": response})
                else:
                    st.error("No valid response generated. Please try your query again.")
                
            except Exception as e:
                st.error(f"Error during analysis: {str(e)}")
                st.session_state.messages.append({"role": "assistant", 
                    "content": f"I encountered an error while analyzing: {str(e)}"})
