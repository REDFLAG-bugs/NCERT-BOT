from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from youtube_transcript_api import TranscriptsDisabled

def get_transcripts(video_ids):
    formatter = TextFormatter()
    transcripts = {}

    for video_id in video_ids:
        try:
            # Attempt to get a Hindi transcript and translate it to English
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            transcript_hi = transcript_list.find_transcript(['hi'])
            translated_transcript = transcript_hi.translate('en')
            translated_data = translated_transcript.fetch()

            # Format the transcript
            text = formatter.format_transcript(translated_data)
            transcripts[video_id] = text

        except TranscriptsDisabled:
            print(f"Subtitles/transcripts are disabled for video ID: {video_id}")
        except Exception as e:
            print(f"Failed to retrieve transcript for video ID {video_id}: {e}")

    return transcripts

if __name__ == '__main__':
    from selenium_extracts.selenium import YoutubeSearch

    keyword = input("Enter the keyword to search for YouTube videos: ")
    num_results = 5  # Specify the number of results you want

    try:
        youtube_search = YoutubeSearch()
        youtube_video_ids = youtube_search.search(keyword, num_results=num_results)
        print("YouTube Video IDs:")
        for video_id in youtube_video_ids:
            print(video_id)

        transcripts = get_transcripts(youtube_video_ids)
        for video_id, transcript in transcripts.items():
            print(f"Transcript for video ID {video_id}:\n{transcript}\n")
    except Exception as e:
        print(f"An error occurred during the YouTube search or transcript retrieval process: {e}")
