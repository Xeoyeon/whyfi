basic_template = """
<|system|>
You are a helpful assistant.<|end|>
<|user|>
{question}<|end|>
<|assistant|>
"""

context_template = """
<|system|>
You are a helpful assistant.<|end|>
<|user|>
# 사용자 질문:
{question}
# 검색 결과
### {context}<|end|>
<|assistant|>
"""

prompt_templates = {
    "basic_template": basic_template,
    "context_template": context_template,
}