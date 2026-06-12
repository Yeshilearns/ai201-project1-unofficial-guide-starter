import gradio as gr
from query import ask


def handle_query(question):
    result = ask(question)

    sources = "\n".join(f"- {source}" for source in result["sources"])

    return result["answer"], sources


with gr.Blocks(title="Queens College CS Guide") as demo:
    gr.Markdown("# Queens College Computer Science Guide")
    gr.Markdown("Ask questions about the Queens College Computer Science program.")

    question = gr.Textbox(
        label="Your Question",
        placeholder="Example: What tutoring resources are available?"
    )

    ask_button = gr.Button("Ask")

    answer = gr.Textbox(
        label="Answer",
        lines=10
    )

    sources = gr.Textbox(
        label="Retrieved Sources",
        lines=5
    )

    ask_button.click(
        fn=handle_query,
        inputs=question,
        outputs=[answer, sources]
    )

    question.submit(
        fn=handle_query,
        inputs=question,
        outputs=[answer, sources]
    )

demo.launch()