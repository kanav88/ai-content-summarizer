import streamlit as st
from services.summarizer import summarize_content
from services.youtube_service import get_transcript
from services.storage import save_summary, list_summaries
from services.vector_store import semantic_search

st.set_page_config(
    page_title="AI Content Summarizer",
    page_icon="🎙️",
    layout="wide"
)

st.markdown("""
<style>
.main-header {
    padding: 1.5rem;
    border-radius: 18px;
    background: linear-gradient(135deg, #6D5DFB, #00C2FF);
    color: white;
    margin-bottom: 1.5rem;
}
.feature-card {
    padding: 1rem;
    border-radius: 14px;
    background-color: #f7f7fb;
    border: 1px solid #e6e6ef;
    margin-bottom: 1rem;
}
.result-card {
    padding: 1.2rem;
    border-radius: 14px;
    background-color: #ffffff;
    border: 1px solid #e6e6ef;
}
.small-muted {
    color: #666;
    font-size: 0.9rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>🎙️ AI Content Summarizer</h1>
    <p>Summarize YouTube videos, podcasts, articles, notes, and long-form content locally using Ollama.</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    page = st.radio(
        "Navigation",
        ["Create Summary", "Summary Library"]
    )

    st.divider()

    if page == "Create Summary":
        st.header("⚙️ Summary Settings")

        input_mode = st.radio(
            "Input Type",
            ["Paste Text", "YouTube URL"]
        )

        tone = st.selectbox(
            "Tone",
            ["Clear", "Practical", "Witty", "Executive", "Deep"]
        )

        output_type = st.selectbox(
            "Output Type",
            ["General Summary", "Learning Notes", "LinkedIn Post", "Action Plan"]
        )

        st.divider()

        st.markdown("### 💡 Best For")
        st.markdown("""
        - Podcast notes
        - YouTube learning videos
        - Tech articles
        - Conference talks
        - LinkedIn post ideas
        """)

if page == "Create Summary":
    col1, col2 = st.columns([2, 1])

    with col1:
        summary_title = st.text_input(
            "Summary Title",
            placeholder="Example: AI podcast episode summary"
        )

        if input_mode == "Paste Text":
            content = st.text_area(
                "Paste your content",
                height=320,
                placeholder="Paste a podcast transcript, article, blog post, meeting notes, or long-form text..."
            )
            youtube_url = ""
        else:
            youtube_url = st.text_input(
                "YouTube URL",
                placeholder="https://www.youtube.com/watch?v=..."
            )
            content = ""

    with col2:
        st.markdown("""
        <div class="feature-card">
            <h4>✨ What this app gives you</h4>
            <p class="small-muted">
            A clean AI-generated summary with key takeaways, action items, insights, and optional LinkedIn-ready content.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-card">
            <h4>🔒 Local-first</h4>
            <p class="small-muted">
            Uses Ollama locally, so your content stays on your machine.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-card">
            <h4>📁 Auto-save</h4>
            <p class="small-muted">
            Every generated summary is saved as a Markdown file.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    generate_clicked = st.button("✨ Generate Summary", use_container_width=True)

    if generate_clicked:
        try:
            if input_mode == "YouTube URL":
                if not youtube_url.strip():
                    st.warning("Please enter a YouTube URL.")
                    st.stop()

                with st.spinner("Fetching YouTube transcript..."):
                    content = get_transcript(youtube_url)

                st.success("Transcript fetched successfully.")

            if not content.strip():
                st.warning("Please provide content to summarize.")
                st.stop()

            word_count = len(content.split())
            st.info(f"Processing approximately {word_count:,} words.")

            with st.spinner("Summarizing locally with Ollama..."):
                result = summarize_content(content, tone, output_type)

            final_title = summary_title.strip() or "Untitled Summary"
            saved_path = save_summary(final_title, result)

            st.success(f"Summary saved to: {saved_path}")

            st.markdown("## 📌 Generated Summary")
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown(result)
            st.markdown('</div>', unsafe_allow_html=True)

            st.download_button(
                label="⬇️ Download Summary as Markdown",
                data=f"# {final_title}\n\n{result}",
                file_name=f"{final_title.lower().replace(' ', '_')}.md",
                mime="text/markdown",
                use_container_width=True
            )

        except Exception as e:
            st.error(f"Something went wrong: {e}")

else:
    st.markdown("## 📚 Summary Library")
    st.caption("Browse your locally saved AI summaries.")

    summaries = list_summaries()

    if not summaries:
        st.info("No summaries saved yet.")
    else:
        search_mode = st.radio(
            "Search Type",
            ["Keyword Search", "Semantic Search"]
        )

        search_query = st.text_input(
            "Search summaries",
            placeholder="Search by title or content..."
        )

        filtered_summaries = summaries

        if search_query.strip():
            if search_mode == "Keyword Search":
                query = search_query.lower()
                filtered_summaries = [
                    summary for summary in summaries
                    if query in summary["title"].lower()
                    or query in summary["content"].lower()
                ]
            else:
                results = semantic_search(search_query)
                matched_ids = results["ids"][0]

                filtered_summaries = [
                    summary for summary in summaries
                    if summary["filename"] in matched_ids
                ]

        st.write(f"Showing {len(filtered_summaries)} summaries")

        for summary in filtered_summaries:
            with st.expander(f"📄 {summary['title']}"):
                st.caption(summary["filename"])
                st.markdown(summary["content"])

                st.download_button(
                    label="⬇️ Download",
                    data=summary["content"],
                    file_name=summary["filename"],
                    mime="text/markdown",
                    key=summary["filename"]
                )
