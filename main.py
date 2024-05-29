import matplotlib.pyplot as plt
import numpy as np
import os
import shutil
import video_generator

# Nastavitve
h = 20  # Višina grafa
w = 20  # Dolžina grafa
N = 10  # Slika grafa na vsak N korak
stop = True  # Program se samodejno ustavi ko vsi objekti zapustijo graf

# Začetek programa
G = 6
dt = 0.001
tmax = N  # Če je tmax = N dobimo vedno 1000 slik

# telo 1
T1 = (-2.0, 0.0)
F1 = (0.0, 0.0)
V1 = (0.0, -0.01)
A1 = (0.0, 0.0)

# telo 2
T2 = (0.02, 0.0)
F2 = (0.0, 0.0)
V2 = (0.0, 1.0)
A2 = (0.0, 0.0)

# telo 3
T3 = (2.0, 0.0)
F3 = (0.0, 0.0)
V3 = (0.0, -0.64)
A3 = (0.0, 0.0)

# Shranjevanje prejšnjih lokacij
traj1 = [T1]
traj2 = [T2]
traj3 = [T3]


def razdalja(a, b):
    return np.sqrt((a[0] - b[0]) ** 2.0 + (a[1] - b[1]) ** 2.0)


def razdaljaxy(a, b):
    return np.abs(a[0] - b[0]), np.abs(a[1] - b[1])


def izbris_slik(dir):
    for file in os.listdir(dir):
        file_path = os.path.join(dir, file)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Izbris ni uspel {file_path}. Vzrok: {e}')


def narisi(tr1, tr2, tr3, ti):
    plt.figure(figsize=(w, h))
    plt.title("Simulacija treh teles")
    plt.xlim(-w / 2, w / 2)
    plt.ylim(-h / 2, h / 2)
    plt.grid(True)

    # Risanje poti za vsako telo
    tr1 = np.array(tr1)
    tr2 = np.array(tr2)
    tr3 = np.array(tr3)

    # telo 1
    plt.plot(tr1[:, 0], tr1[:, 1], color="black", label="Telo 1")
    plt.scatter(tr1[-1, 0], tr1[-1, 1], color="black")
    # telo 2
    plt.plot(tr2[:, 0], tr2[:, 1], color="blue", label="Telo 2")
    plt.scatter(tr2[-1, 0], tr2[-1, 1], color="blue")
    # telo 3
    plt.plot(tr3[:, 0], tr3[:, 1], color="red", label="Telo 3")
    plt.scatter(tr3[-1, 0], tr3[-1, 1], color="red")

    plt.legend()
    plt.savefig("frames/%.6d.png" % ti)
    plt.close()


t = 0.0
n = 0
p = N

# Glavna zanka
izbris_slik("frames")
print("Mapa frames izpraznjena.")

while t < tmax:
    t += dt

    r1 = razdalja(T1, T2)
    r1x, r1y = razdaljaxy(T1, T2)
    r2 = razdalja(T1, T3)
    r2x, r2y = razdaljaxy(T1, T3)
    r3 = razdalja(T2, T3)
    r3x, r3y = razdaljaxy(T2, T3)

    # Sile med telesi
    F12 = G * r1 ** (-1.0)
    F13 = G * r2 ** (-1.0)
    F23 = G * r3 ** (-1.0)

    # Sile po komponentah x in y
    F12x = F12 * (r1x / r1)
    F12y = F12 * (r1y / r1)
    F21x = -F12x
    F21y = -F12y

    F13x = F13 * (r2x / r2)
    F13y = F13 * (r2y / r2)
    F31x = -F13x
    F31y = -F13y

    F23x = F23 * (r3x / r3)
    F23y = F23 * (r3y / r3)
    F32x = -F23x
    F32y = -F23y

    # Sile na telesa
    F1 = (F12x + F13x, F12y + F13y)
    F2 = (F21x + F23x, F21y + F23y)
    F3 = (F31x + F32x, F31y + F32y)

    # Pospešek telesa 1 F = ma => a = F/m
    A1 = F1
    A2 = F2
    A3 = F3

    # Sprememba hitrosti
    dV1 = (A1[0] * dt, A1[1] * dt)
    dV2 = (A2[0] * dt, A2[1] * dt)
    dV3 = (A3[0] * dt, A3[1] * dt)

    # Hitrost
    V1 = (V1[0] + dV1[0], V1[1] + dV1[1])
    V2 = (V2[0] + dV2[0], V2[1] + dV2[1])
    V3 = (V3[0] + dV3[0], V3[1] + dV3[1])

    # Sprememba pozicije
    dxy1 = (V1[0] * dt, V1[1] * dt)
    dxy2 = (V2[0] * dt, V2[1] * dt)
    dxy3 = (V3[0] * dt, V3[1] * dt)

    T1 = (T1[0] + dxy1[0], T1[1] + dxy1[1])
    T2 = (T2[0] + dxy2[0], T2[1] + dxy2[1])
    T3 = (T3[0] + dxy3[0], T3[1] + dxy3[1])

    # Shranjevanje trenutnih lokacij
    traj1.append(T1)
    traj2.append(T2)
    traj3.append(T3)

    if p == N:
        narisi(traj1, traj2, traj3, n)
        if n % 5 == 0:
            os.system('cls')
            print(f"Obdelava podatkov: {n * 0.1:.1f}%")
        n += 1
        p = 0

    if np.abs(T1[0]) > w/2 and np.abs(T1[0]) > h/2 and stop:
        if np.abs(T2[0]) > w/2 and np.abs(T2[0]) > h/2:
            if np.abs(T3[0]) > w/2 and np.abs(T3[0]) > h/2:
                print("Vsi objekti so zapustili graf!")
                break

    p += 1

print("Začetek generiranja animacije.")
video_generator.generate_gif("frames", 1, "animacija1.gif")
print("GIF animacija ustvarjena!")
