# NCERT-BOT

## Overview

`NCERT-BOT` is a repository focused on integrating and processing educational content from the NCERT curriculum. This project aims to create a bot that can assist with accessing and querying NCERT books and related educational resources.

# Repository Structure

```
NCERT-BOT/
│
├── BOOKS/
│ └── English_xii/
│
├── RAG/
│
├── Results/
│
├── src/
│ └── extraction.py
│
├── .gitignore
├── README.md
└── requirements.txt
```

# Installation

### 1. Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/REDFLAG-bugs/NCERT-BOT.git
cd NCERT-BOT
```
## 2. Set Up a Virtual Environment (Optional)
If you want to use a virtual environment, run the following commands:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

## 3. Install Dependencies
Install the necessary dependencies:

```bash
pip install -r requirements.txt
```

## Usage
To run the extraction script:
```bash
python src/extraction.py
```
This script will process the data according to the logic defined in extraction.py.



