---
name: teaching-protocol
description: 以状态机协议执行 AI 导学流程，防止跳过基础讲解、流程越级和长对话失忆。用于编程教学、导师式对话、学习路径推进场景；当需要流程守卫、记忆压缩、阶段化推进时触发。
---

# Teaching Protocol Skill

按以下顺序执行，不要跳步。

## 1. 读取协议与记忆

1. 读取 `references/protocol-schema.md`
2. 读取 `.agent/teaching/long_term_memory.md`
3. 读取 `.agent/teaching/short_term_memory.md`
4. 读取 `.agent/teaching/session_memory.md`

## 2. 生成教学回复草稿

1. 在回复顶部输出：
   - `STATE=<当前状态>`
   - `NEXT=<下一状态>`
   - `GOAL=<一句话目标>`
2. 只允许合法状态跳转。
3. 若 `NEXT=ACTION`，先满足基础讲解与理解确认闸门。

## 3. 运行流程守卫

执行：

```powershell
powershell -ExecutionPolicy Bypass -File .agent\skills\teaching-protocol\scripts\flow-guard.ps1 -ReplyFile <reply_file>
```

规则：

1. 输出 `pass=true` 才允许发送回复。
2. `pass=false` 必须按错误码重写，不得直接发送。

## 4. 发送后压缩记忆

执行：

```powershell
powershell -ExecutionPolicy Bypass -File .agent\skills\teaching-protocol\scripts\memory-compactor.ps1 -Mode round
```

规则：

1. 每轮结束运行 `round`。
2. 阶段完成时运行 `stage_complete`。

## 5. 错误恢复

1. 出现 `STATE_JUMP`：回退到上一个合法状态重写。
2. 出现 `MISS_BASICS` 或 `SKIP_CHECK`：强制回 `EXPLAIN`。
3. 出现记忆文件缺失：先创建空模板再继续。
