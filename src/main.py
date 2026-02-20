from environment import NonStationaryEnvironment
from balancer import SoftmaxLoadBalancer

def main():
    K_SERVERS = 5
    NUM_REQUESTS = 10000

    env = NonStationaryEnvironment(k=K_SERVERS)
    # Temperature (sıcaklık) paramteresi keşfetme (exploration) oranını belirler
    load_balancer = SoftmaxLoadBalancer(k=K_SERVERS, temperature=10.0, alpha=0.1)

    print(f"{K_SERVERS} sunucu için Softmax Load Balancing simülasyonu başlatılıyor...")
    print(f"Toplam İstek Sayısı: {NUM_REQUESTS}")

    for _ in range(NUM_REQUESTS):
        # 1. Softmax yöntemine göre kullanılacak sunucuyu seç
        selected_server = load_balancer.select_server()
        
        # 2. İsteği simüle et ve gecikme süresini (latency) al
        latency = env.get_latency(selected_server)
        
        # 3. Elde edilen gecikme süresine göre ajanın Q değerlerini güncelle
        load_balancer.update_q_value(selected_server, latency)

    # İstatistikler
    avg_latency = load_balancer.total_latency / load_balancer.total_requests

    print("\n--- Simülasyon Tamamlandı ---")
    print(f"Ortalama Gecikme (Average Latency): {avg_latency:.2f} ms")
    print("\nSunucuların Son Q-Değerleri:")
    for i, q in enumerate(load_balancer.q_values):
        print(f"  Sunucu {i}: Q-Değeri = {q:.2f} (Öngörülen Ortalama Gecikme ~ {-q:.2f} ms)")

if __name__ == '__main__':
    main()
