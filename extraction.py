import sys
import os
from fpdf import FPDF

# Add the src directory to the sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.beautifulsoup import extract_and_filter_text
from src.selenium_extracts.selenium import GoogleSearch, YoutubeSearch
from src.youtube_extracts.yt_transcripts import get_transcripts

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Search Results', 0, 1, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(5)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

    def add_chapter(self, title, body):
        self.add_page()
        self.chapter_title(title)
        self.chapter_body(body)

def create_results_pdf(google_texts, youtube_transcripts, filename='results.pdf'):
    pdf = PDF()
    pdf.set_left_margin(10)
    pdf.set_right_margin(10)

    # Add Google search results
    for i, text in enumerate(google_texts):
        pdf.add_chapter(f'Google Result {i+1}', text)

    # Add YouTube transcripts
    for video_id, transcript in youtube_transcripts.items():
        pdf.add_chapter(f'YouTube Video ID {video_id}', transcript)

    # Save the PDF to the specified file
    pdf.output(filename)

def main():
    keyword = input("Enter the keyword to search: ")
    num_results = 5  # Specify the number of results you want

    try:
        # Google Search and Extract
        google_search = GoogleSearch()
        google_links = google_search.search(keyword, num_results=num_results)
        print("Google Search Results:")
        for link in google_links:
            print(link)
        google_texts = extract_and_filter_text(google_links)

        # YouTube Search and Extract Transcripts
        youtube_search = YoutubeSearch()
        youtube_video_ids = youtube_search.search(keyword, num_results=num_results)
        print("YouTube Video IDs:")
        for video_id in youtube_video_ids:
            print(video_id)

        youtube_transcripts = get_transcripts(youtube_video_ids)

        # Create Results folder if it doesn't exist
        results_dir = 'Results'
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)

        # Save results to PDF
        output_file = os.path.join(results_dir, f"{keyword}_results.pdf")
        create_results_pdf(google_texts, youtube_transcripts, filename=output_file)
        print(f"Results saved to {output_file}")

    except Exception as e:
        print(f"An error occurred during the search process: {e}")

if __name__ == '__main__':
    main()
