import streamlit as st
import spacy
from collections import Counter

nlp = spacy.load("en_core_web_sm")

st.title("🔁 Reverse Search Engine")
st.write("Paste a paragraph. I will guess the questions that led to it.")

text_input = st.text_area("Enter paragraph:", height=200)


def generate_question(sentence):
    doc = nlp(sentence)

    for token in doc:
        # Look for main verb (ROOT)
        if token.dep_ == "ROOT" and token.pos_ == "VERB":
            verb = token.lemma_

            subject = None
            obj = None

            # Find subject
            for child in token.children:
                if child.dep_ in ("nsubj", "nsubjpass"):
                    subject = " ".join([t.text for t in child.subtree])

                if child.dep_ in ("dobj", "attr"):
                    obj = " ".join([t.text for t in child.subtree])

            if subject and obj:
                return f"Why did {subject} {verb} {obj}?"

    return None


if st.button("Generate Questions") and text_input.strip():
    doc = nlp(text_input)
    sentences = [sent.text.strip() for sent in doc.sents]

    questions = []
    for sentence in sentences:
        q = generate_question(sentence)
        if q:
            questions.append(q)

    # Add one abstract meta-question
    noun_chunks = [chunk.text for chunk in doc.noun_chunks]
    if noun_chunks:
        most_common = Counter(noun_chunks).most_common(1)[0][0]
        questions.append(f"What are the broader implications of {most_common}?")

    # Remove duplicates and limit to 5
    questions = list(dict.fromkeys(questions))[:5]

    st.subheader("🧠 Possible Original Questions:")
    for q in questions:
        st.write(f"- {q}")
