import fitz
import os
import re
from bs4 import BeautifulSoup

def get_text_from_papers(filename: str, get_html: bool = False):
    all_page_data = {}
    try:
        doc = fitz.open(filename)
        for i, page in enumerate(doc):
            page_text = page.get_text("text")
            all_page_data[i] = {'text': page_text}
            if get_html:
                soup = BeautifulSoup(page_text, 'html.parser')
                all_page_data[i]['html'] = soup.prettify()
    except Exception as e:
        print(f"Error extracting text from {filename}: {e}")
    return all_page_data

def extract_with_regex(text: str, heading: str):
    pattern = rf"{heading}\n(?:\d+\.\s+)?(.*?)(?=^|\n\b{heading}\b|\n\b[A-Z][^A-Z\d\s]*\b)"
    match = re.search(pattern, text, flags=re.DOTALL | re.MULTILINE)
    return match.group(1).strip() if match else ""

def get_text_by_number(filename: str):
    all_text = ""
    section_pattern = r"^\d+\.\s+(.*?)(?=\n|\Z)"
    try:
        doc = fitz.open(filename)
        for page in doc:
            page_text = page.get_text("text")
            matches = re.findall(section_pattern, page_text, flags=re.MULTILINE)
            all_text += "\n\n".join(matches) + "\n\n"
    except Exception as e:
        print(f"Error extracting content from {filename}: {e}")
    return all_text.strip()

def get_all_text_by_page(filename: str, page_numbers: list[int]):
    all_text = ""
    try:
        doc = fitz.open(filename)
        for page_number in page_numbers:
            page_text = doc[page_number - 1].get_text("text")
            all_text += page_text + "\n\n"
    except Exception as e:
        print(f"Error extracting content from {filename}: {e}")
    return all_text.strip()

def get_ordered_content_by_page(filename: str, page_numbers: list[int]):
    all_text = ""
    chapter_pattern = r"^\d+\.\s+(.+?)\s*$"
    chapters = []
    try:
        doc = fitz.open(filename)
        for page_number in page_numbers:
            page_text = doc[page_number - 1].get_text("text")
            lines = page_text.splitlines()
            for line in lines:
                chapter_match = re.match(chapter_pattern, line)
                if chapter_match:
                    chapter_name = chapter_match.group(1).strip()
                    chapters.append((chapter_name, page_number))
                else:
                    all_text += line + "\n"
        chapters.sort(key=lambda x: x[1])
        formatted_text = ""
        for chapter_number, (chapter_name, _) in enumerate(chapters, 1):
            formatted_text += f"{chapter_number}. {chapter_name}\n"
        formatted_text += all_text.strip()
        return formatted_text
    except Exception as e:
        print(f"Error extracting content from {filename}: {e}")
        return ""

def save_extracted_content(filename: str, content: str, folder_name: str = 'Results'):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    file_path = os.path.join(folder_name, filename)
    try:
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"Content saved to {file_path}")
    except Exception as e:
        print(f"Error saving content to {file_path}: {e}")

# Example Usage
if __name__ == '__main__':
    english_folder_dir = 'BOOKS/eng_ncert'  # Adjust this path as necessary

    target_folder = "hornbill"
    target_filename = "kehb103.pdf"

    file_path = os.path.join(english_folder_dir, target_folder, target_filename)
    
    extracted_text = get_text_from_papers(file_path)
    if extracted_text:
        understanding_text = extract_with_regex(extracted_text, "Understanding the text")
        if understanding_text:
            save_extracted_content(f"{target_filename}_understanding.txt", understanding_text)
        else:
            print(f"Content under 'Understanding the text' not found in {target_filename}.")
