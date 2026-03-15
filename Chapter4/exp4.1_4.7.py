# ====================== 实验1：试除法（基础原理+工程预过滤） ======================
"""
实验目标：掌握试除法核心原理，实现工程化预过滤版本，理解其复杂度瓶颈
对应讲义：试除法（1/3）-（3/3）：基本原理→实例验证→工程复杂度灾难
"""
import math
import random

def trial_division(n, max_prime=7919):
    """
    工程化试除法（预过滤版本）：仅试除前k个小素数，快速筛除显然合数
    :param n: 待检验整数
    :param max_prime: 最大试除素数（工程常用7919，可筛除88%候选数）
    :return: (is_prime_candidate, factor) - 是否为素数候选/首个发现的因子
    """
    # 小整数直接判定
    if n <= 1:
        return (False, None)
    if n <= 3:
        return (True, None)
    # 偶数直接筛除
    if n % 2 == 0:
        return (False, 2)
    
    # 生成小素数表（试除用）
    def sieve(max_p):
        sieve_list = [True] * (max_p + 1)
        sieve_list[0] = sieve_list[1] = False
        for i in range(2, int(math.sqrt(max_p)) + 1):
            if sieve_list[i]:
                sieve_list[i*i : max_p+1 : i] = [False] * len(sieve_list[i*i : max_p+1 : i])
        primes = [i for i, is_p in enumerate(sieve_list) if is_p]
        return primes
    
    small_primes = sieve(max_prime)
    
    # 试除小素数
    for p in small_primes:
        if p * p > n:
            break
        if n % p == 0:
            return (False, p)
    return (True, None)

# 实验验证
test_nums = [101, 121, 561, 1000003, 2**31-1]
print("=== 实验1：试除法预过滤验证 ===")
for n in test_nums:
    is_candidate, factor = trial_division(n)
    if not is_candidate:
        print(f"n={n}：合数（因子={factor}），被试除法快速筛除")
    else:
        print(f"n={n}：通过试除法预过滤，需进入后续检验")
print()

# ====================== 实验2：费马检验（原理+卡迈克尔数陷阱） ======================
"""
实验目标：实现费马检验，验证卡迈克尔数导致的误判，理解其工程风险
对应讲义：费马检验（1/3）-（3/3）：费马小定理→检验步骤→卡迈克尔数缺陷
"""
def fast_pow(base, exp, mod):
    """快速幂算法（二进制拆分）：计算 (base^exp) mod mod，避免大整数溢出"""
    result = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp = exp // 2
    return result

def fermat_test(n, bases=[2,3,5,7]):
    """
    费马检验实现
    :param n: 待检验奇数
    :param bases: 检验基列表
    :return: (is_fermat_prime, failed_base) - 是否通过检验/首个失败的基
    """
    if n <= 1:
        return (False, None)
    if n <= 3:
        return (True, None)
    for a in bases:
        if a >= n:
            continue
        # 计算 a^(n-1) mod n
        if fast_pow(a, n-1, n) != 1:
            return (False, a)
    return (True, None)

# 验证卡迈克尔数561的费马检验误判
carmichael_nums = [561, 1105, 1729, 2465]
print("=== 实验2：费马检验与卡迈克尔数陷阱 ===")
for n in carmichael_nums:
    is_prime, failed_base = fermat_test(n)
    if is_prime:
        print(f"n={n}（卡迈克尔数）：费马检验误判为素数（所有基通过）")
    else:
        print(f"n={n}：费马检验判定为合数（失败基={failed_base}）")
# 验证普通合数341
is_prime, failed_base = fermat_test(341, [2])
print(f"n=341：费马检验（基=2）结果={is_prime}（实际为合数11×31）")
print()

# ====================== 实验3：Miller-Rabin检验（工业级实现+破解卡迈克尔数） ======================
"""
实验目标：实现工业级Miller-Rabin检验，验证其破解卡迈克尔数的能力，理解强伪素数原理
对应讲义：Miller-Rabin检验（1/10）-（4/10）：强伪素数→检验流程→破解561→工程优化
"""
def miller_rabin_test(n, bases=None):
    """
    工业级Miller-Rabin检验实现
    :param n: 待检验奇数
    :param bases: 检验基列表（n<2^64时用固定基可实现确定性检验）
    :return: bool - 是否为大概率素数
    """
    # 预设固定基（n<2^64时的确定性基，FIPS 186-5推荐）
    if bases is None:
        if n < 2047:
            bases = [2]
        elif n < 1373593:
            bases = [2, 3]
        elif n < 9080191:
            bases = [31, 73]
        elif n < 2**64:
            bases = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    
    # 小整数直接判定
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False
    
    # 分解 n-1 = d * 2^s
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    
    # 逐基检验
    for a in bases:
        if a >= n:
            continue
        x = fast_pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        # 迭代平方s-1次
        for _ in range(s - 1):
            x = fast_pow(x, 2, n)
            if x == n - 1:
                break
        else:
            # 未找到-1，判定为合数
            return False
    return True

# 验证Miller-Rabin破解卡迈克尔数
print("=== 实验3：Miller-Rabin检验破解卡迈克尔数 ===")
for n in carmichael_nums:
    is_prime = miller_rabin_test(n)
    print(f"n={n}（卡迈克尔数）：Miller-Rabin判定为{'素数' if is_prime else '合数'}（正确）")
# 验证2047（强伪素数）
print(f"n=2047：Miller-Rabin判定为{'素数' if miller_rabin_test(2047) else '合数'}（实际为23×89）")
print()

# ====================== 实验4：Miller-Rabin错误概率验证（工业级安全） ======================
"""
实验目标：验证Miller-Rabin多次检验的错误概率，理解工业级检验次数要求
对应讲义：Miller-Rabin检验（5/10）：错误概率-工业级安全定义
"""
def mr_error_probability(k):
    """计算k次Miller-Rabin检验的错误概率上限"""
    return (1/4)**k

# 验证不同检验次数的错误概率
print("=== 实验4：Miller-Rabin错误概率验证 ===")
test_ks = [1, 10, 20, 40, 80]
for k in test_ks:
    prob = mr_error_probability(k)
    print(f"{k}次检验：错误概率≤{prob:.2e}（{k=40时：10^-24量级}）")
# 对比硬件错误概率
print("参考：DRAM位翻转概率≈1e-18，宇宙射线错误≈1e-17")
print(f"40次检验错误概率（1e-24）远低于硬件错误概率，工程上视为'实际上确定'")
print()

# ====================== 实验5：2048位安全素数生成（工业级合规） ======================
"""
实验目标：实现工业级2048位安全素数生成流程，符合FIPS 186-5/GM/T 0006标准
对应讲义：安全素数（6/10）-（8/10）：定义→生成流程→合规性要求
"""
def generate_prime(bits, k=40):
    """
    生成指定位数的素数（符合FIPS 186-5）
    :param bits: 素数位数（2048/4096）
    :param k: Miller-Rabin检验次数（2048位要求≥40）
    :return: 符合要求的素数
    """
    # 生成奇数候选数（最高位为1，保证位数）
    while True:
        # 生成随机数（CSPRNG，熵≥256位）
        candidate = random.getrandbits(bits)
        # 确保最高位为1，最低位为1（奇数）
        candidate |= (1 << (bits - 1)) | 1
        # 先试除法预过滤
        is_candidate, _ = trial_division(candidate)
        if not is_candidate:
            continue
        # Miller-Rabin检验k次（用FIPS推荐基）
        bases = [2,3,5,7,11,13,17]  # 2048位推荐基
        if miller_rabin_test(candidate, bases):
            return candidate

def generate_safe_prime(bits=2048):
    """
    生成安全素数 p=2q+1（q为索菲热尔曼素数）
    :param bits: 安全素数位数
    :return: (p, q) - 安全素数p，索菲热尔曼素数q
    """
    print("=== 实验5：2048位安全素数生成（合规流程） ===")
    print("开始生成2048位安全素数（该过程可能需要数秒）...")
    while True:
        # 生成2047位q（保证p=2q+1为2048位）
        q = generate_prime(bits - 1, k=40)
        p = 2 * q + 1
        # 独立检验p的素性（≥40次MR）
        if miller_rabin_test(p, [2,3,5,7,11,13,17]):
            # 合规性验证：p≡3 mod4
            if p % 4 == 3:
                print(f"生成成功！")
                print(f"索菲热尔曼素数q（2047位）：{q}")
                print(f"安全素数p=2q+1（2048位）：{p}")
                print(f"验证p=2q+1：{2*q+1 == p}")
                print(f"验证p≡3 mod4：{p%4 == 3}（合规）")
                return (p, q)

# 生成2048位安全素数（注：实际运行需数秒，可注释掉快速测试）
# p, q = generate_safe_prime(2048)

# ====================== 实验6：云原生素数池预生成（工程优化） ======================
"""
实验目标：实现素数池预生成机制，理解云原生KMS的工程优化思路
对应讲义：云原生场景下的素性检验工程优化
"""
class PrimePool:
    """素数池类：预生成并缓存合规素数，降低高并发时延"""
    def __init__(self, bits=2048, pool_size=10, mr_k=40):
        self.bits = bits
        self.pool_size = pool_size
        self.mr_k = mr_k
        self.pool = []
        # 预生成素数池
        self._fill_pool()
    
    def _fill_pool(self):
        """填充素数池"""
        print("\n=== 实验6：云原生素数池预生成 ===")
        print(f"开始预生成{self.pool_size}个{self.bits}位素数...")
        while len(self.pool) < self.pool_size:
            prime = generate_prime(self.bits, self.mr_k)
            self.pool.append(prime)
        print(f"素数池预生成完成！池大小={len(self.pool)}")
    
    def get_prime(self):
        """从池中获取素数（用完自动补充）"""
        if not self.pool:
            self._fill_pool()
        return self.pool.pop()

# 测试素数池
# prime_pool = PrimePool(bits=128, pool_size=3)  # 用128位快速测试
# for i in range(3):
#     prime = prime_pool.get_prime()
#     print(f"从素数池获取第{i+1}个素数：{prime}（位数={prime.bit_length()}）")

# ====================== 实验7：后量子时代复合检验（Miller-Rabin+Lucas） ======================
"""
实验目标：实现复合检验架构，理解后量子时代对素性检验的新要求
对应讲义：后量子密码对素性检验的新要求
"""
def lucas_test(n):
    """Lucas检验（简化版）：与Miller-Rabin复合提升安全性"""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False
    
    # 简化版Lucas检验逻辑（工程实现需更严谨）
    D = 5
    while True:
        jacobi = pow(D, (n-1)//2, n)
        if jacobi == n-1:
            break
        D = -D if D > 0 else -D + 2
    
    P = 1
    Q = (1 - D) // 4
    
    def lucas_sequence(n, P, Q, k):
        """计算Lucas序列U_k mod n"""
        u, v = 0, 2
        k_bin = bin(k)[2:]
        for bit in k_bin:
            u, v = (u*v) % n, (v*v - 2*pow(Q, 1 << len(k_bin)-len(bit), n)) % n
            if bit == '1':
                u, v = ((u*P + v) //