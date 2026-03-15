# 实验3：椭圆曲线点运算与ECDLP基础
import math

class EllipticCurve:
    """椭圆曲线类（Weierstrass形式：y² = x³ + ax + b mod p）"""
    def __init__(self, a, b, p):
        """
        初始化椭圆曲线
        参数：
            a, b: 曲线参数
            p: 有限域模数（素数）
        """
        self.a = a
        self.b = b
        self.p = p
        # 验证判别式非零：Δ = -16(4a³ + 27b²) ≠ 0 mod p
        delta = -16 * (4 * a**3 + 27 * b**2)
        if delta % p == 0:
            raise ValueError("椭圆曲线判别式为0，是奇异曲线")
    
    def is_point_on_curve(self, point):
        """验证点是否在椭圆曲线上"""
        if point is None:  # 无穷远点
            return True
        x, y = point
        # 验证y² ≡ x³ + ax + b (mod p)
        lhs = (y * y) % self.p
        rhs = (x**3 + self.a * x + self.b) % self.p
        return lhs == rhs
    
    def point_add(self, p1, p2):
        """椭圆曲线点加法：P1 + P2"""
        # 处理无穷远点
        if p1 is None:
            return p2
        if p2 is None:
            return p1
        
        x1, y1 = p1
        x2, y2 = p2
        
        # 点加法规则
        if x1 == x2 and y1 == (-y2) % self.p:
            return None  # 相加得到无穷远点
        
        if x1 != x2:
            # 不同点相加
            lam = ((y2 - y1) * pow(x2 - x1, self.p - 2, self.p)) % self.p
        else:
            # 同一点加倍
            lam = ((3 * x1**2 + self.a) * pow(2 * y1, self.p - 2, self.p)) % self.p
        
        x3 = (lam**2 - x1 - x2) % self.p
        y3 = (lam * (x1 - x3) - y1) % self.p
        
        return (x3, y3)
    
    def point_multiply(self, point, scalar):
        """椭圆曲线点乘：k * P（快速幂算法）"""
        if scalar == 0:
            return None
        if point is None:
            return None
        
        # 二进制快速幂实现
        result = None
        current = point
        scalar_bin = bin(scalar)[2:]  # 转为二进制
        
        for bit in scalar_bin:
            # 加倍
            result = self.point_add(result, result) if result is not None else None
            # 加当前点（如果bit为1）
            if bit == '1':
                result = self.point_add(result, current)
        
        return result

def ecdlp_brute_force(ec, G, Q):
    """暴力枚举求解ECDLP：k*G = Q"""
    # 简单暴力枚举（仅用于小阶群演示）
    current = None
    k = 0
    while True:
        if current == Q:
            return k
        current = ec.point_add(current, G)
        k += 1
        # 防止无限循环（实际应限制群阶）
        if k > 10000:
            return None

# 实验步骤1：初始化椭圆曲线（NIST P-256简化版，小素数演示）
# 注意：实际ECC使用大素数，此处用小素数仅作演示
p = 23  # 小素数模数
a = 1   # 曲线参数
b = 1   # 曲线参数
ec = EllipticCurve(a, b, p)
print("=== 椭圆曲线基础实验 ===")
print(f"椭圆曲线：y² = x³ + {a}x + {b} mod {p}")

# 实验步骤2：验证点是否在曲线上
P = (1, 7)
Q = (2, 6)
print(f"\n1. 验证点{P}是否在曲线上：{ec.is_point_on_curve(P)}")
print(f"   验证点{Q}是否在曲线上：{ec.is_point_on_curve(Q)}")

# 实验步骤3：点加法运算
R = ec.point_add(P, Q)
print(f"\n2. 点加法：{P} + {Q} = {R}")
print(f"   验证结果点是否在曲线上：{ec.is_point_on_curve(R)}")

# 实验步骤4：点乘运算
k = 3
kP = ec.point_multiply(P, k)
print(f"\n3. 点乘：{k} * {P} = {kP}")
print(f"   验证：{P} + {P} + {P} = {ec.point_add(ec.point_add(P, P), P)}")

# 实验步骤5：ECDLP暴力求解演示（仅小阶群）
# 选择小阶生成元
G = (1, 7)
k_true = 5
Q_target = ec.point_multiply(G, k_true)
print(f"\n4. ECDLP演示：已知G={G}, Q={Q_target}，求解k使得k*G=Q")
k_found = ecdlp_brute_force(ec, G, Q_target)
print(f"   真实k值：{k_true}，求解结果：{k_found}")
print(f"   验证：{k_found} * {G} = {ec.point_multiply(G, k_found)}")