from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from youtube_transcript_api._errors import TranscriptsDisabled, VideoUnavailable

def fetch_youtube_transcripts(video_ids):
    formatter = TextFormatter()
    transcripts = {}

    for video_id in video_ids:
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            transcript_hi = transcript_list.find_transcript(['hi'])
            translated_transcript = transcript_hi.translate('en')
            translated_data = translated_transcript.fetch()
            text = formatter.format_transcript(translated_data)
            transcripts[video_id] = text
        except TranscriptsDisabled:
            print(f"Subtitles/transcripts are disabled for video ID: {video_id}")
        except VideoUnavailable:
            print(f"Video unavailable for video ID: {video_id}")
        except Exception as e:
            print(f"Failed to retrieve transcript for video ID {video_id}: {e}")

    return transcripts
