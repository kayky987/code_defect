import openai
import os

# 设置 OpenAI API 密钥 (确保你已经在环境变量中设置了 OPENAI_API_KEY)
openai.api_key = os.getenv("OPENAI_API_KEY")

# 设置代理环境变量
os.environ['http_proxy'] = 'http://127.0.0.1:7899'
os.environ['https_proxy'] = 'http://127.0.0.1:7899'
os.environ['ALL_PROXY'] = 'socks5://127.0.0.1:7898'

# 确保 API 密钥存在
if not openai.api_key:
    raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")

# 测试 API 请求
try:
    # 使用 GPT-4 模型生成一个简单的提示
    response = openai.Completion.create(
        model="gpt-4",
        prompt="Say hello world",
        max_tokens=5
    )

    # 输出 API 响应内容
    print("API Key works! Here is the response:")
    print(response.choices[0].text.strip())

except openai.error.OpenAIError as e:
    print(f"Error: {e}")
