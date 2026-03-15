"""
实验2：扩展欧几里得算法（求解贝祖系数+模逆元）
对应讲义：贝祖定理、有限域乘法逆元、RSA密钥生成
"""
def extended_gcd(a, b):
    """
    扩展欧几里得算法
    返回：(gcd(a,b), u, v) 满足 a*u + b*v = gcd(a,b)
    """
    if b == 0:
        return (a, 1, 0)
    else:
        g, u_prev, v_prev = extended_gcd(b, a % b)
        u = v_prev
        v = u_prev - (a // b) * v_prev
        return (g, u, v)

def mod_inverse(a, mod):
    """求解a在模mod下的乘法逆元（若存在）"""
    g, u, _ = extended_gcd(a, mod)
    if g != 1:
        return None  # 无逆元
    else:
        return u % mod

def bezout_all_solutions(a, b, d):
    """
    求解贝祖等式 a*u + b*v = d 的所有解（特解+通解）
    前提：d是gcd(a,b)的倍数
    """
    g, u0, v0 = extended_gcd(a, b)
    if d % g != 0:
        return "无解（d不是gcd(a,b)的倍数）"
    
    # 特解
    k = d // g
    u0 *= k
    v0 *= k
    
    # 通解参数
    a_div = a // g
    b_div = b // g
    
    # 生成3组解示例
    solutions = []
    for k in [-1, 0, 1]:
        u = u0 + k * b_div
        v = v0 - k * a_div
        solutions.append((u, v))
    
    return {
        "gcd(a,b)": g,
        "特解(u0, v0)": (u0, v0),
        "通解形式": f"u = {u0} + k*{b_div}, v = {v0} - k*{a_div} (k∈Z)",
        "示例解": solutions
    }

# 测试案例1：讲义例题3（F7中4的逆元）
a, mod = 4, 7
inv = mod_inverse(a, mod)
print(f"=== 模{mod}下{a}的乘法逆元 ===")
print(f"逆元：{inv}")
print(f"验证：{a} * {inv} mod {mod} = {(a * inv) % mod}\n")

# 测试案例2：讲义贝祖定理实例（a=252, b=105, d=21）
a, b, d = 252, 105, 21
print(f"=== 贝祖等式 {a}u + {b}v = {d} 的解 ===")
solutions = bezout_all_solutions(a, b, d)
for k, v in solutions.items():
    print(f"{k}：{v}")

# 测试案例3：RSA私钥求解（e=17, φ(n)=3120，求解d满足 e*d ≡1 mod φ(n)）
e, phi_n = 17, 3120
d = mod_inverse(e, phi_n)
print(f"\n=== RSA私钥求解 ===")
print(f"公钥e={e}, φ(n)={phi_n}")
print(f"私钥d={d}")
print(f"验证：{e} * {d} mod {phi_n} = {(e * d) % phi_n}")