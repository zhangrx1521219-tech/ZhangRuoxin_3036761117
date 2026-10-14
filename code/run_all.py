"""
run_all.py
一键运行整个项目：从原始数据生成所有表和图
用法：在项目根目录下运行 `python code/run_all.py`
"""
import subprocess
import sys
import os

# 确保在项目根目录运行
if not os.path.exists("data/raw/public.csv"):
    print("错误：请在项目根目录下运行（应能看到 data/ 文件夹）")
    sys.exit(1)

# 按顺序执行的脚本
scripts = [
    "01_clean.py",       # 数据清洗 -> data/processed/ck_analysis.csv
    "02_table3.py",      # Table 3
    "03_table4.py",      # Table 4
    "04_figure1.py",     # Figure 1
    "05_table2.py",      # Table 2
    "06_extension.py",   # Extension
]

for script in scripts:
    path = os.path.join("code", script)
    print(f"\n{'='*60}\n运行 {script}\n{'='*60}")
    result = subprocess.run([sys.executable, path], capture_output=False)
    if result.returncode != 0:
        print(f"\n❌ {script} 运行失败，中止。")
        sys.exit(1)

print(f"\n{'='*60}\n✅ 全部完成！所有表和图已生成到 outputs/")
print("="*60)