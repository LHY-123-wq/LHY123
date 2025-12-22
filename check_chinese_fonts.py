import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 列出所有可用字体
print("系统中可用的中文字体：")
for font in fm.fontManager.ttflist:
    if any('Chinese' in font.name or 'SimHei' in font.name or 'SimSun' in font.name or 'Microsoft YaHei' in font.name or 'FangSong' in font.name or 'KaiTi' in font.name for font in fm.fontManager.ttflist):
        print(f"字体名称: {font.name}, 文件路径: {font.fname}")

# 测试中文字体显示
plt.figure(figsize=(10, 5))
plt.plot([1, 2, 3, 4, 5], [10, 20, 30, 40, 50])
plt.title('测试中文字体显示')
plt.xlabel('年份')
plt.ylabel('数值')
plt.savefig('test_chinese_font.png')
print("\n测试图表已保存为 test_chinese_font.png")
