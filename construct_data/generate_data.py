import json
from zhipuai import ZhipuAI
from tqdm import tqdm

# 初始化 DeepSeek 客户端
# client = OpenAI(api_key="sk-038b8bf64d134a5a997603798309bf5e", base_url=""https://dashscope.aliyuncs.com/compatible-mode/v1"")
client = ZhipuAI(api_key="b51d73c926c548769e8b9712be2a23e5.2JXzSfWEYbWmHu97")


# 调用 GLM API 生成问题
def generate_questions(text):
    """
    调用 GLM API 生成与输入文本相关的问题。
    """
    response = client.chat.completions.create(
        model="glm-4-flashx",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user",
             "content": f"生成一个和给定文本相关的提问，以用于检索数据集的构建，之后我们会认为这个文本很可能能作为参考回答该问题，请只生成提问，不要有其他多余语言\n文本：{text}"}
        ],
        stream=False
    )
    res = response.choices[0].message.content
    print('res', res)
    return res


# 读取 all_samples_strings.json 文件
with open('all_samples_strings.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 构造数据对
dataset = []

for sample in tqdm(data['samples']):
    # 生成与当前字符串相关的问题
    question = generate_questions(sample)

    # 构造一个数据对，包含问题和对应的字符串
    dataset_entry = {
        "question": question,
        "answerable_string": sample
    }

    # 将数据条目添加到数据集中
    dataset.append(dataset_entry)

# 保存为 JSON 文件
with open('generated_data_pairs.json', 'w', encoding='utf-8') as f:
    json.dump(dataset, f, ensure_ascii=False, indent=4)

print("Dataset with question-answer pairs has been successfully generated and saved to 'generated_data_pairs.json'.")