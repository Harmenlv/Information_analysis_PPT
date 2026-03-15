# 实验3：二维SVP（最短向量问题）求解
import numpy as np
import math

def find_shortest_vector(basis, search_range=10):
    """
    暴力求解二维SVP（最短向量问题）
    :param basis: 格基
    :param search_range: 系数搜索范围（-search_range 到 search_range）
    :return: 最短向量及其长度
    """
    shortest_vec = None
    min_length = float('inf')
    
    # 遍历所有整数系数组合
    for a1 in range(-search_range, search_range+1):
        for a2 in range(-search_range, search_range+1):
            # 跳过零向量（a1=0且a2=0）
            if a1 == 0 and a2 == 0:
                continue
            # 计算格向量
            x = a1 * basis[0][0] + a2 * basis[1][0]
            y = a1 * basis[0][1] + a2 * basis[1][1]
            # 计算向量长度
            length = math.sqrt(x**2 + y**2)
            # 更新最短向量
            if length < min_length:
                min_length = length
                shortest_vec = (x, y)
    return shortest_vec, min_length

# 实验执行
if __name__ == "__main__":
    # 1. 标准基SVP求解
    basis_standard = [[1, 0], [0, 1]]
    sv_standard, len_standard = find_shortest_vector(basis_standard)
    print(f"标准基最短向量：{sv_standard}，长度：{len_standard}（理论值1）")
    
    # 2. 非正交基SVP求解
    basis_non_ortho = [[5, 3], [2, 1]]  # 坏基（长向量）
    sv_non_ortho, len_non_ortho = find_shortest_vector(basis_non_ortho, search_range=20)
    print(f"坏基最短向量：{sv_non_ortho}，长度：{len_non_ortho}（验证坏基SVP求解难度）")
    
    # 3. 高维提示（二维易解，高维指数爆炸）
    print("\n提示：二维SVP可暴力求解，但n≥256时，搜索空间达2^256，暴力求解不可行")