import re
import sys
from pathlib import Path

import streamlit as st

# Add backend to path
sys.path.append(str(Path(__file__).parent))

from backend.core import run_llm

# Page configuration
st.set_page_config(
    page_title="LangChain Documentation Helper",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown(
    """
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #6c757d;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    /* Remove default Streamlit containers/padding */
    .block-container {
        padding-top: 2rem !important;
    }
    
    .element-container {
        margin: 0 !important;
    }
    
    /* Hide empty divs */
    div:empty {
        display: none !important;
    }
    
    .chat-container {
        max-width: 900px;
        margin: 0 auto;
        padding: 20px 0;
    }
    
    .chat-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .chat-message {
        display: flex;
        margin-bottom: 1.5rem;
        animation: fadeIn 0.3s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .user-message {
        justify-content: flex-end;
    }
    
    .assistant-message {
        justify-content: flex-start;
    }
    
    .message-avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        flex-shrink: 0;
        margin: 0 12px;
    }
    
    .user-avatar {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        order: 2;
    }
    
    .assistant-avatar {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        order: 1;
    }
    
    .message-content {
        max-width: 70%;
        padding: 14px 18px;
        border-radius: 18px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        line-height: 1.6;
    }
    
    .user-content {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-bottom-right-radius: 4px;
        order: 1;
    }
    
    .assistant-content {
        background: #ffffff;
        color: #2d3748;
        border: 1px solid #e2e8f0;
        border-bottom-left-radius: 4px;
        order: 2;
    }
    
    .message-role {
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 6px;
        opacity: 0.9;
    }
    
    .message-text {
        font-size: 0.95rem;
        line-height: 1.8;
    }
    
    /* Markdown styling within messages */
    .message-text p {
        margin: 0 0 12px 0;
    }
    
    .message-text p:last-child {
        margin-bottom: 0;
    }
    
    .message-text strong {
        font-weight: 700;
        color: inherit;
    }
    
    .assistant-content .message-text strong {
        color: #667eea;
    }
    
    .message-text em {
        font-style: italic;
    }
    
    .message-text code {
        background: rgba(0, 0, 0, 0.05);
        padding: 2px 6px;
        border-radius: 4px;
        font-family: 'Courier New', monospace;
        font-size: 0.9em;
    }
    
    .user-content .message-text code {
        background: rgba(255, 255, 255, 0.2);
    }
    
    .message-text a {
        color: #667eea;
        text-decoration: underline;
        word-break: break-all;
    }
    
    .user-content .message-text a {
        color: #ffffff;
        text-decoration: underline;
    }
    
    .message-text ul, .message-text ol {
        margin: 8px 0;
        padding-left: 20px;
    }
    
    .message-text li {
        margin: 4px 0;
    }
    
    .sources-container {
        margin-left: 52px;
        margin-top: -10px;
        margin-bottom: 20px;
        max-width: 70%;
    }
    
    .source-box {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border-left: 4px solid #f59e0b;
        border-radius: 10px;
        padding: 16px;
        margin: 12px 0;
        box-shadow: 0 2px 6px rgba(245, 158, 11, 0.15);
    }
    
    .source-title {
        font-weight: 600;
        color: #92400e;
        margin-bottom: 10px;
        font-size: 0.9rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .source-url {
        font-size: 0.8rem;
        color: #b45309;
        margin-bottom: 8px;
        word-break: break-all;
    }
    
    .source-content {
        color: #78350f;
        font-size: 0.85rem;
        line-height: 1.6;
        background: rgba(255, 255, 255, 0.5);
        padding: 10px;
        border-radius: 6px;
        font-family: 'Courier New', monospace;
    }
    
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        padding: 12px 20px;
        font-weight: 500;
        transition: all 0.3s ease;
        border: 2px solid #e2e8f0;
        background: white;
        color: #4a5568;
    }
    
    .stButton > button:hover {
        border-color: #667eea;
        color: #667eea;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
    }
    
    .example-section {
        background: transparent;
        padding: 24px;
        border-radius: 12px;
        margin-top: 0px;
    }
    
    /* Fix expander styling */
    .stExpander {
        background: transparent !important;
        border: none !important;
    }
    
    div[data-testid="stExpander"] {
        background: transparent !important;
    }
    
    div[data-testid="stExpander"] > div {
        background: transparent !important;
    }
    
    .streamlit-expanderHeader {
        background: transparent !important;
        color: #667eea !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
    }
    
    .streamlit-expanderContent {
        background: transparent !important;
        border: none !important;
    }
    
    /* Hide the default header styles */
    h1, h2, h3 {
        margin-top: 0 !important;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "processing_query" not in st.session_state:
    st.session_state.processing_query = None


# Helper function to convert simple markdown to HTML
def markdown_to_html(text):
    """Convert common markdown patterns to HTML"""
    # Escape HTML first
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    # Convert **bold**
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)

    # Convert *italic*
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)

    # Convert `code`
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)

    # Convert [text](url) links
    text = re.sub(
        r"\[([^\]]+)\]\(([^\)]+)\)", r'<a href="\2" target="_blank">\1</a>', text
    )

    # Convert line breaks to paragraphs
    paragraphs = text.split("\n\n")
    paragraphs = [
        f'<p>{p.replace(chr(10), "<br>")}</p>' for p in paragraphs if p.strip()
    ]

    return "".join(paragraphs)


# Helper function to process queries
def process_query(query: str):
    """Process a query and add the response to messages"""
    try:
        # Call your backend
        result = run_llm(query=query)

        answer = result["answer"]
        context_docs = result["context"]

        # Format sources and remove duplicates based on URL
        seen_urls = set()
        sources = []
        for doc in context_docs:
            url = doc.metadata.get("source", "Unknown")
            # Only add if we haven't seen this URL before
            if url not in seen_urls:
                seen_urls.add(url)
                sources.append(
                    {
                        "url": url,
                        "content": doc.page_content,
                    }
                )

        # Add assistant message to history
        st.session_state.messages.append(
            {"role": "assistant", "content": answer, "sources": sources}
        )

        return True

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        st.error(
            "Make sure your .env file is configured with OPENAI_API_KEY and PINECONE_API_KEY"
        )
        return False


# Header
st.markdown(
    '<div class="main-header">📚 LangChain Documentation Helper</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="sub-header">Ask questions about LangChain documentation using AI-powered search</div>',
    unsafe_allow_html=True,
)

# Sidebar
with st.sidebar:
    st.header("ℹ️ About")
    st.markdown("""
    This app helps you find answers from LangChain documentation using:
    
    - **Pinecone Vector Store** for semantic search
    - **OpenAI GPT** for intelligent answers
    - **LangChain Agents** for retrieval
    
    The documentation is pre-indexed from [python.langchain.com](https://python.langchain.com/)
    """)

    st.divider()

    st.header("📊 Stats")
    st.metric("Total Messages", len(st.session_state.messages))
    st.metric(
        "Conversations",
        len([m for m in st.session_state.messages if m["role"] == "user"]),
    )

    st.divider()

    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.session_state.processing_query = None
        st.rerun()

    st.divider()

    st.markdown("---")
    st.caption("Built with Streamlit & LangChain")

# Check if we need to process a pending query
if st.session_state.processing_query:
    with st.spinner("🔍 Searching documentation and generating answer..."):
        query = st.session_state.processing_query
        st.session_state.processing_query = None
        if process_query(query):
            st.rerun()

# Main chat interface - using custom HTML header instead of st.header
st.markdown('<div class="chat-header">💬 Chat</div>', unsafe_allow_html=True)

# Display chat history only if there are messages
if len(st.session_state.messages) > 0:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)

    for idx, message in enumerate(st.session_state.messages):
        # Convert markdown to HTML for better rendering
        content_html = markdown_to_html(message["content"])

        if message["role"] == "user":
            st.markdown(
                f"""
            <div class="chat-message user-message">
                <div class="message-content user-content">
                    <div class="message-role">You</div>
                    <div class="message-text">{content_html}</div>
                </div>
                <div class="message-avatar user-avatar">👤</div>
            </div>
            """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
            <div class="chat-message assistant-message">
                <div class="message-avatar assistant-avatar">🤖</div>
                <div class="message-content assistant-content">
                    <div class="message-role">Assistant</div>
                    <div class="message-text">{content_html}</div>
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )

            # Show sources if available
            if "sources" in message and message["sources"]:
                with st.expander("📚 View Sources", expanded=False):
                    st.markdown(
                        '<div class="sources-container">', unsafe_allow_html=True
                    )
                    for i, source in enumerate(message["sources"], 1):
                        st.markdown(
                            f"""
                        <div class="source-box">
                            <div class="source-title">
                                <span>📄 Source {i}</span>
                            </div>
                            <div class="source-url">🔗 {source["url"]}</div>
                        </div>
                        """,
                            unsafe_allow_html=True,
                        )
                    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input("Ask a question about LangChain documentation..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.processing_query = prompt
    st.rerun()

# Example questions - only show when no messages
if len(st.session_state.messages) == 0:
    st.markdown('<div class="example-section">', unsafe_allow_html=True)
    st.markdown(
        '<div style="font-size: 1.2rem; font-weight: 600; color: #2d3748; margin-bottom: 1rem;">💡 Try asking:</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("What are LangChain agents?"):
            query = "What are LangChain agents?"
            st.session_state.messages.append({"role": "user", "content": query})
            st.session_state.processing_query = query
            st.rerun()

        if st.button("How do I use LCEL?"):
            query = "How do I use LCEL?"
            st.session_state.messages.append({"role": "user", "content": query})
            st.session_state.processing_query = query
            st.rerun()

    with col2:
        if st.button("What are deep agents?"):
            query = "What are deep agents?"
            st.session_state.messages.append({"role": "user", "content": query})
            st.session_state.processing_query = query
            st.rerun()

        if st.button("How do I create a RAG pipeline?"):
            query = "How do I create a RAG pipeline?"
            st.session_state.messages.append({"role": "user", "content": query})
            st.session_state.processing_query = query
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #a0aec0; padding: 1rem;'>
        <p style='margin: 0; font-size: 0.9rem;'>Powered by LangChain, OpenAI & Pinecone | Built with ❤️ using Streamlit</p>
    </div>
""",
    unsafe_allow_html=True,
)