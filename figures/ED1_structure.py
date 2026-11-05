"""Extended Data Fig. 1 | Structure of the theory-guided network (illustrative curves; not fitted values)."""
import numpy as np, matplotlib as mpl, matplotlib.pyplot as plt, sys
from matplotlib.patches import FancyBboxPatch
out = sys.argv[1] if len(sys.argv) > 1 else '.'
mpl.rcParams.update({'font.family': 'Liberation Sans', 'font.size': 6, 'axes.linewidth': 0.5, 'xtick.major.width': 0.5,
                     'ytick.major.width': 0.5, 'xtick.major.size': 2, 'ytick.major.size': 2, 'axes.spines.top': False,
                     'axes.spines.right': False, 'pdf.fonttype': 42, 'savefig.dpi': 300, 'legend.frameon': False, 'legend.fontsize': 5.5})
MM = 1 / 25.4
fig = plt.figure(figsize=(183 * MM, 120 * MM))
sig = lambda x: 1 / (1 + np.exp(-x))
def harf(ax, h, x=-0.22): ax.text(x, 1.06, h, transform=ax.transAxes, fontsize=8, fontweight='bold', va='bottom')

# a: size-dependent growth potential, smoothed form used in fitting
a = fig.add_axes([0.06, 0.62, 0.24, 0.31]); B = np.linspace(0.001, 1.6, 400)
for m, rk in [(0.5, '#9ecae1'), (2 / 3, '#08519c'), (0.8, '#6baed6')]:
    G = B ** m * np.log1p(np.exp(20 * (1 - B ** (1 - m)))) / 20
    a.plot(B, G / G.max(), color=rk, lw=1.2 if m == 2 / 3 else 0.8, label=f'm = {m:.2f}' + (' (metabolic)' if m == 2 / 3 else ''))
a.axvline(1, color='#999999', lw=0.5, ls='--'); a.text(1.02, 0.92, '$B_{max}$', fontsize=5.5, color='#666666')
a.set_xlabel('Basal area, $B/B_{max}$'); a.set_ylabel('Growth potential $G(B)$ (relative)'); a.set_ylim(0, 1.08)
a.legend(loc='upper left', bbox_to_anchor=(0, -0.22), ncol=1); a.set_title('Size-dependent growth potential, eq. (1)', fontsize=6, loc='left'); harf(a, 'a')

# b: monotone responses and the temperature optimum
b = fig.add_axes([0.40, 0.62, 0.24, 0.31]); x = np.linspace(0, 1, 300)
gT = 0.7 * sig((x - 0.25) / 0.05) + 0.3 * sig((x - 0.45) / 0.08); opt = 1 - sig((x - 0.80) / 0.04)
b.plot(x, gT * opt, color='#d6604d', lw=1.1, label='Temperature, $g_T(T)\\,[1-\\sigma((T-c_H)/s_H)]$')
b.plot(x, gT, color='#d6604d', lw=0.6, ls=':')
b.plot(x, 0.6 * sig((x - 0.3) / 0.06) + 0.4 * sig((x - 0.55) / 0.1), color='#8c510a', lw=1.1, label='Soil moisture, $g_M(M)$')
b.plot(x, 1 - (0.5 * sig((x - 0.5) / 0.07) + 0.5 * sig((x - 0.75) / 0.06)), color='#5aae61', lw=1.1, label='VPD, $1-g_D(\\mathrm{VPD})$')
b.axvline(0.80, color='#999999', lw=0.5, ls='--'); b.text(0.81, 0.04, '$c_H$', fontsize=5.5, color='#666666')
b.set_xlabel('Climate variable (scaled to site range)'); b.set_ylabel('Response (0–1)'); b.set_ylim(0, 1.05)
b.legend(loc='upper left', bbox_to_anchor=(0, -0.22), ncol=1)
b.set_title('Monotone responses, eq. (3)', fontsize=6, loc='left'); harf(b, 'b')

# c: law of the minimum over 24 months, limiting factor shaded
c = fig.add_axes([0.74, 0.62, 0.24, 0.31]); mo = np.arange(24)
T = 0.5 + 0.45 * np.sin((mo % 12 - 3) / 12 * 2 * np.pi); rT = np.clip(T * 1.25 - 0.05, 0, 1)
rM = np.clip(0.95 - 0.55 * np.clip(np.sin((mo % 12 - 4) / 12 * 2 * np.pi), 0, 1) ** 2 - 0.15 * (mo >= 12), 0, 1)
rD = np.clip(1 - 0.6 * np.clip(np.sin((mo % 12 - 4) / 12 * 2 * np.pi), 0, 1) ** 3, 0, 1)
R = np.vstack([rT, rM, rD]); mn = R.min(0); arg = R.argmin(0); RK = ['#d6604d', '#8c510a', '#5aae61']
for i, (r, ad) in enumerate(zip(R, ['T', 'M', 'VPD'])): c.plot(mo, r, color=RK[i], lw=0.8, label=ad)
c.bar(mo, mn, 0.9, color=[RK[k] for k in arg], alpha=0.35, lw=0)
c.set_xticks([0, 6, 12, 18, 23]); c.set_xticklabels(['Jan', 'Jul', 'Jan', 'Jul', 'Dec']); c.set_ylim(0, 1.05)
c.text(5.5, 1.07, 'previous year', ha='center', fontsize=5, color='#666666'); c.text(17.5, 1.07, 'current year', ha='center', fontsize=5, color='#666666')
c.set_xlabel('Month'); c.set_ylabel('Response'); c.legend(loc='upper left', bbox_to_anchor=(0, -0.22), ncol=3)
c.text(0.98, 0.02, 'shading: limiting factor', transform=c.transAxes, ha='right', fontsize=5, color='#666666')
c.set_title('Law of the minimum, eq. (2)', fontsize=6, loc='left', pad=9); harf(c, 'c')

# d: structure
d = fig.add_axes([0.02, 0.0, 0.96, 0.40]); d.set_xlim(0, 100); d.set_ylim(0, 40); d.axis('off')
def kutu(x, y, w, h, metin, rk='#f2f2f2', kenar='#666666', kalin=False):
    d.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.4,rounding_size=1.2', fc=rk, ec=kenar, lw=0.8 if kalin else 0.5))
    d.text(x + w / 2, y + h / 2, metin, ha='center', va='center', fontsize=5.4, linespacing=1.35)
def ok(x1, y1, x2, y2): d.annotate('', xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle='-|>', lw=0.6, color='#444444', mutation_scale=6))
d.text(0, 38.5, 'd', fontsize=8, fontweight='bold'); d.text(3, 38.5, 'Structure of the theory-guided network', fontsize=6)
kutu(1, 22, 17, 13, 'Site and species inputs\ngenus, species embeddings\n8 site descriptors\n11 soil and topography variables\nbiome, ecoregion, Köppen')
kutu(23, 24, 14, 9, 'Site-parameter network\n2 hidden layers × 128\n(chosen from 25)', rk='#deebf7', kenar='#3182bd', kalin=True)
kutu(42, 22, 18, 13, 'Site parameters\n$\\eta$, $m$, $B_{max}$, initial radius\nresponse shapes $g_T$, $g_M$, $g_D$\noptimum $c_H$, monthly weights $\\omega$\nspread $s_0$, $s_C$, $s_R$')
kutu(1, 3, 17, 12, 'Monthly climate, 24 months\ntemperature $T$, soil moisture $M$\nVPD; growing-season weight $g_E$')
kutu(23, 3, 14, 12, 'Tree size\nradius $r$ from cumulative rings\n$B=\\pi r^2$')
kutu(65, 26, 15, 7, 'Climatic modifier $C$\n(law of the minimum)', rk='#fee8c8', kenar='#e6550d')
kutu(65, 13, 15, 7, 'Growth potential $G(B)$', rk='#fee8c8', kenar='#e6550d')
kutu(84, 19, 15, 9, 'BAI $= G(B)\\,C\\,e^{u}$\nring width $w$', rk='#e5f5e0', kenar='#31a354', kalin=True)
kutu(84, 3, 15, 11, 'Censored Gaussian\nlikelihood of $\\log w$\n$\\log\\sigma=s_0+s_C\\log C+s_R\\log r$')
kutu(65, 2, 15, 7, 'Tree effect $u$\n(penalty s.d. 0.3)')
ok(18, 28.5, 23, 28.5); ok(37, 28.5, 42, 28.5); ok(60, 30, 65, 30); ok(60, 26, 65, 17); d.plot([9.5, 9.5, 62], [15.4, 18.5, 18.5], color='#444444', lw=0.6); ok(62, 18.5, 65, 27.5)
ok(37, 9, 65, 15); ok(80, 29.5, 84, 25); ok(80, 16.5, 84, 21); ok(80, 5.5, 84, 21); ok(91.5, 19, 91.5, 14)
for uz in ('pdf', 'png'): fig.savefig(f'{out}/ED1.{uz}', bbox_inches='tight')
print('ED1 saved')
