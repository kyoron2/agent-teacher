# 短期记忆 (Short-term Memory)

> 此文件由 Agent 在教学过程中自动维护，记录当前教学步骤的细节。
> 当一个教学阶段完成后，关键内容归档到长期记忆，此文件清空重写。

## 当前状态

**阶段**：全部完成（讨论 Rule 优化中）
**上一步操作**：完成了对 PyInstaller 原理、指令集、spec 文件、工具对比的深入讲解

## 最近遇到的错误及解决方案

| 错误 | 原因 | 解决方案 |
|:-----|:-----|:---------|
| `ModuleNotFoundError: rich._unicode_data.unicode17-0-0` | Python 3.13 太新，rich 的 Unicode 数据文件使用动态加载，PyInstaller 静态分析无法检测到 | 在 spec 文件中使用 `collect_all('rich')` 强制收集所有文件 |
| 打包成功但 dist 目录下没有 exe | spec 文件中缺少 `PYZ()` 和 `EXE()` 部分，只有 `Analysis()` | 补全完整的 spec 文件结构（Analysis → PYZ → EXE） |

## 关键发现

- Python 3.13.3 + rich 的组合在 PyInstaller 中需要 `collect_all` 才能正常工作
- FastAPI 打包时需要同时 collect_all: rich, uvicorn, fastapi, starlette 四个包
- uvicorn 在 exe 中运行时必须 reload=False, workers=1

## 学生偏好

.eg 使用 uv 管理 Python 环境（而非 venv + pip）
- 希望详细解释每条命令和配置，不要跳过
- 对"为什么这样做"比"怎么做"更感兴趣
