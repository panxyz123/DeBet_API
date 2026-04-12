import os
import json
from datetime import datetime
from dotenv import load_dotenv
from debet.engine import DebetEngine
from debet.client import LLMManager

# Load environment variables from .env file
load_dotenv()

class DeBetScorer:
    def __init__(self):
        # API keys are retrieved from environment variables
        self.api_keys = {
            "openai": os.getenv("OPENAI_API_KEY"),
            "anthropic": os.getenv("ANTHROPIC_API_KEY"),
            # "google": os.getenv("GOOGLE_API_KEY")
        }
        
        # Initialize the calculation engine and the multi-API manager
        self.engine = DebetEngine()
        self.llm_manager = LLMManager(self.api_keys)

    def run_evaluation(self, argument_text: str):
        """
        Orchestrates the evaluation:
        1. Calls OpenAI, Anthropic, and Gemini.
        2. Calculates S for each based on the Bayesian update formula. [cite: 5, 6]
        3. Saves logs and returns the composite average.
        """
        call_map = {
            "OpenAI": self.llm_manager.call_openai,
            "Anthropic": self.llm_manager.call_anthropic,
            # "Gemini": self.llm_manager.call_gemini
        }
        
        session_results = []
        final_scores = []

        print(f"Starting evaluation of argument: {argument_text[:50]}...")

        for name, call_func in call_map.items():
            try:
                # Step 1: Extract parameters (E, L, C, R) via LLM [cite: 12]
                raw_params = call_func(argument_text)
                
                # Step 2: Use the engine to calculate the final S score
                # This ensures mathematical precision and the 'zero-score collapse' logic [cite: 10, 83]
                e_val = float(raw_params.get("E", 0.0))
                l_val = float(raw_params.get("L", 0.0))  # Now directly includes gap penalties 
                c_val = float(raw_params.get("C", 0.0))  # Fallacy penalty [cite: 57, 63]
                r_val = float(raw_params.get("R", 1.0))  # Rebuttal multiplier [cite: 67, 76]

                # 3. Step 3: Call the updated engine
                # The engine now performs the weighted Bayesian calculation [cite: 12, 13]
                s = self.engine.calculate_s(
                    e=e_val, 
                    l=l_val, 
                    c=c_val, 
                    r=r_val
                )
                
                entry = {
                    "timestamp": datetime.now().isoformat(),
                    "provider": name,
                    "input text": argument_text,
                    "parameters": raw_params,
                    "final_s": s,
                    "status": "success"
                }
                final_scores.append(s)
                print(f"[{name}] Evaluation complete. Score: {s}")

            except Exception as e:
                entry = {
                    "timestamp": datetime.now().isoformat(),
                    "provider": name, 
                    "status": "error", 
                    "error": str(e)
                }
                print(f"[{name}] Failed: {e}")
            
            session_results.append(entry)

        # Step 3: Persistence - Save granular results for auditing [cite: 96]
        self.engine.save_results(session_results)

        # Step 4: Aggregate final composite result
        avg_s = round(sum(final_scores) / len(final_scores), 2) if final_scores else 0
        
        return {
            "composite_average_s": avg_s,
            "individual_provider_results": session_results,
            "log_files_created": ["debet_master_logs.json"]
        }

if __name__ == "__main__":
    scorer = DeBetScorer()
    # Replace with the argument you wish to score
    # test_argument = "AI will not replace most workers, but instead transform how work is done. This view emphasizes that jobs are made up of many different tasks, and while AI can automate some of them, it rarely replaces an entire role. Human workers still provide judgment, accountability, creativity, and social interaction—qualities that AI struggles to replicate reliably."
    # result = scorer.run_evaluation(test_argument)
    
    # print("\n--- Final Results ---")
    # print(f"Composite DeBet Score: {result['composite_average_s']}")