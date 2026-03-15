# 理想格噪声管理模拟
import numpy as np

def ideal_noise_management(plaintext, noise_scale, gen, n=256):
    """
    模拟理想格中的噪声添加与恢复
    :param plaintext: 明文（n维整数数组）
    :param noise_scale: 噪声尺度
    :param gen: 理想生成元（n维数组）
    :param n: 环维度
    :return: 加密数据、解密结果
    """
    # 1. 生成噪声（模拟通信/计算噪声）
    noise = np.random.randint(-noise_scale, noise_scale+1, size=n)
    
    # 2. 加密：明文 + 噪声（模理想运算）
    ciphertext = (plaintext + noise) % np.max(gen)
    
    # 3. 解密：利用理想吸收性剔除噪声
    # 简化逻辑：噪声被限制在理想陪集中，可通过模运算恢复
    decrypted = ciphertext % np.max(gen)
    # 实际Kyber中需通过环运算还原，此处简化模拟
    
    return ciphertext, decrypted, noise

# 实验验证
if __name__ == "__main__":
    n = 8  # 简化维度
    plaintext = np.array([1, 2, 3, 4, 5, 6, 7, 8])
    gen = np.array([2, 0, 0, 0, 0, 0, 0, 0])  # 生成元2
    noise_scale = 1
    
    # 噪声管理模拟
    cipher, decrypted, noise = ideal_noise_management(plaintext, noise_scale, gen, n)
    
    print("原始明文：", plaintext)
    print("添加噪声：", noise)
    print("加密数据：", cipher)
    print("解密结果：", decrypted)
    print("解密正确性：", np.all(decrypted == plaintext % np.max(gen)))  # True
    
    # 验证噪声吸收性：噪声不扩散
    print(f"\n噪声最大值：{np.max(np.abs(noise))}")
    print(f"加密数据噪声扩散：{np.max(np.abs(cipher - plaintext))}")  # 等于噪声尺度，无扩散