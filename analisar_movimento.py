import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

# loads data
try:
    df = pd.read_csv('dados_pendulo.csv')
except FileNotFoundError:
    print("ERRO: O arquivo 'dados_pendulo.csv' nao foi encontrado.")
    exit()

# center positions
t = df['tempo'].values
x_centered = df['x'] - df['x'].mean()
y_centered = df['y'] - df['y'].mean()

# --- PARAMETROS OBTIDOS DO AJUSTE (ATUALIZE SE NECESSARIO) ---
# Estes valores foram extraídos da saida do seu ajustar_oha.py
# A: 80.20, b: 0.010223, w: 3.9301, phi: -1.9115
A_fit = 80.20
b_fit = 0.010223
omega_fit = 3.9301
phi_fit = -1.9115
# -----------------------------------------------------------

# defines equation for DHO
def oha(t, A, b, omega, phi):
    return A * np.exp(-b * t) * np.cos(omega * t + phi)

# calculates variations
var_x = np.std(x_centered)
var_y = np.std(y_centered)
amplitude_x = np.ptp(x_centered)
amplitude_y = np.ptp(y_centered)

print("\n" + "=" * 50)
print("ANALISE DE MOVIMENTO (FOCO EM X):")
print("=" * 50)
print(f"Desvio padrao em X: {var_x:.2f} pixels")
print(f"Desvio padrao em Y: {var_y:.2f} pixels")
print(f"Amplitude X (pico a pico): {amplitude_x:.2f} pixels")
print(f"Razao Y/X (variacao): {var_y/var_x:.4f}")

# plots the graph

# subplot for DHO
plt.figure(figsize=(14, 6))

# plots data with points
plt.plot(t, x_centered, 'b.', markersize=3, alpha=0.5, label='Dados de Posicao X (pixels)')

# doted red lines
envelope_pos = A_fit * np.exp(-b_fit * t)
envelope_neg = -A_fit * np.exp(-b_fit * t)
plt.plot(t, envelope_pos, 'r--', linewidth=2, label=f'$A e^{{-bt}}$') 
plt.plot(t, envelope_neg, 'r--', linewidth=2)

# curve for comparison
plt.plot(t, oha(t, A_fit, b_fit, omega_fit, phi_fit), 'k-', linewidth=1, alpha=0.5, label='Curva OHA Ajustada')

plt.xlabel('Tempo (s)', fontsize=12)
plt.ylabel('Posicao X Centralizada (pixels)', fontsize=12)
plt.title('Movimento Amortecido (Validacao Visual do Item 6)', fontsize=14)
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)
plt.ylim(ymin = -A_fit * 1.05, ymax = A_fit * 1.05) 

plt.tight_layout()
plt.savefig('analise_movimento_OHA_visual.png', dpi=300)
plt.show()

