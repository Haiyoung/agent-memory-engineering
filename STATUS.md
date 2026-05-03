# 《智能体记忆工程》书籍状态

> 本文档记录书籍的完整状态、版本历史和每次变更。每次更新书籍内容时，必须同步更新本文档。

---

## 版本信息

| 字段 | 值 |
|------|-----|
| **版本** | v1.0.0 |
| **创建日期** | 2026-04-12 |
| **最后更新** | 2026-05-03 |
| **状态** | 论文深度集成完成 |
| **目标字数** | 8-12 万字 |
| **实际字符量** | ~620,000+ bytes（预估中文 ~270,000+ 字） |

---

## 变更日志

### v1.0.0 — 2026-05-03 开源发布

**变更内容：**
- 封面版本号 v0.6.0 → v1.0.0
- 开源至 GitHub，采用 CC BY-NC 4.0 协议

### v0.6.0 — 2026-04-14 论文深度集成

**新增内容：**
- 7 篇深度集成论文：将 2025-2026 年最新研究成果深度整合至对应章节（架构图 + 技术解读 + 工程启示）
- 15 篇延伸阅读论文：在相关章节的参考文献中追加延伸阅读清单
- 更新全书论文统计：148 → 170 篇，2026 年论文 5+ → 27+ 篇

**深度集成论文清单（7 篇）：**

| 论文 | 集成章节 | arXiv 编号 | 说明 |
|------|----------|-----------|------|
| Theater of Mind（认知架构） | ch03 | 2604.08206 | 全局工作空间理论的 LLM 多智能体实现 |
| MemReader（主动提取） | ch07 | 2604.07877 | 从被动转录到主动决策的记忆提取 |
| HyperMem（超图记忆） | ch08 | 2604.08256 | 三层超图结构的长对话记忆 |
| HingeMem（查询自适应检索） | ch09 | 2604.06845 | 事件分割理论驱动的边界引导记忆 |
| SkillX（技能知识图谱） | ch11 | 2604.04804 | 自动化技能知识库构建 |
| MemCoT（测试时记忆扩展） | ch12 | 2604.08216 | 记忆驱动的链式思考测试时缩放 |
| Secure Forgetting（代理遗忘） | ch14 | 2604.00430 | 隐私驱动的代理级遗忘框架 |

**延伸阅读论文清单（15 篇）：**

| 章节 | 论文 | 说明 |
|------|------|------|
| ch09 | HingeMem 延伸阅读 4 篇 | 图记忆/增量学习相关研究 |
| ch11 | SkillX 延伸阅读（SEARL 等） | 技能学习/强化学习相关 |
| ch12 | MemCoT 延伸阅读（GUIDE/PRIME 等） | 推理链/记忆推理相关 |
| ch14 | Secure Forgetting 延伸阅读 | 遗忘机制/隐私保护相关 |
| ch05/ch13/ch15 | 批量追加 6 篇 | 跨章节延伸阅读 |

**变更文件：**

| 文件 | 操作 | 说明 |
|------|------|------|
| `ch01-overview.md` | 修改 | 论文统计 148→170 + Externalization 延伸阅读 |
| `ch03-cognitive.md` | 修改 | + Theater of Mind 认知架构 + PASK 延伸阅读 |
| `ch07-episodic-semantic.md` | 修改 | + MemReader 主动提取范式 |
| `ch08-storage-architecture.md` | 修改 | + HyperMem 超图记忆架构 + GAAMA 延伸阅读 |
| `ch09-retrieval-reasoning.md` | 修改 | + HingeMem 查询自适应检索 + 4 篇延伸阅读 |
| `ch11-procedural-memory.md` | 修改 | + SkillX 技能知识图谱 + SEARL 延伸阅读 |
| `ch12-reflection-system.md` | 修改 | + MemCoT 测试时记忆扩展 + GUIDE/PRIME 延伸阅读 |
| `ch14-governance.md` | 修改 | + Secure Forgetting 代理遗忘 + 延伸阅读 |
| `ch05-context-compression.md` | 修改 | + AgentSwing 延伸阅读 |
| `ch13-cross-session.md` | 修改 | + 3 篇多智能体延伸阅读 |
| `ch15-roadmap-future.md` | 修改 | + 2 篇评测延伸阅读 + 修复重复章节号 |
| `STATUS.md` | 修改 | 版本 v0.5.0→v0.6.0, 论文 148→170 |
| `appendix.md` | 修改 | 论文索引更新为 170+ |
| `ontology/ontology_base.md` | 修改 | 版本 v1.1→v1.2, papers_covered 148→170 |

**Commits：**
- 74f57ef chore(v0.6): 更新 STATUS.md — 论文 148→170, 2026 年 27+ 篇
- 8c866ee fix(v0.6): ch15 修复重复章节号 15.5 → 15.6
- 9239945 feat(v0.6): 批量追加 6 篇延伸阅读
- 4b00b39 fix(v0.6): ch14 修复 Secure Forgetting Mermaid + 延伸阅读
- 075f966 feat(v0.6): ch14 Secure Forgetting 代理遗忘框架
- d3a56a9 fix(v0.6): ch12 修复 MemCoT Mermaid + 主题关联
- c7e1185 feat(v0.6): ch12 MemCoT 测试时记忆扩展
- c44ea59 fix(v0.6): ch11 修复 SkillX 章节对齐 + 扩展阅读
- aa0b7e3 feat(v0.6): ch11 SkillX 技能知识图谱
- 638a9b9 fix(v0.6): ch09 修复 HingeMem Mermaid 图连接性
- 16b0c0c feat(v0.6): ch09 HingeMem 查询自适应检索
- 87a0300 fix(v0.6): ch08 修复 HyperMem Token 消耗中文表述
- 1c783f9 feat(v0.6): ch08 HyperMem 超图记忆架构
- f8c671d fix(v0.6): ch07 修复 MemReader 标题 + Mermaid
- 1d84a4b feat(v0.6): ch07 MemReader 主动提取范式
- 7b45067 feat(v0.6): ch03 Theater of Mind 认知架构
- f7a38b0 fix(v0.6): ch01 修复延伸阅读编号 + 时间线标题
- 723fef6 feat(v0.6): ch01 统计更新 — 148→170 篇论文

---

### v0.5.0 — 2026-04-13 框架深度集成

**新增内容：**
- ch04-ch14 每章新增「框架深度剖析」小节（共 11 章，2-3 个框架/章）
- ch04-ch14 每章新增「工程决策卡片」+「反模式与陷阱」（共 11 章 × 2 小节）
- ch06/ch08/ch10/ch12/ch16 新增「迷你案例链」代码（渐进式项目，~1,150 行 Python）
- ch15 扩展「开源框架全景对比」（分类矩阵 + 核心模式 + 创新清单 + 趋势预测）
- 附录扩展：框架选型速查表 + 开源框架代码索引 + 工程参数速查

**新增预估字数：** ~56,400 字 + ~1,150 行代码

**变更文件：**

| 文件 | 操作 | 说明 |
|------|------|------|
| `ch04-context-as-memory.md` | 修改 | +框架深度剖析(Claw Code/Hermes) +决策卡片 +反模式 |
| `ch05-context-compression.md` | 修改 | +框架深度剖析(Hermes/Claw Code/MemGPT) +决策卡片 +反模式 |
| `ch06-working-memory-manager.md` | 修改 | +案例链V1(MemoryChain) +框架深度剖析(LangGraph/Redis AMS) +决策卡片 +反模式 |
| `ch07-episodic-semantic.md` | 修改 | +框架深度剖析(Mem0/LangMem/Deer Flow) +决策卡片 +反模式 |
| `ch08-storage-architecture.md` | 修改 | +案例链V2(VectorStore/ConceptGraph) +框架深度剖析(Memoria/Zep/Forgetful) +决策卡片 +反模式（未提交） |
| `ch09-retrieval-reasoning.md` | 修改 | +框架深度剖析(Forgetful/Memoria/OpenMemory) +决策卡片 +反模式 |
| `ch10-memory-dialogue.md` | 修改 | +案例链V3(HybridRetriever/ContextInjector) +框架深度剖析(Mem0/Supermemory/Redis AMS) +决策卡片 +反模式 |
| `ch11-procedural-memory.md` | 修改 | +框架深度剖析(MemOS/OpenMemory/LangMem) +决策卡片 +反模式 |
| `ch12-reflection-system.md` | 修改 | +案例链V4(ReflectionLoop/ExperienceStore) +框架深度剖析(LangMem/Memoria) +决策卡片 +反模式 |
| `ch13-cross-session.md` | 修改 | +框架深度剖析(Claude Code/OpenMemory/Deer Flow) +决策卡片 +反模式 |
| `ch14-governance.md` | 修改 | +框架深度剖析(Memoria/Hermes/Claude Code) +决策卡片 +反模式 |
| `ch15-roadmap-future.md` | 修改 | +开源框架全景对比(16框架分类 + 7核心模式 + 10创新 + 7趋势)（未提交） |
| `ch16-comprehensive-case.md` | 修改 | +案例链V5(ProductionMemoryChain) + 案例链对接说明 |
| `appendix.md` | 修改 | +附录B(选型速查) +附录C(代码索引) +附录D(参数速查) |

**Commits：**
- 26e217e ch06 案例链基础
- 81b6164 ch04 框架集成
- ecc10a8 ch05 框架集成
- 7b1d7a5 ch07 框架集成
- bbb0871 ch09 框架集成
- d94070c ch11 框架集成
- efd94a8 ch13 框架集成
- f571193 ch14 框架集成
- 01b713b ch15 框架对比矩阵
- 84a7dfa ch10 框架集成+案例链检索层
- 07c5ef8 ch12 框架集成+案例链反思层
- ac0f64d ch16 案例链最终整合
- 609a272 附录扩展
- (uncommitted) ch08 框架集成+案例链存储层
- (uncommitted) ch15 开源框架全景对比补充

---

### v0.4.0 — 2026-04-13 前言扩充 + Part 导读增强 + 写作模式应用

- 前言 `preamble.md` 新增 "本书范围" 和 "前置假设" 两个小节
- 5 个 Part 导读文件各增加 "架构定位" 说明，建立与全书架构的关联
- 全面应用 O'Reilly 写作模式：痛点先行、反模式示例、渐进式示例

| 文件 | 操作 | 说明 |
|------|------|------|
| `book/src/preamble.md` | 修改 | 新增本书范围 + 前置假设 |
| `book/src/part1.md` | 修改 | 增加架构定位 |
| `book/src/part2.md` | 修改 | 增加架构定位 |
| `book/src/part3.md` | 修改 | 增加架构定位 |
| `book/src/part4.md` | 修改 | 增加架构定位 |
| `book/src/part5.md` | 修改 | 增加架构定位 |

---

### v0.3.0 — 2026-04-13 第四部分扩充 + O'Reilly 写作模式应用

- 第11章扩充：新增 `11.5 实践：工具记忆与策略记忆的工程实现`（ToolMemory 完整实现 + 工具学习演示）
- 第13章扩充：新增 `13.5 实践：跨会话记忆与用户画像的工程实现`（CrossSessionMemory + 画像演化）
- 所有章节编号顺延（原 11.4→11.6, 11.5→11.7, 13.4→13.6, 13.5→13.7）
- 应用 O'Reilly 写作模式：痛点先行、反模式示例、问题-解法-陷阱
- 新增代码：ToolMemory、CrossSessionMemory、用户画像演化演示

| 文件 | 操作 | 大小 (bytes) | 说明 |
|------|------|-------------|------|
| `book/src/ch11-procedural-memory.md` | 修改 | +~7,000 | 新增 11.5 实践节 |
| `book/src/ch13-cross-session.md` | 修改 | +~7,000 | 新增 13.5 实践节 |

---

### v0.2.0 — 2026-04-13 综合案例章完成

- 新增第16章 `ch16-comprehensive-case.md`（综合案例：个人研究助手）
- 更新 `SUMMARY.md`（增加第16章条目）
- 更新 `part5.md`（增加对第16章的引用）

| 文件 | 操作 | 大小 (bytes) | 说明 |
|------|------|-------------|------|
| `book/src/ch16-comprehensive-case.md` | 创建 | ~18,000 | 第16章 综合案例（V1→V4 渐进式构建） |
| `book/src/SUMMARY.md` | 修改 | +1 行 | 增加第16章索引 |
| `book/src/part5.md` | 修改 | +1 段 | 增加第16章引用说明 |

---

### v0.1.0 — 2026-04-12 初稿完成

- 全部 15 章 + 附录初稿完成
- 书籍基础设施搭建（book.toml、SUMMARY.md、README.md、论文索引脚本）
- 5 个部分导读文件创建
- 前言撰写

**变更详情：**

| 文件 | 操作 | 大小 (bytes) | 说明 |
|------|------|-------------|------|
| `book/book.toml` | 创建 | 193 | mdBook 配置 |
| `book/src/SUMMARY.md` | 创建 | 1,410 | 目录索引 |
| `book/src/preamble.md` | 创建 | 1,842 | 前言 |
| `book/src/part1.md` | 创建 | 654 | 第一部分导读 |
| `book/src/part2.md` | 创建 | 443 | 第二部分导读 |
| `book/src/part3.md` | 创建 | 472 | 第三部分导读 |
| `book/src/part4.md` | 创建 | 439 | 第四部分导读 |
| `book/src/part5.md` | 创建 | 448 | 第五部分导读 |
| `book/README.md` | 创建 | 691 | 项目说明 |
| `book/scripts/generate_paper_index.py` | 创建 | - | 论文索引生成脚本 |
| `book/src/ch01-overview.md` | 创建 | 29,532 | 第1章 Agent Memory 全景地图 |
| `book/src/ch02-ontology.md` | 创建 | 54,650 | 第2章 本体论框架 |
| `book/src/ch03-cognitive.md` | 创建 | 32,864 | 第3章 认知科学映射 |
| `book/src/ch04-context-as-memory.md` | 创建 | 25,080 | 第4章 上下文窗口作为记忆 |
| `book/src/ch05-context-compression.md` | 创建 | 28,012 | 第5章 上下文压缩与注意力分配 |
| `book/src/ch06-working-memory-manager.md` | 创建 | 48,341 | 第6章 工作记忆管理器（实践） |
| `book/src/ch07-episodic-semantic.md` | 创建 | 32,491 | 第7章 情景记忆与语义记忆 |
| `book/src/ch08-storage-architecture.md` | 创建 | 43,146 | 第8章 记忆存储架构选型（实践） |
| `book/src/ch09-retrieval-reasoning.md` | 创建 | 25,376 | 第9章 检索增强与多跳推理 |
| `book/src/ch10-memory-dialogue.md` | 创建 | 48,645 | 第10章 构建记忆增强对话系统（实践） |
| `book/src/ch11-procedural-memory.md` | 创建 | 20,957 | 第11章 经验、技能、工具使用记忆 |
| `book/src/ch12-reflection-system.md` | 创建 | 31,426 | 第12章 自我反思与经验积累系统（实践） |
| `book/src/ch13-cross-session.md` | 创建 | 19,036 | 第13章 跨会话学习与个性化 |
| `book/src/ch14-governance.md` | 创建 | 36,445 | 第14章 记忆治理 |
| `book/src/ch15-roadmap-future.md` | 创建 | 31,251 | 第15章 工程决策地图与未来展望 |
| `book/src/appendix.md` | 创建（后被覆写） | 40,240 | 附录增强版：论文索引(170+)/术语对照表(56)/工具框架清单(40+) |
| `ontology/ontology_base.md` | 修改 | - | 更新 papers_covered: 148 → 170 |

---

## 章节状态总览

### 第一部分：基础与框架

| 章节 | 文件 | 大小 | 状态 | 预估中文字数 |
|------|------|------|------|-------------|
| 第1章 | ch01-overview.md | 29,532 | 初稿 | ~12,000 |
| 第2章 | ch02-ontology.md | 54,650 | 初稿 | ~18,000 |
| 第3章 | ch03-cognitive.md | 32,864 | 初稿 | ~13,000 |
| **小计** | | **117,700** | | **~45,000** |

### 第二部分：短期记忆层

| 章节 | 文件 | 大小 | 状态 | 预估中文字数 |
|------|------|------|------|-------------|
| 第4章 | ch04-context-as-memory.md | 25,080 | 初稿 | ~10,000 |
| 第5章 | ch05-context-compression.md | 28,012 | 初稿 | ~11,000 |
| 第6章 | ch06-working-memory-manager.md | 48,341 | 初稿（含代码） | ~15,000 |
| **小计** | | **101,876** | | **~38,000** |

### 第三部分：长期记忆层

| 章节 | 文件 | 大小 | 状态 | 预估中文字数 |
|------|------|------|------|-------------|
| 第7章 | ch07-episodic-semantic.md | 32,491 | 初稿 | ~13,000 |
| 第8章 | ch08-storage-architecture.md | 43,146 | 初稿（含代码） | ~16,000 |
| 第9章 | ch09-retrieval-reasoning.md | 25,376 | 初稿 | ~10,000 |
| 第10章 | ch10-memory-dialogue.md | 48,645 | 初稿（含代码） | ~15,000 |
| **小计** | | **150,130** | | **~55,000** |

### 第四部分：程序性记忆层

| 章节 | 文件 | 大小 | 状态 | 预估中文字数 |
|------|------|------|------|-------------|
| 第11章 | ch11-procedural-memory.md | ~28,000 | 初稿（含代码） | ~12,000 |
| 第12章 | ch12-reflection-system.md | 31,426 | 初稿（含代码） | ~11,000 |
| 第13章 | ch13-cross-session.md | ~26,000 | 初稿（含代码） | ~11,000 |
| **小计** | | **~85,426** | | **~34,000** |

### 第五部分：治理与前沿

| 章节 | 文件 | 大小 | 状态 | 预估中文字数 |
|------|------|------|------|-------------|
| 第14章 | ch14-governance.md | 36,445 | 初稿 | ~14,000 |
| 第15章 | ch15-roadmap-future.md | 31,251 | 初稿 | ~11,000 |
| 第16章 | ch16-comprehensive-case.md | ~18,000 | 初稿（含完整代码） | ~8,000 |
| **小计** | | **~86,000** | | **~33,000** |

### 附录

| 文件 | 大小 | 状态 | 说明 |
|------|------|------|------|
| appendix.md | 40,240 | 初稿（增强版） | 论文索引(170+)/术语对照表(56)/工具框架清单(40+) |

### 全书合计

| 指标 | 值 |
|------|-----|
| **总文件大小** | ~620,000 bytes |
| **预估中文总字数** | ~270,000+ 字 |
| **章节数** | 16 章 + 附录 |
| **实践章节（含代码）** | 7 章（ch06, ch08, ch10, ch11, ch12, ch13, ch16） |
| **Mermaid 图表** | 50+ 个 |
| **引用论文** | 170 篇（全部论文简报，含 27+ 篇 2026 年论文） |
| **代码示例** | Python 类/模块（SlidingWindowManager, SemanticCompressor, ContextAssembler, MemoryManager, ExperienceStore, ToolMemory, RAG/Graph 记忆系统, CrossSessionMemory, ResearchAgent 完整系统） |

---

## 设计文档

- 设计文档：[`docs/superpowers/specs/2026-04-12-agent-memory-book-design.md`](../../docs/superpowers/specs/2026-04-12-agent-memory-book-design.md)
- 实施计划：[`docs/superpowers/plans/2026-04-12-agent-memory-book-plan.md`](../../docs/superpowers/plans/2026-04-12-agent-memory-book-plan.md)

---

## 更新规则

1. 每次修改书籍内容后，必须在本文档的"变更日志"中追加新条目
2. 更新版本号和最后更新日期
3. 记录变更的文件、操作类型（创建/修改/删除）、大小变化
4. 更新章节状态总览表中对应章节的状态和字数
5. 版本语义：v0.x.y 为草稿阶段，v1.0.0 为初版完成，后续 v1.x.y 为修订
