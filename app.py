import streamlit as st
from huggingface_hub import InferenceClient
import textstat

PROMPTS = {
    "General Adult": """
Simplify this scientific text so any adult can understand it.
Do not add information that is not in the original:

{abstract}

Simplified:
""",
    "Middle School": """
You are a science teacher explaining this to a middle school class.
Keep it accurate and easy:

{abstract}

Explanation:
""",
    "Undergraduate": """
You are a teaching assistant.
Rewrite this for undergraduates, preserving accuracy while improving readability:

{abstract}

Rewrite:
"""
}

st.title("🔬 Audience-Aware Scientific Abstract Simplification")

audience = st.selectbox(
    "Choose target audience",
    list(PROMPTS.keys())
)

uploaded_file = st.file_uploader(
    "Upload an abstract as a TXT file",
    type=["txt"]
)

pasted_abstract = st.text_area(
    "Or paste a scientific abstract",
    height=250
)

abstract = pasted_abstract

if uploaded_file is not None:
    abstract = uploaded_file.read().decode("utf-8")

if st.button("Simplify"):
    if len(abstract.strip().split()) < 20:
        st.error("Please enter an abstract with at least 20 words.")
    else:
        try:
            client = InferenceClient(
                provider="auto",
                api_key=st.secrets["HF_TOKEN"]
            )

            prompt = PROMPTS[audience].format(
                abstract=abstract.strip()
            )

            with st.spinner("Simplifying the abstract..."):
                response = client.chat.completions.create(
                    model="meta-llama/Meta-Llama-3-8B-Instruct",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    max_tokens=256
                )

            simplified = response.choices[0].message.content

            source_fkgl = textstat.flesch_kincaid_grade(abstract)
            output_fkgl = textstat.flesch_kincaid_grade(simplified)

            st.subheader(f"Simplified for {audience}")
            st.write(simplified)

            col1, col2, col3 = st.columns(3)

            col1.metric("Source FKGL", f"{source_fkgl:.1f}")
            col2.metric("Output FKGL", f"{output_fkgl:.1f}")
            col3.metric(
                "Grade-level reduction",
                f"{source_fkgl - output_fkgl:.1f}"
            )

        except Exception as error:
            st.error(f"Generation failed: {error}")    
            st.subheader("Original Scientific Abstract")
    st.write(row["source"])

with right:
    st.subheader(f"Simplified for {audience}")
    st.write(row["prediction"])

with st.expander("Human-written reference"):
    st.write(row["reference"])

st.subheader("Overall Experiment Results")

results = pd.read_csv("final_results_table.csv")
st.dataframe(results, use_container_width=True)
