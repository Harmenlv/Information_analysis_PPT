# 实验4：标量乘与ECDLP特性验证
def ec_scalar_mult(k, point, a, p):
    """
    椭圆曲线标量乘：k*P = P⊕P⊕...⊕P（k次）
    优化实现：二进制法（快速幂思想）
    """
    if k == 0 or point == "O":
        return "O"
    
    # 初始化结果为无穷远点
    result = "O"
    current = point
    
    # 二进制分解k，逐位处理
    while k > 0:
        if k % 2 == 1:
            result = ec_point_add(result, current, a, p)
        # 倍点
        current = ec_point_add(current, current, a, p)
        k = k // 2
    
    return result

# 测试1：标量乘计算（正向快速）
print("=== 测试1：标量乘正向计算 ===")
a, p = 2, 7
G = (2, 1)  # 基点
k = 3       # 标量
kG = ec_scalar_mult(k, G, a, p)
print(f"3*{G} = {kG}（计算过程：2G⊕G = (3,6)⊕(2,1) = {ec_point_add((3,6), G, a, p)}）")

# 测试2：ECDLP反向求解难度演示（暴力枚举）
print("\n=== 测试2：ECDLP反向求解（暴力枚举） ===")
target = (2, 6)  # 目标点：3G=(2,6)
found_k = None
# 暴力枚举k∈[1, 群阶-1]（群阶=6）
for candidate_k in range(1, 6):
    candidate_point = ec_scalar_mult(candidate_k, G, a, p)
    print(f"尝试k={candidate_k}: {candidate_point}")
    if candidate_point == target:
        found_k = candidate_k
        break

if found_k:
    print(f"找到离散对数k={found_k}（目标点{target} = {found_k}*{G}）")
else:
    print("未找到离散对数")

# 说明：小域下可暴力破解，但256位大域下√(2^256)=2^128次运算，现有算力无法完成
print("\n=== ECDLP安全说明 ===")
print("小有限域（如F_7）可暴力破解，但256位素数域下：")
print("- 正向标量乘：O(log2(2^256))=256次运算，毫秒级完成")
print("- 反向ECDLP：最优算法需约2^128次运算，现有算力无法完成")