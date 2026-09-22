# AI Learning 90 Days 🚀

这是我的 90 天 AI 学习项目。

通过每天完成一个小项目，逐步学习：

Python → 大模型 API → Prompt 工程 → AI 应用开发 → AI Agent

## 项目进度

### Day 1 - Python 入门
完成：
- 第一个 Python 程序
- 基础输入输出


### Day 2 - Python 基础
完成：
- Python 基础语法
- 函数
- 简单程序结构


### Day 3 - 接入大模型 API
完成：
- 阿里云百炼 API 接入
- DeepSeek 模型调用
- 第一个 AI Chat 程序


### Day 4 - Prompt Engineering
完成：
- Prompt 基础设计
- AI角色设定
- 小红书标题生成器


### Day 5 - 多轮对话 ChatBot
完成：
- 对话历史管理
- Context上下文理解
- 多轮AI聊天程序
- 实现连续对话
- 构建基础ChatBot框架


### Day 6 - AI Agent Function Calling
完成：
- Agent 基础结构
- AI 自动判断工具调用
- Function Calling 实现
- 自定义计算工具
- AI + Python 工具协作


### Day 7 - API 基础与 AI API 调用
完成：
- 理解 API 是程序之间沟通的接口
- 理解 Request（请求）与 Response（响应）
- 理解 API Key 与 base_url
- 使用 requests 调用测试 API
- 使用 Python 调用阿里云百炼 API
- 理解 client 与 AI API 的通信过程
- 理解 messages 的 List + Dictionary 结构
- 理解 role / user / assistant / system
- 理解 response.choices[0].message.content
- 实现用户输入问题并获取 AI 回答
- 理解 AI API 的基本数据流


### Day 8 - Structured Output / JSON结构化输出
完成：
- 理解 AI 结构化输出的意义
- 理解 JSON 字符串与 Python Dictionary 的区别
- 使用 json.loads() 将 JSON 字符串转换为 Python Dictionary
- 使用 Dictionary Key 获取 AI 返回的数据
- 使用 List 存储多个数据
- 使用 for 循环遍历 AI 返回的 List
- 实现 AI 美妆产品结构化分析
- 获取产品类型
- 获取目标用户
- 获取产品评分
- 获取产品卖点
- 自动生成小红书选题
- 理解 AI + Python 的结构化数据处理流程


### Day 9 - RAG 检索增强生成
完成：
- 理解 RAG（Retrieval-Augmented Generation）
- 理解 Retrieval（检索）的作用
- 理解企业知识库
- 理解 RAG 基本工作流程
- 使用 Python 模拟知识库
- 实现简单关键词检索
- 理解关键词检索的局限
- 理解语义检索的需求
- 理解 RAG 与最终企业知识工作台的关系


### Day 10 - Embedding 向量表示
完成：
- 理解 Embedding 的基本概念
- 理解文字转换为向量的过程
- 使用阿里云百炼 Embedding API
- 使用 text-embedding-v4 模型
- 成功生成 1024 维 Embedding 向量
- 理解向量与语义相似度
- 使用 Cosine Similarity 比较文本相似度
- 理解 Embedding 在 RAG 中的作用


### Day 11 - 向量数据库与最小 RAG
完成：
- 理解向量数据库的基本概念
- 使用 Chroma 向量数据库
- 创建 Collection
- 向向量数据库添加文档
- 使用 Embedding 生成文档向量
- 使用 text-embedding-v4 生成查询向量
- 将 Embedding 向量存入 Chroma
- 根据查询向量检索相关文档
- 理解 Context（上下文）
- 将检索结果交给大模型
- 实现最小 RAG 问答流程
- 理解 RAG 的完整数据流


### Day 12 - RAG 应用化
完成：
- 将固定问题 RAG Demo 改造成可连续提问的应用
- 使用 while True 实现持续对话
- 使用 break 退出程序
- 实现用户连续输入问题
- 实现每次问题的 Embedding
- 实现向量数据库检索
- 将检索结果作为 Context 提供给大模型
- 显示 AI 回答
- 显示 AI 回答的参考资料
- 测试知识库中不存在的问题
- 理解 RAG 防止模型无依据编造的基本思路
- 完成一个命令行企业知识库问答助手


### Day 13 - FastAPI + RAG
完成：
- 学习 FastAPI 基础
- 创建 GET API
- 使用 query parameter 接收用户问题
- 接入 DeepSeek 大模型
- 接入 Embedding
- 使用 Chroma 向量数据库进行检索
- 将检索结果作为 Context 提供给大模型
- 完成 RAG + FastAPI Web API
- 测试知识库存在和不存在答案的情况
- 理解完整的 RAG 应用数据流


### Day 14 - Document RAG
完成：
- 学习 Python 读取外部文档
- 将文档内容切分成 Chunks
- 使用 Embedding 将 Chunks 转换为向量
- 将向量和文档写入 Chroma
- 实现用户问题 Embedding
- 使用 Chroma 检索相关文档
- 将检索结果作为 Context
- 接入 DeepSeek 生成回答
- 完成外部文档 RAG 流程


### Day 15 - RAG Chunking
完成：
- 理解为什么 RAG 需要进行文档切分
- 理解 Chunk 的概念
- 学习 Chunk Size
- 学习 Chunk Overlap
- 使用 Python 实现固定长度 Chunk
- 理解 Overlap 对上下文连续性的作用
- 理解固定长度切分的局限
- 理解按照章节、段落、句子进行语义切分的思路
- 理解 Chunk 大小需要在语义完整性和检索效果之间进行平衡
- 理解 RAG 文档切分的基本原理





## 技术栈

- Python
- PyCharm
- Git / GitHub
- 阿里云百炼
- DeepSeek API


