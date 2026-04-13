# DeBet: Bayesian Argument Strength Scorer

DeBet is a multi-model evaluation framework designed to quantify the strength of an argument using **Bayesian updating principles**. Instead of measuring what an argument contains (length, citations), it measures how much a rational skeptic should shift their belief after reading it.

---

## 🧠 Core Philosophy

Traditional scoring systems measure content; DeBet measures **inferential move**.

- **Multiplicative Model**  
  If evidence ($E$) or logic ($L$) fails independently, the argument strength collapses to zero.

- **Evidence over Logic**  
  In empirical questions, facts decide the world. Evidence is weighted at $0.6$ ($\alpha$) and Logic at $0.4$ ($\beta$).

- **The Gap Penalty**  
  Unstated inferential jumps result in an exponential reduction in logical strength.

---

## 🛠 Installation

    # Clone the repository
    git clone https://github.com/panxyz123/DeBet_API.git

    # Install dependencies in editable mode
    pip install -e .

---

## ⚙️ Configuration

Create a `.env` file in the root directory and add your API keys:

    OPENAI_API_KEY=your_openai_key_here
    ANTHROPIC_API_KEY=your_anthropic_key_here

---

## 📊 The Equation

The engine implements the following formalized scoring model:

$$
S = (E^{0.6} \times L^{0.4} \times (1 - C) \times R)^{1.25} \times 100
$$

### Definitions

- **$E$ (Evidence)**  
  Calculated as the average of individual evidence pieces ($e_i$), where:

$$
e_i = \text{Credibility} \times \text{Recency} \times \text{Relevance} \times \text{Specificity}
$$

- **$L$ (Logic)**  
  Represents the logical transfer from evidence to conclusion:

$$
L = (\text{Average Step Strength}) \times (0.5^g)
$$

  where $g$ is the number of unstated logical gaps.

- **$C$ (Fallacy)**  
  A multiplicative penalty derived from identified logical fallacies.

- **$R$ (Rebuttal)**  
  A bonus multiplier (range: 1.0 – 1.5) awarded for:
  - Steelmanning the strongest counterargument  
  - Successfully refuting it

- **Exponent $1.25$**  
  A convexity parameter ($\gamma = 0.8$) used to spread the score distribution and reward genuinely excellent arguments.

---

## 🚀 API Usage (External Call)

For integration into other repositories:

    from debet import DeBetScorer

    # Initialize the Scorer (automatically loads keys from .env)
    scorer = DeBetScorer()

    # The argument to analyze
    argument = "Your text here..."

    # Run Multi-model Evaluation (OpenAI, Anthropic, Gemini)
    result = scorer.run_evaluation(argument)

    print(f"Composite Score: {result['composite_average_s']}")

---

## 📁 Audit Trail

Every evaluation generates two files for transparency and auditing:

- **`debet_master_logs.json`**  
  A cumulative record of raw parameters extracted by each LLM

---

## 🎯 Summary

DeBet shifts argument evaluation from surface-level metrics to **Bayesian belief updates**, rewarding:

- Strong, credible evidence
- Tight logical reasoning
- Explicit inference steps
- Thoughtful counterargument handling

While penalizing:

- Logical gaps
- Weak or outdated evidence
- Fallacies