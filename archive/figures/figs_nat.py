import json, numpy as np, pandas as pd, matplotlib
from blok import P2B, P2 as P2S, P1_STRICT, P4 as P4B, Q1, Q1_OBS, Q5T, Q5M, R1
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.colors import LinearSegmentedColormap, BoundaryNorm
from matplotlib.lines import Line2D

plt.rcParams.update({'font.family': 'Liberation Sans', 'font.size': 7, 'axes.titlesize': 7, 'axes.labelsize': 7,
                     'xtick.labelsize': 6.5, 'ytick.labelsize': 6.5, 'legend.fontsize': 6.5, 'axes.linewidth': 0.6,
                     'xtick.major.width': 0.6, 'ytick.major.width': 0.6, 'xtick.major.size': 2.5, 'ytick.major.size': 2.5,
                     'axes.spines.top': False, 'axes.spines.right': False, 'savefig.dpi': 450, 'pdf.fonttype': 42})
INK, INK2, MUTED, GRID = '#0b0b0b', '#52514e', '#8a897f', '#e4e3df'
BLUE, ORANGE, AQUA, YELLOW, MAG, GREEN, VIOLET, RED = '#2a78d6', '#eb6834', '#1baf7a', '#eda100', '#e87ba4', '#008300', '#6250d6', '#e34948'
DIV = LinearSegmentedColormap.from_list('div', ['#a3302e', '#e34948', '#f2aaa7', '#f0efec', '#9ec5f4', '#2a78d6', '#184f95'])
MM = 1 / 25.4; W2 = 180 * MM
LAND = json.load(open('../app/data.json'))['land']

N1 = pd.read_csv('N1_uc_olay_kanali.csv').set_index('grup')
N2 = pd.read_csv('N2_sinirlayici_faktor_ozet.csv'); N3a = pd.read_csv('N3a_uc_olay_saglamlik.csv')
N1a = pd.read_csv('N1a.csv'); N2a = pd.read_csv('N2a.csv'); K2 = pd.read_csv('K2.csv'); M1a = pd.read_csv('M1a.csv')
S = N1a.merge(N2a.drop(columns=['cins', 'bolge']), on='studyCode').merge(K2[['studyCode', 'lat', 'lon', 'kurak_ceyrek', 'soguk_ceyrek']], on='studyCode')
rng = np.random.default_rng(1)
ln = lambda p: np.log1p(np.asarray(p) / 100); pc = lambda x: 100 * (np.exp(x) - 1)

def harita(ax):
    ps = [Polygon(np.array(r), closed=True) for r in LAND]
    ax.add_collection(PatchCollection(ps, facecolor='#eeede9', edgecolor='#cfcec8', lw=0.25, zorder=0))
    ax.set_xlim(-170, 180); ax.set_ylim(-56, 75); ax.set_aspect('equal'); ax.axis('off')
def etiket(ax, s, x=-0.08, y=1.04):
    ax.text(x, y, s, transform=ax.transAxes, fontsize=8, fontweight='bold', va='bottom', ha='left', color=INK)
def izgara(ax, axis='x'):
    ax.grid(axis=axis, color=GRID, lw=0.5, zorder=0); ax.set_axisbelow(True)

# ---------------- Figure 1 ----------------
fig = plt.figure(figsize=(W2, 122 * MM))
gs = fig.add_gridspec(1, 3, wspace=0.62, left=0.065, right=0.975, top=0.40, bottom=0.08)
ax = fig.add_axes([0.0, 0.46, 1.0, 0.54]); harita(ax)
v = S.gecerli & np.isfinite(S.L_yuzde_yil)
bnd = [-12, -8, -4, -2, -0.5, 0.5, 2, 4, 8, 12]; norm = BoundaryNorm(bnd, DIV.N, extend='both')
o = np.argsort(np.abs(S.L_yuzde_yil[v].values))
sc = ax.scatter(S.lon[v].values[o], S.lat[v].values[o], c=S.L_yuzde_yil[v].values[o], cmap=DIV, norm=norm, s=3.2, lw=0.15, edgecolors='white', zorder=2)
cax = ax.inset_axes([0.02, 0.10, 0.20, 0.035]); cb = fig.colorbar(sc, cax=cax, orientation='horizontal', ticks=[-8, -4, 0, 4, 8])
cb.ax.tick_params(labelsize=6, length=1.5); cb.outline.set_linewidth(0.4)
cax.set_title('Growth change via extreme years,\n1990–2019 (% per year)', fontsize=6.5, loc='left', color=INK2)
etiket(ax, 'a', 0.005, 0.93)
# b: frequency
ax = fig.add_subplot(gs[0, 0]); izgara(ax, 'y'); etiket(ax, 'b', -0.25)
ev = [('sicak', 'Hot'), ('kurak', 'Dry'), ('soguk', 'Cold\nwinter')]; x = np.arange(3); w = 0.36
f = [N1.loc['Tüm alanlar', f'{k}_olgusal_10yil'] for k, _ in ev]; c = [N1.loc['Tüm alanlar', f'{k}_karsi_10yil'] for k, _ in ev]
ax.bar(x - w / 2 - 0.01, c, w, color='#b7b6ae', label='No climate change', zorder=2)
ax.bar(x + w / 2 + 0.01, f, w, color=ORANGE, label='Observed', zorder=2)
for i in range(3):
    ax.text(x[i] + w / 2, f[i] + 0.12, f'{f[i]:.1f}', ha='center', fontsize=6, color=INK2)
    ax.text(x[i] - w / 2, c[i] + 0.12, f'{c[i]:.1f}', ha='center', fontsize=6, color=INK2)
ax.set_xticks(x, [e for _, e in ev]); ax.set_ylabel('Extreme years per decade, 1990–2019'); ax.set_ylim(0, 7)
ax.legend(frameon=False, loc='upper right', handlelength=1, fontsize=6)
# c: per-event effect
ax = fig.add_subplot(gs[0, 1]); izgara(ax, 'x'); etiket(ax, 'c', -0.42)
grp = [('En soğuk %25', 'Coldest quarter', BLUE), ('Tüm alanlar', 'All sites', INK2), ('En kurak %25', 'Driest quarter', RED)]
y0 = np.arange(3)
for j, (g, lab, col) in enumerate(grp):
    vals = [N1.loc[g, f'{k}_olay_etkisi_yuzde'] for k, _ in ev]
    ax.barh(y0 + (j - 1) * 0.26, vals, 0.24, color=col, label=lab, zorder=2)
ax.axvline(0, color=INK, lw=0.6); ax.set_yticks(y0, ['Hot', 'Dry', 'Cold winter']); ax.invert_yaxis()
ax.set_xlabel('Growth, extreme year + next year (%)'); ax.legend(frameon=False, fontsize=6, loc='lower left', handlelength=1)
# d: channel totals
ax = fig.add_subplot(gs[0, 2]); izgara(ax, 'x'); etiket(ax, 'd', -0.62)
rows = [('Tüm alanlar', 'All sites'), ('En soğuk %25', 'Coldest quarter'), ('En kurak %25', 'Driest quarter'), ('Bölge: Europe', 'Europe'),
        ('Bölge: North America', 'North America'), ('Bölge: Asia', 'Asia'), ('Bölge: Southern Hemisphere', 'S. Hemisphere')]
for i, (g, lab) in enumerate(rows):
    n_, mu_, lo_, hi_ = P2B[g]; col = BLUE if lo_ > 0 else (RED if hi_ < 0 else MUTED)
    ax.plot([lo_, hi_], [i, i], color=col, lw=1.2, solid_capstyle='round'); ax.plot(mu_, i, 'o', ms=4, color=col, mec='white', mew=0.5)
    ax.text(4.9, i, f'{mu_:+.1f}', va='center', ha='right', fontsize=6, color=INK2)
ax.axvline(0, color=INK, lw=0.6); ax.set_yticks(range(len(rows)), [l for _, l in rows]); ax.invert_yaxis(); ax.set_xlim(-7.5, 5)
ax.set_xlabel('Change via extreme years (% per year)')
fig.savefig('Fig1.png'); fig.savefig('Fig1.pdf'); plt.close(fig)

# ---------------- Figure 2 ----------------
fig = plt.figure(figsize=(W2, 150 * MM))
gs2 = fig.add_gridspec(2, 2, width_ratios=[1.2, 1], wspace=0.66, hspace=0.42, left=0.12, right=0.985, top=0.95, bottom=0.08)
axs = [fig.add_subplot(gs2[:, 0]), fig.add_subplot(gs2[0, 1])]
gsc = gs2[1, 1].subgridspec(1, 2, wspace=0.95); axc = fig.add_subplot(gsc[0, 0]); axd = fig.add_subplot(gsc[0, 1])
ax = axs[0]; izgara(ax, 'x'); etiket(ax, 'a', -0.22, 1.02)
cins = [i for i in N1.index if i.startswith('Cins:')]
G = pd.DataFrame({k: dict(n_alan=v[0], toplam_yuzde_yil=v[1], alt95=v[2], ust95=v[3]) for k, v in P2B.items() if k.startswith('Cins:')}).T.sort_values('toplam_yuzde_yil')
payT = S.groupby('cins')['T+S_pay_T'].mean()
cm2 = LinearSegmentedColormap.from_list('tm', [RED, '#f0efec', BLUE])
for i, (g, r) in enumerate(G.iterrows()):
    gn = g.split(': ')[1]; pt = payT.get(gn, np.nan); col = cm2(pt)
    ax.plot([r.alt95, r.ust95], [i, i], color=INK2, lw=0.9)
    ax.plot(r.toplam_yuzde_yil, i, 'o', ms=5, color=col, mec=INK, mew=0.4, zorder=3)
    ax.text(9.3, i, f'{int(r.n_alan)}', va='center', ha='right', fontsize=5.8, color=MUTED)
ax.set_yticks(range(len(G)), [g.split(': ')[1] for g in G.index], fontstyle='italic'); ax.axvline(0, color=INK, lw=0.6)
ax.set_xlim(-12, 9.5); ax.set_xlabel('Growth change via extreme years, 1990–2019 (% per year)')
ax.text(9.3, len(G) - 0.2, 'sites', ha='right', fontsize=5.8, color=MUTED)
sm = plt.cm.ScalarMappable(cmap=cm2, norm=plt.Normalize(0, 1)); cax = ax.inset_axes([0.05, 0.86, 0.28, 0.026])
cb = fig.colorbar(sm, cax=cax, orientation='horizontal', ticks=[0, 0.5, 1]); cb.ax.tick_params(labelsize=5.8, length=1.5); cb.outline.set_linewidth(0.4)
cb.ax.set_xticklabels(['moisture', '', 'temperature']); cax.set_title('Limiting factor (theory-embedded AI)', fontsize=6, loc='left', color=INK2)
ax = axs[1]; izgara(ax, 'x'); etiket(ax, 'b', -0.62, 1.02)
sec = list(P2S); lab = sec
for j, (g, nm, col) in enumerate(grp):
    for i, s_ in enumerate(sec):
        mu_, lo_, hi_ = P2S[s_][g]; yy = i + (j - 1) * 0.22
        ax.plot([lo_, hi_], [yy, yy], color=col, lw=0.8); ax.plot(mu_, yy, 'o', ms=3.2, color=col, mec='white', mew=0.3, label=nm if i == 0 else None)
ax.set_yticks(range(len(sec)), lab); ax.invert_yaxis(); ax.axvline(0, color=INK, lw=0.6)
ax.set_xlabel('Growth change via extreme years (% per year)'); ax.legend(frameon=False, fontsize=6, loc='lower left', handlelength=0.8, ncol=3, bbox_to_anchor=(0, 1.0), columnspacing=0.8)
ax = axc; izgara(ax, 'y'); etiket(ax, 'c', -0.75, 1.02)
gk = list(R1); x = np.arange(3)
for j, (k, lab, col) in enumerate([('e', '1902–1960', MUTED), ('l', '1961–2019', INK)]):
    for i, g in enumerate(gk):
        m_, lo_, hi_ = R1[g][k]; xx = i + (j - 0.5) * 0.3
        ax.plot([xx, xx], [lo_, hi_], color=col, lw=0.9); ax.plot(xx, m_, 'o', ms=3.6, color=col, mec='white', mew=0.3, label=lab if i == 0 else None)
ax.axhline(0, color=INK, lw=0.6); ax.set_xticks(x, gk, fontsize=5.6); ax.set_ylabel('Growth change via\nextreme years (% per year)', fontsize=6.3)
ax.legend(frameon=False, fontsize=5.6, loc='lower left', handlelength=0.6, borderaxespad=0.1); ax.set_ylim(-8, 5)
ax = axd; izgara(ax, 'y'); etiket(ax, 'd', -0.75, 1.02)
for i, g in enumerate(gk):
    m_, lo_, hi_ = R1[g]['d']; ax.plot([i - 0.12] * 2, [lo_, hi_], color=VIOLET, lw=0.9); ax.plot(i - 0.12, m_, 'o', ms=3.6, color=VIOLET, mec='white', mew=0.3, label='Separate chronologies' if i == 0 else None)
    m_, lo_, hi_ = R1[g]['ds']; ax.plot([i + 0.12] * 2, [lo_, hi_], color=AQUA, lw=0.9); ax.plot(i + 0.12, m_, 'D', ms=3.2, color=AQUA, mec='white', mew=0.3, label='Same chronologies' if i == 0 else None)
ax.axhline(0, color=INK, lw=0.6); ax.set_xticks(x, gk, fontsize=5.6); ax.set_ylabel('Later − earlier\n(percentage points)', fontsize=6.3)
ax.legend(frameon=False, fontsize=5.6, loc='upper right', handlelength=0.6, borderaxespad=0.1); ax.set_ylim(-6, 3.2)
fig.savefig('Fig2.png'); fig.savefig('Fig2.pdf'); plt.close(fig)

# ---------------- Figure 3 ----------------
fig = plt.figure(figsize=(W2, 125 * MM))
gs = fig.add_gridspec(1, 3, wspace=0.62, left=0.075, right=0.985, top=0.40, bottom=0.12)
ax = fig.add_axes([0.0, 0.47, 1.0, 0.53]); harita(ax); etiket(ax, 'a', 0.005, 0.93)
cl = S['T+S_sinif']; sw = (S['T+S_sinif_karsi'] == 'T') & (cl == 'M')
ax.scatter(S.lon[cl == 'T'], S.lat[cl == 'T'], s=2.6, color=BLUE, lw=0, zorder=2, label='Temperature-limited')
ax.scatter(S.lon[(cl == 'M') & ~sw], S.lat[(cl == 'M') & ~sw], s=2.6, color=ORANGE, lw=0, zorder=2, label='Moisture-limited')
ax.scatter(S.lon[sw], S.lat[sw], s=7, color=INK, marker='x', lw=0.5, zorder=3, label='Temperature-limited in counterfactual, moisture-limited in observed climate')
ax.legend(frameon=False, loc='lower left', fontsize=6.3, markerscale=2.2, handletextpad=0.3, bbox_to_anchor=(0.0, 0.03))
# b: binned
ax = fig.add_subplot(gs[0, 0]); izgara(ax, 'y'); etiket(ax, 'b', -0.3)
bins = [0, .1, .3, .5, .7, .9, 1.001]; lb = ['<0.1', '0.1–0.3', '0.3–0.5', '0.5–0.7', '0.7–0.9', '>0.9']
v = S.gecerli & np.isfinite(S.L_yuzde_yil)
for i in range(6):
    m = v & (S['T+S_pay_T'] >= bins[i]) & (S['T+S_pay_T'] < bins[i + 1]); x_ = ln(S.L_yuzde_yil[m])
    bs = [rng.choice(x_, len(x_)).mean() for _ in range(1000)]; mu = pc(x_.mean()); lo, hi = pc(np.quantile(bs, [0.025, 0.975]))
    col = cm2((bins[i] + min(bins[i + 1], 1)) / 2)
    ax.bar(i, mu, 0.7, color=col, edgecolor=INK2, lw=0.4, zorder=2); ax.plot([i, i], [lo, hi], color=INK, lw=0.8, zorder=3)
    ax.text(i, -7.4, f'n={m.sum()}', ha='center', va='bottom', fontsize=5, color=MUTED)
ax.plot(range(6), P1_STRICT, 'D-', color=INK, ms=3, lw=0.8, zorder=4, label='Independent test')
ax.legend(frameon=False, fontsize=5.8, loc='upper left', handlelength=1.4)
ax.axhline(0, color=INK, lw=0.6); ax.set_xticks(range(6), lb, rotation=35, ha='right'); ax.set_ylim(-7.6, 3.2)
ax.set_xlabel('Share of growing season limited by temperature'); ax.set_ylabel('Growth change via extreme years\n(% per year, model-independent)')
# c: model attributions by class
ax = fig.add_subplot(gs[0, 1]); izgara(ax, 'y'); etiket(ax, 'c', -0.3)
q = N2[(N2.grup == 'Tüm alanlar')].set_index('sinif')
mods = [('T+S', 'T+S'), ('T_D+S', 'T$_D$+S'), ('Karma model', 'LMM')]
x = np.arange(len(mods)); w = 0.34
def medci(xx):
    xx = xx[np.isfinite(xx)]; bs = [np.median(rng.choice(xx, len(xx))) for _ in range(500)]; return np.median(xx), *np.quantile(bs, [0.025, 0.975]), len(xx)
for sg, cl_, col, nm_ in [(-1, 'T', BLUE, 'Temperature-limited'), (1, 'M', ORANGE, 'Moisture-limited')]:
    R_ = [medci(S.loc[S['T+S_sinif'] == cl_, f'atif_{m}_yuzde'].values) for m, _ in mods]
    ax.bar(x + sg * w / 2, [r[0] for r in R_], w, color=col, label=f'{nm_} sites (n = {R_[0][3]:,})', zorder=2)
    for i, r in enumerate(R_): ax.plot([x[i] + sg * w / 2] * 2, [r[1], r[2]], color=INK, lw=0.7, zorder=3)
ax.axhline(0, color=INK, lw=0.6); ax.set_xticks(x, [l for _, l in mods]); ax.set_ylabel('Attributed growth change,\n1990–2019 (%, median)')
ax.legend(frameon=False, fontsize=5.8, loc='upper right', handlelength=1); ax.set_ylim(-7.8, 9.0)
# d: decomposition
ax = fig.add_subplot(gs[0, 2]); izgara(ax, 'y'); etiket(ax, 'd', -0.3)
gg = [('En soğuk %25', 'Coldest\nquarter'), ('Tüm alanlar', 'All\nsites'), ('En kurak %25', 'Driest\nquarter')]
q = N2[N2.sinif == 'Tümü'].set_index('grup'); x = np.arange(3)
ax.bar(x - w / 2, [q.loc[g, 'T+S_dC_T_yuzde'] for g, _ in gg], w, color=VIOLET, label='Warming alone', zorder=2)
ax.bar(x + w / 2, [q.loc[g, 'T+S_dC_M_yuzde'] for g, _ in gg], w, color=AQUA, label='Soil-moisture change alone', zorder=2)
ax.plot(x, [q.loc[g, 'T+S_dC_toplam_yuzde'] for g, _ in gg], 'D', color=INK, ms=3.5, label='Both', zorder=3)
ax.axhline(0, color=INK, lw=0.6); ax.set_xticks(x, [l for _, l in gg]); ax.set_ylabel('Change in climatic modifier,\n1990–2019 (%, median)')
ax.legend(frameon=False, fontsize=6, loc='upper right', handlelength=1); ax.set_ylim(-2.8, 7.4)
fig.savefig('Fig3.png'); fig.savefig('Fig3.pdf'); plt.close(fig)

# ---------------- Figure 4 ----------------
K = [0, 1, 4, 5, 6]                     # T+S, T_D+S, LMM, RF, VS-Lite (teorili YZ + klasik yöntemler)
L4 = pd.DataFrame(P4B).iloc[[0, 1, 4]].reset_index(drop=True); Q = pd.DataFrame(Q1).iloc[K].reset_index(drop=True)
fig, axs = plt.subplots(2, 2, figsize=(W2, 118 * MM), gridspec_kw=dict(wspace=0.42, hspace=0.62, left=0.1, right=0.985, top=0.95, bottom=0.12))
axs = axs.ravel()
cols = [list(M1a.columns[3:10])[k] for k in K]; nm = [['T+S', 'T$_D$+S', 'U+S', 'XGB', 'LMM', 'RF', 'VS-Lite'][k] for k in K]
dry = M1a.studyCode.isin(K2.studyCode[K2.kurak_ceyrek]); cold = M1a.studyCode.isin(K2.studyCode[K2.soguk_ceyrek])
ax = axs[0]; izgara(ax, 'y'); etiket(ax, 'a', -0.16)
x = np.arange(5); w = 0.27
for j, (msk, lab, col) in enumerate([(cold, 'Coldest quarter', BLUE), (np.ones(len(M1a), bool), 'All sites', INK2), (dry, 'Driest quarter', RED)]):
    ax.bar(x + (j - 1) * w, [M1a.loc[msk, c].median() for c in cols], w * 0.92, color=col, label=lab, zorder=2)
    for i, c in enumerate(cols):
        xx = M1a.loc[msk, c].dropna().values; bs = [np.median(rng.choice(xx, len(xx))) for _ in range(300)]
        ax.plot([x[i] + (j - 1) * w] * 2, np.quantile(bs, [0.025, 0.975]), color=INK, lw=0.6, zorder=3)
ax.axvspan(1.5, 4.6, color='#f3f2ee', zorder=0)
ax.set_xticks(x, nm, rotation=35, ha='right'); ax.set_ylabel('Out-of-sample skill, 1961–2019\n(median site r)'); ax.set_ylim(0, 0.7); ax.set_xlim(-0.6, 4.6)
ax.legend(frameon=False, fontsize=5.8, loc='upper left', handlelength=0.9, ncol=3, columnspacing=0.5, handletextpad=0.3)
ax = axs[1]; izgara(ax, 'x'); etiket(ax, 'b', -0.2)
for i, r in L4.iterrows():
    col = INK if r.lo > 0 else MUTED
    ax.plot([r.lo, r.hi], [i, i], color=col, lw=1.1); ax.plot(r.b, i, 'o', ms=4.5, color=col, mec='white', mew=0.5)
ax.axvline(1, color=AQUA, lw=0.8, ls='--'); ax.axvline(0, color=INK, lw=0.6)
ax.text(1.04, -0.45, 'β = 1: consistent amplitude', fontsize=5.6, color=AQUA, va='center')
ax.set_yticks(range(3), L4.model); ax.set_ylim(2.5, -0.8); ax.set_xlim(-0.5, 1.75); ax.set_xlabel('Detection scaling factor β (95% spatial-block CI)')
ax = axs[2]; izgara(ax, 'y'); etiket(ax, 'c', -0.16)
ax.bar(x, Q.r, 0.62, color=[ORANGE, ORANGE, MUTED, MUTED, MUTED], zorder=2)
for i, r in Q.iterrows():
    if r.d is None or pd.isna(r.d): ax.text(i, r.r + 0.02, 'ref.', ha='center', fontsize=5.6, color=INK2); continue
    sig = (r.dlo > 0) or (r.dhi < 0)
    ax.text(i, r.r + 0.02, ('%+.2f' % (-r.d)) + ('*' if sig else ''), ha='center', fontsize=5.6, color=INK if sig else MUTED)
ax.axvspan(1.5, 4.6, color='#f3f2ee', zorder=0)
ax.set_xticks(x, nm, rotation=35, ha='right'); ax.set_ylim(0, 0.6); ax.set_xlim(-0.6, 4.6)
ax.set_ylabel('Agreement with observed\nextreme-year change (site r)')
ax = axs[3]; izgara(ax, 'y'); etiket(ax, 'd', -0.24)
w = 0.36
dT = np.array(Q.Lt) - Q1_OBS['Lt']; dM = np.array(Q.Lm) - Q1_OBS['Lm']
ax.bar(x - w / 2, dT, w * 0.92, color=BLUE, label='Temperature-limited (obs. +0.1%)', zorder=2)
ax.bar(x + w / 2, dM, w * 0.92, color=RED, label='Moisture-limited (obs. −3.7%)', zorder=2)
for i, k in enumerate(K):
    ax.plot([x[i] - w / 2] * 2, [Q5T['lo'][k], Q5T['hi'][k]], color=INK, lw=0.6, zorder=3)
    ax.plot([x[i] + w / 2] * 2, [Q5M['lo'][k], Q5M['hi'][k]], color=INK, lw=0.6, zorder=3)
ax.axhline(0, color=INK, lw=0.7); ax.axvspan(1.5, 4.6, color='#f3f2ee', zorder=0)
ax.text(4.55, 5.4, 'model > observed', ha='right', fontsize=5.6, color=MUTED); ax.text(4.55, -3.1, 'model < observed', ha='right', fontsize=5.6, color=MUTED)
ax.set_xticks(x, nm, rotation=35, ha='right'); ax.set_xlim(-0.6, 4.6); ax.set_ylim(-3.5, 6.0)
ax.set_ylabel('Predicted − observed growth change\nthrough extreme years (% points per year)')
ax.legend(frameon=False, fontsize=5.6, loc='lower center', bbox_to_anchor=(0.5, 1.0), handlelength=0.9, ncol=2, columnspacing=0.6)
fig.savefig('Fig4.png'); fig.savefig('Fig4.pdf'); plt.close(fig)

# ---------------- Extended Data Fig. 2 (direnç) ----------------
M3 = pd.DataFrame(dict(m=['T+S', 'T$_D$+S', 'U+S', 'XGB', 'LMM', 'RF', 'VS-Lite'],
                       kurak=[0.559, 0.559, 0.559, 0.612, 0.166, 0.487, 0.587], sicak=[0.450, 0.451, 0.438, 0.469, 0.274, 0.323, 0.337],
                       soguk=[0.406, 0.397, 0.437, 0.417, 0.160, 0.250, 0.388])).iloc[[0, 1, 4, 5, 6]].reset_index(drop=True)
fig, ax = plt.subplots(figsize=(110 * MM, 62 * MM), gridspec_kw=dict(left=0.16, right=0.98, top=0.95, bottom=0.22))
izgara(ax, 'y'); x = np.arange(5); w = 0.27
for j, (k, lab, col) in enumerate([('kurak', 'Dry years', YELLOW), ('sicak', 'Hot years', RED), ('soguk', 'Cold winters', BLUE)]):
    ax.bar(x + (j - 1) * w, M3[k], w * 0.92, color=col, label=lab, zorder=2)
ax.set_xticks(x, M3.m, rotation=35, ha='right'); ax.set_ylabel('Reproduction of extreme-year\ngrowth drops (site r)'); ax.set_ylim(0, 0.8)
ax.legend(frameon=False, fontsize=6, loc='upper right', handlelength=1, ncol=3)
fig.savefig('EDFig2.png'); fig.savefig('EDFig2.pdf'); plt.close(fig)
print('ok')
