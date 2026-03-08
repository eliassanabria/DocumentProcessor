from app.gemini_client import GeminiClient
from app.rag.ingest import ingest_pdf
from app.rag.retrieve import retrieve_relevant_chunks
from app.rag.store import InMemoryVectorStore
from app.tools.checklist import generate_checklist
from app.tools.extract import extract_requirements
from app.tools.issues import create_issue_payload


def print_help() -> None:
    print("\nAvailable commands:")
    print("  ask <question>              Ask a grounded question")
    print("  extract <topic>             Extract requirements related to a topic")
    print("  checklist <topic>           Generate a checklist")
    print("  issue <request>             Create a mock issue payload")
    print("  help                        Show commands")
    print("  exit                        Quit\n")


def main() -> None:
    pdf_path = input("Enter PDF path: ").strip()

    print("\nIngesting document...")
    records = ingest_pdf(pdf_path)

    store = InMemoryVectorStore()
    store.add_records(records)

    print(f"Loaded {len(records)} chunks.")
    client = GeminiClient()

    print_help()

    while True:
        user_input = input("doc-assistant> ").strip()
        if not user_input:
            continue

        if user_input.lower() == "exit":
            print("Goodbye.")
            break

        if user_input.lower() == "help":
            print_help()
            continue

        if user_input.startswith("ask "):
            question = user_input[4:].strip()
            chunks = retrieve_relevant_chunks(store, question)
            answer = client.answer_grounded_question(question, chunks)
            print("\n" + answer + "\n")
            continue

        if user_input.startswith("extract "):
            topic = user_input[8:].strip()
            chunks = retrieve_relevant_chunks(store, topic)
            result = extract_requirements(client, chunks)
            print("\n" + result + "\n")
            continue

        if user_input.startswith("checklist "):
            topic = user_input[10:].strip()
            chunks = retrieve_relevant_chunks(store, topic)
            result = generate_checklist(client, chunks)
            print("\n" + result + "\n")
            continue

        if user_input.startswith("issue "):
            request = user_input[6:].strip()
            chunks = retrieve_relevant_chunks(store, request)
            result = create_issue_payload(client, request, chunks)
            print("\n" + result + "\n")
            continue

        print("Unknown command. Type 'help' for options.")


if __name__ == "__main__":
    main()