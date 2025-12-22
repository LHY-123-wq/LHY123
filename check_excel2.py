import pandas as pd

# 只读取第二个Excel文件
df2 = pd.read_excel('c:\\Users\\13541\\Desktop\\LHY\\最终数据dta格式-上市公司年度行业代码至2021.xlsx')
print("第二个Excel文件的结构：")
print(df2.head(20))
print("\n列名：")
print(df2.columns.tolist())
print("\n数据类型：")
print(df2.dtypes)
print("\n数据量：", len(df2))