# 🔬 Audience-Aware Scientific Abstract Simplification

Making dense scientific abstracts easier to understand for different audiences while preserving the original scientific meaning.

---

## 📖 Overview

Scientific abstracts are usually written for experts. Their technical vocabulary, compressed sentence structure, and assumed background knowledge can make them difficult for students, journalists, patients, policymakers, and general readers.

This project investigates whether language models can rewrite scientific abstracts for three target audiences:

- Middle-school readers
- General adult readers
- Undergraduate readers

The main challenge is the **readability–faithfulness trade-off**.

A model may make an abstract easier to read, but aggressive simplification can also:

- remove important details,
- omit scientific qualifications,
- change the meaning of a claim,
- or introduce unsupported explanations.

Our experiments compare fine-tuned sequence-to-sequence models with an instruction-tuned large language model and evaluate how well each approach balances readability, simplification quality, semantic similarity, and source support.

---

## 🎯 Research Questions

This project investigates five research questions:

1. How do technical abstracts and expert lay summaries differ in length, vocabulary, and readability?
2. How do supervised models and an instruction-tuned LLM balance readability, reference similarity, and source support?
3. Does validation-based prompt selection improve over manually written zero-shot prompts?
4. How does the target audience affect readability and factual-support scores?
5. Does iterative self-refinement improve factual support after prompt selection?

---

## 📊 Dataset

We use **SciLay**, a dataset containing paired scientific text and expert-written lay summaries from multiple journal domains.

After filtering empty and very short examples, the exploratory analysis contains:

- **43,060 valid source–reference pairs**
- Average source length: **210.44 words**
- Average reference length: **132.71 words**
- References are approximately **36.9% shorter**
- Average source FKGL: **15.80**
- Average reference FKGL: **16.07**

The expert references are substantially shorter, but they do not have a lower average Flesch–Kincaid Grade Level.

This shows that FKGL alone is not a complete measure of scientific accessibility.

The dataset domains used for exploratory analysis are:

- Biology
- Medicine
- Computer science
- Other journals

The domain grouping is used only for dataset analysis and not for model training or prompt selection.

---

## 🧠 Models and Experimental Conditions

### Fine-tuned baselines

We fine-tune two sequence-to-sequence models:

- **T5-base**
- **BART-base**

T5 and BART are trained on paired technical abstracts and expert-written lay summaries.

These models are audience-agnostic because their training data does not contain separate labels for middle-school, general-adult, and undergraduate readers.

---

### Llama 3 zero-shot baseline

We evaluate:

- **Meta-Llama-3-8B-Instruct**

Llama 3 receives different instructions for:

- General adults
- Middle-school students
- Undergraduate students

This allows us to test whether an instruction-tuned model can produce different levels of simplification without additional fine-tuning.

---

### Validation-based prompt selection

For each audience, we define four fixed candidate prompts.

Each prompt is evaluated on the first 15 validation examples using SARI.

The highest-scoring prompt is selected separately for:

- General adults
- Middle-school readers
- Undergraduate readers

This is a transparent fixed-pool prompt-selection method.

It does not automatically generate new prompts and is not full prompt compilation.

---

### Iterative self-refinement

The selected Llama output is passed through up to three critique-and-revision rounds.

The model is asked to identify:

- dropped claims,
- altered scientific meaning,
- unsupported additions,
- and factual inconsistencies.

It then generates a revised simplification.

However, the final experiments show that the implemented self-refinement method does **not** reliably improve factual support.

Entailment decreases sharply after the first revision and only partially recovers in later rounds.

---

## 🏗️ Methodology

```text
Scientific Abstract
        │
        ▼
Select Target Audience
        │
        ├── General Adult
        ├── Middle School
        └── Undergraduate
        │
        ▼
Generate Audience-Specific Simplification
        │
        ▼
Validation-Based Prompt Selection
        │
        ▼
Optional Self-Refinement
        │
        ▼
Evaluate Readability, Similarity, and Source Support
```

The project compares:

```text
T5 fine-tuned
BART fine-tuned
Llama 3 zero-shot
Llama 3 with validation-selected prompts
Llama 3 with self-refinement
```

---

## 📏 Evaluation Metrics

| Dimension | Metric | Purpose |
|---|---|---|
| Simplification quality | SARI | Measures appropriate additions, deletions, and retained content |
| Reference overlap | ROUGE-L | Measures longest-sequence overlap with the expert reference |
| Reference overlap | BLEU-4 | Measures n-gram overlap with the expert reference |
| Semantic similarity | BERTScore | Measures contextual similarity to the expert reference |
| Readability | ΔFKGL | Source FKGL minus output FKGL; higher means a larger grade-level reduction |
| Source support | NLI-Entail | Estimates whether the output is supported by the source abstract |

> **Important:** NLI-Entail is an automatic support proxy. It should not be interpreted as definitive factual verification.

---

## 🔬 Final Results

All systems are evaluated on the same first 50 SciLay test examples.

| System | Audience | SARI ↑ | ROUGE-L ↑ | BLEU-4 ↑ | BERTScore ↑ | ΔFKGL ↑ | NLI-Entail ↑ |
|---|---|---:|---:|---:|---:|---:|---:|
| T5 fine-tuned | General baseline | **44.223** | **0.343** | **0.193** | **0.898** | 0.98 | **0.974** |
| BART fine-tuned | General baseline | 43.828 | 0.324 | 0.178 | 0.895 | 0.70 | 0.868 |
| Llama 3 zero-shot | General | 36.582 | 0.112 | 0.012 | 0.848 | 5.26 | 0.812 |
| Llama 3 zero-shot | Middle school | 36.491 | 0.092 | 0.005 | 0.832 | 7.88 | 0.416 |
| Llama 3 zero-shot | Undergraduate | 36.609 | 0.120 | 0.016 | 0.853 | 3.37 | 0.616 |
| Prompt-selected Llama 3 | General | 36.383 | 0.144 | 0.014 | 0.862 | 4.33 | 0.944 |
| Prompt-selected Llama 3 | Middle school | 38.083 | 0.093 | 0.007 | 0.828 | **9.72** | 0.360 |
| Prompt-selected Llama 3 | Undergraduate | 38.034 | 0.141 | 0.028 | 0.861 | 2.69 | 0.661 |
| Self-refined Llama 3 | General | 36.912 | 0.140 | 0.024 | 0.859 | 3.28 | 0.602 |
| Self-refined Llama 3 | Middle school | 38.161 | 0.115 | 0.019 | 0.846 | 6.10 | 0.260 |
| Self-refined Llama 3 | Undergraduate | 37.854 | 0.145 | 0.031 | 0.862 | 2.49 | 0.585 |

---

## ✨ Main Findings

- **T5 achieves the strongest reference similarity and source support**, but produces only a small readability improvement.
- **BART performs similarly to T5**, although its NLI support score is lower.
- **Llama 3 responds clearly to audience instructions** and produces much larger grade-level reductions.
- **Middle-school prompts simplify most aggressively**, but also produce the lowest source-support scores.
- **Prompt selection improves average SARI and average NLI support**, but the effects are not consistent across all audiences.
- **Self-refinement does not reliably recover factual support** and may damage a strong initial output.
- No single model is best on every metric.
- The strongest system depends on whether the priority is readability, reference similarity, or source support.

---

## 🧩 Core Readability–Faithfulness Trade-off

| Model type | Readability gain | Source support |
|---|---|---|
| Fine-tuned T5/BART | Low | High |
| Audience-prompted Llama 3 | High | Lower under aggressive simplification |
| Prompt-selected Llama 3 | Audience-dependent | Audience-dependent |
| Self-refined Llama 3 | Moderate | Did not recover initial support |

The results show that simpler text is not automatically safer or more accurate.

---

## 📝 Selected Prompts

### General adult

```text
Simplify this scientific text so any adult can understand it.
Do not add information that is not in the original:

{abstract}

Simplified:
```

### Middle school

```text
You are a science teacher explaining this to a middle school class.
Keep it accurate and easy:

{abstract}

Explanation:
```

### Undergraduate

```text
You are a teaching assistant.
Rewrite this for undergraduates, preserving accuracy while improving readability:

{abstract}

Rewrite:
```

---

## 🖥️ Interactive Streamlit Dashboard

The repository includes a lightweight Streamlit dashboard that reads the saved prediction CSV files.

The dashboard allows users to:

- select a target audience,
- browse previously generated test examples,
- compare the original scientific abstract with the simplified output,
- view the human-written reference,
- and explore the final experiment results.

The current dashboard does **not** load Llama 3 or generate a new simplification from a newly pasted abstract.

It is designed as a fast and reproducible project demonstration that does not require:

- a GPU,
- a Hugging Face token,
- or rerunning the full notebook.

---

## 📁 Repository Structure

```text
audience-aware-scientific-simplification/
│
├── README.md
├── requirements.txt
├── app.py
├── NLP_Colab_Final.ipynb
│
├── results/
│   ├── final_results_table.csv
│   ├── promptsearch_general_predictions.csv
│   ├── promptsearch_middle_school_predictions.csv
│   ├── promptsearch_undergraduate_predictions.csv
│   ├── eda_summary.json
│   └── figures/
│
└── paper/
    └── final_paper.pdf
```

> Update the file names in this section if your actual GitHub repository uses different names.

---

## 🚀 Running the Dashboard Locally

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/audience-aware-scientific-simplification.git
cd audience-aware-scientific-simplification
```

Replace `YOUR-USERNAME` with your GitHub username.

---

### 2. Install dependencies

```bash
python3 -m pip install -r requirements.txt
```

For the saved-results Streamlit dashboard, the main dependencies are:

```text
streamlit>=1.40
pandas>=2.0
huggingface_hub>=0.27
textstat>=0.7
```

---

### 3. Start the Streamlit app -  LINK {https://audience-aware-scientific-simplification.streamlit.app}

```bash
python3 -m streamlit run app.py
```

Open the local application at:

```text
http://localhost:8501
```

---

## 🌐 Deploying on Streamlit Community Cloud

1. Push the repository to GitHub.
2. Sign in to Streamlit Community Cloud using GitHub.
3. Click **Create app**.
4. Select the repository and branch.
5. Set the main file path to:

```text
app.py
```

6. Click **Deploy**.

Because the dashboard reads saved CSV files, deployment does not require a GPU or Hugging Face token.

---

## 🔁 Reproducing the Full Experiments

The complete experimental pipeline is available in:

```text
NLP_Colab_Final.ipynb
```

The notebook contains:

- Dataset loading
- Data preprocessing
- Exploratory data analysis
- T5 fine-tuning
- BART fine-tuning
- Llama 3 zero-shot generation
- Validation-based prompt selection
- Iterative self-refinement
- Automatic evaluation
- Result tables
- Figures and visualizations

Running the complete notebook requires significantly more time and GPU resources than running the Streamlit dashboard.

---

## ⚠️ Limitations

- Test evaluation uses only the first 50 test examples.
- Prompt selection uses only the first 15 validation examples.
- The examples are not randomized or stratified.
- The experiment does not report confidence intervals or statistical significance.
- All three audiences are evaluated against the same expert reference.
- FKGL does not measure background knowledge or true comprehension.
- NLI-Entail is not specialized for scientific factuality.
- The audience categories are defined through prompts and were not validated with real readers.
- The self-refinement implementation accepts the first revision before comparing later revisions.

---

## 🔮 Future Work

Future experiments should:

- evaluate a larger randomized test sample,
- preserve per-example scores,
- report confidence intervals,
- create audience-specific references,
- conduct human comprehension studies,
- evaluate factual consistency at the claim level,
- use multi-objective prompt selection,
- compare every refinement candidate with the original output,
- and retain the strongest candidate instead of automatically accepting the newest revision.

---

## 🛠️ Tech Stack

- Python
- PyTorch
- Hugging Face Transformers
- T5
- BART
- Llama 3 8B Instruct
- DeBERTa NLI
- BERTScore
- SARI
- ROUGE
- BLEU
- Streamlit
- Pandas
- Matplotlib

---

## 👥 Team

**Northeastern University — CS6120 Natural Language Processing, Summer 2026**

- Drashti Bhavsar
- Hard Gondaliya
- Akshat Mehta
- Dev Patel

Under the mentorship of **Prof. Silvio Amir**.

---

## 📄 Research Paper

The final research paper is available at:

```text
paper/final_paper.pdf
```

---

## 🔐 Security

Do not upload private tokens or credentials to GitHub.

Recommended `.gitignore` entries:

```gitignore
.streamlit/secrets.toml
.env
__pycache__/
.ipynb_checkpoints/
.DS_Store
*.pyc
```

---

## 📜 License

Add a `LICENSE` file before claiming a specific open-source license.

The project code may be released under a license selected by the team.

SciLay, Llama 3, pretrained models, and third-party libraries remain subject to their own licenses and usage terms.

---

## Final Message

**Making scientific information easier to access—without assuming that simpler always means safer.**
