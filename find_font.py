import matplotlib.font_manager as fm

# 查找所有字体
fonts = fm.findSystemFonts(fontpaths=None, fontext='ttf')

# 输出所有可用字体，以便用户查看
print("所有可用字体文件：")
for font in fonts[:50]:  # 只显示前50个
    print(font)

# 特别查找微软雅黑相关字体
print("\n查找微软雅黑相关字体：")
for font in fonts:
    if any(keyword in font.lower() for keyword in ['microsoft', 'yahei', 'msyh', '微软雅黑']):
        print(font)