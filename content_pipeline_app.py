import streamlit as st
from openai import OpenAI
from duckduckgo_search import DDGS

OPENAI_API_KEY = "YOUR_OPENAI_KEY_HERE"  # ENTER YOUR KEY HERE
client = OpenAI(api_key=OPENAI_API_KEY)  # LEAVE THIS LINE ALONE

def web_search(query):
    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=4)
        return "\n".join([r["body"] for r in results])

def researcher(topic):
    search_results = web_search(topic)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a research agent. Summarize key facts from search results."},
            {"role": "user", "content": f"Topic: {topic}\n\nSearch Results:\n{search_results}"}
        ]
    )
    return response.choices[0].message.content

def writer(topic, research):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a professional writer. Write a clear engaging article with title, introduction, main points, and conclusion."},
            {"role": "user", "content": f"Topic: {topic}\n\nResearch:\n{research}"}
        ]
    )
    return response.choices[0].message.content

def editor(article):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a professional editor. Polish this article for clarity and flow."},
            {"role": "user", "content": f"Please edit and improve this article:\n\n{article}"}
        ]
    )
    return response.choices[0].message.content

# ---- STREAMLIT UI ----
st.title("🤖 AI Content Pipeline")
st.subheader("Powered by 3 AI Agents working together")
st.write("Enter any topic and 3 AI agents will research, write, and edit a full article automatically.")

topic = st.text_input("Enter a topic:", placeholder="e.g. The future of AI in healthcare")

if st.button("Generate Article"):
    if topic:
        with st.spinner("Agent 1 researching..."):
            research = researcher(topic)
        st.success("✅ Research complete")
        
        with st.spinner("Agent 2 writing..."):
            article = writer(topic, research)
        st.success("✅ Article written")
        
        with st.spinner("Agent 3 editing..."):
            final = editor(article)
        st.success("✅ Editing complete")
        
        st.markdown("---")
        st.markdown("## Final Article")
        st.markdown(final)
    else:
        st.warning("Please enter a topic first")