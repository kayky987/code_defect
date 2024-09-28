import os
import pandas as pd
import openai

# Step 1: 从环境变量中读取API密钥
openai.api_key = os.getenv("OPENAI_API_KEY")

# 确保环境变量已正确设置
if not openai.api_key:
    raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")

# Step 2: 下载并加载本地数据集
data_path = '../data'  # 数据集存放路径
splits = {
    'train': os.path.join(data_path, 'train-00000-of-00001.parquet'),
    'validation': os.path.join(data_path, 'validation-00000-of-00001.parquet'),
    'test': os.path.join(data_path, 'test-00000-of-00001.parquet')
}

# 加载训练数据集
df = pd.read_parquet(splits['train'])

# Step 3: 定义生成解释的函数，使用 GPT API
def generate_explanation(row):
    if row['target']:
        prompt = f"这段代码存在缺陷。缺陷代码：{row['func']}。请解释这个问题："

        try:
            # 调用 GPT 模型生成解释，并增加 max_tokens
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "你是一个专业的c语言代码分析助手。你的任务是生成简明扼要的代码缺陷解释。回答格式为：【存在问题】该代码片段的问题为："},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,  # 增加 max_tokens 以生成更长的解释
                temperature=0.7,
                stop=["\n\n"]  # 定义生成停止的条件
            )
            explanation = response['choices'][0]['message']['content'].strip()
            print(explanation)
            return explanation
        except Exception as e:
            print(f"Error generating explanation: {e}")
            return "生成解释时出错。"
    else:
        return "【代码无问题】"

# Step 4: 为每个样本生成缺陷解释（限制生成前10条）
df_limited = df.head(10)
# 使用 .loc[] 来避免 SettingWithCopyWarning
df_limited.loc[:, 'explanation'] = df_limited.apply(generate_explanation, axis=1)

# Step 5: 保存优化后的数据集
output_path = '../data/optimized_train_with_gpt_10_samples.parquet'
df_limited.to_parquet(output_path)
print(f"优化后的数据集（前10条）已保存到 {output_path}")
