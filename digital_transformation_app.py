import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 配置中文字体
def get_chinese_font_properties():
    # 直接使用系统默认的微软雅黑字体文件路径
    # 优先使用常规版本
    yahei_path = "C:\\Windows\\Fonts\\msyh.ttc"
    
    # 检查文件是否存在
    import os
    if not os.path.exists(yahei_path):
        print(f"字体文件不存在: {yahei_path}")
        # 尝试其他可能的路径
        alternative_paths = [
            "C:\\Windows\\Fonts\\msyhbd.ttc",  # 粗体
            "C:\\Windows\\Fonts\\msyhl.ttc"   # 细体
        ]
        for path in alternative_paths:
            if os.path.exists(path):
                yahei_path = path
                print(f"使用备选字体路径: {yahei_path}")
                break
        else:
            raise FileNotFoundError("未找到微软雅黑字体文件")
    
    # 创建FontProperties对象
    font_properties = fm.FontProperties(fname=yahei_path)
    print(f"已创建字体属性对象: {yahei_path}")
    
    # 同时设置全局字体作为备选
    plt.rcParams.update({
        'font.sans-serif': ['Microsoft YaHei', 'DejaVu Sans'],
        'axes.unicode_minus': False,
        'font.family': 'sans-serif'
    })
    
    return font_properties

# 获取字体属性对象
chinese_font = get_chinese_font_properties()

# 设置页面标题
st.title('企业数字化转型指数查询系统')

# 加载数据
@st.cache_data
def load_data():
    # 加载数字化转型指数数据
    df = pd.read_excel('1999-2023数值化转型指数数据汇总表.xlsx')
    
    # 加载行业代码数据
    industry_df = pd.read_excel('最终数据dta格式-上市公司年度行业代码至2021.xlsx')
    
    # 合并数据，基于股票代码和年份
    merged_df = pd.merge(df, industry_df, 
                        left_on=['股票代码', '年份'], 
                        right_on=['股票代码全称', '年度'], 
                        how='left')
    
    return merged_df

# 加载数据
df = load_data()

# 数据统计信息
total_records = df.shape[0]
total_companies = df['企业名称'].nunique()
year_range = (df['年份'].min(), df['年份'].max())

# 显示数据统计信息
st.sidebar.subheader('数据统计')
st.sidebar.write(f'总数据量: {total_records}')
st.sidebar.write(f'企业数量: {total_companies}')
st.sidebar.write(f'年份范围: {year_range[0]}-{year_range[1]}')

# 查询条件
st.sidebar.subheader('查询条件')

# 获取唯一的股票代码和年份
stock_codes = df['股票代码'].unique()
years = df['年份'].unique()

# 获取股票代码对应的企业名称
stock_code_to_name = {}
for code in stock_codes:
    # 获取该股票代码对应的企业名称
    company_names = df[df['股票代码'] == code]['企业名称'].unique()
    company_name = company_names[0] if len(company_names) > 0 else ''
    stock_code_to_name[int(code)] = company_name

# 格式化股票代码选项，显示为"股票代码 - 企业名称"格式
stock_code_options = []
for code in stock_codes:
    code_int = int(code)
    formatted_code = f"{code_int:06d}"
    company_name = stock_code_to_name[code_int]
    option_text = f"{formatted_code} - {company_name}"
    stock_code_options.append(option_text)

# 股票代码选择
selected_option = st.sidebar.selectbox(
    '选择股票代码',
    sorted(stock_code_options)
)

# 从选择的选项中提取股票代码
selected_stock_code_str = selected_option.split(' - ')[0]
selected_stock_code = int(selected_stock_code_str)

# 年份选择
selected_year = st.sidebar.selectbox(
    '选择年份',
    sorted(years, reverse=True)
)

# 从选择的选项中提取企业名称
company_name = selected_option.split(' - ')[1] if ' - ' in selected_option else ''

# 过滤数据
filtered_data = df[(df['股票代码'] == selected_stock_code) & (df['年份'] == selected_year)]

# 获取该企业的所有历史数据
company_data = df[df['股票代码'] == selected_stock_code].sort_values('年份')

# 显示企业信息
if not filtered_data.empty:
    st.subheader('企业基本信息')
    st.write(f'**{company_name} ({selected_stock_code_str})**')
    
    # 获取行业信息
    industry_name = filtered_data.iloc[0]['行业名称'] if not pd.isnull(filtered_data.iloc[0]['行业名称']) else 'N/A'
    # 去除行业名称中的额外空格
    industry_name = industry_name.strip() if isinstance(industry_name, str) else industry_name
    st.write(f'行业: {industry_name}')
    
    # 显示企业基本信息
    col1, col2, col3 = st.columns(3)
    col1.metric('年份', filtered_data.iloc[0]['年份'])
    col2.metric('数字化转型指数', round(filtered_data.iloc[0]['数字化转型指数'], 2) if not pd.isnull(filtered_data.iloc[0]['数字化转型指数']) else 'N/A')
    col3.metric('技术维度', round(filtered_data.iloc[0]['技术维度'], 2) if not pd.isnull(filtered_data.iloc[0]['技术维度']) else 'N/A')
    
    col4, col5, col6 = st.columns(3)
    col4.metric('应用维度', round(filtered_data.iloc[0]['应用维度'], 2) if not pd.isnull(filtered_data.iloc[0]['应用维度']) else 'N/A')
    col5.metric('人工智能词频数', filtered_data.iloc[0]['人工智能词频数'])
    col6.metric('大数据词频数', filtered_data.iloc[0]['大数据词频数'])
    
    col7, col8, col9 = st.columns(3)
    col7.metric('云计算词频数', filtered_data.iloc[0]['云计算词频数'])
    col8.metric('区块链词频数', filtered_data.iloc[0]['区块链词频数'])
    col9.metric('数字技术运用词频数', filtered_data.iloc[0]['数字技术运用词频数'])
    

else:
    st.warning('未找到该股票代码和年份的数据')

# 显示折线图
st.subheader('数字化转型指数趋势')
if not company_data.empty:
    # 创建图表 - 使用更简洁的样式
    fig, ax = plt.subplots(figsize=(12, 5))
    
    # 绘制主线条 - 更细的线条和更小的标记，并添加标签用于图例
    ax.plot(company_data['年份'], company_data['数字化转型指数'], marker='o', linestyle='-', color='#1f77b4', linewidth=1.5, markersize=5, label='数字化转型指数')
    
    # 标记当前选择的年份 - 使用橙色星形
    if not filtered_data.empty and '年份' in filtered_data.columns and '数字化转型指数' in filtered_data.columns:
        current_year = filtered_data.iloc[0]['年份']
        current_index = filtered_data.iloc[0]['数字化转型指数']
        ax.plot(current_year, current_index, marker='*', color='#ff7f0e', markersize=10, label='当前年份')
    
    # 设置图表标题 - 使用FontProperties对象
    ax.set_title(f'{company_name}历年数字化转型指数趋势 (1999-2023)', 
                fontsize=14, fontweight='normal', 
                fontproperties=chinese_font)
    
    # 设置坐标轴标签 - 使用FontProperties对象
    ax.set_xlabel('年份', 
                fontsize=12, 
                fontproperties=chinese_font)
    ax.set_ylabel('数字化转型指数', 
                fontsize=12, 
                fontproperties=chinese_font)
    
    # 隐藏右侧和顶部边框
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    
    # 简化网格线 - 只显示水平网格
    ax.yaxis.grid(True, linestyle='-', alpha=0.1)
    ax.xaxis.grid(False)
    
    # 设置x轴样式
    # 只显示年份在下方，不显示额外的刻度线
    years = company_data['年份'].tolist()
    ax.set_xticks(years)
    # 使用FontProperties对象设置x轴刻度标签
    ax.set_xticklabels(years, rotation=0, fontsize=10, fontproperties=chinese_font)
    
    # 使用FontProperties对象设置y轴刻度标签
    ax.tick_params(axis='y', labelsize=10)
    for label in ax.get_yticklabels():
        label.set_fontproperties(chinese_font)
    
    # 调整x轴标签位置，确保显示在图表下方
    ax.tick_params(axis='x', direction='out', pad=5, length=0)
    ax.tick_params(axis='y', direction='in', length=4)
    
    # 设置y轴范围从0开始，与示例图表一致
    y_max = max(company_data['数字化转型指数']) * 1.1
    ax.set_ylim(0, y_max)
    
    # 添加图例 - 使用FontProperties对象
    legend = ax.legend(loc='best', prop=chinese_font)
    
    # 优化图表布局
    plt.tight_layout(pad=2.0)
    
    # 显示图表
    st.pyplot(fig)
    
else:
    st.warning('未找到该企业的历史数据')

# 显示原始数据（可选）
if st.checkbox('显示原始数据'):
    # 清理列名，去除不规范的空格
    cleaned_data = company_data.copy()
    cleaned_data.columns = [col.replace(' ', '') for col in cleaned_data.columns]
    
    st.subheader(f'{company_name}数字化转型指数原始数据')
    st.dataframe(cleaned_data, width=2000, height=800)
