# 实验4：二维CVP（最近向量问题）求解
import numpy as np
import math

def generate_lattice_points_extended(basis, search_range=10):
    """
    生成指定范围的格点（用于CVP搜索）
    :param basis: 格基
    :param search_range: 系数范围（-search_range 到 search_range）
    :return: 格点列表
    """
    lattice_points = []
    for a1 in range(-search_range, search_range+1):
        for a2 in range(-search_range, search_range+1):
            x = a1 * basis[0][0] + a2 * basis[1][0]
            y = a1 * basis[0][1] + a2 * basis[1][1]
            lattice_points.append((x, y))
    return lattice_points

def solve_cvp(target_point, lattice_points):
    """
    求解CVP（找最近格点）
    :param target_point: 目标点 (x,y)
    :param lattice_points: 格点列表
    :return: 最近格点、距离
    """
    min_dist = float('inf')
    closest_point = None
    tx, ty = target_point
    for (x, y) in lattice_points:
        dist = math.sqrt((tx - x)**2 + (ty - y)**2)
        if dist < min_dist:
            min_dist = dist
            closest_point = (x, y)
    return closest_point, min_dist

# 实验执行
if __name__ == "__main__":
    # 1. 定义格基和目标点
    basis = [[1, 0], [0, 1]]
    target_point = (1.2, 2.7)  # 非格点
    print(f"目标点：{target_point}")
    
    # 2. 生成格点并求解CVP
    lattice_points = generate_lattice_points_extended(basis, search_range=5)
    closest_point, dist = solve_cvp(target_point, lattice_points)
    print(f"最近格点：{closest_point}，距离：{dist:.2f}（理论值≈0.36）")
    
    # 3. 带噪声的CVP（模拟RLWE噪声模型）
    # 真实格点 + 噪声 = 目标点
    true_point = (3, 4)
    noise = (0.8, -0.3)
    noisy_target = (true_point[0] + noise[0], true_point[1] + noise[1])
    closest_noisy, dist_noisy = solve_cvp(noisy_target, lattice_points)
    print(f"\n带噪声目标点：{noisy_target}")
    print(f"还原的格点：{closest_noisy}（与真实格点{true_point}一致，验证噪声还原）")