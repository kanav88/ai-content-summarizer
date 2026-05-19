import streamlit as st
from services.storage import save_summary
from services.summarizer import summarize_content
from services.youtube_service import get_transcript

st.set_page_config(
    page_title="AI Content Summarizer",
    page_icon="🎙️",
    layout="wide"
)

st.title("🎙️ AI Content Summarizer")
st.caption("Summarize podcasts, transcripts, articles, notes, and long text locally using Ollama.")

input_mode = st.radio(
    "Choose Input Type",
    ["Paste Text", "YouTube URL"]
)

summary_title = st.text_input(
    "Summary title",
    placeholder="Example: AI podcast episode summary"
)

if input_mode == "Paste Text":
    content = st.text_area(
        "Paste your content here",
        height=300
    )

else:
    youtube_url = st.text_input(
        "Paste YouTube URL"
    )

    content = ""

col1, col2 = st.columns(2)

with col1:
    tone = st.selectbox(
        "Tone",
        ["Clear", "Practical", "Witty", "Executive", "Deep"]
    )

with col2:
    output_type = st.selectbox(
        "Output Type",
        ["General Summary", "Learning Notes", "LinkedIn Post", "Action Plan"]
    )

if st.button("Summarize"):

    try:

        if input_mode == "YouTube URL":

            if not youtube_url.strip():
                st.warning("Please enter a YouTube URL.")
                st.stop()

            with st.spinner("Fetching transcript..."):
                content = get_transcript(youtube_url)

        if not content.strip():
            st.warning("Please provide content.")
            st.stop()

        with st.spinner("Summarizing locally with Ollama..."):
            result = summarize_content(content, tone, output_type)

        st.markdown(result)

        final_title = summary_title.strip() or "Untitled Summary"

        saved_path = save_summary(final_title, result)

        st.success(f"Summary saved to: {saved_path}")

        st.download_button(
            label="Download Summary as Markdown",
            data=f"# {final_title}\n\n{result}",
            file_name=f"{final_title.lower().replace(' ', '_')}.md",
            mime="text/markdown"
        )

    except Exception as e:
        st.error(f"Something went wrong: {e}")
