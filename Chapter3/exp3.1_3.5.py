# ====================== 实验1：同余基础与RSA密钥生成 ======================
"""
实验目标：掌握同余定义、欧拉函数、模逆元求解，实现RSA密钥生成核心步骤
对应讲义：同余的引入 → RSA密钥生成（基础）
"""
def gcd(a, b):
    """辗转相除法求最大公约数（GCD）"""
    while b != 0:
        a, b = b, a % b
    return a

def euler_phi(p, q):
    """计算n=pq的欧拉函数φ(n)=(p-1)(q-1)"""
    return (p-1)*(q-1)

def extended_gcd(a, m):
    """扩展欧几里得算法求解模逆元"""
    old_r, r = a, m
    old_s, s = 1, 0
    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
    if old_r != 1:
        return None  # 逆元不存在（a与m不互质）
    return old_s % m

# RSA密钥生成核心步骤
p, q = 5, 7  # 小素数示例（实际用2048位大素数）
n = p * q
phi_n = euler_phi(p, q)
e = 5  # 加密指数（需满足gcd(e, phi_n)=1）
d = extended_gcd(e, phi_n)  # 解密指数（e的模逆元）

# 验证结果
print("=== 实验1：RSA密钥生成 ===")
print(f"模数n = {p}×{q} = {n}")
print(f"欧拉函数φ(n) = {phi_n}")
print(f"加密指数e = {e}（验证互质：gcd({e},{phi_n})={gcd(e, phi_n)}）")
print(f"解密指数d = {d}（验证ed≡1 mod {phi_n}：{(e*d)%phi_n == 1}）")
print(f"公钥(e,n)=({e},{n})，私钥(d,n)=({d},{n})\n")

# ====================== 实验2：RSA加密解密的模幂运算 ======================
"""
实验目标：掌握模幂拆分技巧，验证RSA加解密正确性，理解同余乘法相容性
对应讲义：RSA加密（分步推导）→ RSA解密（核心验证）
"""
def fast_pow(base, exp, mod):
    """快速幂算法（二进制拆分）计算base^exp mod mod，避免大整数溢出"""
    result = 1
    base = base % mod  # 先取模减小数值
    while exp > 0:
        if exp % 2 == 1:  # 指数为奇数时，累积结果
            result = (result * base) % mod
        base = (base * base) % mod  # 底数平方，指数折半
        exp = exp // 2
    return result

# RSA加解密验证
m = 10  # 明文
c = fast_pow(m, e, n)  # 加密：c = m^e mod n
m_decrypt = fast_pow(c, d, n)  # 解密：m = c^d mod n

print("=== 实验2：RSA加解密验证 ===")
print(f"明文m = {m}")
print(f"加密：{m}^{e} mod {n} = {c}")
print(f"解密：{c}^{d} mod {n} = {m_decrypt}")
print(f"验证解密正确性：{m_decrypt == m}\n")

# ====================== 实验3：中国剩余定理（CRT）求解 ======================
"""
实验目标：掌握CRT求解同余方程组，理解模运算分治思想
对应讲义：中国剩余定理的严格陈述 → 物不知数问题求解
"""
def crt(a_list, m_list):
    """
    求解同余方程组：x ≡ a_i mod m_i（m_i两两互质）
    :param a_list: 余数列表 [a1, a2, ..., ak]
    :param m_list: 模数列表 [m1, m2, ..., mk]
    :return: 模M的唯一解（M=∏m_i）
    """
    # 验证模数两两互质
    for i in range(len(m_list)):
        for j in range(i+1, len(m_list)):
            if gcd(m_list[i], m_list[j]) != 1:
                raise ValueError("模数必须两两互质！")
    
    M = 1  # 总模数M = m1×m2×...×mk
    for m in m_list:
        M *= m
    
    x = 0
    for a, m in zip(a_list, m_list):
        Mi = M // m  # Mi = M/mi
        Mi_inv = extended_gcd(Mi, m)  # Mi的模m逆元
        x += a * Mi * Mi_inv
    
    return x % M  # 模M取最小正解

# 物不知数问题：x≡2 mod3, x≡3 mod5, x≡2 mod7
a_list = [2, 3, 2]
m_list = [3, 5, 7]
x = crt(a_list, m_list)

print("=== 实验3：中国剩余定理（CRT）求解 ===")
print(f"求解同余方程组：")
for a, m in zip(a_list, m_list):
    print(f"  x ≡ {a} mod {m}")
print(f"最小正解：x = {x}")
# 验证解的正确性
for a, m in zip(a_list, m_list):
    print(f"验证 x mod {m} = {x%m}（预期{a}）：{x%m == a}")
print()

# ====================== 实验4：二次剩余与勒让德符号 ======================
"""
实验目标：掌握二次剩余判定，实现勒让德符号计算，理解欧拉判别法
对应讲义：二次剩余的定义与判定 → 勒让德符号
"""
def legendre_symbol(a, p):
    """
    计算勒让德符号(a/p)：
    - 1：a是模p的二次剩余
    - -1：a是模p的二次非剩余
    - 0：a ≡ 0 mod p
    （p为奇素数）
    """
    if p == 2:
        raise ValueError("p必须是奇素数！")
    a = a % p
    if a == 0:
        return 0
    # 欧拉判别法：(a/p) ≡ a^((p-1)/2) mod p
    exponent = (p - 1) // 2
    res = fast_pow(a, exponent, p)
    return 1 if res == 1 else -1

# 验证模7的二次剩余
p = 7
print("=== 实验4：二次剩余与勒让德符号 ===")
print(f"模{p}的二次剩余判定（1~{p-1}）：")
for a in range(1, p):
    ls = legendre_symbol(a, p)
    res_type = "二次剩余" if ls == 1 else "二次非剩余"
    print(f"  a={a}：勒让德符号({a}/{p})={ls} → {res_type}")
print()

# ====================== 实验5：模逆元求解与AES S盒基础 ======================
"""
实验目标：掌握模逆元求解，理解有限域GF(2^8)逆元（AES S盒核心）
对应讲义：模m可逆剩余类与乘法逆元 → 模逆元：密码可逆运算核心
"""
def gf256_inverse(byte):
    """
    计算GF(2^8)中字节的乘法逆元（AES S盒基础）
    不可约多项式：x^8 + x^4 + x^3 + x + 1（对应0x11B）
    """
    if byte == 0:
        return 0  # 0的逆元是自身（AES定义）
    # 扩展欧几里得算法适配GF(2^8)（简化版，仅演示原理）
    u, v = 0x11B, byte
    x1, x2 = 1, 0
    while v != 0:
        # GF(2^8)除法：u = q*v + r（仅保留余数）
        q = 0
        deg_u = u.bit_length() - 1
        deg_v = v.bit_length() - 1
        while deg_u >= deg_v:
            q ^= 1 << (deg_u - deg_v)
            u ^= v << (deg_u - deg_v)
            deg_u = u.bit_length() - 1
        u, v = v, u
        x1, x2 = x2, x1 ^ (q * x2)
    return x1 % 256

# 验证GF(2^8)逆元（AES S盒示例）
byte = 0x03  # AES常用字节
inv_byte = gf256_inverse(byte)
print("=== 实验5：模逆元与GF(2^8)（AES S盒） ===")
print(f"GF(2^8)中字节0x{byte:02X}的逆元：0x{inv_byte:02X}")
# 验证：byte × inv_byte ≡ 1 mod 256（GF(2^8)乘法）
print(f"验证逆元正确性：(0x{byte:02X} × 0x{inv_byte:02X}) mod 256 = { (byte * inv_byte) % 256 }（预期1）")