# Tạo các file âm thanh chưởng bóng hồng vào Assets/Resources/Audio (22050 Hz, mono, 16-bit).
# Chạy lại: python3 Tools/make_bubble_sfx.py   (muốn đổi âm sắc thì chỉnh các hàm bên dưới)
import math, random, struct, wave, os

SR = 22050
OUT = os.path.join(os.path.dirname(__file__), "..", "Assets", "Resources", "Audio")
random.seed(7)

def save(name, samples, peak=0.8):
    m = max(1e-9, max(abs(s) for s in samples))
    data = b"".join(struct.pack("<h", int(max(-1, min(1, s / m * peak)) * 32767)) for s in samples)
    with wave.open(os.path.join(OUT, name + ".wav"), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(data)

def env(i, n, attack=0.01, release=0.3):
    t = i / SR; d = n / SR
    a = min(1.0, t / attack) if attack > 0 else 1.0
    r = min(1.0, (d - t) / (d * release)) if release > 0 else 1.0
    return a * max(0.0, r)

def sweep(n, f0, f1, power=1.0):
    ph = 0.0; out = []
    for i in range(n):
        f = f0 + (f1 - f0) * (i / n) ** power
        ph += 2 * math.pi * f / SR
        out.append(ph)
    return out

# 1) Gồng khí: tiếng ngân dâng cao dần + rung (0.9 s)
n = int(0.9 * SR); ph = sweep(n, 220, 760, 1.6); s = []
for i in range(n):
    trem = 0.75 + 0.25 * math.sin(2 * math.pi * (6 + 14 * i / n) * i / SR)
    v = math.sin(ph[i]) + 0.5 * math.sin(ph[i] * 2.01) + 0.25 * math.sin(ph[i] * 3.0)
    s.append(v * trem * env(i, n, 0.05, 0.15) * (0.4 + 0.6 * i / n))
save("bubble_charge", s, 0.6)

# 2) Bắn chưởng: "bloop" bóng nước đi xuống + hơi gió (0.3 s)
n = int(0.3 * SR); ph = sweep(n, 1100, 260, 0.6); s = []
for i in range(n):
    noise = (random.random() * 2 - 1) * 0.25 * (1 - i / n)
    s.append((math.sin(ph[i]) + 0.4 * math.sin(ph[i] * 2) + noise) * env(i, n, 0.003, 0.9))
save("bubble_shoot", s, 0.8)

# 3) Bắt chưởng: tiếng chuông sáng hai tầng + quét lên (0.6 s)
n = int(0.6 * SR); ph = sweep(n, 500, 1500, 0.5); s = []
for i in range(n):
    t = i / SR
    bell = math.sin(2 * math.pi * 1318 * t) * math.exp(-t * 7) + 0.7 * math.sin(2 * math.pi * 1976 * t) * math.exp(-t * 9) \
         + 0.5 * math.sin(2 * math.pi * 2637 * t) * math.exp(-t * 12)
    whoosh = math.sin(ph[i]) * 0.5 * math.exp(-t * 8)
    s.append((bell + whoosh) * env(i, n, 0.002, 0.2))
save("bubble_catch", s, 0.85)

# 4) Bóng vàng trúng boss: tiếng đấm trầm + tiếng lấp lánh (0.5 s)
n = int(0.5 * SR); s = []
for i in range(n):
    t = i / SR
    boom = math.sin(2 * math.pi * (140 * math.exp(-t * 5) + 45) * t) * math.exp(-t * 6)
    crack = (random.random() * 2 - 1) * math.exp(-t * 30) * 0.8
    spark = sum(math.sin(2 * math.pi * f * t) for f in (1568, 2093, 2637)) * math.exp(-t * 10) * 0.25
    s.append((boom * 1.2 + crack + spark) * env(i, n, 0.001, 0.15))
save("bubble_hit", s, 0.95)

# 5) Bóng nổ: "póc" ngắn (0.12 s)
n = int(0.12 * SR); ph = sweep(n, 700, 1500, 0.4); s = []
for i in range(n):
    noise = (random.random() * 2 - 1) * 0.35 * math.exp(-i / SR * 40)
    s.append((math.sin(ph[i]) * math.exp(-i / SR * 28) + noise) * env(i, n, 0.001, 0.3))
save("bubble_pop", s, 0.7)

# 6) Báo hiệu "bắt ngay!": hai tiếng tick sáng (0.18 s)
n = int(0.18 * SR); s = []
for i in range(n):
    t = i / SR; f = 1760 if t < 0.08 else 2349
    tt = t if t < 0.08 else t - 0.08
    s.append(math.sin(2 * math.pi * f * t) * math.exp(-tt * 40))
save("bubble_tick", s, 0.55)
print("done")
