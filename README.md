# Softmax Load Balancer

[![Python](https://img.shields.io/badge/python-3.x-blue.svg)]()
[![Algorithm](https://img.shields.io/badge/algorithm-softmax%20action%20selection-orange.svg)]()
[![Topic](https://img.shields.io/badge/topic-reinforcement%20learning-purple.svg)]()
[![Domain](https://img.shields.io/badge/domain-distributed%20systems-green.svg)]()

Klasik Round-Robin veya Random algoritmalarının aksine, geçmiş performans verisine dayalı olasılıksal sunucu seçimi yapan bir istemci taraflı yük dengeleyici.

---

## Problem

Gerçek dünyada sunucu gecikmeleri (latency) sabite değildir; yük değişir, donanım farklılıkları olur, ağ koşulları dalgalanır. Bu nedenle statik dağıtım algoritmaları optimal değildir.

Bu proje şu soruyu yanıtlar:  
**"Geçmiş gözlemlerden öğrenerek, bir sonraki isteği en hızlı sunucuya nasıl yönlendiririz?"**

---

## Yaklaşım

Reinforcement Learning'deki **Multi-Armed Bandit** probleminden ilham alınmıştır.

Her sunucu bir "kol" (arm) olarak modellenir. Ajan, her istekte hangi sunucuyu seçeceğine dair bir karar verir; gözlemlediği gecikme süresine göre öğrenir ve bir sonraki kararını günceller.

### Softmax Action Selection

Sunucular arasında olasılıksal seçim yapılır. Düşük gecikmeli (yüksek ödüllü) sunucular daha yüksek seçilme olasılığı kazanır; ancak diğer sunucular tamamen göz ardı edilmez (exploration devam eder).

```
P(server_i) = exp(Q(i) / τ) / Σ exp(Q(j) / τ)
```

- `Q(i)` → Sunucu i'nin tahmini ortalama gecikmesi (negatif ödül)  
- `τ` (temperature) → Keşif/sömürü dengesini kontrol eder. Yüksek τ = daha eşit dağılım, düşük τ = greedy seçim

### Q-Değeri Güncelleme

Non-stationary ortamlara uygun **sabit öğrenme oranı (constant step-size)** kullanılır:

```
Q(A) ← Q(A) + α × [Reward − Q(A)]
```

- `α = 0.1` → Yakın geçmişe daha fazla ağırlık verir, eski gözlemleri unutur
- `Reward = −latency` → Gecikme minimizasyonu, ödül maksimizasyonuna dönüştürülür

---

## Ortam (NonStationaryEnvironment)

Sunucu gecikmeleri **random walk** ile zamanla değişir; her adımda Gaussian gürültü eklenir. Bu sayede gerçek dünya koşulları simüle edilir.

```
mean_latency[i] += Gaussian(0, 1.0)   # zamanla kayma
observed_latency  = Gaussian(mean, 5.0) # ölçüm gürültüsü
```

---

## Kurulum ve Çalıştırma

```bash
# Gereksinim yok, sadece Python 3 standart kütüphanesi kullanılıyor
python main.py
```

**Örnek çıktı:**

```
5 sunucu için Softmax Load Balancing simülasyonu başlatılıyor...
Toplam İstek Sayısı: 10000

--- Simülasyon Tamamlandı ---
Ortalama Gecikme (Average Latency): 38.74 ms

Sunucuların Son Q-Değerleri:
  Sunucu 0: Q-Değeri = -41.23  (Öngörülen Ortalama Gecikme ~ 41.23 ms)
  Sunucu 1: Q-Değeri = -35.87  (Öngörülen Ortalama Gecikme ~ 35.87 ms)
  ...
```

---

## Parametreler

| Parametre | Varsayılan | Açıklama |
|-----------|-----------|----------|
| `K_SERVERS` | 5 | Sunucu sayısı |
| `NUM_REQUESTS` | 10 000 | Toplam istek sayısı |
| `temperature (τ)` | 10.0 | Keşif/sömürü dengesi |
| `alpha (α)` | 0.1 | Öğrenme hızı |

---

## Dosya Yapısı

```
├── environment.py   # Non-stationary sunucu ortamı simülasyonu
├── balancer.py      # Softmax Load Balancer (Q-learning + action selection)
└── main.py          # Simülasyon döngüsü ve çıktılar
```

---

## Neden Round-Robin veya Random Değil?

| Algoritma | Sunucu Performansını Öğrenir mi? | Non-Stationary Ortam | Exploration |
|-----------|----------------------------------|----------------------|-------------|
| Round-Robin | ✗ | ✗ | — |
| Random | ✗ | ✗ | — |
| **Softmax (bu proje)** | ✓ | ✓ | ✓ |

Round-Robin her sunucuya eşit güvenir; Random hiçbir şey öğrenmez. Softmax ise zamanla kötüleşen bir sunucuyu fark eder, ona daha az istek yönlendirir — ama tamamen de kesmez, çünkü ileride toparlanabilir. Bu denge, `temperature` parametresiyle kontrol edilir.

---

## Geliştirme Fikirleri

- `temperature` parametresine **decay** eklemek: başta daha fazla keşif, zamanla daha kararlı seçim
- **UCB (Upper Confidence Bound)** algoritmasıyla karşılaştırmalı benchmark
- Gerçek bir HTTP sunucusuyla entegrasyon (örn. `aiohttp` ile async istek simülasyonu)
---
