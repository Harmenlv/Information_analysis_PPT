# 实验1：二维格的生成与离散性验证
import numpy as np
import math

def generate_lattice_points(basis, num_points=20):
    """
    生成二维格点（整数线性组合）
    :param basis: 格基，二维数组 [[b1x, b1y], [b2x, b2y]]
    :param num_points: 生成格点数量
    :return: 格点列表
    """
    lattice_points = []
    # 随机生成整数系数（-5到5）
    for _ in range(num_points):
        a1 = np.random.randint(-5, 6)
        a2 = np.random.randint(-5, 6)
        x = a1 * basis[0][0] + a2 * basis[1][0]
        y = a1 * basis[0][1] + a2 * basis[1][1]
        lattice_points.append((x, y))
    return lattice_points

def calculate_min_distance(points):
    """
    计算格点间的最小距离（验证离散性）
    :param points: 格点列表
    :return: 最小距离
    """
    min_dist = float('inf')
    n = len(points)
    for i in range(n):
        for j in range(i+1, n):
            dx = points[i][0] - points[j][0]
            dy = points[i][1] - points[j][1]
            dist = math.sqrt(dx**2 + dy**2)
            if dist > 0 and dist < min_dist:
                min_dist = dist
    return min_dist

# 实验执行
if __name__ == "__main__":
    # 1. 定义格基（标准正交基）
    basis_standard = [[1, 0], [0, 1]]
    # 2. 生成格点
    lattice_points = generate_lattice_points(basis_standard, 30)
    print("生成的格点示例：", lattice_points[:10])
    # 3. 验证离散性（计算最小距离）
    min_dist = calculate_min_distance(lattice_points)
    print(f"格点最小距离：{min_dist}（验证离散性，理论值应为1）")
    
    # 非正交基验证
    basis_non_ortho = [[1, 1], [1, -1]]
    lattice_points_non_ortho = generate_lattice_points(basis_non_ortho, 30)
    min_dist_non_ortho = calculate_min_distance(lattice_points_non_ortho)
    print(f"非正交基格点最小距离：{min_dist_non_ortho}（仍大于0，验证离散性）")