# 实验3：小子群攻击验证（非原根导致的安全坍缩）
import math

# 复用实验1的fast_pow函数
def fast_pow(base, exponent, mod):
    result = 1
    base = base % mod
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % mod
        exponent = exponent >> 1
        base = (base * base) % mod
    return result

def generate_subgroup(g, p):
    """生成由g生成的模p乘法子群（展示元素范围）"""
    subgroup = set()
    current = 1
    while current not in subgroup:
        subgroup.add(current)
        current = (current * g) % p
    return sorted(list(subgroup))

def dh_key_exchange(p, g, a, b):
    """模拟DH密钥交换：返回双方计算的共享密钥"""
    # 甲方：私钥a，公钥A = g^a mod p
    A = fast_pow(g, a, p)
    # 乙方：私钥b，公钥B = g^b mod p
    B = fast_pow(g, b, p)
    # 甲方计算共享密钥：B^a mod p
    key_a = fast_pow(B, a, p)
    # 乙方计算共享密钥：A^b mod p
    key_b = fast_pow(A, b, p)
    return key_a, key_b, A, B

# 测试用例（对应课件攻击实例：p=17, g=4）
if __name__ == "__main__":
    # 场景1：使用非原根g=4（模17），验证小子群生成
    p = 17
    g_invalid = 4  # 非原根，阶为4
    subgroup = generate_subgroup(g_invalid, p)
    print(f"非原根g={g_invalid}生成的子群（模{p}）：{subgroup}")
    print(f"子群规模：{len(subgroup)}，完整群规模：{p-1}，安全空间坍缩{((p-1)-len(subgroup))/(p-1)*100:.0f}%")
    
    # 场景2：模拟DH密钥交换（非原根导致密钥空间极小）
    a = 3  # 甲方私钥
    b = 5  # 乙方私钥
    key_a, key_b, A, B = dh_key_exchange(p, g_invalid, a, b)
    print(f"\nDH密钥交换（非原根g={g_invalid}）：")
    print(f"甲方公钥A={A}，乙方公钥B={B}")
    print(f"甲方计算密钥：{key_a}，乙方计算密钥：{key_b}")
    
    # 场景3：暴力破解小子群密钥（仅需遍历子群元素）
    print("\n暴力破解小子群密钥（遍历所有可能私钥）：")
    target_pub = A  # 目标公钥
    for candidate in range(1, len(subgroup)+1):
        if fast_pow(g_invalid, candidate, p) == target_pub:
            print(f"破解成功！私钥为：{candidate}")
            break