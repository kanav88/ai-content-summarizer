from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs


def extract_video_id(url: str):
    parsed_url = urlparse(url)

    if parsed_url.hostname == "youtu.be":
        return parsed_url.path[1:]

    if parsed_url.hostname in ("www.youtube.com", "youtube.com"):
        return parse_qs(parsed_url.query).get("v", [None])[0]

    return None


def get_transcript(url: str):

    video_id = extract_video_id(url)

    if not video_id:
        raise ValueError("Invalid YouTube URL")

    ytt_api = YouTubeTranscriptApi()

    fetched_transcript = ytt_api.fetch(video_id)

    full_text = " ".join([snippet.text for snippet in fetched_transcript])

    return full_text