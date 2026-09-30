# Judgment Calibration · 判断校准

一个中文优先的 Agent Skill，用于检查具体判断的证据、推断、竞争解释和验证条件。

目标是帮你看清“当前证据能支持到哪一步”，保留有依据的判断，避免附和和机械唱反调。它不是测谎器，不诊断人格，也不保证判断正确。

## 使用

将 `skills/judgment-calibration` 文件夹复制到你的技能目录。Codex 可使用 `~/.agents/skills/`；在部分现有安装中也可使用 `~/.codex/skills/`。只选一个位置，避免同名副本。

显式调用：

```text
使用 $judgment-calibration：我用 AI 做出了软件，所以具备独立开发能力。帮我校准一下。
```

也可自然表达：

```text
我不确定“没人反对就说明大家认可”这个判断对不对，帮我检查一下。
```

当宿主支持自动选择时，自然请求是否选中取决于 Skill 描述与上下文，不能保证每次触发。普通闲聊、单纯表达情绪、创意发散和已决定后的执行请求不应主动进入校准流程。

默认先给简短结论和关键依据；复杂问题或用户要求深入时再展开。它会区分证据不足、推理缺口和明确反证，提供能增强、削弱或仍无法确定结论的观察。

## 示例

输入：“我用 AI 做出了软件，所以具备独立开发能力。”

预期方向：若自述属实，一次成果提供初步证据，但还需了解责任、判断与验收过程。使用 AI 本身不取消能力；验证默认保留实际允许的工具。该示例是说明，不是对任何真实用户能力的判断。

## 验证与限制

见 [EVALUATION.md](EVALUATION.md)。测试使用人工构造输入，不能当成统计准确率、长期效果或跨模型保证。无 Skill 的强模型也能回答很多问题；本项目不声称已证明普遍提升。

`evals/` 包含合成用例和运行器。运行器会调用你本地已登录的 Codex CLI、消耗账号额度，并将结果保存到本地；它不会上传结果或修改技能。先阅读代码，再小批运行。

本仓库不包含 API 密钥、真实聊天、机器配置、原始工具日志或个人进度记录。

## 方法参考

参考了 [CIA 的结构化分析方法](https://www.cia.gov/resources/csi/static/Tradecraft-Primer-apr09.pdf)与现有 [Critical Thinking Skill](https://github.com/tronghieu/agent-skills)、[Agent Thinking Skills](https://github.com/mlevison/agent-thinking-skills)、[Ground Truth](https://github.com/glichtenthal/ground-truth)。这些是方法与设计比较的来源；本 Skill 未直接拼接它们的指令文本。
