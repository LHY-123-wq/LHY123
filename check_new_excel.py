import pandas as pd

# 读取Excel文件
df = pd.read_excel(r'c:\Users\13541\Desktop\LHY\最终数据dta格式-上市公司年度行业代码至2021.xlsx')

# 查看数据结构
print('数据形状:', df.shape)
print('\n列名:', df.columns.tolist())
print('\n前10行数据:')
print(df.head(10))
print('\n数据类型:')
print(df.dtypes)

# 查看股票代码列的信息
if '股票代码' in df.columns:
    print('\n股票代码列信息:')
    print(df['股票代码'].head(20))
    print('股票代码唯一值数量:', df['股票代码'].nunique())