from transformers import pipeline

qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

def answer_question(question, context):
    if not question or not context:
        return "Question or context is empty."

    try:
        result = qa_pipeline({
            'question': question,
            'context': context
        })
        return result['answer']
    except Exception as e:
        return f"[ERROR] QA failed: {e}"

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python answer_question.py <question> <context_file>")
    else:
        question = sys.argv[1]
        context_path = sys.argv[2]

        try:
            with open(context_path, 'r', encoding='utf-8') as f:
                context = f.read()
        except FileNotFoundError:
            print(f"Context file '{context_path}' not found.")
            sys.exit(1)

        answer = answer_question(question, context)
        print("\n[ANSWER]")
        print(answer)
