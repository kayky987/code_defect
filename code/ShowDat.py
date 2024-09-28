import pandas as pd

def save_data_to_excel(input_parquet_path, output_excel_path, start_index, end_index):
    """
    从 Parquet 文件中读取数据，并将第 i 到 j 条数据保存到 Excel 文件。

    参数:
    - input_parquet_path: 输入 Parquet 文件路径
    - output_excel_path: 输出 Excel 文件路径
    - start_index: 起始索引
    - end_index: 结束索引
    """
    try:
        # 从 Parquet 文件中加载数据
        df = pd.read_parquet(input_parquet_path)

        # 提取第 i 到 j 条数据
        df_limited = df.iloc[start_index:end_index]

        # 保存到 Excel 文件
        df_limited.to_excel(output_excel_path, index=False)

        print(f"优化后的数据集（第 {start_index + 1} 到 {end_index} 条）已保存到 {output_excel_path}")

    except Exception as e:
        print(f"Error: {e}")


# 示例调用
input_parquet_path = '../data/optimized_train_with_gpt_10_samples.parquet'
output_excel_path = '../data/optimized_train_subset.xlsx'

# 保存第 3 到 5 条数据到 Excel
save_data_to_excel(input_parquet_path, output_excel_path, 0, 9)
