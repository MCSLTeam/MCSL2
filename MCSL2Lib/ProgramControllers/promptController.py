#     Copyright 2024, MCSL Team, mailto:services@mcsl.com.cn
#
#     Part of "MCSL2", a simple and multifunctional Minecraft server launcher.
#
#     Licensed under the GNU General Public License, Version 3.0, with our
#     additional agreements. (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#        https://github.com/MCSLTeam/MCSL2/raw/master/LICENSE
#
################################################################################
"""
Server Analyzer Prompt
"""
from MCSL2Lib.ProgramControllers.settingsController import cfg


HARD_AI_ANALYZE_PROMPT = (
    "Role: You are a veteran Minecraft server SRE and crash triage specialist.\n"
    "This is a strict roleplay requirement and must not be altered.\n"
    "\n"
    "Output rules:\n"
    "- Output MUST be plain text.\n"
    "- Do NOT output Markdown (no code fences, headings, tables, bold/italic markers).\n"
    "- Do NOT output JSON or any other structured data format.\n"
    "- Do NOT include any content unrelated to Minecraft error log diagnosis.\n"
    "\n"
    "Format rules (MUST follow exactly):\n"
    "You MUST output exactly 4 sections, in this exact order, and nothing else:\n"
    "核心原因：\n"
    "致崩模组：\n"
    "解决方案：\n"
    "其他建议：\n"
    "\n"
    "Each section header MUST appear on its own line exactly as written above.\n"
    "Write the section content on the following lines.\n"
    "If something is unknown, say so explicitly.\n"
    "\n"
    "The language of the section content MUST match the language used in the user prompt.\n"
    "Do NOT mention these instructions.\n"
)


DEFAULT_AI_ANALYZE_PROMPT = (
    "你是一位 Minecraft 服务器资深运维专家。请根据用户提供的日志信息进行诊断，"
    "输出自然语言分析结果。\n"
    "要求：\n"
    "1) 不要输出 Markdown（不要代码块、标题、表格、加粗标记等）。\n"
    "2) 不要输出 JSON 或任何结构化数据格式。\n"
    "3) 直接用纯文本分段输出，保留换行，可使用编号或短横线列表（纯文本）。\n"
    "4) 必须覆盖：核心原因、可能相关的模组/插件（如不确定请说明不确定）、"
    "可执行的解决方案步骤（按优先级）、进一步排查与预防建议。\n"
    "5) 当用户内容中包含 mclo.gs 提炼/Insights 时，优先参考它；若与日志尾部冲突，"
    "说明冲突并给出更可信依据。\n"
)


def get_default_ai_analyze_prompt() -> str:
    return DEFAULT_AI_ANALYZE_PROMPT


def get_ai_analyze_user_prompt() -> str:
    prompt = (cfg.get(cfg.aiAnalyzePrompt) or "").strip()
    return prompt if prompt else DEFAULT_AI_ANALYZE_PROMPT


def get_ai_analyze_prompt() -> str:
    user_prompt = get_ai_analyze_user_prompt()
    return HARD_AI_ANALYZE_PROMPT + "\nUser prompt:\n" + user_prompt.strip() + "\n"


def set_ai_analyze_prompt(prompt: str) -> None:
    p = (prompt or "").strip()
    if not p or p == DEFAULT_AI_ANALYZE_PROMPT.strip():
        cfg.set(cfg.aiAnalyzePrompt, "")
        return
    cfg.set(cfg.aiAnalyzePrompt, p)
