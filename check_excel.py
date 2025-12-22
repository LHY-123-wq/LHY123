import pandas as pd

# 读取第一个Excel文件
df1 = pd.read_excel('c:\\Users\\13541\\Desktop\\LHY\\1999-2023数值化转型指数数据汇总表.xlsx')
print("第一个Excel文件的结构：")
print(df1.head())
print("\n列名：")
print(df1.columns.tolist())
print("\n数据类型：")
print(df1.dtypes)
print("\n数据量：", len(df1))

# 读取第二个Excel文件
df2 = pd.read_excel('c:\\Users\\13541\\Desktop\\LHY\\最终数据dta格式-上市公司年度行业代码至2021.xlsx')
print("\n\n第二个Excel文件的结构：")
print(df2.head())
print("\n列名：")
print(df2.columns.tolist())
print("\n数据类型：")
print(df2.dtypes)
print("\n数据量：", len(df2))