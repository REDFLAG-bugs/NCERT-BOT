import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from src.beautifulsoup import BeautifulSoupScraper
from src.selenium_extracts.selenium import GoogleSearch, YoutubeSearch
from src.youtube_extracts.yt_transcripts import fetch_youtube_transcripts

def generate_pdf(transcripts, filename='transcripts.pdf'):
    # Create a PDF document
    doc = SimpleDocTemplate(filename, pagesize=letter)
    elements = []

    # Styles for the PDF
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    heading_style = styles['Heading2']
    body_style = styles['BodyText']

    # Add title
    elements.append(Paragraph("Search Results", title_style))
    elements.append(Spacer(1, 12))

    # Add transcript content
    for title, body in transcripts.items():
        elements.append(Paragraph(title, heading_style))
        elements.append(Spacer(1, 6))
        elements.append(Paragraph(body, body_style))
        elements.append(Spacer(1, 12))

    # Build PDF
    doc.build(elements)

def main():
    keyword = input("Enter the keyword to search: ")
    num_results = 5

    transcripts = {}

    # Fetch Google search results and extract text
    try:
        google_links = GoogleSearch.search(keyword, num_results=num_results)
        scraper = BeautifulSoupScraper()
        articles = scraper.extract_and_filter_text(google_links)
        transcripts.update({f"Article {i+1}": article for i, article in enumerate(articles)})
    except Exception as e:
        print(f"An error occurred while fetching or processing Google search results: {e}")

    # Fetch YouTube captions
    try:
        youtube_video_ids = YoutubeSearch.search(keyword, num_results=num_results)
        youtube_transcripts = fetch_youtube_transcripts(youtube_video_ids)
        transcripts.update({f"YouTube Video ID: {video_id}": transcript for video_id, transcript in youtube_transcripts.items()})
    except Exception as e:
        print(f"An error occurred while fetching YouTube captions: {e}")

    # Generate the PDF with the transcripts
    if transcripts:
        if not os.path.exists('Results'):
            os.makedirs('Results')
        output_file = os.path.join('Results', f"{keyword}_results.pdf")
        generate_pdf(transcripts, filename=output_file)
        print(f"PDF has been generated successfully and saved to {output_file}")
    else:
        print("No transcripts were found. No PDF generated.")

if __name__ == "__main__":
    main()

