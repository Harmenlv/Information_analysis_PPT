# 实验5：简化版RLWE问题实现
import numpy as np

def rlwe_keygen(n, q):
    """
    RLWE密钥生成
    :param n: 多项式维度
    :param q: 模数
    :return: 私钥s（n维向量）
    """
    # 私钥：小整数向量（-1,0,1）
    s = np.random.randint(-1, 2, size=n)
    return s

def rlwe_encrypt(s, q, noise_scale=1):
    """
    RLWE加密（生成带噪声的线性方程）
    :param s: 私钥
    :param q: 模数
    :param noise_scale: 噪声规模
    :return: 公钥(a, b)，其中b = a·s + e mod q
    """
    n = len(s)
    # 生成随机向量a
    a = np.random.randint(0, q, size=n)
    # 生成小噪声e
    e = np.random.randint(-noise_scale, noise_scale+1)
    # 计算b = a·s + e mod q
    b = (np.dot(a, s) + e) % q
    return a, b

def rlwe_decrypt_brute_force(a_list, b_list, q, n):
    """
    暴力破解RLWE（模拟攻击者）
    :param a_list: 多个a向量
    :param b_list: 多个b值
    :param q: 模数
    :param n: 维度
    :return: 破解的私钥s
    """
    # 暴力搜索所有可能的私钥（仅适用于极小n）
    # 注意：n≥5时，搜索空间达3^5=243，n≥10时不可行
    from itertools import product
    possible_s = product([-1,0,1], repeat=n)
    for s_candidate in possible_s:
        valid = True
        for a, b in zip(a_list, b_list):
            # 验证 b ≈ a·s mod q（允许小噪声）
            b_calc = (np.dot(a, s_candidate)) % q
            # 噪声范围±1，故差值应≤1
            if abs(b_calc - b) > 1:
                valid = False
                break
        if valid:
            return np.array(s_candidate)
    return None

# 实验执行
if __name__ == "__main__":
    # 1. 参数设置（极小n，仅用于演示）
    n = 3  # 维度（实际RLWE中n≥256）
    q = 23 # 模数
    
    # 2. 密钥生成
    s = rlwe_keygen(n, q)
    print(f"私钥s：{s}")
    
    # 3. 生成多个RLWE样本
    a_list = []
    b_list = []
    for _ in range(5):
        a, b = rlwe_encrypt(s, q)
        a_list.append(a)
        b_list.append(b)
    print(f"RLWE样本（a,b）示例：")
    for a, b in zip(a_list[:3], b_list[:3]):
        print(f"a={a}, b={b}")
    
    # 4. 模拟攻击者暴力破解
    s_cracked = rlwe_decrypt_brute_force(a_list, b_list, q, n)
    print(f"破解的私钥：{s_cracked}（与真实私钥{s}一致）")
    
    # 5. 高维提示
    print("\n提示：n=256时，可能的私钥数量达3^256≈10^122，暴力破解完全不可行")