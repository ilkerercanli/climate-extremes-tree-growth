import numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
plt.rcParams.update({'font.family': 'Liberation Sans', 'font.size': 7, 'axes.linewidth': 0.6, 'xtick.labelsize': 6.5, 'ytick.labelsize': 6.5,
                     'axes.spines.top': False, 'axes.spines.right': False, 'savefig.dpi': 450, 'pdf.fonttype': 42})
INK, INK2, MUTED, GRID = '#0b0b0b', '#52514e', '#8a897f', '#e4e3df'
BLUE, ORANGE, VIOLET, AQUA, RED = '#2a78d6', '#eb6834', '#6250d6', '#1baf7a', '#e34948'
MM = 1 / 25.4
sig = lambda x: 1 / (1 + np.exp(-x))
fig = plt.figure(figsize=(180 * MM, 112 * MM))
gs = fig.add_gridspec(2, 3, height_ratios=[1, 1.05], hspace=0.62, wspace=0.42, left=0.07, right=0.98, top=0.93, bottom=0.1)
def lab(ax, s, x=-0.2, y=1.06): ax.text(x, y, s, transform=ax.transAxes, fontsize=8, fontweight='bold', va='bottom')

# a: growth potential
ax = fig.add_subplot(gs[0, 0]); lab(ax, 'a')
B = np.linspace(1, 3000, 400); Bmax = 3000; eta = 1
for m, col, ls in [(0.5, MUTED, '--'), (2 / 3, BLUE, '-'), (0.8, MUTED, ':')]:
    G = eta * B ** m * np.clip(1 - (B / Bmax) ** (1 - m), 0, None); ax.plot(B / 100, G / G.max(), color=col, lw=1.3 if col == BLUE else 0.9, ls=ls, label=f'm = {m:.2f}')
ax.set_xlabel('Basal area B (dm²)'); ax.set_ylabel('Growth potential G(B) (relative)'); ax.legend(frameon=False, fontsize=6, loc='lower center')
ax.set_title('Size-dependent growth potential\n(Richards; metabolic scaling)', fontsize=6.8, color=INK2)

# b: monotone responses
ax = fig.add_subplot(gs[0, 1]); lab(ax, 'b')
x = np.linspace(-5, 30, 300); gT = 0.6 * sig((x - 6) / 2) + 0.4 * sig((x - 14) / 3)
ax.plot(x, gT, color=RED, lw=1.3, label='g_T (temperature)')
ax.set_xlabel('Temperature (°C)'); ax.set_ylabel('Response (0–1)'); ax.set_ylim(-0.02, 1.05)
ax2 = ax.twiny(); xm = np.linspace(0, 0.6, 300); gM = 0.7 * sig((xm - 0.12) / 0.03) + 0.3 * sig((xm - 0.3) / 0.05)
ax2.plot(xm, gM, color=BLUE, lw=1.3); ax2.set_xlabel('Soil moisture (v/v)', fontsize=6.5, color=BLUE); ax2.tick_params(axis='x', colors=BLUE, labelsize=6)
ax2.spines['top'].set_visible(True); ax2.spines['top'].set_color(BLUE)
ax.text(28, 0.62, 'g$_T$', color=RED, fontsize=7, ha='right'); ax.text(1, 0.9, 'g$_M$', color=BLUE, fontsize=7)
ax.text(0.98, 0.04, 'monotone mixtures of\nlogistic functions', transform=ax.transAxes, ha='right', fontsize=6, color=INK2)

# c: Liebig min over a season
ax = fig.add_subplot(gs[0, 2]); lab(ax, 'c')
mo = np.arange(1, 13); T = np.array([-8, -6, -1, 5, 11, 16, 19, 18, 13, 6, -1, -6]); M = np.array([0.35, 0.35, 0.38, 0.36, 0.3, 0.2, 0.12, 0.1, 0.13, 0.22, 0.3, 0.34])
gt = 0.6 * sig((T - 6) / 2) + 0.4 * sig((T - 14) / 3); gm = 0.7 * sig((M - 0.12) / 0.03) + 0.3 * sig((M - 0.3) / 0.05)
ax.plot(mo, gt, 'o-', color=RED, ms=3, lw=1, label='g$_T$'); ax.plot(mo, gm, 's-', color=BLUE, ms=3, lw=1, label='g$_M$')
mn = np.minimum(gt, gm); ax.fill_between(mo, 0, mn, color='#d9d8d2', zorder=0, label='min (limiting)')
for i in range(12):
    ax.text(mo[i], -0.13, 'T' if gt[i] < gm[i] else 'M', ha='center', fontsize=5.8, color=RED if gt[i] < gm[i] else BLUE)
ax.set_xticks(mo, ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'])
ax.set_ylabel('Response (0–1)'); ax.set_ylim(-0.18, 1.32); ax.legend(frameon=False, fontsize=6, loc='upper center', ncol=3, columnspacing=0.8, handlelength=1.2)
ax.set_title('Principle of limiting factors (Liebig)', fontsize=6.8, color=INK2)

# d: architecture diagram
ax = fig.add_subplot(gs[1, :]); ax.axis('off'); ax.set_xlim(0, 100); ax.set_ylim(0, 30); lab(ax, 'd', -0.02, 1.0)
def box(x, y, w, h, txt, fc, ec=INK2, fs=6.5, bold=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.4,rounding_size=1.2', fc=fc, ec=ec, lw=0.6))
    ax.text(x + w / 2, y + h / 2, txt, ha='center', va='center', fontsize=fs, color=INK, fontweight='bold' if bold else 'normal')
def arr(x0, y0, x1, y1): ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle='-|>', mutation_scale=7, lw=0.7, color=INK2))
box(0.5, 11, 15, 9, 'Species & genus\nSite climate normals\nSoil, topography,\nbiome, Köppen', '#f3f2ee')
box(21, 12.5, 13, 6, 'Neural network\n(site parameters)', '#ece9fb', ec=VIOLET, bold=True)
arr(16.3, 15.5, 20.4, 15.5)
box(40, 21, 19, 7.5, 'Growth potential G(B)\nη, m, B$_{max}$  — eq. (1)', '#e6f0fb', ec=BLUE)
box(40, 2, 19, 8.5, 'Climatic modifier C\nmin[g$_T$, g$_M$], ω, g$_E$ — eqs. (2, 3)', '#fdece5', ec=ORANGE)
arr(34.6, 17, 39.4, 24.5); arr(34.6, 14, 39.4, 6.5)
box(40.5, 12.6, 18, 5.2, 'Tree size B (from rings)', '#f3f2ee', fs=6.2); arr(49.5, 17.9, 49.5, 20.4)
box(62.5, 1.2, 17, 6.2, 'Monthly climate, 24 months\n(temperature, soil moisture)', '#f3f2ee', fs=6); arr(62.1, 4.3, 59.6, 4.3)
box(81, 12, 18, 8, 'Basal area increment\nBAI = G(B) · C\n→ ring width', '#e8f6ef', ec=AQUA, bold=True)
arr(59.6, 24.5, 80.4, 17.5); arr(59.6, 9.5, 80.4, 13.5)
fig.savefig('EDFig1.png'); fig.savefig('EDFig1.pdf'); print('ok')
