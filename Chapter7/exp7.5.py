# 实验5：弱椭圆曲线检测（Pohlig-Hellman攻击演示）
import math
from experiment3 import EllipticCurve

def factor(n):
    """分解整数为素因子"""
    factors = {}
    while n % 2 == 0:
        factors[2] = factors.get(2, 0) + 1
        n = n // 2
    i = 3
    while i * i <= n:
        while n % i == 0:
            factors[i] = factors.get(i, 0) + 1
            n = n // i
        i += 2
    if n > 2:
        factors[n] = 1
    return factors

def pohlig_hellman_ecdlp(ec, G, Q, order):
    """
    Pohlig-Hellman算法求解ECDLP（仅适用于群阶含小素因子的情况）
    参数：
        ec: 椭圆曲线对象
        G: 生成元
        Q: 目标点
        order: 生成元G的阶
    返回：
        k: 离散对数值
    """
    # 分解群阶
    factors = factor(order)
    print(f"1. 群阶分解：{order} = {factors}")
    
    # 中国剩余定理求解
    k_list = []
    mod_list = []
    
    for p, e in factors.items():
        pe = p**e
        print(f"\n2. 求解k mod {pe}")
        
        # 计算G_pe = (order/pe)*G，阶为pe
        G_pe = ec.point_multiply(G, order // pe)
        Q_pe = ec.point_multiply(Q, order // pe)
        
        # 求解k mod p^e
        k_pe = 0
        current = 0
        for i in range(e):
            # 计算Q_i = (Q - k_pe*G) * (order/p^i)
            k_pe_G = ec.point_multiply(G, k_pe)
            Q_minus = ec.point_add(Q, ec.point_multiply(k_pe_G, pe - 1))  # 减法：Q - k_pe*G
            Q_i = ec.point_multiply(Q_minus, order // (p**(i+1)))
            
            # 暴力求解k_i
            found = False
            for ki in range(p):
                if ec.point_multiply(G_pe, ki * (p**i)) == Q_i:
                    k_pe += ki * (p**i)
                    found = True
                    break
            if not found:
                return None
        
        k_list.append(k_pe)
        mod_list.append(pe)
        print(f"   k mod {pe} = {k_pe}")
    
    # 中国剩余定理合并结果
    from functools import reduce
    def crt(a_list, m_list):
        """中国剩余定理"""
        x = 0
        M = reduce(lambda a, b: a*b, m_list)
        for a_i, m_i in zip(a_list, m_list):
            M_i = M // m_i
            inv_M_i = pow(M_i, -1, m_i)
            x = (x + a_i * M_i * inv_M_i) % M
        return x
    
    k = crt(k_list, mod_list)
    return k

# 实验步骤1：创建弱椭圆曲线（群阶含小素因子）
p = 101  # 素数
a = 2
b = 3
ec = EllipticCurve(a, b, p)

# 选择小阶生成元（阶=10，含小素因子2和5）
G = (4, 9)
order = 10  # G的阶
print("=== Pohlig-Hellman攻击演示（弱椭圆曲线） ===")
print(f"椭圆曲线：y² = x³ + {a}x + {b} mod {p}")
print(f"生成元G={G}，阶={order}")

# 实验步骤2：生成目标点Q = k*G
k_true = 7
Q = ec.point_multiply(G, k_true)
print(f"\n真实私钥k = {k_true}，公钥Q = {Q}")

# 实验步骤3：Pohlig-Hellman攻击求解ECDLP
k_found = pohlig_hellman_ecdlp(ec, G, Q, order)
print(f"\nPohlig-Hellman求解结果：k = {k_found}")
print(f"验证：{k_found} * {G} = {ec.point_multiply(G, k_found)}")
print(f"攻击成功：{k_found == k_true}")

# 实验步骤4：对比暴力破解
print("\n=== 对比暴力破解 ===")
start = time.time()
k_brute = ecdlp_brute_force(ec, G, Q)
brute_time = time.time() - start

start = time.time()
k_ph = pohlig_hellman_ecdlp(ec, G, Q, order)
ph_time = time.time() - start

print(f"暴力破解耗时：{brute_time*1000:.2f}毫秒")
print(f"Pohlig-Hellman攻击耗时：{ph_time*1000:.2f}毫秒")
print(f"攻击效率提升：{brute_time/ph_time:.1f}倍")