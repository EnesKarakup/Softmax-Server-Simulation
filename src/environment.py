import random

class NonStationaryEnvironment:
    """K sunuculu, gürültülü ve performansı zamanla değişen (non-stationary) ortam."""
    def __init__(self, k):
        self.k = k
        # Sunucuların başlangıçtaki ortalama gecikme süreleri rastgele atanıyor (örn. 20ms ile 100ms arası)
        self.mean_latencies = [random.uniform(20.0, 100.0) for _ in range(k)]

    def get_latency(self, server):
        # Her bir istekte sunucuların performansını rastgele yürüyüş (random walk) ile değiştir
        for i in range(self.k):
            self.mean_latencies[i] += random.gauss(0, 1.0)
            # Gecikme süresi mantıksız seviyelere düşmesin diye alt sınır belirliyoruz
            self.mean_latencies[i] = max(5.0, self.mean_latencies[i])

        # Seçilen sunucu için gürültülü (noisy) bir gecikme değeri döndür
        latency = random.gauss(self.mean_latencies[server], 5.0)
        return max(1.0, latency)
