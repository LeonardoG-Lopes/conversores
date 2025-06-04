import numpy as np
import matplotlib.pyplot as plt

# Parâmetros conforme valores calculados fornecidos pelo usuário
Vin = 30.0            # Tensão de entrada (V)
L = 432.2e-6          # Indutância do indutor (H) = 432.2 µH
R = 1.44              # Resistência de carga (Ω) = 1.44 Ω
C = 43.39e-6          # Capacitância do capacitor de saída (F) = 43.39 µF
Fs = 20e3             # Frequência de chaveamento (Hz) = 20 kHz
D = 0.4               # Duty cycle (40%)
Ts = 1 / Fs           # Período de chaveamento (s)

# Valor médio de saída (esperado)
Voutmed = D * Vin     # 12 V

# Tempo de simulação: 5 ms para ver o amortecimento
t_end = 5e-3       # 5 ms
dt = Ts / 200      # subdividindo cada período em 200 passos
t = np.arange(0, t_end, dt)

# Vetores de simulação
iL = np.zeros_like(t)     # Corrente do indutor
vout = np.zeros_like(t)   # Tensão do capacitor/saída

# Condições iniciais
iL[0] = 0.0
vout[0] = 0.0

# Loop de integração (Euler explícito)
for k in range(len(t) - 1):
    t_cycle = t[k] % Ts
    # Determinar ON ou OFF
    if t_cycle < D * Ts:
        vL = Vin - vout[k]   # ON: tensão no indutor
    else:
        vL = -vout[k]        # OFF: tensão no indutor

    # Atualizar corrente do indutor
    iL[k + 1] = iL[k] + (vL / L) * dt

    # Atualizar tensão do capacitor
    i_load = vout[k] / R
    vout[k + 1] = vout[k] + (iL[k] - i_load) / C * dt

# Plot dos resultados
plt.figure(figsize=(10, 4))
plt.plot(t * 1e3, vout, label='Tensão de Saída (vout)')
plt.axhline(Voutmed, color='red', linestyle='--', label=f'Média Teórica = {Voutmed:.1f} V')
plt.title('Resposta Transitória e Estabilização da Tensão de Saída (30 V → 12 V)')
plt.xlabel('Tempo (ms)')
plt.ylabel('Tensão (V)')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
