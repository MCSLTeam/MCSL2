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


DEFAULT_AI_ANALYZE_PROMPT = (
    "你是一位 Minecraft 服务器资深运维专家。请根据用户提供的日志信息进行诊断，并输出 JSON："
    '{"cause":"","mod_name":"","fix_solution":"","advice":""}'
    "\n"
    "要求：\n"
    "1) 只输出 JSON 对象本体，不要 Markdown/代码块/多余解释。\n"
    "2) cause：核心原因（尽量具体到错误触发点）。\n"
    "3) mod_name：如果能确定导致崩溃的模组/插件/组件名称，填名称；不确定留空字符串。\n"
    "4) fix_solution：给出可执行的解决方案步骤（按优先级排序）。\n"
    "5) advice：给出进一步排查建议与预防建议（如版本匹配、依赖、配置、内存、Java 版本等）。\n"
    "6) 当用户内容中包含 mclo.gs 提炼/Insights 时，优先参考它；"
    "若与日志尾部冲突，说明冲突并给出更可信依据。\n"
)


def get_default_ai_analyze_prompt() -> str:
    return DEFAULT_AI_ANALYZE_PROMPT


def get_ai_analyze_prompt() -> str:
    prompt = (cfg.get(cfg.aiAnalyzePrompt) or "").strip()
    return prompt if prompt else DEFAULT_AI_ANALYZE_PROMPT


def set_ai_analyze_prompt(prompt: str) -> None:
    p = (prompt or "").strip()
    if not p or p == DEFAULT_AI_ANALYZE_PROMPT.strip():
        cfg.set(cfg.aiAnalyzePrompt, "")
        return
    cfg.set(cfg.aiAnalyzePrompt, p)
