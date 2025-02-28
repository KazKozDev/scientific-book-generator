# ScientificGenerator

<div align="center">

<img src="images/banner.jpg" alt="ScientificGenerator" width="800"/>

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Ollama](https://img.shields.io/badge/LLM-Ollama-orange.svg)](https://ollama.ai)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/KazKozDev/scientific-book-generator/blob/master/LICENSE)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/KazKozDev/scientific-book-generator/graphs/commit-activity)
[![GitHub issues](https://img.shields.io/github/issues/KazKozDev/scientific-book-generator)](https://github.com/KazKozDev/scientific-book-generator/issues)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://makeapullrequest.com)

</div>

# Scientific Book Generator

A powerful tool that generates complete scientific books on any topic using Large Language Models (LLMs) via Ollama.

## Features

- Generate complete books with professional structure and academic writing style
- Create detailed chapter outlines with logical subsections (6-9 per chapter)
- Generate book metadata (title, author, annotation)
- Produce academic-quality content with consistent narrative flow
- Generate comprehensive introductions, conclusions, and bibliographies
- Generate chapter summaries that ensure logical flow between sections
- Save output in organized Markdown format, ready for publishing
- Automatic retry mechanism for API request failures

## How It Works

1. The generator uses Ollama's API to access large language models
2. First, it creates a logical book structure based on your topic
3. It then generates each chapter section-by-section with context awareness
4. Each section maintains continuity with previous content
5. The system creates navigable file structure with full markdown formatting
6. All content is combined into both individual files and a complete book file

## Requirements

- Python 3.7+
- [Ollama](https://ollama.ai/) running locally or accessible via API
- An LLM available through Ollama (default: gemma2:27b)
- Python packages: requests, tqdm

## Installation

Clone the repository:

```bash
git clone https://github.com/KazKozDev/scientific-book-generator.git
cd scientific-book-generator
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the script with default parameters:

```bash
python ScientificGenerator.py
```

The script will prompt you for the topic and number of chapters.

Or specify parameters directly:

```bash
python ScientificGenerator.py --topic "Quantum Computing" --chapters 5
```

### Command line arguments

- `--topic`: Book topic (if not specified, will be prompted)
- `--chapters`: Number of chapters (default: 5)
- `--output`: Directory for saving results (default: auto-generated with timestamp)
- `--model`: LLM model to use (default: gemma2:27b)
- `--api`: Ollama API URL (default: http://localhost:11434)

## Output Structure

The generator creates a directory with the following structure:

```
book_20250228_123456_Topic_Name/
├── README.md (Book overview)
├── metadata.json (Title, author, annotation)
├── outline.txt (Chapter titles)
├── introduction.md
├── conclusion.md
├── bibliography.md
├── full_book.md (Complete book in one file)
└── chapter_01/
    ├── README.md (Chapter overview)
    ├── full_chapter.md (Complete chapter)
    ├── section_01.md (Introduction)
    ├── section_02.md (Section 1)
    ├── section_03.md (Section 2)
    └── ... (Additional sections and conclusion)
└── chapter_02/
    └── ...
```

## Content Generation Features

- **Academic Writing Style**: Generates professional-level academic content
- **Coherent Narrative**: Each chapter maintains continuity through summarization
- **Bibliographic Sources**: Creates relevant, professionally formatted references
- **Metadata Generation**: Creates appropriate titles, author names and annotations
- **Section Structure**: Each chapter includes introduction, logical subsections, and conclusion
- **Complete Book Structure**: Includes proper front matter, chapters, and back matter

## Advanced Usage

For advanced usage or integration with other systems, you can import the `BookGenerator` class:

```python
from ScientificGenerator import BookGenerator

generator = BookGenerator(api_url="http://localhost:11434", model="gemma2:27b")
generator.generate_book("Quantum Physics", 7)
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
<div align="center">
Made with ❤️ by KazKozDev

[GitHub](https://github.com/KazKozDev)
</div>