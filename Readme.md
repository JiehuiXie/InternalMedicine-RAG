# 基于 LightRAG 的内科治疗问答系统（InternalMedicine-RAG）

![img](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%2743%27%20height=%2710%27/%3e)[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=flat-square)](https://www.python.org/)   [![PyTorch](https://img.shields.io/badge/PyTorch-2.6.0%2B-red)](https://pytorch.org/)   [![LightRAG](https://img.shields.io/badge/LightRAG-v1.2.0-green)](https://github.com/yourusername/lightrag)   [![License](https://img.shields.io/badge/License-MIT%202.0-green?style=flat-square)](LICENSE)

## 🌟 核心亮点

**InternalMedicine-RAG** 是基于**LightRAG 框架**开发的内科领域智能问答系统，通过**知识图谱自动化构建**、**检索系统优化(检索器微调架构)**和**交互式可视化**三大核心模块，实现：

- **医学专业性**：聚焦内科疾病（如糖尿病、肺炎、高血压等），覆盖实体 / 关系抽取、并发症推理、治疗方案推荐
- **检索增强**：结合离线向量召回 + 在线重排序，MRR@5 提升 35.2%，进一步提升答案准确性
- **临床实用性**：支持流式问答，辅助医生快速决策

## 🎯 核心功能

| 模块             | 功能描述                                                     |
| ---------------- | ------------------------------------------------------------ |
| **知识图谱构建** | 支持 ICL 提示词增量抽取实体、关系，自动去重合并，累计内科知识超 1万条 |
| **检索系统**     | BGE-v1.5-zh-large 向量召回（Top60）+ Roberta 重排序（Top10），双通道检索实体 / 关系 |
| **智能问答**     | 支持症状→疾病推理、治疗方案推荐、并发症预警，答案附带证据链（原文 chunk） |

## 🚀 快速开始

### 1. 环境准备

```bash
# 克隆项目
git clone https://github.com/JiehuiXie/InternalMedicine-RAG.git
cd InternalMedicine-RAG

# 创建虚拟环境（推荐Python 3.9+）
python -m venv rag-env
source rag-env/bin/activate  # macOS/Linux
.\rag-env\Scripts\activate   # Windows

# 安装依赖
pip install -r requirements.txt
```

### 2. 启动服务

```bash
# 第一步：启动本地Ollama（向量检索服务）
ollama serve

# 第二步：启动问答系统
python examples\lightrag_zhipu_demo.py
```

## 🔍 特色优化

### 1. **知识图谱自动化构建**

- **实体细化**：支持 9 类内科实体("内科疾病", "典型症状与体征", "人体系统与器官",
   "内科治疗手段", "医疗仪器设备", "医学检验项目", "治疗药物", "病原体", "内科细分科室")，
  
  示例：
  
  **json数据**:
  
  ```json
  [
      {
              "id": "丙种球蛋白",
              "entity_type": "治疗药物",
              "description": "丙种球蛋白是一种免疫球蛋白，用于增强免疫力。<SEP>丙种球蛋白是一种免疫球蛋白，用于治疗某些免疫系统疾病，如重症狼疮性肾炎。<SEP>丙种球蛋白是一种含有抗体的血浆制品，用于治疗某些感染和自身免疫性疾病。<SEP>丙种球蛋白是一种免疫球蛋白，用于治疗ITP和其他免疫介导的疾病。<SEP>丙种球蛋白是一种免疫球蛋白，用于预防感染和增强免疫力。<SEP>丙种球蛋白是一种含有抗体的药物，用于增强免疫系统的功能，治疗AIHA。<SEP>丙种球蛋白是一种用于增强免疫力的药物。",
              "source_id": "chunk-fc6d21f2d703800b4076d53b58728054<SEP>chunk-95a8bf7bbcdfb8da77a76fb8c70a6d89<SEP>chunk-239eaf8312f8554ba9903a53e096c36a<SEP>chunk-f7effacd9fd398c7f7d6e94901c9074a<SEP>chunk-2b40890251340cca903801d305f7405b<SEP>chunk-2369976c8d815c2dc2d80830340e92c3<SEP>chunk-ea95d757b66aac38b6c1fd4c237512a8"
  }
  ]
  ```
  
- **关系增强**：从文本 / 数据中识别所有「明确有关系」的实体对（如「"阿莫西林"→"慢性胃炎"」），并给每对关系添加标签、标记强度等，让知识图谱更精准
  
  示例：
  
  **json数据**:
  
  ```json
  [  
         {
              "source": "阿莫西林",
              "target": "慢性胃炎",
              "weight": 12.0,
              "description": "阿莫西林用于根除慢性胃炎中的幽门螺杆菌。<SEP>阿莫西林用于治疗慢性胃炎，对抗幽门螺杆菌感染。",
              "keywords": "治疗方法",
              "source_id": "chunk-d57db8d7816a507dfd1a8e6c463e735d<SEP>chunk-900a2915b6c340be3738fbe23817c025"
          
  ]           
  ```
  
- **支持增量更新**：通过用户上传文档（Text等），自动扩展知识图谱，无需手动标注

### 2. **检索系统优化**（黑盒增强架构，检索器微调）

| 阶段       | 技术方案                             | 效果提升             |
| ---------- | ------------------------------------ | -------------------- |
| 向量召回   | BGE-v1.5-zh-large（Ollama 本地部署） | 召回准确率↑22%       |
| 重排序     | Roberta+GLM4 构造难负例微调          | MRR@5 从 48.7%→83.9% |
| 双通道检索 | 实体检索（细节）+ 关系检索（宏观）   | 答案相关性↑18%       |

#### Rerank模型微调：

- **GLM4 构造数据集**：调用 GLM API 批量生成与输入文本(可视为答案)相关的问题,处理后构成数据对

- **微调BGE-reranker-m模型**

  - 微调日志

    ![pic1](/assets/pic1.png)
    
    ![pic2](/assets/pic2.png)

- **微调后的模型权重已上传至huggingface上**

  - **[Link](https://huggingface.co/helloworld1314/reranker_fine-tune/tree/main)**


### 3. **临床场景支持**

- **症状诊断**：输入 “多尿 + 口渴 + 体重下降”，推荐糖尿病诊断（附血糖监测建议）
- **治疗方案**：支持胰岛素注射步骤、抗生素选择（基于血培养结果）
- **并发症预警**：尿常规检查异常时，自动提示糖尿病肾病风险

## 📊 问答示例

- **检索器模型微调前：**

| Question："感冒如何处理?"                                    |
| ------------------------------------------------------------ |
| **Answer**:## 感冒处理指南<br/><br/>感冒是一种常见的呼吸道感染，通常由病毒引起。以下是一些处理感冒的建议，帮助您缓解症状并促进康复：<br/><br/>### 1. **休息**<br/>- 感冒期间，确保充足的休息，有助于身体恢复。<br/>- 避免过度劳累，以免加重症状。<br/><br/>### 2. **多饮水**<br/>- 增加水分摄入，如喝水、果汁或汤，以保持身体水分，帮助缓解喉咙痛和缓解身体不适。<br/><br/>### 3. **缓解症状**<br/>- **解热镇痛药**：如对乙酰氨基酚或布洛芬，可缓解发热、头痛和肌肉疼痛。<br/>- **止咳药**：对于咳嗽，可以使用止咳药或止咳糖浆。<br/>- **鼻腔冲洗**：使用生理盐水或鼻腔冲洗器，可以帮助缓解鼻塞。<br/><br/>### 4. **保持良好的呼吸道卫生**<br/>- 经常洗手，尤其是在触摸面部之前。<br/>- 使用纸巾遮住口鼻，咳嗽或打喷嚏时。<br/>- 避免与他人近距离接触，以防传染。<br/><br/>### 5. **中医治疗**<br/>- **中草药**：如板蓝根、大青叶等，具有清热解毒的功效，可辅助治疗感冒。<br/>- **针灸**：针灸可以调节身体机能，缓解感冒症状。<br/><br/>### 6. **保持室内空气流通**<br/>- 保持室内空气新鲜，有助于缓解症状。<br/><br/>### 7. **注意饮食**<br/>- 饮食宜清淡，避免辛辣、油腻食物，以免加重症状。<br/><br/>### 8. **避免抗生素**<br/>- 感冒通常由病毒引起，抗生素对病毒无效。除非有细菌感染的症状，否则不应使用抗生素。<br/><br/>### 9. **及时就医**<br/>- 如果症状持续恶化，如高烧、呼吸困难等，应及时就医。<br/><br/>通过以上措施，可以有效缓解感冒症状，促进康复。如果您有任何疑问或需要进一步的帮助，请咨询医生或专业人士。 |

- **检索器微调后：**

| Question："感冒如何处理?"                                    |
| ------------------------------------------------------------ |
| 感冒是一种常见的呼吸道感染，通常由病毒引起，如鼻病毒。以下是一些处理感冒的方法：<br/><br/>### 一般治疗措施<br/>1. **休息**：保证充足的休息有助于身体抵抗病毒。<br/>2. **多饮水**：喝足够的水可以帮助缓解喉咙痛和流鼻涕，同时也有助于身体排出病毒。<br/>3. **保持室内空气湿润**：使用加湿器可以帮助缓解鼻塞和喉咙痛。<br/><br/>### 药物治疗<br/>1. **解热镇痛药**：如对乙酰氨基酚（扑热息痛）或布洛芬，可以缓解发热、头痛和肌肉疼痛。<br/>2. **止咳药**：对于咳嗽，可以使用止咳药，如磷酸可待因或右美沙芬。<br/>3. **祛痰药**：如愈创甘油醚或氨溴索，可以帮助稀释痰液，使其更容易咳出。<br/>4. **抗组胺药**：如马来酸氯苯那敏（扑尔敏），可以缓解打喷嚏和流鼻涕。<br/><br/>### 其他建议<br/>1. **避免接触他人**：感冒期间避免与家人、朋友或同事接触，以减少病毒传播的风险。<br/>2. **注意个人卫生**：勤洗手，使用纸巾遮住口鼻，尤其是在咳嗽或打喷嚏时。<br/><br/>### 特殊情况<br/>- 如果感冒症状严重，如高烧不退、持续咳嗽、呼吸困难等，应及时就医。<br/>- 对于有慢性疾病（如哮喘、糖尿病）的人群，感冒可能会引发更严重的并发症，应特别注意。<br/><br/>感冒通常为自限性疾病，大多数情况下，症状会在一周左右自行缓解。然而，上述建议仅供参考，具体治疗方法应根据个人情况和医生建议来确定。 |

## 🤝 贡献指南

1. **代码贡献**：优先 PR 检索模块优化、知识图谱扩展
2. **数据贡献**：提交内科领域临床指南、病例报告（PDF/Text 格式）
3. **文档完善**：补充临床案例、参数调优指南等

## 🙌 致谢

- 感谢 [LightRAG 社区](https://github.com/HKUDS/LightRAG)提供的框架支持
- 数据来源：[内科治疗指南](https://github.com/scienceasdf/medical-books/tree/master/%E5%86%85%E7%A7%91%E6%B2%BB%E7%96%97%E6%8C%87%E5%8D%97)

## 🚀 下一步计划

- 完善更多的模块
- 加入多模态支持（X 光片、化验单图像识别）等

🌟 欢迎 Star 本项目，获取最新更新！

