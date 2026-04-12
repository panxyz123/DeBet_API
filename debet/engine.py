import json
import os
import pandas as pd
from datetime import datetime

class DebetEngine:
    def __init__(self, log_file="debet_master_logs.json"):
        self.ALPHA = 0.6
        self.BETA = 0.4
        self.GAMMA = 0.8
        self.log_file = log_file

    def calculate_s(self, e: float, l: float, c: float, r: float) -> float:
            """
            Calculates the final Argument Strength Score (S).
            S = (E^α × L^β × (1 - C) × R) ^ (1/γ) × 100 
            
            Parameters:
            - e: Evidence Quality (0.0 - 1.0) [cite: 19]
            - l: Logical Transfer (0.0 - 1.0), includes gap penalties [cite: 34, 52]
            - c: Fallacy Penalty (0.0 - 1.0) [cite: 57]
            - r: Rebuttal Multiplier (1.0 - 1.5) [cite: 67, 76]
            """
            # alpha=0.6, beta=0.4, gamma=0.8 
            # Multiplicative structure ensures that if E or L is zero, S is zero [cite: 10, 84, 85]
            
            # 1. Calculate the base score using weighted components
            # Evidence is weighted more than logic (0.6 vs 0.4) 
            # (1 - C) collapses the score if fallacies are present [cite: 63, 65]
            base = (e ** self.ALPHA) * (l ** self.BETA) * (1 - c) * r
            
            # 2. Apply the convexity parameter (1/gamma = 1.25)
            # This spreads the distribution to reward genuinely excellent arguments [cite: 17, 18]
            s_score = (base ** (1 / self.GAMMA)) * 100
            
            # Cap at 100.0 and round to 2 decimal places [cite: 12]
            return round(min(max(s_score, 0.0), 100.0), 2)

    def save_results(self, session_data: list):
        """Append session results to a master JSON file and export to Excel."""
        # Save to JSON
        existing_data = []
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r') as f:
                existing_data = json.load(f)
        
        existing_data.extend(session_data)
        with open(self.log_file, 'w') as f:
            json.dump(existing_data, f, indent=2)

        # Export to Excel for readability
        df = pd.json_normalize(session_data)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        # df.to_excel(f"debet_audit_{timestamp}.xlsx", index=False)