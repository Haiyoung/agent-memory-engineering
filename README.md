# 智能体记忆工程 — Agent Memory Engineering

一本关于 Agent Memory 工程的中文技术书籍。

## 内容

- **16 章** 正文 + **附录**（论文索引、术语对照表、工具框架清单）
- **~27 万字**，引用 **170+** 篇学术论文
- **7 个实践章节** 含完整 Python 代码示例
- **50+** Mermaid 架构图

### 章节结构

| 部分 | 章节 | 主题 |
|------|------|------|
| Part I | 第 1-3 章 | 基础与框架 |
| Part II | 第 4-6 章 | 短期记忆层 |
| Part III | 第 7-10 章 | 长期记忆层 |
| Part IV | 第 11-13 章 | 程序性记忆层 |
| Part V | 第 14-16 章 | 治理与前沿 |

## 在线阅读

👉 https://haiyoung.github.io/agent-memory-engineering/（配置后生效）

## 本地构建

```bash
# 安装 mdBook
cargo install mdbook

# 克隆仓库
git clone https://github.com/Haiyoung/agent-memory-engineering.git
cd agent-memory-engineering

# 构建
mdbook build

# 或使用构建脚本
./build.sh build

# 本地预览
./build.sh serve
```

## 许可证

本作品采用 [CC BY-NC 4.0](LICENSE) 许可协议。
