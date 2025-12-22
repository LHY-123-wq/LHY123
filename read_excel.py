import pandas as pd

# 读取Excel文件
df = pd.read_excel('c:\\Users\\13541\\Desktop\\LHY\\1999-2023数值化转型指数数据汇总表.xlsx')

# 查看文件的基本信息
print("数据基本信息：")
df.info()

# 查看前几行数据
print("\n前10行数据：")
print(df.head(10))

# 查看列名
print("\n列名：")
print(df.columns.tolist())

# 查看数据范围
print("\n年份范围：", df['年份'].min(), "- ", df['年份'].max())
print("股票代码数量：", df['股票代码'].nunique())
print("总数据量：", len(df))

# 查看部分股票代码
print("\n部分股票代码：")
print(df['股票代码'].unique()[:10])