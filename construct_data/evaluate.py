from FlagEmbedding import FlagReranker
import json
from tqdm import tqdm

# 初始化 reranker
reranker = FlagReranker(r'F:\CODE\项目2\project2\LightRAG\BAAI\bge-reranker-v2-m3', use_fp16=True)

# 读取 test_data.json 文件
with open('test_data.json', 'r', encoding='utf-8') as f:
    test_data = json.load(f)


# 计算 MRR@5
def calculate_mrr_at_5(test_data, reranker):
    mrr_sum = 0
    total_queries = len(test_data)

    for query_data in tqdm(test_data):
        query = query_data['query']
        relevant_docs = query_data['pos']  # 正样本
        all_docs = relevant_docs + query_data['neg']  # 正负样本合并，总共 11 个文档

        # 计算每个文档的得分
        scores = [reranker.compute_score([query, doc], normalize=True) for doc in all_docs]

        # 按得分排序，获取排名
        ranked_docs = sorted(zip(all_docs, scores), key=lambda x: x[1], reverse=True)

        # 找到第一个相关文档的排名（前 5 个文档中）
        rank = -1
        for idx, (doc, score) in enumerate(ranked_docs[:5]):  # 只考虑前 5 个文档
            if doc in relevant_docs:
                rank = idx + 1  # 排名从 1 开始
                break

        if rank != -1:
            mrr_sum += 1 / rank  # 如果找到了相关文档，则加上倒数排名

    mrr_at_5 = mrr_sum / total_queries
    return mrr_at_5


# 计算 MRR@5
mrr_at_5 = calculate_mrr_at_5(test_data, reranker)

# 输出 MRR@5
print(f"MRR@5: {mrr_at_5:.4f}")
