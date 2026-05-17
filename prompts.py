def build_summary_prompt(content: str, tone: str, output_type: str) -> str:
    return f"""
You are an AI assistant that summarizes long-form content clearly and practically.

Content to summarize:
{content}

Tone:
{tone}

Output type:
{output_type}

Create a clean markdown response with these sections:

## Quick Summary
Summarize the content in 5-7 lines.

## Key Takeaways
List the most important points.

## Actionable Ideas
List practical actions, lessons, or things worth trying.

## Interesting Insights
Mention surprising, thoughtful, or memorable ideas.

## Best One-Liner
Give one strong one-line summary of the whole content.

If the selected output type is LinkedIn Post, also include:

## LinkedIn Post Draft
Create a short, engaging LinkedIn post based on the content.

Keep the response useful, concise, and easy to skim.
"""