from lightrag.llm.ollama import ollama_embedding
texts = ["测试文本"]
embeddings = ollama_embedding(texts, embed_model="quentinz/bge-large-zh-v1.5:latest", host="http://localhost:11434")
print(f"嵌入向量的形状: {embeddings[0].shape}")