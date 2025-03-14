import os
import logging


from lightrag import LightRAG, QueryParam
from lightrag.llm.zhipu import zhipu_complete, zhipu_embedding
from lightrag.llm.ollama import ollama_embedding
from lightrag.utils import EmbeddingFunc

WORKING_DIR = "./dickens"

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)

if not os.path.exists(WORKING_DIR):
    os.mkdir(WORKING_DIR)



api_key = "b51d73c926c548769e8b9712be2a23e5.2JXzSfWEYbWmHu97"
if api_key is None:
    raise Exception("Please set ZHIPU_API_KEY in your environment")


rag = LightRAG(
    working_dir=WORKING_DIR,
    llm_model_func=zhipu_complete,
    llm_model_name="glm-4-plus",  # Using the most cost/performance balance model, but you can change it here.
    llm_model_max_async=4,
    chunk_token_size=1024,
    llm_model_max_token_size=32768,
    embedding_func=EmbeddingFunc(
        embedding_dim=1024,  # Zhipu embedding-3 dimension
        max_token_size=4000,
        func=lambda texts: ollama_embedding(
            texts,embed_model="quentinz/bge-large-zh-v1.5:latest",host="http://localhost:11434"),
    ),
)

# with open("docs/chap01.txt", "r", encoding="utf-8") as f:
#     rag.insert(f.read())
# with open("docs/chap02.txt", "r", encoding="utf-8") as f:
#     rag.insert(f.read())
# with open("docs/chap03.txt", "r", encoding="utf-8") as f:
#     rag.insert(f.read())
# with open("docs/chap04.txt", "r", encoding="utf-8") as f:
#     rag.insert(f.read())
# with open("docs/chap05.txt", "r", encoding="utf-8") as f:
#     rag.insert(f.read())

# ------------------------------------检索模式选择------------------------------------------ #

# # Perform naive search
# print(
#     rag.query("What are the top themes in this story?", param=QueryParam(mode="naive"))
# )
#
# # Perform local search
# print(
#     rag.query("What are the top themes in this story?", param=QueryParam(mode="local"))
# )
#
# # Perform global search
# print(
#     rag.query("What are the top themes in this story?", param=QueryParam(mode="global"))
# )

# Perform hybrid search
print(
    rag.query("感冒如何处理？", param=QueryParam(mode="hybrid"))
)
