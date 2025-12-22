import matplotlib.font_manager as fm

# 列出所有可用字体
all_fonts = [font.name for font in fm.fontManager.ttflist]
print("所有可用字体 (共", len(all_fonts), "个):")
for font in sorted(all_fonts[:20]):  # 只显示前20个
    print(f"  - {font}")
if len(all_fonts) > 20:
    print(f"  ... 还有 {len(all_fonts) - 20} 个字体未显示")

# 查找中文字体
chinese_keywords = ['Hei', 'Song', 'Kai', 'YaHei', 'Sim', 'FangSong', 'LiSu', 'YouYuan']
chinese_fonts = [font.name for font in fm.fontManager.ttflist 
                 if any(keyword in font.name for keyword in chinese_keywords)]

print("\n检测到的中文字体:")
if chinese_fonts:
    for font in sorted(chinese_fonts):
        print(f"  - {font}")
else:
    print("  未检测到中文字体")
