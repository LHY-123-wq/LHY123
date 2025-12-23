import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# 设置页面标题
st.set_page_config(page_title='企业数字化转型指数查询系统', layout='wide')

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

# 显示折线图 (使用 Plotly 替代 Matplotlib)
st.subheader('数字化转型指数趋势')
if not company_data.empty:
    # 使用 Plotly 创建图表
    fig = px.line(
        company_data,
        x='年份',
        y='数字化转型指数',
        title=f'{company_name}历年数字化转型指数趋势 (1999-2023)',
        markers=True,
        labels={'年份': '年份', '数字化转型指数': '数字化转型指数'},
        template='plotly_white'
    )
    
    # 设置图表样式
    fig.update_layout(
        hovermode='x unified',
        xaxis=dict(
            title='年份',
            showgrid=False,
            tickangle=0
        ),
        yaxis=dict(
            title='数字化转型指数',
            showgrid=True,
            gridwidth=1,
            gridcolor='#f0f0f0',
            range=[0, max(company_data['数字化转型指数']) * 1.1]
        ),
        showlegend=True,
        legend_title_text='',
        height=400
    )
    
    # 标记当前选择的年份
    if not filtered_data.empty and '年份' in filtered_data.columns and '数字化转型指数' in filtered_data.columns:
        current_year = filtered_data.iloc[0]['年份']
        current_index = filtered_data.iloc[0]['数字化转型指数']
        
        # 添加当前年份的标记点
        fig.add_scatter(
            x=[current_year],
            y=[current_index],
            mode='markers',
            marker=dict(
                color='#ff7f0e',
                size=12,
                symbol='star'
            ),
            name='当前年份'
        )
    
    # 显示图表
    st.plotly_chart(fig, use_container_width=True)
    
else:
    st.warning('未找到该企业的历史数据')

# 显示原始数据（可选）
if st.checkbox('显示原始数据'):
    # 清理列名，去除不规范的空格
    cleaned_data = company_data.copy()
    cleaned_data.columns = [col.replace(' ', '') for col in cleaned_data.columns]
    
    st.subheader(f'{company_name}数字化转型指数原始数据')
    st.dataframe(cleaned_data, width=2000, height=800)