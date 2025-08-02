import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# Parâmetros físicos
mu_v = 1e-13            # Mobilidade de íons (m²/sV)
D = 10e-9               # Espessura do filme (10 nm)
R_ON = 1                # Resistência TiO2-x (Ohm)
R_OFF = 160             # Resistência TiO2  (Ohm)
V0 = 1                  # Amplitude da voltagem (V)
freq = 5                # Frequência (5 Hz)
omega = 2*np.pi*freq    # periodo (1 kHz)
w0 = 1e-9               # Largura inicial da região dopada (1 nm)


# Tempo de simulação
t_total = 2            # 1 s
h = 1e-4               # Passo de tempo (1 ms)
passo = int(t_total / h)

def mem(t, w):
    tensao = V0 * np.sin(omega * t)           # Fonte de tensão oscilando
    R = R_ON * (w / D) + R_OFF * (1 - w / D) 
    corrente = tensao / R                     # Lei de Ohm
    dwdt = mu_v * R_ON / D * corrente
    return dwdt

def rk4_step(func, t, w, h):
    k1 = func(t, w)
    k2 = func(t + h/2, w + h * k1/2)
    k3 = func(t + h/2, w + h * k2/2)
    k4 = func(t + h, w + h * k3)
    return w + h * (k1 + 2*k2 + 2*k3 + k4) / 6

t_arr = np.zeros(passo)
w_arr = np.zeros(passo)
V_arr = np.zeros(passo)
I_arr = np.zeros(passo)
R_arr = np.zeros(passo)

w = w0 # Condição inicial

# runge-kutta 4
for i in range(passo):
    t = i * h
    V_arr[i] = V0 * np.sin(omega * t)
    R_arr[i] = R_ON * (w / D) + R_OFF * (1 - w / D)
    I_arr[i] = V_arr[i] / R_arr[i]

    w = rk4_step(mem, t, w, h)
    w = np.clip(w, 0, D)  # Garante limites físicos

    # Armazenar valores
    t_arr[i] = t
    w_arr[i] = w

# Gráfico 1: Estado e Resistência
fig, ax1 = plt.subplots(figsize=(12, 6))

ymax = lambda arr: max(arr) + max(arr) * 5e-2

ax1.plot(t_arr, w_arr * 1e9, label='Largura w do material dopado (nm)', color='blue')
ax1.set_xlabel('Tempo (s)')
ax1.set_ylabel('Largura (nm)')
ax1.set_ylim(0, ymax(w_arr * 1e9))

ax2 = ax1.twinx()
ax2.plot(t_arr, R_arr, label='Resistência do memristor', color='red')
ax2.set_ylim(0, ymax(R_arr))
ax2.set_ylabel('Resistência (Ohm)')

ax1.grid(True)
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right')
plt.title('Evolução do Estado e Resistência')
plt.show()

fig1, ax3 = plt.subplots(figsize=(10, 6))

ax3.plot(t_arr, V_arr, label='Voltagem (V)', color='g')
ax3.set_xlabel('Tempo (s)')
ax3.set_ylabel('Voltagem( V)')

ax4 = ax3.twinx()
ax4.plot(t_arr, I_arr * 1e-3, label='Corrente (mA)', color='red')
ax4.set_ylabel('Corrente (mA)')

ax3.grid(True)

lines3, labels3 = ax3.get_legend_handles_labels()
lines4, labels4 = ax4.get_legend_handles_labels()
ax3.legend(lines3 + lines4, labels3 + labels4, loc='upper right')
plt.show()

# Gráfico 2: Histerese V-I
plt.figure(figsize=(12, 6))
diff = np.diff(I_arr)/np.diff(V_arr)  # dI/dV
sinal = np.sign(diff)  # Capturar o sinal
muda = np.where(np.diff(sinal) != 0)[0] + 1 #

v_partes = np.split(V_arr[:-1], muda)
i_partes = np.split(I_arr[:-1], muda)

n_partes = len(v_partes)
initial_size = 70
size_reduction = initial_size / n_partes

for i, (v_seg, i_seg) in enumerate(zip(v_partes, i_partes)):
    color = plt.cm.viridis(i/n_partes)
    size = initial_size - i*size_reduction # Minimum size of 10
    plt.scatter(v_seg, i_seg, color=color, s=size, label=f'Segment {i+1}')

plt.grid(True)
plt.show()

muda = np.where(np.diff(sinal) != 0)[0] + 1 #
print(muda)

"""#Layout dos Gráficos igual ao PAPER RK normal

"""

import matplotlib.gridspec as gridspec

# Criar a figura e o layout com 3 linhas
fig = plt.figure(figsize=(6, 8))
gs = gridspec.GridSpec(3, 1, height_ratios=[1.2, 1, 2.5], hspace=0.5)

# --- Gráfico 1: tensão e corrente vs tempo com eixos duplos ---
ax1 = fig.add_subplot(gs[0])
ax1.set_xlabel("Time")
ax1.set_ylabel("Tensão", color='blue')
ax1.tick_params(axis='y', labelcolor='blue')

ax1_right = ax1.twinx()
ax1_right.set_ylabel("Corrente", color='green')
ax1_right.tick_params(axis='y', labelcolor='green')

ax1.plot(t_arr, V_arr, label='Voltagem (V)', color='g')
ax1_right.plot(t_arr, I_arr * 1e-3, label='Corrente (mA)', color='red')

# --- Gráfico 2: w/D vs tempo ---
ax2 = fig.add_subplot(gs[1])
ax2.set_xlabel("Tempo")
ax2.set_ylabel("w/D")
ax2.set_ylim(-0.1, 1.1)  # como no artigo
ax2.plot(t_arr, w_arr/D, label='Tensão (V)', color='g')

# --- Gráfico 3: I vs V ---
diff = np.diff(I_arr) / np.diff(V_arr)
sinal = np.sign(diff)
muda = np.where(np.diff(sinal) != 0)[0] + 1
ax2.axhline(1, linestyle='--', color='black', linewidth=1)
ax2.axhline(0, linestyle='--', color='black', linewidth=1)

# Dividir os dados em segmentos baseados nos pontos onde a derivada muda de sinal
ax3 = fig.add_subplot(gs[2])

v_partes = np.split(V_arr[:-1], muda)
i_partes = np.split(I_arr[:-1], muda)

n_partes = len(v_partes)
initial_size = 1
size_reduction = initial_size / n_partes

for i, (v_seg, i_seg) in enumerate(zip(v_partes, i_partes)):
    color = plt.cm.viridis(i / n_partes)
    size = max(initial_size - i * size_reduction, 10)
    ax3.scatter(v_seg, i_seg, color=color, s=size, label=f'Segmento {i+1}')

ax3.set_xlabel('Tensão (V)')
ax3.set_ylabel('Corrente (I)')

V_arr_rk4 = V_arr
I_arr_rk4 = I_arr

# Exibir
plt.tight_layout()
plt.show()

# Após sua simulação anterior
import numpy as np

# Calcular potência instantânea
P = V_arr * I_arr

# Energia total "dissipada"
E_total = np.trapz(P, t_arr)

# Energia por ciclo
T = 2*np.pi / omega  # Período
num_ciclos = t_total / T
E_por_ciclo = E_total / num_ciclos

print(f"Energia dissipada por ciclo: {E_por_ciclo:.4e} Joules")

"""# RK Multi Passos"""

# reseta
t_arr = np.zeros(passo)
w_arr = np.zeros(passo)
V_arr = np.zeros(passo)
I_arr = np.zeros(passo)
R_arr = np.zeros(passo)

w = w0

# Para armazenar derivadas
f_arr = np.zeros(passo)

# Primeiros 2 passos com RK4 para iniciar o método multi-passos
for i in range(2):
    t = i * h
    V_arr[i] = V0 * np.sin(omega * t)
    R_arr[i] = R_ON * (w / D) + R_OFF * (1 - w / D)
    I_arr[i] = V_arr[i] / R_arr[i]
    f_arr[i] = mem(t, w)

    w = rk4_step(mem, t, w, h)
    w = np.clip(w, 0, D)
    t_arr[i] = t
    w_arr[i] = w

for i in range(2, passo):
    t = i * h
    V_arr[i] = V0 * np.sin(omega * t)
    R_arr[i] = R_ON * (w / D) + R_OFF * (1 - w / D)
    I_arr[i] = V_arr[i] / R_arr[i]

    # AB3
    w_next = w + (h / 12) * (23 * f_arr[i-1] - 16 * f_arr[i-2] + 5 * f_arr[i-3])
    w_next = np.clip(w_next, 0, D)

    t_arr[i] = t
    w_arr[i] = w_next

    # Atualiza f_arr com novo valor de derivada
    f_arr[i] = mem(t, w_next)

    # Atualiza w para próximo passo
    w = w_next

V_arr_ab3 = V_arr
I_arr_ab3 = I_arr

# Calcular a derivada dI/dV para identificar mudanças de inclinação
diff = np.diff(I_arr) / np.diff(V_arr)
sinal = np.sign(diff)
muda = np.where(np.diff(sinal) != 0)[0] + 1

# Dividir os dados em segmentos baseados nos pontos onde a derivada muda de sinal
v_partes = np.split(V_arr[:-1], muda)
i_partes = np.split(I_arr[:-1], muda)

n_partes = len(v_partes)
initial_size = 100
#size_reduction = initial_size / n_partes

# Criar a figura e o layout com 3 linhas
fig = plt.figure(figsize=(6, 8))
gs = gridspec.GridSpec(3, 1, height_ratios=[1.2, 1, 2.5], hspace=0.5)

# --- Gráfico 1: tensão e corrente vs tempo com eixos duplos ---
ax1 = fig.add_subplot(gs[0])
ax1.set_xlabel("Time")
ax1.set_ylabel("Tensão", color='blue')
ax1.tick_params(axis='y', labelcolor='blue')

ax1_right = ax1.twinx()
ax1_right.set_ylabel("Corrente", color='green')
ax1_right.tick_params(axis='y', labelcolor='green')

ax1.plot(t_arr, V_arr, label='Voltagem (V)', color='g')
ax1_right.plot(t_arr, I_arr * 1e-3, label='Corrente (mA)', color='red')

# --- Gráfico 2: w/D vs tempo ---
ax2 = fig.add_subplot(gs[1])
ax2.set_xlabel("Tempo")
ax2.set_ylabel("w/D")
ax2.set_ylim(-0.1, 1.1)  # como no artigo
ax2.plot(t_arr, w_arr/D, label='Tensão (V)', color='g')

# --- Gráfico 3: I vs V ---
diff = np.diff(I_arr) / np.diff(V_arr)
sinal = np.sign(diff)
muda = np.where(np.diff(sinal) != 0)[0] + 1
ax2.axhline(1, linestyle='--', color='black', linewidth=1)
ax2.axhline(0, linestyle='--', color='black', linewidth=1)

# Dividir os dados em segmentos baseados nos pontos onde a derivada muda de sinal
ax3 = fig.add_subplot(gs[2])

v_partes = np.split(V_arr[:-1], muda)
i_partes = np.split(I_arr[:-1], muda)

n_partes = len(v_partes)
initial_size = 1
size_reduction = initial_size / n_partes

for i, (v_seg, i_seg) in enumerate(zip(v_partes, i_partes)):
    color = plt.cm.viridis(i / n_partes)
    size = max(initial_size - i * size_reduction, 10)
    ax3.scatter(v_seg, i_seg, color=color, s=size, label=f'Segmento {i+1}')

ax3.set_xlabel('Tensão (V)')
ax3.set_ylabel('Corrente (I)')

# Exibir
plt.tight_layout()
plt.show()

# Calcular potência instantânea
P = V_arr * I_arr

# Energia total "dissipada"
E_total = np.trapz(P, t_arr)

# Energia por ciclo
T = 2*np.pi / omega  # Período
num_ciclos = t_total / T
E_por_ciclo = E_total / num_ciclos

print(f"Energia dissipada por ciclo: {E_por_ciclo:.4e} Joules")

"""# Passo Variado

"""

def adams_bashforth_4(func, t, w, h, f_hist):
    f_n, f_n1, f_n2, f_n3 = f_hist
    return w + h/24*(55*f_n - 59*f_n1 + 37*f_n2 - 9*f_n3)

passos = int(t_total / h)

t_arr = np.zeros(passos)
w_arr = np.zeros(passos)
V_arr = np.zeros(passos)
I_arr = np.zeros(passos)
R_arr = np.zeros(passos)

w = w0

# Inicialização com RK4 para os primeiros 4 pontos
f_history = np.zeros(4)  # Armazenará os últimos 4 valores de dw/dt

for i in range(4):
    t = i * h
    V_arr[i] = V0 * np.sin(omega * t)
    R_arr[i] = R_ON * (w / D) + R_OFF * (1 - w / D)
    I_arr[i] = V_arr[i] / R_arr[i]

    dwdt = mem(t, w)
    f_history[3-i] = dwdt  # Preenche do passado mais recente para o mais antigo

    w = rk4_step(mem, t, w, h)
    w = np.clip(w, 0, D)

    t_arr[i] = t
    w_arr[i] = w

# Simulação principal com Adams-Bashforth (multi-passos)
for i in range(4, passos):
    t = i * h

    # Atualiza estado com Adams-Bashforth
    w = adams_bashforth_4(mem, t, w_arr[i-1], h, f_history)
    w = np.clip(w, 0, D)

    # Calcula variáveis do circuito
    V_arr[i] = V0 * np.sin(omega * t)
    R_arr[i] = R_ON * (w / D) + R_OFF * (1 - w / D)
    I_arr[i] = V_arr[i] / R_arr[i]

    # Atualiza histórico de derivadas
    f_history[:-1] = f_history[1:]  # Desloca histórico
    f_history[-1] = mem(t, w)  # Adiciona novo valor

    # Armazena resultados
    t_arr[i] = t
    w_arr[i] = w

V_arr_ab4 = V_arr
I_arr_ab4 = I_arr

# Criar a figura e o layout com 3 linhas
fig = plt.figure(figsize=(6, 8))
gs = gridspec.GridSpec(3, 1, height_ratios=[1.2, 1, 2.5], hspace=0.5)

# --- Gráfico 1: tensão e corrente vs tempo com eixos duplos ---
ax1 = fig.add_subplot(gs[0])
ax1.set_xlabel("Time")
ax1.set_ylabel("Tensão", color='blue')
ax1.tick_params(axis='y', labelcolor='blue')

ax1_right = ax1.twinx()
ax1_right.set_ylabel("Corrente", color='green')
ax1_right.tick_params(axis='y', labelcolor='green')

ax1.plot(t_arr, V_arr, label='Voltagem (V)', color='g')
ax1_right.plot(t_arr, I_arr * 1e-3, label='Corrente (mA)', color='red')

# --- Gráfico 2: w/D vs tempo ---
ax2 = fig.add_subplot(gs[1])
ax2.set_xlabel("Tempo")
ax2.set_ylabel("w/D")
ax2.set_ylim(-0.1, 1.1)  # como no artigo
ax2.plot(t_arr, w_arr/D, label='Tensão (V)', color='g')

# --- Gráfico 3: I vs V ---
diff = np.diff(I_arr) / np.diff(V_arr)
sinal = np.sign(diff)
muda = np.where(np.diff(sinal) != 0)[0] + 1
ax2.axhline(1, linestyle='--', color='black', linewidth=1)
ax2.axhline(0, linestyle='--', color='black', linewidth=1)

# Dividir os dados em segmentos baseados nos pontos onde a derivada muda de sinal
ax3 = fig.add_subplot(gs[2])

v_partes = np.split(V_arr[:-1], muda)
i_partes = np.split(I_arr[:-1], muda)

n_partes = len(v_partes)
initial_size = 1
size_reduction = initial_size / n_partes

for i, (v_seg, i_seg) in enumerate(zip(v_partes, i_partes)):
    color = plt.cm.viridis(i / n_partes)
    size = max(initial_size - i * size_reduction, 10)
    ax3.scatter(v_seg, i_seg, color=color, s=size, label=f'Segmento {i+1}')

ax3.set_xlabel('Tensão (V)')
ax3.set_ylabel('Corrente (I)')

# Exibir
plt.tight_layout()
plt.show()
