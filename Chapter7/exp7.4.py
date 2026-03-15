# 实验4：密钥长度对比与性能测试
import time
import math

def mod_pow_time(base, exp, mod, iterations=100):
    """测试模幂运算的平均耗时"""
    start = time.time()
    for _ in range(iterations):
        pow(base, exp, mod)
    end = time.time()
    return (end - start) / iterations

def point_multiply_time(ec, point, scalar, iterations=100):
    """测试椭圆曲线点乘的平均耗时（复用实验3的EllipticCurve类）"""
    start = time.time()
    for _ in range(iterations):
        ec.point_multiply(point, scalar)
    end = time.time()
    return (end - start) / iterations

# 实验步骤1：密钥长度对比
print("=== 安全等效密钥长度对比 ===")
key_sizes = {
    "128位安全强度": {"RSA": 2048, "ECC": 256},
    "192位安全强度": {"RSA": 4096, "ECC": 384},
    "256位安全强度": {"RSA": 15360, "ECC": 521}
}

for security_level, sizes in key_sizes.items():
    rsa_size = sizes["RSA"]
    ecc_size = sizes["ECC"]
    ratio = rsa_size / ecc_size
    print(f"{security_level}:")
    print(f"  RSA密钥长度：{rsa_size}位，ECC密钥长度：{ecc_size}位")
    print(f"  ECC密钥长度仅为RSA的{1/ratio:.2%}（{ratio:.1f}倍差距）")
    print()

# 实验步骤2：运算性能对比（模拟）
print("=== 运算性能对比（模拟） ===")
# 模拟RSA模幂运算（2048位密钥）
rsa_exp = 65537  # 常用RSA公钥指数
rsa_mod = 2**2048 - 12345  # 模拟2048位模数
rsa_time = mod_pow_time(2, rsa_exp, rsa_mod, iterations=10)
print(f"RSA-2048模幂运算平均耗时：{rsa_time*1000:.2f}毫秒")

# 模拟ECC点乘运算（256位）
from experiment3 import EllipticCurve  # 复用实验3的椭圆曲线类
p = 2**256 - 2**224 + 2**192 + 2**96 - 1  # NIST P-256素数
a = -3
b = 0x5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B
ec_p256 = EllipticCurve(a, b, p)
G = (0x6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296,
     0x4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5)
ecc_time = point_multiply_time(ec_p256, G, 123456789, iterations=10)
print(f"ECC-256点乘运算平均耗时：{ecc_time*1000:.2f}毫秒")

# 性能提升倍数
speedup = rsa_time / ecc_time
print(f"\nECC-256相比RSA-2048性能提升：{speedup:.1f}倍")

# 实验步骤3：存储/带宽对比
print("\n=== 存储/带宽对比 ===")
# 密钥存储大小（字节）
rsa_2048_size = 2048 / 8  # 256字节
ecc_256_size = 256 / 8     # 32字节
print(f"RSA-2048密钥存储大小：{rsa_2048_size}字节")
print(f"ECC-256密钥存储大小：{ecc_256_size}字节")
print(f"存储节省：{100 - (ecc_256_size/rsa_2048_size)*100:.1f}%")

# 签名长度对比
rsa_signature_size = 2048 / 8  # 256字节
ecc_signature_size = 256 / 4   # 64字节（ECDSA签名）
print(f"\nRSA-2048签名长度：{rsa_signature_size}字节")
print(f"ECDSA-256签名长度：{ecc_signature_size}字节")
print(f"带宽节省：{100 - (ecc_signature_size/rsa_signature_size)*100:.1f}%")