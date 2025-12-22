import pandas as pd

# 读取第一个Excel文件
df1 = pd.read_excel('c:\\Users\\13541\\Desktop\\LHY\\1999-2023数值化转型指数数据汇总表.xlsx')
print("第一个Excel文件的股票代码列数据类型：", df1['股票代码'].dtype)
print("第一个Excel文件的前5行股票代码：")
print(df1['股票代码'].head())

# 读取第二个Excel文件
df2 = pd.read_excel('c:\\Users\\13541\\Desktop\\LHY\\最终数据dta格式-上市公司年度行业代码至2021.xlsx')
print("\n第二个Excel文件的股票代码全称列数据类型：", df2['股票代码全称'].dtype)
print("第二个Excel文件的前5行股票代码全称：")
print(df2['股票代码全称'].head())

# 检查数据范围
print("\n第一个Excel文件的年份范围：", df1['年份'].min(), "- ", df1['年份'].max())
print("第二个Excel文件的年份范围：", df2['年度'].min(), "- ", df2['年度'].max())

# 检查是否有匹配的数据
print("\n检查是否有匹配的股票代码和年份数据：")
df1_sample = df1[['股票代码', '年份']].head(5)
df2_sample = df2[['股票代码全称', '年度']].head(5)
print("第一个文件的样本数据：")
print(df1_sample)
print("\n第二个文件的样本数据：")
print(df2_sample)

# 尝试手动合并前5行数据
test_merge = pd.merge(df1_sample, df2_sample, left_on=['股票代码', '年份'], right_on=['股票代码全称', '年度'], how='left')
print("\n手动合并结果：")
print(test_merge)