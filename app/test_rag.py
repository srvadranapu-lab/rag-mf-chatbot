from rag import query_rag

query = "What is the expense ratio of HDFC Top 100 Fund?"

results = query_rag(query)

print("\nTop Results:\n")
for r in results:
    print("-", r[:200])