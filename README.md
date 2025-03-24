# Youtube Chat and Comment Analysis
A Python&AI based analysis tool that compares japanese **YouTube live chats** and **comments** to uncover key differences in opinion, sentiment, and word usage.

---

## Features
- Collects **YouTube live chat** and **comment** data  
- **Natural Language Processing (NLP)** for word level visualisation (word cloud freqency graph) 
- Summarizes differences between live chat and comments using **AI analysis**  

---
## Project Structure
```bash
project_root/ 
│── src/ 
│   ├── data_collection/    # Scripts for fetching YouTube data
│   ├── nlp_processing/     # NLP for visualisation
│   ├── ai_analysis/        # AI-based comparison analysis
│── data/                   # Data extracted from youtube
│── results/                # Generated visualizations
│── requirements.txt        # List of Python dependencies
│── setup.sh                # System-level dependency installer
│── README.md               # Installation and usage guide
│── main.py                 # Entry point to run the analysis
```

---

## Installation Instructions

### 1. Install System Dependencies (Linux/Ubuntu)
Run the following script to install necessary system-level dependencies:
```bash
bash setup.sh
```

### 2.Install Python Dependencies
After system dependencies are installed, install the required Python packages:
```bash
pip install -r requirements.txt
```


## Usage Guide
To run the full analysis pipeline, use:
```bash
python main.py 
```

You will be asked to type in your
1. Youtube API
2. OpenAI API
3. Youtube video id

After running, the comparison results will be stored as final_report.md.


## Sample Output
The sample report can be found in [Here](final_report.md)



