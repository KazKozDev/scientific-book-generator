import requests
import json
import os
from typing import List, Dict, Tuple
import time
import argparse
from datetime import datetime
from tqdm import tqdm

class BookGenerator:
    def __init__(self, api_url: str = "http://localhost:11434", model: str = "gemma2:27b"):
        """
        Initialization of the book generator
        
        Args:
            api_url: API URL for Ollama
            model: LLM model for generation
        """
        self.api_url = api_url
        self.generate_endpoint = f"{api_url}/api/generate"
        self.model = model
        
    def generate_outline(self, topic: str, num_chapters: int) -> List[str]:
        """
        Generate a detailed outline for a book on the given topic.
        
        Args:
            topic: Main topic of the book
            num_chapters: Number of chapters to generate
            
        Returns:
            List[str]: List of chapter titles
        """
        prompt = f"""
        Create a detailed outline for a book on the topic "{topic}".
        The outline should contain exactly {num_chapters} chapters.
        Each chapter should have a logical sequence and connection to the other chapters.
        Each chapter title should be informative and appealing to the reader.
        Return only the chapter titles, one per line.
        """
        
        response = self._make_request(prompt)
        if response:
            # Split the response into lines and remove empty lines
            chapters = [line.strip() for line in response.split('\n') if line.strip()]
            
            # Check if we got the required number of chapters
            if len(chapters) > num_chapters:
                chapters = chapters[:num_chapters]
            elif len(chapters) < num_chapters:
                # If there are fewer chapters, generate additional ones
                additional_needed = num_chapters - len(chapters)
                additional_prompt = f"""
                Create {additional_needed} more chapters for a book on the topic "{topic}".
                These chapters should complement the existing chapters:
                {', '.join(chapters)}
                Each new chapter should be on a separate line.
                """
                additional_response = self._make_request(additional_prompt)
                if additional_response:
                    additional_chapters = [line.strip() for line in additional_response.split('\n') if line.strip()]
                    chapters.extend(additional_chapters[:additional_needed])
            
            return chapters
        return []

    def generate_chapter_structure(self, chapter_title: str, previous_summary: str = "") -> List[str]:
        """
        Generate the structure of a chapter with subsections.
        
        Args:
            chapter_title: Title of the chapter
            previous_summary: Summary of the previous chapter
            
        Returns:
            List[str]: List of chapter sections
        """
        context = f"Summary of the previous chapter: {previous_summary}\n" if previous_summary else ""
        
        prompt = f"""
        {context}
        Create a detailed structure for the chapter titled: "{chapter_title}"
        
        The chapter should have the following structure:
        1. Chapter introduction
        2. 3-5 logically connected subsections with informative titles
        3. Chapter conclusion
        
        Return only the section titles, one per line, including "Introduction" and "Conclusion".
        """
        
        response = self._make_request(prompt)
        if response:
            sections = [line.strip() for line in response.split('\n') if line.strip()]
            return sections
        return ["Introduction", "Main Content", "Conclusion"]  # Return a simple structure in case of an error

    def generate_chapter_chunk(self, chapter_title: str, section_title: str, previous_content: str = "") -> str:
        """
        Generate a chunk of a chapter.
        
        Args:
            chapter_title: Title of the chapter
            section_title: Title of the section
            previous_content: Previously generated content for context
            
        Returns:
            str: Text for the chapter chunk
        """
        context = f"Previous content: {previous_content[-500:]} (continuation)" if previous_content else ""
        
        prompt = f"""
        {context}
        Write the section "{section_title}" for the book chapter "{chapter_title}"
        
        Requirements:
        1. Length - approximately 500-700 words
        2. Academic writing style with professional terminology
        3. Substantial arguments supported by facts
        4. Logical structure with smooth transitions between paragraphs
        5. If this is the introduction, provide an overview of the chapter
        6. If this is the conclusion, summarize and link to the next chapter
        
        Begin writing the section:
        """
        
        return self._make_request(prompt)

    def summarize_chapter(self, chapter_content: str) -> str:
        """
        Create a brief summary of a chapter.
        
        Args:
            chapter_content: Text of the chapter
            
        Returns:
            str: Chapter summary
        """
        prompt = f"""
        Create a summary (150-200 words) of the following text:
        
        {chapter_content[:3000]}...
        
        The summary should:
        1. Cover the key ideas and arguments
        2. Highlight the main conclusions
        3. Be written in the present tense
        4. Serve as a good context for the next chapter
        """
        
        return self._make_request(prompt)

    def generate_metadata(self, topic: str, chapters: List[str]) -> Dict:
        """
        Generate book metadata (title, author, annotation).
        
        Args:
            topic: Topic of the book
            chapters: List of chapter titles
            
        Returns:
            Dict: Book metadata
        """
        prompt = f"""
        Create metadata for a book on the topic "{topic}" with the following chapters:
        {', '.join(chapters)}
        
        The metadata should include:
        1. A professional book title (without quotes)
        2. A fictional first and last name for the author
        3. A brief book annotation (150-200 words)
        
        Response format:
        Title: [book title]
        Author: [first and last name]
        Annotation: [annotation text]
        """
        
        response = self._make_request(prompt)
        metadata = {"title": f"Book on {topic}", "author": "Author Not Specified", "annotation": ""}
        
        if response:
            lines = response.strip().split('\n')
            for line in lines:
                if line.startswith("Title:"):
                    metadata["title"] = line.replace("Title:", "").strip()
                elif line.startswith("Author:"):
                    metadata["author"] = line.replace("Author:", "").strip()
                elif line.startswith("Annotation:"):
                    metadata["annotation"] = line.replace("Annotation:", "").strip()
                else:
                    # If the line does not start with a known key, append it to the annotation
                    if metadata["annotation"]:
                        metadata["annotation"] += " " + line.strip()
        
        return metadata

    def generate_introduction(self, topic: str, chapters: List[str], metadata: Dict) -> str:
        """
        Generate an introduction for the book.
        
        Args:
            topic: Topic of the book
            chapters: List of chapter titles
            metadata: Book metadata
            
        Returns:
            str: Introduction text
        """
        prompt = f"""
        Write a professional introduction to the book "{metadata['title']}" on the topic "{topic}".
        
        Book structure:
        {', '.join(chapters)}
        
        The introduction should:
        1. Capture the reader's attention
        2. Explain the relevance of the topic
        3. Briefly describe the structure of the book
        4. Specify the target audience
        5. Be approximately 800-1000 words in length
        """
        
        return self._make_request(prompt)

    def generate_conclusion(self, topic: str, chapters: List[str], metadata: Dict) -> str:
        """
        Generate a conclusion for the book.
        
        Args:
            topic: Topic of the book
            chapters: List of chapter titles
            metadata: Book metadata
            
        Returns:
            str: Conclusion text
        """
        prompt = f"""
        Write a professional conclusion to the book "{metadata['title']}" on the topic "{topic}".
        
        Book structure:
        {', '.join(chapters)}
        
        The conclusion should:
        1. Summarize all the material
        2. Consolidate the key ideas from all chapters
        3. Propose directions for further study
        4. End with a strong concluding statement
        5. Be approximately 800-1000 words in length
        """
        
        return self._make_request(prompt)

    def generate_bibliography(self, topic: str) -> List[str]:
        """
        Generate a bibliography for the book.
        
        Args:
            topic: Topic of the book
            
        Returns:
            List[str]: List of bibliographic entries
        """
        prompt = f"""
        Create a list of 10-15 professional bibliographic sources for a book on the topic "{topic}".
        
        The sources should:
        1. Be real, current, and relevant to the topic
        2. Include books, scholarly articles, and studies
        3. Be formatted in academic style
        4. Include author names, publication year, title, and publisher
        
        Return only the bibliographic entries, one per line.
        """
        
        response = self._make_request(prompt)
        if response:
            return [line.strip() for line in response.split('\n') if line.strip()]
        return []

    def _make_request(self, prompt: str, max_retries: int = 3, retry_delay: int = 5) -> str:
        """
        Send a request to the Ollama API with a retry mechanism.
        
        Args:
            prompt: Prompt text
            max_retries: Maximum number of attempts
            retry_delay: Delay between attempts in seconds
            
        Returns:
            str: API response
        """
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.75,
                "top_p": 0.9,
                "num_ctx": 8000,
                "seed": int(time.time())  # Use current time for response variety
            }
        }
        
        for attempt in range(max_retries):
            try:
                response = requests.post(self.generate_endpoint, json=payload, timeout=120)
                if response.status_code == 200:
                    return response.json()['response']
                else:
                    print(f"API error: {response.status_code}, attempt {attempt+1}/{max_retries}")
                    if attempt < max_retries - 1:
                        time.sleep(retry_delay)
            except Exception as e:
                print(f"Request error: {e}, attempt {attempt+1}/{max_retries}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
        
        print("All request attempts have been exhausted. Returning an empty result.")
        return ""

    def generate_book(self, topic: str, num_chapters: int, output_dir: str = None):
        """
        Generate a complete book.
        
        Args:
            topic: Topic of the book
            num_chapters: Number of chapters
            output_dir: Directory to save files (if None, created automatically)
        """
        # Create a directory with a timestamp if not specified
        if output_dir is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_dir = f"book_{timestamp}_{topic.replace(' ', '_')[:30]}"
        
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"Generating book on the topic: \"{topic}\" with {num_chapters} chapters")
        print(f"Results will be saved in: {output_dir}")
        
        # Generate the book outline
        print("\nCreating book outline...")
        chapters = self.generate_outline(topic, num_chapters)
        
        # Generate book metadata
        print("Creating book metadata...")
        metadata = self.generate_metadata(topic, chapters)
        
        # Save metadata
        with open(f"{output_dir}/metadata.json", "w", encoding="utf-8") as f:
            json.dump(metadata, f, ensure_ascii=False, indent=4)
        
        # Write the outline to a file
        with open(f"{output_dir}/outline.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(chapters))
        
        # Generate the introduction for the book
        print("Generating introduction...")
        introduction = self.generate_introduction(topic, chapters, metadata)
        with open(f"{output_dir}/introduction.md", "w", encoding="utf-8") as f:
            f.write(f"# Introduction\n\n{introduction}")
        
        # Create README.md with main book information
        with open(f"{output_dir}/README.md", "w", encoding="utf-8") as f:
            f.write(f"# {metadata['title']}\n\n")
            f.write(f"**Author:** {metadata['author']}\n\n")
            f.write(f"**Annotation:**\n\n{metadata['annotation']}\n\n")
            f.write("## Contents\n\n")
            f.write("- [Introduction](introduction.md)\n")
            for i, chapter in enumerate(chapters, 1):
                f.write(f"- [Chapter {i}: {chapter}](chapter_{i:02d}/README.md)\n")
            f.write("- [Conclusion](conclusion.md)\n")
            f.write("- [Bibliography](bibliography.md)\n")
        
        # Generate chapters
        previous_summary = ""
        for i, chapter in enumerate(chapters, 1):
            chapter_dir = f"{output_dir}/chapter_{i:02d}"
            os.makedirs(chapter_dir, exist_ok=True)
            
            print(f"\nGenerating chapter {i}/{num_chapters}: \"{chapter}\"")
            
            # Generate chapter structure
            sections = self.generate_chapter_structure(chapter, previous_summary)
            
            # Create README.md for the chapter
            with open(f"{chapter_dir}/README.md", "w", encoding="utf-8") as f:
                f.write(f"# Chapter {i}: {chapter}\n\n")
                f.write("## Chapter Contents\n\n")
                for j, section in enumerate(sections, 1):
                    f.write(f"{j}. [{section}](section_{j:02d}.md)\n")
            
            # Generate each section of the chapter
            full_chapter_content = ""
            for j, section in enumerate(sections, 1):
                print(f"  Generating section {j}/{len(sections)}: \"{section}\"")
                
                # Generate section content
                previous_content = full_chapter_content[-1000:] if full_chapter_content else ""
                section_content = self.generate_chapter_chunk(chapter, section, previous_content)
                full_chapter_content += section_content
                
                # Save the section
                with open(f"{chapter_dir}/section_{j:02d}.md", "w", encoding="utf-8") as f:
                    f.write(f"## {section}\n\n")
                    f.write(section_content)
                
                # Small pause between requests
                time.sleep(1)
            
            # Create a summary for the next chapter
            previous_summary = self.summarize_chapter(full_chapter_content)
            
            # Save the full text of the chapter
            with open(f"{chapter_dir}/full_chapter.md", "w", encoding="utf-8") as f:
                f.write(f"# Chapter {i}: {chapter}\n\n")
                f.write(full_chapter_content)
        
        # Generate the conclusion for the book
        print("\nGenerating conclusion...")
        conclusion = self.generate_conclusion(topic, chapters, metadata)
        with open(f"{output_dir}/conclusion.md", "w", encoding="utf-8") as f:
            f.write(f"# Conclusion\n\n{conclusion}")
        
        # Generate bibliography
        print("Creating bibliography...")
        bibliography = self.generate_bibliography(topic)
        with open(f"{output_dir}/bibliography.md", "w", encoding="utf-8") as f:
            f.write("# Bibliography\n\n")
            for i, ref in enumerate(bibliography, 1):
                f.write(f"{i}. {ref}\n")
        
        # Additionally, create a file for the complete book text
        print("Combining all materials into a single file...")
        with open(f"{output_dir}/full_book.md", "w", encoding="utf-8") as f:
            # Title page
            f.write(f"# {metadata['title']}\n\n")
            f.write(f"**Author:** {metadata['author']}\n\n")
            f.write(f"**Annotation:**\n\n{metadata['annotation']}\n\n")
            
            # Add introduction
            f.write("# Introduction\n\n")
            f.write(introduction)
            f.write("\n\n")
            
            # Add chapters
            for i, chapter in enumerate(chapters, 1):
                chapter_content = ""
                chapter_dir = f"{output_dir}/chapter_{i:02d}"
                
                with open(f"{chapter_dir}/full_chapter.md", "r", encoding="utf-8") as chapter_file:
                    chapter_content = chapter_file.read()
                
                f.write(f"{chapter_content}\n\n")
            
            # Add conclusion
            f.write("# Conclusion\n\n")
            f.write(conclusion)
            f.write("\n\n")
            
            # Add bibliography
            f.write("# Bibliography\n\n")
            for i, ref in enumerate(bibliography, 1):
                f.write(f"{i}. {ref}\n")
        
        print(f"\nBook successfully generated and saved in the directory: {output_dir}")
        print(f"Main book file: {output_dir}/full_book.md")
        print(f"Number of chapters: {num_chapters}")
        print(f"Book structure available in: {output_dir}/README.md")

def main():
    parser = argparse.ArgumentParser(description="Book generator using LLM")
    parser.add_argument("--topic", type=str, help="Book topic")
    parser.add_argument("--chapters", type=int, default=5, help="Number of chapters (default: 5)")
    parser.add_argument("--output", type=str, help="Directory for saving results")
    parser.add_argument("--model", type=str, default="gemma2:27b", help="LLM model (default: gemma2:27b)")
    parser.add_argument("--api", type=str, default="http://localhost:11434", help="Ollama API URL")
    
    args = parser.parse_args()
    
    # Create an instance of the generator
    generator = BookGenerator(api_url=args.api, model=args.model)
    
    # Get parameters from the user if not provided in the arguments
    topic = args.topic
    if not topic:
        topic = input("Enter the topic for the book: ")
    
    num_chapters = args.chapters
    if args.chapters == 5 and not args.topic:  # If the user did not specify the number of chapters in the arguments
        try:
            num_chapters = int(input(f"Enter the number of chapters (default: {num_chapters}): ") or num_chapters)
        except ValueError:
            print(f"Invalid value. The default value will be used: {num_chapters}")
    
    # Generate the book
    generator.generate_book(topic, num_chapters, args.output)

if __name__ == "__main__":
    main()
