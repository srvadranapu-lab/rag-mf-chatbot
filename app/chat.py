from rag import generate_answer

while True:
    query = input("\nAsk a question: ")
    if query.lower() == "exit":
        break

    answer = generate_answer(query)
    print("\nAnswer:\n", answer)