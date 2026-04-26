import os
from dotenv import load_dotenv
from education_agent.agents import quiz_generator, flashcard_generator
from education_agent.utils import image_gen
from langchain_groq import ChatGroq
from concurrent.futures import ThreadPoolExecutor # For Parallel Processing
# Assuming we will use a simple synchronous orchestration for now
from .researcher import get_researcher_chain
from .writer import get_writer_chain

load_dotenv()

class Orchestrator:
    def __init__(self):
        # Ensure API Key is set
        if not os.getenv("GROQ_API_KEY"):
            raise ValueError("GROQ_API_KEY not found in environment variables.")
            
        self.llm = ChatGroq(model="llama-3.3-70b-versatile")
        self.researcher_chain = get_researcher_chain(self.llm)
        self.writer_chain = get_writer_chain(self.llm)

    def run(self, topic: str):
        print(f"--- [ORCHESTRATOR] Starting Process for Topic: {topic} ---")
        
        # Step 1: Research Phase
        print("--- [ORCHESTRATOR] Triggering Researcher Agent (with DuckDuckGo Search) ---")
        # The researcher chain now handles search internally based on the topic
        research_output = self.researcher_chain.invoke({"topic": topic})
        print("--- [RESEARCHER] Output Generated ---")
        # print(research_output) # Debugging

        # 3. Write Content
        print(f"--- [ORCHESTRATOR] Writing Content ---")
        article = self.writer_chain.invoke({"research_data": research_output})
        
        # 4. Multimedia (Videos) - REMOVED
        print(f"--- [ORCHESTRATOR] Multimedia (Videos) Removed ---")
        videos = []
        
        # 5. Generate Flashcards
        print(f"--- [ORCHESTRATOR] Generating Flashcards ---")
        try:
            flashcard_chain = flashcard_generator.get_flashcard_chain(self.llm)
            flashcards_data = flashcard_chain.invoke({"topic": topic, "content": article})
            print(f"--- [DEBUG] Flashcards JSON: {flashcards_data}")
            
            # Generate Images for Flashcards in PARALLEL
            if flashcards_data and 'flashcards' in flashcards_data:
                print(f"--- [ORCHESTRATOR] Generating {len(flashcards_data['flashcards'])} visuals in parallel ---")
                
                def fetch_image(fc):
                    print(f"--- [ORCHESTRATOR] Generating Visual for: {fc['concept']} ---")
                    fc['image_b64'] = image_gen.generate_image(fc['image_prompt'])
                
                # Use ThreadPoolExecutor to run image generation simultaneously
                with ThreadPoolExecutor(max_workers=5) as executor:
                    executor.map(fetch_image, flashcards_data['flashcards'])
        except Exception as e:
            print(f"!!! [ORCHESTRATOR ERROR] Flashcards Failed: {e}")
            import traceback
            traceback.print_exc()
            flashcards_data = None

        # 6. Generate Quiz
        print(f"--- [ORCHESTRATOR] Generating Quiz ---")
        try:
            quiz_chain = quiz_generator.get_quiz_chain(self.llm)
            quiz_data = quiz_chain.invoke({"topic": topic, "content": article})
        except Exception as e:
            print(f"Error generating quiz: {e}")
            quiz_data = None
            
        # --- LOGGING FORMATTED OUTPUT TO TERMINAL ---
        print("\n" + "="*60)
        print(f"📘 COURSE GENERATED: {topic.upper()}")
        print("="*60 + "\n")
        print(article)
        print(f"--- [ORCHESTRATOR] Videos: REMOVED ---")
        
        print("\n" + "-"*60)
        print("🎴 FLASHCARDS")
        print("-"*60)
        if flashcards_data and 'flashcards' in flashcards_data:
            for idx, fc in enumerate(flashcards_data['flashcards'], 1):
                img_status = "✅ Image Generated" if fc.get('image_b64') else "❌ No Image"
                print(f"{idx}. {fc['concept']} - {img_status}")

        print("\n" + "-"*60)
        print("🧠 QUIZ")
        print("-"*60)
        if quiz_data and 'questions' in quiz_data:
            for idx, q in enumerate(quiz_data['questions'], 1):
                print(f"{idx}. {q['question']} (Ans: {q['correct_answer']})")
        print("="*60 + "\n")
        # --------------------------------------------

        return {
            "article": article,
            "research": research_output,
            "videos": videos,
            "flashcards": flashcards_data,
            "quiz": quiz_data
        }
