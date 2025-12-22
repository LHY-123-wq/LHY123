import pandas as pd

# 读取Excel文件
df = pd.read_excel('c:\\Users\\13541\\Desktop\\LHY\\1999-2023数值化转型指数数据汇总表.xlsx')

# 查看数据基本信息
print("数据基本信息：")
df.info()

# 查看前10行数据
print("\n前10行数据：")
print(df.head(10))

# 查看所有列名
print("\n列名：")
print(df.columns.tolist())

# 查看数据统计信息
print("\n数据统计信息：")
print(df.describe())

# 查看数据量
print("\n数据量：")
print(f"总共有 {df.shape[0]} 行，{df.shape[1]} 列数据")

# 查看年份范围
if '年份' in df.columns:
    print("\n年份范围：")
    print(f"从 {df['年份'].min()} 到 {df['年份'].max()}")

# 查看企业数量
if '企业名称' in df.columns:
    print("\n企业数量：")
    print(f"总共有 {df['企业名称'].nunique()} 家企业")

# 查看股票代码格式
if '股票代码' in df.columns:
    print("\n股票代码示例：")
    print(df['股票代码'].head(10))
