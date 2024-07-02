import random

import matplotlib

matplotlib.use('Agg')  # 确保在无图形界面环境下运行
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

out_path = "."


def latex_to_image(latex_code, out_path):
    plt.rcParams['text.usetex'] = True
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
