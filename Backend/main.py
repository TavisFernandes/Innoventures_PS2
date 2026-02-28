import requests
import os
from io import BytesIO
import PyPDF2
import re

class PDFQASystem:
    def __init__(self):
        """
        Initialize PDF QA System with basic text search
        """
        self.documents = []
        self.full_text = ""
    
    def download_and_process_pdf(self, pdf_url):
        """
        Download PDF from URL and process it
        """
        try:
            # Download PDF
            response = requests.get(pdf_url, timeout=30)
            response.raise_for_status()
            
            # Save temporarily
            temp_pdf_path = "temp_document.pdf"
            with open(temp_pdf_path, 'wb') as f:
                f.write(response.content)
            
            # Load and process PDF using PyPDF2 directly
            pdf_file = open(temp_pdf_path, 'rb')
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            # Extract text from all pages
            documents = []
            full_text = ""
            for page_num, page in enumerate(pdf_reader.pages):
                text = page.extract_text()
                if text.strip():
                    documents.append({"page": page_num + 1, "content": text})
                    full_text += text + "\n"
            
            pdf_file.close()
            
            self.documents = documents
            self.full_text = full_text
            
            # Clean up temporary file
            os.remove(temp_pdf_path)
            
            print(f"✅ PDF processed successfully. {len(documents)} pages extracted.")
            return True
            
        except Exception as e:
            print(f"❌ Error processing PDF: {e}")
            return False
    
    def answer_question(self, question):
        """
        Answer question based on the processed PDF using improved keyword search
        """
        if not self.documents:
            return "❌ No PDF has been processed yet. Please load a PDF first."
        
        try:
            # Extract keywords from question, prioritize longer phrases
            question_lower = question.lower()
            
            # Look for exact phrase matches first
            relevant_snippets = []
            
            for doc in self.documents:
                content = doc['content'].lower()
                score = 0
                
                # Exact phrase matching (highest score)
                if question_lower in content:
                    score += 50
                
                # Word-by-word matching with context
                question_words = re.findall(r'\b\w+\b', question_lower)
                question_words = [word for word in question_words if len(word) > 2]
                
                # Count consecutive word matches (phrase matching)
                for i in range(len(question_words) - 1):
                    phrase = ' '.join(question_words[i:i+2])
                    if phrase in content:
                        score += 10
                
                # Individual word matches
                for word in question_words:
                    word_count = content.count(word)
                    if word_count > 0:
                        score += word_count
                
                # Bonus for definition-like content
                if any(word in content for word in ['definition', 'refers to', 'means', 'is defined as']):
                    if score > 0:
                        score += 5
                
                if score > 0:
                    # Find the most relevant snippet around the matches
                    best_snippet = self._find_best_snippet(doc['content'], question_words)
                    relevant_snippets.append({
                        'page': doc['page'],
                        'content': best_snippet,
                        'score': score
                    })
            
            # Sort by relevance score
            relevant_snippets.sort(key=lambda x: x['score'], reverse=True)
            
            if not relevant_snippets:
                return f"❌ No information found about: {question}"
            
            # Return top relevant snippet for better focus
            best_match = relevant_snippets[0]
            result = f"📝 Answer for '{question}':\n\n"
            result += f"📄 Page {best_match['page']} (Relevance: {best_match['score']}):\n"
            result += f"{best_match['content']}\n\n"
            
            # Show other relevant pages if available
            if len(relevant_snippets) > 1:
                result += "📚 Additional relevant pages:\n"
                for snippet in relevant_snippets[1:3]:
                    result += f"• Page {snippet['page']} (Relevance: {snippet['score']})\n"
            
            return result
            
        except Exception as e:
            return f"❌ Error answering question: {e}"
    
    def _find_best_snippet(self, content, question_words, max_length=400):
        """
        Find the most relevant snippet around keyword matches
        """
        content_lower = content.lower()
        best_start = 0
        best_score = 0
        
        for word in question_words:
            word_pos = content_lower.find(word)
            if word_pos != -1:
                # Score based on position and surrounding context
                score = 0
                start = max(0, word_pos - 100)
                end = min(len(content), word_pos + 300)
                snippet = content[start:end]
                
                # Count total keyword matches in this snippet
                for w in question_words:
                    score += snippet.lower().count(w) * 2
                
                if score > best_score:
                    best_score = score
                    best_start = start
        
        # Return the best snippet
        end = min(len(content), best_start + max_length)
        return content[best_start:end].strip()
    
    def interactive_qa(self):
        """
        Interactive Q&A session
        """
        print("\n🤖 PDF Q&A System Ready!")
        print("Type 'quit' to exit, 'new' to load a new PDF\n")
        
        while True:
            question = input("❓ Ask your question: ").strip()
            
            if question.lower() == 'quit':
                print("👋 Goodbye!")
                break
            elif question.lower() == 'new':
                pdf_url = input("📄 Enter PDF URL: ").strip()
                if pdf_url:
                    self.download_and_process_pdf(pdf_url)
                continue
            elif not question:
                continue
            
            answer = self.answer_question(question)
            print(f"\n{answer}\n")

def main():
    """
    Main function to run the PDF Q&A system
    """
    print("🚀 Initializing PDF Q&A System...")
    
    # Initialize the QA system
    qa_system = PDFQASystem()
    
    # Get PDF URL from user
    pdf_url = input("📄 Enter PDF URL: ").strip()
    
    if not pdf_url:
        print("❌ No PDF URL provided. Exiting.")
        return
    
    # Process the PDF
    if qa_system.download_and_process_pdf(pdf_url):
        # Start interactive Q&A session
        qa_system.interactive_qa()
    else:
        print("❌ Failed to process PDF. Please check the URL and try again.")

if __name__ == "__main__":
    main()