# 实验2：小步大步法（Baby-step Giant-step）实现
import math
import hashlib

def baby_step_giant_step(g, h, p):
    """
    小步大步法求解离散对数：g^k ≡ h (mod p)
    参数：
        g: 生成元
        h: 目标值
        p: 模数（素数）
    返回：
        k: 离散对数值，不存在则返回None
    """
    # 确保g和p互质
    if math.gcd(g, p) != 1:
        raise ValueError("g和p必须互质")
    
    # 初始化参数
    m = math.ceil(math.sqrt(p - 1))  # m = ceil(sqrt(p-1))
    table = {}
    
    # 小步：计算g^i mod p，存入哈希表
    print(f"1. 小步计算（m={m}）：")
    current = 1
    for i in range(m):
        table[current] = i
        print(f"   g^{i} = {current} mod {p}")
        current = (current * g) % p
    
    # 计算g^(-m) mod p
    g_m = pow(g, m, p)
    g_inv_m = pow(g_m, p - 2, p)  # 素数模下逆元 = 底数^(p-2) mod p
    print(f"\n2. 计算g^(-m) mod {p} = {g_inv_m}")
    
    # 大步：计算h * (g^(-m))^j mod p
    print("\n3. 大步计算并匹配：")
    current = h % p
    for j in range(m):
        if current in table:
            k = table[current] + j * m
            print(f"   找到匹配：h*(g^(-m))^{j} = {current}, k = {table[current]} + {j}*{m} = {k}")
            return k
        current = (current * g_inv_m) % p
        print(f"   h*(g^(-m))^{j+1} = {current} mod {p}")
    
    # 未找到解
    return None

# 实验演示：素数模下的小步大步法
if __name__ == "__main__":
    # 示例1：小素数模测试（易验证）
    p = 101  # 素数模数
    g = 2    # 生成元
    k_true = 67  # 真实的离散对数
    h = pow(g, k_true, p)
    
    print("=== 小步大步法实验 ===")
    print(f"已知：g={g}, h={h}, p={p}，求解g^k ≡ h (mod p)")
    k = baby_step_giant_step(g, h, p)
    
    if k is not None:
        print(f"\n4. 求解结果：k = {k}")
        print(f"   验证：{g}^{k} mod {p} = {pow(g, k, p)} (预期值：{h})")
        print(f"   结果正确：{pow(g, k, p) == h}")
    else:
        print("\n4. 未找到解")
    
    # 示例2：模18乘法群测试（非素数模，需调整）
    print("\n=== 模18乘法群测试 ===")
    p_18 = 18
    g_18 = 5
    h_18 = 11
    # 由于18不是素数，需用欧拉函数调整
    phi_18 = 6
    m_18 = math.ceil(math.sqrt(phi_18))
    k_18 = baby_step_giant_step(g_18, h_18, p_18)
    print(f"求解log_5(11) mod 18 = {k_18}")
    print(f"验证：5^{k_18} mod 18 = {pow(g_18, k_18, p_18)}")