# DeBet: Bayesian Argument Strength Scorer

DeBet is a multi-model evaluation framework designed to quantify the strength of an argument using **Bayesian updating principles**. Instead of measuring what an argument contains (length, citations), it measures how much a rational skeptic should shift their belief after reading it.

## 🧠 Core Philosophy
Traditional scoring systems measure content; DeBet measures **inferential move**.
* **Multiplicative Model**: If evidence ($E$) or logic ($L$) fails independently, the argument strength collapses to zero.
* **Evidence over Logic**: In empirical questions, facts decide the world. Evidence is weighted at $0.6$ ($\alpha$) and Logic at $0.4$ ($\beta$).
* **The Gap Penalty**: Unstated inferential jumps result in an exponential reduction in logical strength.



## 🛠 Installation

```bash
# Clone the repository
git clone [https://github.com/your-username/debet-scorer.git](https://github.com/your-username/debet-scorer.git)
cd debet-scorer

# Install dependencies in editable mode
pip install -e .
⚙️ ConfigurationCreate a .env file in the root directory and add your API keys:
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
GOOGLE_API_KEY=your_google_key_here
📊 The EquationThe engine implements the following formalized scoring model:$$S = (E^{0.6} \times L^{0.4} \times (1 - C) \times R)^{1.25} \times 100$$$E$ (Evidence): Calculated as the average of individual evidence pieces ($e_i$), where $e_i = \text{Credibility} \times \text{Recency} \times \text{Relevance} \times \text{Specificity}$.$L$ (Logic): Represents the logical transfer from evidence to conclusion, calculated as $L = (\text{Average Step Strength}) \times (0.5^g)$, where $g$ is the count of unstated logical gaps.$C$ (Fallacy): A multiplicative penalty derived from identified logical fallacies.$R$ (Rebuttal): A bonus multiplier (1.0 to 1.5) for "Steelmanning" the strongest counterargument and successfully refuting it.$1.25$ Exponent: A convexity parameter ($\gamma=0.8$) used to spread the score distribution to reward genuinely excellent arguments.🚀 API Usage (External Call)For integration into other repositories, use the following pattern:
```
from debet import DeBetScorer

# Initialize the Scorer (automatically loads keys from .env)
scorer = DeBetScorer()

# The argument to analyze
argument = "Your text here..."

# Run Multi-model Evaluation (OpenAI, Anthropic, Gemini)
result = scorer.run_evaluation(argument)

print(f"Composite Score: {result['composite_average_s']}")
```
📁 Audit TrailEvery evaluation generates two files for transparency and auditing:debet_master_logs.json: A cumulative record of raw parameters extracted by each LLM.debet_audit_TIMESTAMP.xlsx: A human-readable spreadsheet containing the rationale for every score dimension.