from pathlib import Path

import pandas as pd
import streamlit as st
import textstat
from huggingface_hub import InferenceClient

st.set_page_config(
    page_title="Audience-Aware Scientific Abstract Simplification",
    page_icon="🔬",
    layout="wide",
)

MODEL_ID = "meta-llama/Llama-3.1-8B-Instruct"

PROMPTS = {
    "General Adult": (
        "Simplify this scientific text so any adult can understand it. "
        "Do not add information that is not in the original:\n\n"
        "{abstract}\n\nSimplified:"
    ),
    "Middle School": (
        "You are a science teacher explaining this to a middle school class. "
        "Keep it accurate and easy:\n\n"
        "{abstract}\n\nExplanation:"
    ),
    "Undergraduate": (
        "You are a teaching assistant. Rewrite this for undergraduates, "
        "preserving accuracy while improving readability:\n\n"
        "{abstract}\n\nRewrite:"
    ),
}


def locate_file(filename: str) -> Path:
    for candidate in [Path("results") / filename, Path(filename)]:
        if candidate.exists():
            return candidate
    raise FileNotFoundError(
        f"Could not find '{filename}'. Put it in the repository root "
        "or inside a results folder."
    )


@st.cache_data(show_spinner=False)
def load_csv(filename: str) -> pd.DataFrame:
    return pd.read_csv(locate_file(filename))


def get_hf_token() -> str:
    try:
        token = st.secrets["HF_TOKEN"]
    except Exception as exc:
        raise RuntimeError(
            "HF_TOKEN is missing. Open Streamlit → Manage app → Settings "
            "→ Secrets and add: HF_TOKEN = \"hf_your_token\""
        ) from exc
    if not token:
        raise RuntimeError("HF_TOKEN is empty.")
    return token


def generate_simplification(abstract: str, audience: str) -> str:
    client = InferenceClient(provider="auto", api_key=get_hf_token())
    prompt = PROMPTS[audience].format(abstract=abstract.strip())
    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=256,
        temperature=0.0,
    )
    output = response.choices[0].message.content
    if not output:
        raise RuntimeError("The model returned an empty response.")
    return output.strip()


def readability_metrics(source: str, output: str) -> dict:
    source_fkgl = textstat.flesch_kincaid_grade(source)
    output_fkgl = textstat.flesch_kincaid_grade(output)
    return {
        "source_fkgl": source_fkgl,
        "output_fkgl": output_fkgl,
        "fkgl_reduction": source_fkgl - output_fkgl,
        "source_words": len(source.split()),
        "output_words": len(output.split()),
    }


st.title("🔬 Audience-Aware Scientific Abstract Simplification")
st.write(
    "Use the Live Simplifier for a new abstract, or open Saved Experiment "
    "Results to browse the 50 outputs generated during the project."
)

live_tab, saved_tab = st.tabs(
    ["✨ Live Simplifier", "📊 Saved Experiment Results"]
)

with live_tab:
    st.subheader("Generate a new audience-specific simplification")

    audience = st.selectbox(
        "Choose target audience",
        list(PROMPTS.keys()),
        key="live_audience",
    )

    uploaded_file = st.file_uploader(
        "Upload an abstract as a TXT file",
        type=["txt"],
        key="live_upload",
    )

    pasted_abstract = st.text_area(
        "Or paste a scientific abstract",
        height=260,
        key="live_text",
    )

    abstract = pasted_abstract.strip()
    if uploaded_file is not None:
        try:
            abstract = uploaded_file.read().decode("utf-8").strip()
        except UnicodeDecodeError:
            st.error("The uploaded TXT file must use UTF-8 encoding.")
            abstract = ""

    if st.button("Simplify", type="primary", key="live_simplify"):
        if len(abstract.split()) < 20:
            st.error("Please enter an abstract with at least 20 words.")
        else:
            try:
                with st.spinner("Generating the simplified abstract..."):
                    simplified = generate_simplification(abstract, audience)

                metrics = readability_metrics(abstract, simplified)
                st.success("Simplification complete.")

                col1, col2, col3, col4, col5 = st.columns(5)
                col1.metric("Source FKGL", f"{metrics['source_fkgl']:.1f}")
                col2.metric("Output FKGL", f"{metrics['output_fkgl']:.1f}")
                col3.metric(
                    "Grade-level reduction",
                    f"{metrics['fkgl_reduction']:.1f}",
                )
                col4.metric("Source words", metrics["source_words"])
                col5.metric("Output words", metrics["output_words"])

                source_col, output_col = st.columns(2)
                with source_col:
                    st.subheader("Original Scientific Abstract")
                    st.write(abstract)
                with output_col:
                    st.subheader(f"Simplified for {audience}")
                    st.write(simplified)

                st.download_button(
                    "Download simplified text",
                    data=simplified,
                    file_name=(
                        audience.lower().replace(" ", "_")
                        + "_simplification.txt"
                    ),
                    mime="text/plain",
                )

                st.info(
                    "SARI, ROUGE, BLEU, and BERTScore are not shown for a "
                    "new abstract because those metrics require a human reference."
                )
            except Exception as error:
                st.error(f"Generation failed: {error}")

with saved_tab:
    st.subheader("Browse previously generated project outputs")

    prediction_files = {
        "General Adult": "promptsearch_general_predictions.csv",
        "Middle School": "promptsearch_middle_school_predictions.csv",
        "Undergraduate": "promptsearch_undergraduate_predictions.csv",
    }

    saved_audience = st.selectbox(
        "Choose audience",
        list(prediction_files.keys()),
        key="saved_audience",
    )

    try:
        predictions = load_csv(prediction_files[saved_audience])
        if predictions.empty:
            st.warning("The selected prediction file is empty.")
        else:
            example_number = st.slider(
                "Choose test example",
                min_value=1,
                max_value=len(predictions),
                value=1,
                key="saved_example",
            )
            row = predictions.iloc[example_number - 1]
            st.caption(f"Journal: {row.get('journal', 'Not available')}")

            source_col, output_col = st.columns(2)
            with source_col:
                st.subheader("Original Scientific Abstract")
                st.write(row.get("source", "Source column not found."))
            with output_col:
                st.subheader(f"Simplified for {saved_audience}")
                st.write(
                    row.get("prediction", "Prediction column not found.")
                )

            with st.expander("Human-written reference"):
                st.write(row.get("reference", "Reference column not found."))
    except Exception as error:
        st.error(f"Could not load saved predictions: {error}")

    st.divider()
    st.subheader("Final experiment results")
    try:
        results = load_csv("final_results_table.csv")
        st.dataframe(results, use_container_width=True, hide_index=True)
    except Exception as error:
        st.error(f"Could not load final results table: {error}")

st.divider()
st.caption(
    "Live generation uses the project's selected audience prompts. "
    "Saved results reproduce the outputs already generated during evaluation."
)
