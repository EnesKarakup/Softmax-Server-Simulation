import math
import random

class SoftmaxLoadBalancer:
    def __init__(self, k, temperature=10.0, alpha=0.1):
        self.k = k
        self.temperature = temperature
        self.alpha = alpha  # Sabit öğrenme oranı (constant step-size)
        
        # Başlangıç Q değerlerini sıfır olarak atıyoruz
        self.q_values = [0.0 for _ in range(k)]
        
        self.total_latency = 0.0
        self.total_requests = 0

    def select_server(self):
        # Softmax Action Selection
        # math.exp hesaplamalarında aşırı büyük sayılar çıkmasını (overflow) önlemek için max_q çıkarılır
        max_q = max(self.q_values)
        
        exps = [math.exp((q - max_q) / self.temperature) for q in self.q_values]
        sum_exps = sum(exps)
        probabilities = [e / sum_exps for e in exps]
        
        # Olasılıklara göre rulet tekerleği (Roulette Wheel) seçimi
        rand = random.random()
        cumulative_prob = 0.0
        for i, p in enumerate(probabilities):
            cumulative_prob += p
            if rand <= cumulative_prob:
                return i
        return self.k - 1

    def update_q_value(self, server, latency):
        # Bekleme süresini minimize etmek istediğimiz için latency'yi negatif bir ödüle dönüştürüyoruz
        reward = -latency
        
        # Constant step-size (sabit öğrenme oranı) ile hedef Q değerini güncelleme
        # Q(A) <- Q(A) + alpha * [Reward - Q(A)]
        self.q_values[server] += self.alpha * (reward - self.q_values[server])
        
        self.total_latency += latency
        self.total_requests += 1
