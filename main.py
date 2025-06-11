import numpy as np
import matplotlib.pyplot as plt

##=========RETIFICADOR CA-CC=========##

# Parâmetros de simulação
Vm = 30                # Pico da tensão de entrada (V)
f = 50                 # Frequência da rede (Hz)
omega = 2 * np.pi * f  # Frequência angular (rad/s)
C = 1000e-6            # Capacitância do filtro (F)
L = 100e-3             # Indutância em série (H)
RL = 1e3               # Resistência de carga (Ω)
t_end = 0.5            # Tempo de simulação (s) - tempo maior para atingir regime
dt = 1e-5              # Passo de tempo (s)

# Vetor de tempo
t = np.arange(0, t_end, dt)

# Tensão retificada (full-wave)
v_in = Vm * np.sin(omega * t)
v_rect = np.abs(v_in)

# Estados iniciais
# Estados iniciais REALISTAS
i_L = np.zeros_like(t)
v_C = np.zeros_like(t)  # Começa em 0V

# Integração de Euler CORRIGIDA
for k in range(1, len(t)):
    # Verifica estado de condução (diodo ON se v_rect > v_C ou corrente positiva)
    if v_rect[k] > v_C[k-1] or i_L[k-1] > 0:
        # Modo condução: diodos ON
        diL_dt = (v_rect[k] - v_C[k-1]) / L  # Sinal CORRETO
        dvC_dt = (i_L[k-1] - v_C[k-1] / RL) / C  # Considera corrente de carga
    else:
        # Modo bloqueio: diodos OFF
        diL_dt = 0
        dvC_dt = -v_C[k-1] / (RL * C)  # Apenas descarga do capacitor
    
    # Atualização dos estados
    i_L[k] = i_L[k-1] + diL_dt * dt
    v_C[k] = v_C[k-1] + dvC_dt * dt
    
    # Garantir não negatividade da corrente
    if i_L[k] < 0:
        i_L[k] = 0


# Seleciona último ciclo para plotar
cycle_start = int((t_end - 1/f) / dt)

plt.figure(figsize=(8,4))
plt.plot(t[cycle_start:], v_rect[cycle_start:], label='Tensão Retificada')
plt.plot(t[cycle_start:], v_C[cycle_start:], label='Tensão de Saída (v_C)')
plt.xlabel('Tempo (s)')
plt.ylabel('Tensão (V)')
plt.title('Simulação de Retificador com Filtro LC (Regime Permanente)')
plt.legend(loc='upper left', title='Curvas', fontsize=10, ncol=1)
plt.grid(True)
plt.tight_layout()
plt.show()


##=========CONVERSOR CC-CC BUCK=========##
# Parâmetros conforme valores calculados
Vin = v_C[k]          # Tensão de entrada (V)
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