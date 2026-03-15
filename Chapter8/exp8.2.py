# 实验2：有限域椭圆曲线点集枚举
def legendre_symbol(n, p):
    """计算勒让德符号，判断n是否为F_p的二次剩余"""
    ls = pow(n, (p - 1) // 2, p)
    if ls == p - 1:
        return -1  # 非剩余
    return ls       # 0: n≡0 mod p；1: 二次剩余

def enumerate_ec_points(a, b, p):
    """枚举F_p上椭圆曲线y²=x³+ax+b的所有点（含无穷远点）"""
    # 先验证非奇异性
    if not is_non_singular(a, b, p):
        print("无法枚举奇异曲线的点集！")
        return []
    
    points = []
    # 遍历所有x∈F_p
    for x in range(p):
        # 计算右侧值: x³ + ax + b mod p
        rhs = (pow(x, 3, p) + a * x + b) % p
        
        # 判断rhs是否为二次剩余
        ls = legendre_symbol(rhs, p)
        if ls == -1:
            continue  # 无对应的y
        elif ls == 0:
            # y=0，仅一个点
            points.append((x, 0))
        else:
            # 求解y²≡rhs mod p（简化版：遍历找解）
            for y in range(1, p):
                if (y * y) % p == rhs:
                    points.append((x, y))
                    points.append((x, p - y))  # 对称点
                    break  # 找到一个即可，另一个是p-y
    
    # 补充无穷远点标识
    points.append("O (无穷远点)")
    return points

# 测试：枚举F_7上y²=x³+2x+3的点集
print("=== 枚举F_7上y²=x³+2x+3的点集 ===")
points = enumerate_ec_points(a=2, b=3, p=7)
print(f"所有点：{points}")
print(f"群阶（点集大小）：{len(points)}")