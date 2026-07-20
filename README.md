# 🔬 Audience-Aware Scientific Abstract Simplification

> Making dense scientific research readable for *everyone* — from middle schoolers to undergraduates — without losing the facts.

<p align="center">
  <img src="https://img.shields.io/badge/Task-Text%20Simplification-blue" />
  <img src="https://img.shields.io/badge/Model-Llama%203%208B-orange" />
  <img src="https://img.shields.io/badge/Framework-PyTorch%20%7C%20HuggingFace-red" />
  <img src="https://img.shields.io/badge/Course-NEU%20CS6120%20NLP-green" />
  <img src="https://img.shields.io/badge/License-MIT-lightgrey" />
</p>

---

## 📖 Overview

Scientific abstracts are written for experts, which locks out the people who often need them most — patients, journalists, students, and policymakers. This project asks a simple question:

> **Can large language models rewrite scientific abstracts for a specific audience while keeping the science accurate?**

We build and evaluate a system that simplifies biomedical abstracts for **three distinct reading levels** — middle school, general adult, and undergraduate — and we tackle the core challenge nobody can ignore in this space: **the readability–faithfulness trade-off.** The easier you make the text, the more likely the model is to quietly drop or distort a scientific claim. Our pipeline is designed to fight exactly that.

---

## ✨ Key Highlights

- **Audience-aware** — one abstract, three tailored simplifications for different reading levels.
- **Four-dimensional evaluation** — we go beyond BLEU/ROUGE to measure simplification quality, semantic preservation, readability, *and* factual consistency.
- **Automatic prompt optimization** — instead of hand-writing prompts, we search a candidate pool and pick the best per audience using a validation metric.
- **Self-refinement loop** — the model critiques its own output for dropped/altered facts and revises, recovering factual accuracy lost during aggressive simplification.
- **Domain analysis** — we compare how simplification behaves across medicine, biology, and computer science.
- **Interactive dashboard** — a Gradio app to try the system live and view results. 

---

## 🧠 The Core Finding

Different model families sit at opposite ends of a fundamental trade-off:

| Model type | Readability gain | Factual accuracy |
|------------|:---------------:|:----------------:|
| **Fine-tuned (T5/BART)** | 🔴 Low — barely simplifies | 🟢 High — very faithful |
| **Zero-shot LLM (Llama 3)** | 🟢 High — big readability jump | 🟡 Drops as simplification gets aggressive |
| **Our pipeline** | 🟢 High | 🟢 Recovered via self-refinement |

> The more aggressively a model simplifies (e.g., for middle-schoolers), the more facts it risks losing. Our two-stage pipeline is built to find the sweet spot.

*(Full results table in the [paper](paper/) and [`results/`](results/).)*

---

## 🏗️ Method

```
┌─────────────────┐     ┌──────────────────────┐     ┌───────────────────┐
│  Scientific     │────▶│  Stage 1:            │────▶│  Stage 2:         │
│  Abstract       │     │  Prompt Optimization │     │  Self-Refinement  │
│  (technical)    │     │  (best prompt per    │     │  (critique + fix  │
│                 │     │   audience via SARI) │     │   factual errors) │
└─────────────────┘     └──────────────────────┘     └───────────────────┘
                                                              │
                                                              ▼
                                              ┌───────────────────────────┐
                                              │  Audience-tailored, fact-  │
                                              │  checked simplification    │
                                              └───────────────────────────┘
```

**Baselines:** T5-base, BART-base (fine-tuned) · Llama 3 8B (zero-shot)
**Our system:** Llama 3 + prompt optimization + self-refinement

---

## 📁 Repository Structure

```
audience-aware-scientific-simplification/
│
├── README.md                     
├── requirements.txt              ← dependencies
│
├── NLP.ipynb                     ← full end-to-end notebook (all steps in one place)
│                                    ↳ EDA · baselines · prompt optimization ·
│                                      self-refinement · evaluation · figures
│
├── results/
│   ├── final_results_table.csv   ← headline numbers
│   ├── eda_summary.json          ← dataset statistics
│   └── figures/                  ← generated plots
│
├── paper/
│   └── final_paper.pdf           ← the research paper (ACL 2023 format)
│
└── app/
    └── gradio_dashboard.py       ← interactive demo 
```
The entire pipeline lives in a single self-contained notebook, NLP.ipynb, organized into clearly labeled step-by-step cells 
(data analysis → baselines → prompt optimization → self-refinement → evaluation → visualization). 
---

## 📊 Dataset

We use **[SciLay](https://huggingface.co/datasets/disi-unibo-nlp/SciLay)** — ~44K pairs of scientific articles and expert-written plain-language summaries across biology, medicine, and computational science.

- **Input:** `technical_text` (the expert abstract)
- **Target:** `plain_text` (the human-written lay summary)
- **Domain labels:** from the `journal` field, enabling real domain analysis

---

## 📏 Evaluation Metrics

| Dimension | Metric | What it captures |
|-----------|--------|------------------|
| Simplification quality | **SARI** (primary) | rewards good additions, deletions, retained content |
| Semantic preservation | **BERTScore** | meaning kept vs. the reference |
| Readability | **Δ FKGL** | grade-level reduction (higher = simpler) |
| Factual consistency | **FactScore** (NLI entailment) | does the output stay true to the source? |

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/<your-username>/audience-aware-scientific-simplification.git
cd audience-aware-scientific-simplification
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the pipeline (in order)
```bash
python src/step2_eda.py              # explore the data
python src/step3_eval_pipeline.py    # test the metrics
python src/step4_llama3_baseline.py  # zero-shot baseline
python src/step5_finetune.py         # fine-tune T5 / BART
python src/step6_prompt_search.py    # optimize prompts
python src/step7_self_refine.py      # self-refinement
python src/step8_breakdown.py        # final results + breakdowns
python src/step9_visualizations.py   # figures
```

> 💡 **Tip:** The easiest way to run everything is the [Colab notebook](notebooks/NLP.ipynb) — it handles GPU setup and runs the whole pipeline end-to-end. A T4 GPU is enough (Llama 3 runs in 4-bit).

### 4. Launch the demo 
```bash
python app/gradio_dashboard.py
```

---

## 🖥️ Interactive Demo

A Gradio dashboard where you can:
- 📝 Paste any scientific abstract and pick a target audience
- 🔄 See all three audience levels side by side
- 📈 View readability + faithfulness scores computed live
- 📊 Explore our research findings and charts

---

## 🔬 Results at a Glance

*(Filled in after experiments — placeholder table)*

| System | SARI ↑ | BERTScore ↑ | Δ FKGL ↑ | FactScore ↑ |
|--------|:------:|:-----------:|:--------:|:-----------:|
| T5 (fine-tuned) | – | – | – | – |
| BART (fine-tuned) | – | – | – | – |
| Llama 3 (zero-shot) | – | – | – | – |
| Llama 3 + Prompt Opt. | – | – | – | – |
| Llama 3 + Self-Refine | – | – | – | – |
| **Llama 3 + Opt. + Self-Refine** | – | – | – | – |

---

## 🛠️ Tech Stack

**Python**  <br>
**PyTorch** <br>
**HuggingFace Transformers** <br>
**Llama 3 8B** <br>
**T5 / BART** <br>
**BERTScore** <br>
**DeBERTa-NLI** <br>
**Gradio** <br>
**Matplotlib** <br>

---

## 👥 Team

**NEU CS6120 — Natural Language Processing (Summer 2026)**

- Drashti Bhavsar - 002513797
- Hard Gondaliya - 002539979
- Akshat Mehta - 002598926
- Dev Patel - 002566173 

*Under the mentorship of **Prof. Silvio Amir**.*

---


## 📄 License

Released under the [MIT License](LICENSE).

---

<p align="center">
  <i>Making science accessible, one abstract at a time. 🔬 → 📖</i>
</p>
