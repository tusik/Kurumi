'''
Author: Image image@by.cx
Date: 2024-08-28 11:06:46
LastEditors: Image image@by.cx
LastEditTime: 2024-08-28 11:08:16
filePathColon: /
Description: 

Copyright (c) 2024 by Image, All Rights Reserved. 
'''
import random

import matplotlib
import matplotlib as mpl
import re
matplotlib.use('Agg')  # 确保在无图形界面环境下运行
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

out_path = "."

# 定义检查和添加所需宏包的函数
def add_required_packages(latex_str):
    packages = set()
    
    # 检查是否使用了 aligned 环境
    if r'\begin{aligned}' in latex_str:
        packages.add(r'amsmath')
    
    # 检查是否使用了 bold math
    if r'\mathbf{' in latex_str:
        packages.add(r'amsfonts')
    
    # 检查是否使用了 \mathbb
    if r'\mathbb{' in latex_str:
        packages.add(r'amsfonts')
    
    # 检查是否使用了 \boldsymbol
    if r'\boldsymbol{' in latex_str:
        packages.add(r'amsmath')
        
    # 生成 preamble 字符串
    preamble = r'\usepackage{' + '}\n\\usepackage{'.join(packages) + '}'
    return preamble

def latex_to_image(latex_code, out_path):
    preamble = add_required_packages(latex_code)
    mpl.rc('text', usetex=True)

    mpl.rc('text.latex', preamble=preamble)
    # 创建一个图形对象
    fig = plt.figure(figsize=(2, 2))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')  # 关闭坐标轴
    rand_id = random.Random().randint(1, 1000)
    latex_code = latex_code.replace('\n', '')
    # 渲染LaTeX公式
    t = ax.text(0.5, 0.5, f"${latex_code}$", fontsize=20, ha='center', va='center')

    # 保存为图片
    fig.savefig(f'{out_path}/{rand_id}_latex.png', bbox_inches='tight', pad_inches=0)
    plt.close(fig)
    return f'{out_path}/{rand_id}_latex.png'


if __name__ == '__main__':
    # 示例LaTeX公式
    latex_code = r"""\begin{aligned}
\nabla \cdot \mathbf{E} &= \frac{\rho}{\varepsilon_0} \\
\nabla \cdot \mathbf{B} &= 0 \\
\nabla \times \mathbf{E} &= -\frac{\partial \mathbf{B}}{\partial t} \\
\nabla \times \mathbf{B} &= \mu_0\left(\mathbf{J} + \varepsilon_0\frac{\partial \mathbf{E}}{\partial t}\right)
\end{aligned}"""
    output_file = "output.png"

    # 转换并保存图片
    latex_to_image(latex_code, out_path)

    # 显示图片（可选）
    img = mpimg.imread(output_file)
    plt.imshow(img)
    plt.show()
