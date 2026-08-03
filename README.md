🔬 Audience-Aware Scientific Abstract Simplification

Making dense scientific abstracts easier to understand for different audiences while preserving the original scientific meaning.

Overview

Scientific abstracts are usually written for experts. Their technical vocabulary, compressed sentence structure, and assumed background knowledge can make them difficult for students, journalists, patients, and general readers.

This project studies whether language models can rewrite scientific abstracts for three target audiences:

Middle-school readers

General adult readers

Undergraduate readers

The main challenge is the readability–faithfulness trade-off. A model may make an abstract easier to read, but aggressive simplification can remove qualifications, omit important details, or introduce unsupported explanations.

Our experiments compare fine-tuned sequence-to-sequence models with an instruction-tuned large language model and evaluate how well each approach balances simplification, readability, semantic similarity, and source support.

Research Questions

This project investigates five questions:

How do technical abstracts and expert lay summaries differ in length, vocabulary, and readability?

How do supervised models and an instruction-tuned LLM balance readability, reference similarity, and source support?

Does validation-based prompt selection improve over manually written zero-shot prompts?

How does the target audience affect readability and factual-support scores?

Does iterative self-refinement improve factual support after prompt selection?

Dataset

We use SciLay, a dataset containing paired scientific text and expert-written lay summaries from multiple journal domains.

After filtering empty and very short examples, the exploratory analysis contains:

43,060 valid source–reference pairs

Average source length: 210.44 words

Average reference length: 132.71 words

References are 36.9% shorter on average

Average source FKGL: 15.80

Average reference FKGL: 16.07

The references are substantially shorter, but they do not have a lower average Flesch–Kincaid Grade Level. This shows that FKGL alone is not a complete measure of scientific accessibility.

The domain grouping is used only for dataset analysis:

Biology

Medicine

Computer science

Other journals

Models and Experimental Conditions

Fine-tuned baselines

T5-base

BART-base

T5 and BART are trained on paired technical abstracts and lay summaries. They are audience-agnostic baselines because the training data does not contain separate middle-school, general-adult, and undergraduate labels.

Llama 3 baseline

Meta-Llama-3-8B-Instruct

Llama 3 is evaluated with separate prompts for:

General adults

Middle-school students

Undergraduates

Validation-based prompt selection

For each audience, four fixed candidate prompts are evaluated on 15 validation examples. The prompt with the highest validation SARI score is selected for test generation.

This is a transparent fixed-pool prompt-selection procedure. It does not automatically generate new prompts or perform full prompt compilation.

Iterative self-refinement

The selected Llama output is passed through up to three critique-and-revision rounds. The model is asked to identify dropped, altered, or unsupported claims and produce a revised simplification.

The final experiments show that this self-refinement procedure does not reliably improve factual support. Entailment drops sharply after the first revision and only partially recovers in later rounds.

Evaluation Metrics

Dimension

Metric

Purpose

Simplification quality

SARI

Measures appropriate additions, deletions, and retained content

Reference overlap

ROUGE-L

Measures longest-sequence overlap with the expert reference

Reference overlap

BLEU-4

Measures n-gram overlap with the expert reference

Semantic similarity

BERTScore

Measures contextual similarity to the expert reference

Readability

ΔFKGL

Source FKGL minus output FKGL; higher means a larger grade-level reduction

Source support

NLI-Entail

Estimates whether the generated output is supported by the source abstract

Important: NLI-Entail is an automatic support proxy, not definitive factual verification.

Results

All systems are evaluated on the same first 50 SciLay test examples.

System

Audience

SARI ↑

ROUGE-L ↑

BLEU-4 ↑

BERTScore ↑

ΔFKGL ↑

NLI-Entail ↑

T5 fine-tuned

General baseline

44.223

0.343

0.193

0.898

0.98

0.974

BART fine-tuned

General baseline

43.828

0.324

0.178

0.895

0.70

0.868

Llama 3 zero-shot

General

36.582

0.112

0.012

0.848

5.26

0.812

Llama 3 zero-shot

Middle school

36.491

0.092

0.005

0.832

7.88

0.416

Llama 3 zero-shot

Undergraduate

36.609

0.120

0.016

0.853

3.37

0.616

Prompt-selected Llama 3

General

36.383

0.144

0.014

0.862

4.33

0.944

Prompt-selected Llama 3

Middle school

38.083

0.093

0.007

0.828

9.72

0.360

Prompt-selected Llama 3

Undergraduate

38.034

0.141

0.028

0.861

2.69

0.661

Self-refined Llama 3

General

36.912

0.140

0.024

0.859

3.28

0.602

Self-refined Llama 3

Middle school

38.161

0.115

0.019

0.846

6.10

0.260

Self-refined Llama 3

Undergraduate

37.854

0.145

0.031

0.862

2.49

0.585

Main Findings

T5 achieves the strongest reference similarity and source support, but it makes only a small readability change.

BART performs similarly to T5, although its factual-support score is lower.

Llama 3 responds clearly to audience instructions and produces much larger readability gains.

Middle-school prompts simplify most aggressively, but they also receive the lowest NLI support.

Prompt selection improves average SARI and average NLI support, but the effect is not consistent across audiences.

Self-refinement does not reliably recover factual support and can damage a strong initial output.

No single model is best on every metric. The strongest system depends on whether the priority is reference similarity, readability, or source support.

Selected Prompts

General adult

Simplify this scientific text so any adult can understand it.
Do not add information that is not in the original:

{abstract}

Simplified:

Middle school

You are a science teacher explaining this to a middle school class.
Keep it accurate and easy:

{abstract}

Explanation:

Undergraduate

You are a teaching assistant.
Rewrite this for undergraduates, preserving accuracy while improving readability:

{abstract}

Rewrite:

Interactive Streamlit Dashboard

The repository includes a lightweight Streamlit dashboard that reads the saved prediction CSV files.

The dashboard allows users to:

Select an audience

Browse the previously generated test examples

Compare the original scientific abstract with the simplified output

View the human-written reference

Explore the final results table

The current dashboard does not load the Llama model or generate a new simplification from a newly pasted abstract. It is designed as a fast, reproducible results demo that does not require a GPU or rerunning the notebook.

Repository Structure

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

Update this structure in the README if your actual GitHub file names are different.

Running the Dashboard Locally

1. Clone the repository

git clone https://github.com/<your-username>/audience-aware-scientific-simplification.git
cd audience-aware-scientific-simplification

2. Install dependencies

python3 -m pip install -r requirements.txt

The dashboard only requires:

streamlit
pandas

3. Start the app

python3 -m streamlit run app.py

Then open:

http://localhost:8501

Deploying on Streamlit Community Cloud

Push the repository to GitHub.

Sign in to Streamlit Community Cloud with GitHub.

Create a new app.

Select the repository and branch.

Set the main file path to app.py.

Click Deploy.

Because the dashboard reads saved CSV files, deployment does not require a GPU or Hugging Face token.

Reproducing the Full Experiments

The complete experiment pipeline is contained in:

NLP_Colab_Final.ipynb

The notebook includes:

Dataset loading and preprocessing

Exploratory data analysis

T5 fine-tuning

BART fine-tuning

Llama 3 zero-shot generation

Validation-based prompt selection

Iterative self-refinement

Automatic evaluation

Result tables and figures

Running the full notebook requires significantly more time and GPU resources than running the Streamlit dashboard.

Limitations

Test evaluation uses only the first 50 test examples.

Prompt selection uses only the first 15 validation examples.

The examples are not randomized or stratified.

The experiment does not report confidence intervals or statistical significance.

All three audiences are evaluated against the same expert reference.

FKGL does not measure background knowledge or true comprehension.

NLI-Entail is not specialized for scientific factuality.

The audience labels are prompt-defined and were not validated with real readers.

The self-refinement implementation always accepts the first revision before later NLI comparisons.

Future Work

Future experiments should:

Evaluate a larger randomized test sample

Preserve per-example scores for confidence intervals

Use audience-specific references

Conduct human comprehension studies

Evaluate factual consistency at the claim level

Select prompts using multiple objectives

Compare every refinement candidate with the original output

Retain the best candidate instead of automatically accepting the latest revision

Team

Northeastern University — CS6120 Natural Language Processing, Summer 2026

Drashti Bhavsar

Hard Gondaliya

Akshat Mehta

Dev Patel

Under the mentorship of Prof. Silvio Amir.

Paper

The final research paper is available in:

paper/final_paper.pdf

License

Add a LICENSE file before claiming a specific open-source license.

The project code may be released under an appropriate license selected by the team. SciLay, Llama 3, pretrained models, and third-party libraries remain subject to their own licenses and terms.
