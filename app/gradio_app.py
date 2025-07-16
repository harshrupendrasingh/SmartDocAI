import gradio as gr
import os
from ocr.extract_text import extract_text_from_pdf, extract_text_from_image
from qa.answer_question import answer_question

def process_doc_and_qa(file, question):
    if not file:
        return "Please upload a document."

    filepath = file.name
    filename = os.path.basename(filepath)

    if filename.lower().endswith((".jpg", ".jpeg", ".png")):
        context = extract_text_from_image(filepath)
    else:
        context = extract_text_from_pdf(filepath)

    if len(context.strip()) == 0:
        return "No text found in document."

    answer = answer_question(question, context)
    return answer

iface = gr.Interface(
    fn=process_doc_and_qa,
    inputs=[
        gr.File(label="Upload PDF or Image"),
        gr.Textbox(lines=1, placeholder="Ask a question about the document...", label="Your Question"),
    ],
    outputs="text",
    title="SmartDocAI",
    description="Upload a document and ask a question. Extracts text and answers using Transformers."
)

if __name__ == "__main__":
    iface.launch()
