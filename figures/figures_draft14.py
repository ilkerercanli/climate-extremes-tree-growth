"""Revised figures after the reviewer analyses (Defter 23A/23B), as in draft 14 of the manuscript.
Redraws Fig. 2 (panel b: same sites, same statistic, 10-degree block intervals), Fig. 3 (chain-linked and balanced panels),
Fig. 4 (Shapley decomposition in 100 x log units, which add up; limiting factors on common sites) and adds Extended Data Fig. 6 (structural and transfer tests).
Inputs are the small summary tables of SONUC_23A / SONUC_23B and the source data of Defter 22 (site map, limiting factors)."""
import os, numpy as np, pandas as pd, matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import cartopy.crs as ccrs, shapefile
from shapely.geometry import shape
from shapely.ops import unary_union

V = 'tables'                    # SONUC_23A / SONUC_23B summary tables
S22 = 'SEKILLER_22'              # output folder of Defter 22 (source data of Figs 2, 4, 5 and ED5)
S21 = 'SONUC_21'                 # output folder of Defter 21 (Q4_sinirlayici_alan.csv: limiting-factor shares per site and period)
CIKTI = 'SEKILLER_23'; os.makedirs(CIKTI, exist_ok=True)
NE = 'naturalearth_lowres.shp'   # Natural Earth 1:110m land polygons (public domain)

# --- Nature style (identical to Defter 22) ---
from matplotlib import font_manager
aile = next((f for f in ['Arial', 'Helvetica', 'Liberation Sans', 'DejaVu Sans'] if any(f == x.name for x in font_manager.fontManager.ttflist)), 'DejaVu Sans')
mpl.rcParams.update({'font.family': aile, 'font.size': 6, 'axes.titlesize': 6.5, 'axes.labelsize': 6, 'xtick.labelsize': 5.5,
                     'ytick.labelsize': 5.5, 'legend.fontsize': 5.5, 'axes.linewidth': 0.5, 'xtick.major.width': 0.5,
                     'ytick.major.width': 0.5, 'xtick.major.size': 2, 'ytick.major.size': 2, 'lines.linewidth': 1.0,
                     'axes.spines.top': False, 'axes.spines.right': False, 'pdf.fonttype': 42, 'ps.fonttype': 42,
                     'savefig.dpi': 300, 'figure.dpi': 150, 'legend.frameon': False, 'axes.unicode_minus': True})
MM = 1 / 25.4; TEK, CIFT = 89 * MM, 183 * MM
RENK = {'All sites': '#3b3b3b', 'Driest 25%': '#b35806', 'Coldest 25%': '#2166ac', 'Region: Europe': '#7b3294'}
ETIKET = {'All sites': 'All sites', 'Driest 25%': 'Driest quarter', 'Coldest 25%': 'Coldest quarter',
          'Region: Europe': 'Europe', 'Region: North America': 'North America', 'Region: Asia': 'Asia',
          'Region: Southern Hemisphere': 'Southern Hemisphere'}
CIZGI = {'All sites': '-', 'Driest 25%': '-', 'Coldest 25%': '--', 'Region: Europe': ':'}
def etiket(g): return ETIKET.get(g, g.replace('Genus: ', ''))
def harf(ax, h, x=-0.16, y=1.04):
    ax.text(x, y, h, transform=ax.transAxes, fontsize=8, fontweight='bold', va='bottom', ha='left')
def kaydet(fig, ad, kaynak=None):
    for uz in ('pdf', 'png'):
        fig.savefig(os.path.join(CIKTI, f'{ad}.{uz}'), bbox_inches='tight')
    if kaynak is not None:
        kaynak.to_csv(os.path.join(CIKTI, f'SOURCE_DATA_{ad}.csv'), index=False)
    print('saved', ad); plt.close(fig)

KARA = unary_union([shape(s.__geo_interface__) for s in shapefile.Reader(NE).shapes()])
def harita(fig, konum, lon, lat, deger, cmap, vmin, vmax, baslik, birim, isaret=None, harf_=None):
    ax = fig.add_axes(konum, projection=ccrs.Robinson()); ax.set_extent([-180, 180, -57, 84], crs=ccrs.PlateCarree())
    ax.add_geometries([KARA], ccrs.PlateCarree(), facecolor='#ececec', edgecolor='#9a9a9a', linewidth=0.25, zorder=0)
    ax.spines['geo'].set_linewidth(0.4); tr = dict(transform=ccrs.PlateCarree())
    lon, lat, deger = np.asarray(lon), np.asarray(lat), np.asarray(deger)
    kw = dict(cmap=cmap, vmin=vmin, vmax=vmax, linewidths=0, rasterized=True, **tr)
    z = ~isaret; ax.scatter(lon[z], lat[z], c=deger[z], s=0.8, alpha=0.45, zorder=3, **kw)
    o = np.where(isaret)[0]; o = o[np.argsort(np.abs(deger[o]))]
    sc = ax.scatter(lon[o], lat[o], c=deger[o], s=2.4, zorder=4, **kw)
    ax.text(0.0, 1.015, harf_ + '   ', transform=ax.transAxes, fontsize=8, fontweight='bold', va='bottom')
    ax.text(0.045, 1.015, baslik, transform=ax.transAxes, fontsize=6.5, va='bottom')
    cax = fig.add_axes([konum[0] + konum[2] * 0.30, konum[1] - 0.02, konum[2] * 0.40, 0.014])
    cb = fig.colorbar(sc, cax=cax, orientation='horizontal', extend='both'); cb.outline.set_linewidth(0.3)
    cb.ax.tick_params(labelsize=5, width=0.4, length=1.5, pad=1); cb.set_label(birim, fontsize=5.5, labelpad=1)
    return ax

A1 = pd.read_csv(f'{V}/A1_ayni_saha.csv'); A2 = pd.read_csv(f'{V}/A2_denge_onyil.csv'); A6 = pd.read_csv(f'{V}/A6_faktoriyel.csv')
B3 = pd.read_csv(f'{V}/B3_karsilastirma.csv'); B3o = pd.read_csv(f'{V}/B3_onyil.csv')
F2 = pd.read_csv(f'{S22}/SOURCE_DATA_Fig2.csv'); F4 = pd.read_csv(f'{S22}/SOURCE_DATA_Fig4.csv')

# ---------------------------------------------------------------------------------------------------------------
# Fig. 2 | Growth change attributed to climate change, 1990-2019
kol = 'total 1990-2019 (%)'; p05 = 'total 1990-2019 members p05 (%)'; p95 = 'total 1990-2019 members p95 (%)'
d = F2[F2.panel == 'a'].copy()
emin = ((d[p95] < 0) | (d[p05] > 0)).to_numpy()
fig = plt.figure(figsize=(CIFT, 0.38 * CIFT))
harita(fig, [0.0, 0.16, 0.58, 0.76], d.lon, d.lat, d[kol].clip(-10, 10), 'BrBG', -6, 6,
       f'Growth change attributed to climate change, 1990–2019 ({len(d):,} sites)', '% per year', isaret=emin, harf_='a')
axb = fig.add_axes([0.72, 0.12, 0.27, 0.78])
gr = ['Driest 25%', 'Region: Europe', 'All sites', 'Region: North America', 'Region: Asia', 'Coldest 25%']
yy = np.arange(len(gr))[::-1]; src2 = []
c = A1[A1.site_set == 'common sites']
for y, g in zip(yy, gr):
    for kay, dy, mk, rk, ms in [('network', 0.15, 'o', '#1f78b4', 3), ('rings', -0.15, 'D', '#e66101', 2.6)]:
        r = c[(c.group == g) & (c.source == kay)].iloc[0]
        axb.errorbar(r.mean_pct, y + dy, xerr=[[r.mean_pct - r.mean_lo95], [r.mean_hi95 - r.mean_pct]], fmt=mk, ms=ms,
                     color=rk, elinewidth=0.7, capsize=0)
        src2.append(dict(group=g, source=kay, statistic='mean over sites', estimate=r.mean_pct, lo95=r.mean_lo95, hi95=r.mean_hi95,
                         n_sites=r.n_sites, n_blocks=r.n_blocks))
axb.axvline(0, color='k', lw=0.4); axb.set_yticks(yy); axb.set_yticklabels([etiket(g) for g in gr])
axb.set_xlabel('Mean growth change, 1990–2019 (% per year)'); axb.set_ylim(-0.6, len(gr) - 0.4)
axb.legend(handles=[Line2D([], [], marker='o', color='#1f78b4', ls='', ms=3, label='Network (20 members)'),
                    Line2D([], [], marker='D', color='#e66101', ls='', ms=2.6, label='Rings (no network)')],
           loc='lower right', bbox_to_anchor=(1.0, 1.0), ncol=1)
harf(axb, 'b', x=-0.55)
kaydet(fig, 'Fig2', pd.concat([d[['studyCode', 'lat', 'lon', 'region', 'genus', kol, p05, p95]].assign(panel='a'),
                               pd.DataFrame(src2).assign(panel='b')], ignore_index=True))

# ---------------------------------------------------------------------------------------------------------------
# Fig. 3 | Emergence of the divide: chain-linked index (a) and a balanced panel with block intervals (b)
fig = plt.figure(figsize=(CIFT, 0.36 * CIFT))
axa = fig.add_axes([0.06, 0.14, 0.41, 0.72]); axb = fig.add_axes([0.575, 0.14, 0.41, 0.72])
ch = A2[A2.method == 'chain-linked']; src3 = []
for g in ['Coldest 25%', 'All sites', 'Region: Europe', 'Driest 25%']:
    x = ch[ch.group == g].sort_values('decade'); xc = x.decade + 5
    axa.fill_between(xc, x.members_p05, x.members_p95, color=RENK[g], alpha=0.18, lw=0)
    axa.plot(xc, x.median_pct, CIZGI[g], color=RENK[g], marker='o', ms=2.2, label=etiket(g))
    src3.append(x.assign(panel='a'))
axa.axhline(0, color='k', lw=0.4); axa.set_xlim(1900, 2020)
axa.set_xlabel('Decade'); axa.set_ylabel('Attributed growth change (% per year)')
axa.set_title('All sites with rings in each decade, chain-linked', loc='left', fontsize=6.5, pad=9)
axa.legend(loc='lower left', ncol=2)
na = ch[ch.group == 'All sites'].sort_values('decade')
for dc, n in zip(na.decade, na.n_sites):
    axa.text(dc + 5, 1.0, f'{n:,}', transform=axa.get_xaxis_transform(), ha='center', va='bottom', fontsize=4.3, color='#555555')
axa.text(1.0, 1.0, ' n', transform=axa.transAxes, ha='left', va='bottom', fontsize=4.3, color='#555555')
harf(axa, 'a', x=-0.13, y=1.08)

bp = A2[A2.method == 'balanced 1930s-2000s']
for g in ['Coldest 25%', 'All sites', 'Region: Europe', 'Driest 25%']:
    x = bp[bp.group == g].sort_values('decade'); xc = x.decade + 5
    axb.fill_between(xc, x.block_lo95, x.block_hi95, color=RENK[g], alpha=0.14, lw=0)
    axb.plot(xc, x.median_pct, CIZGI[g], color=RENK[g], lw=1.0)
    ok = ((x.block_hi95 < 0) | (x.block_lo95 > 0)).to_numpy()
    axb.scatter(xc[ok], x.median_pct[ok], s=7, color=RENK[g], zorder=4, lw=0)
    axb.scatter(xc[~ok], x.median_pct[~ok], s=7, facecolor='white', edgecolor=RENK[g], lw=0.6, zorder=4)
    src3.append(x.assign(panel='b', block_interval_excludes_zero=ok))
axb.axhline(0, color='k', lw=0.4); axb.set_xlim(1930, 2012); axb.set_xlabel('Decade')
axb.set_ylabel('Attributed growth change (% per year)')
nb = bp.groupby('group').n_sites.first()
axb.set_title(f'Same {nb["All sites"]:,} sites in every decade, 1930s–2000s', loc='left', fontsize=6.5, pad=9)
axb.legend(handles=[Line2D([], [], color=RENK[g], ls=CIZGI[g], label=f'{etiket(g)} (n = {nb[g]:,})')
                    for g in ['Coldest 25%', 'All sites', 'Region: Europe', 'Driest 25%']] +
                   [Line2D([], [], marker='o', color='#555555', ls='', ms=2.6, label='95% block interval excludes zero'),
                    Line2D([], [], marker='o', mfc='white', mec='#555555', ls='', ms=2.6, label='includes zero')],
           loc='lower left', ncol=2, fontsize=5)
harf(axb, 'b', x=-0.13, y=1.08)
kaydet(fig, 'Fig3', pd.concat(src3, ignore_index=True))

# ---------------------------------------------------------------------------------------------------------------
# Fig. 4 | Mechanisms: Shapley decomposition (a) and limiting factors (b)
fig = plt.figure(figsize=(CIFT, 0.40 * CIFT))
axa = fig.add_axes([0.06, 0.16, 0.40, 0.70])
grk = ['All sites', 'Coldest 25%', 'Driest 25%', 'Region: Europe', 'Genus: Fagus', 'Genus: Cedrus']
kan = [('shapley_temperature_mean_pct', 'Temperature', '#d6604d'),
       ('shapley_moisture (precipitation + soil moisture)_mean_pct', 'Water supply (precipitation + soil moisture)', '#8c510a'),
       ('shapley_VPD_mean_pct', 'Atmospheric demand (VPD)', '#5aae61')]
k = A6.set_index('group').copy(); w = 0.25; xg = np.arange(len(grk))
# group values in A6 are 100(e^x - 1) of the mean log contribution x; convert back to 100 x (mean log change), where they add up
for c_ in [c for c in k.columns if c.startswith('shapley_')] + ['total_mean_pct']: k[c_] = 100 * np.log1p(k[c_] / 100)
for j, (cc, ad, rk) in enumerate(kan):
    axa.bar(xg + (j - 1) * w, [k.loc[g, cc] for g in grk], w, color=rk, label=ad, lw=0)
axa.scatter(xg, [k.loc[g, 'total_mean_pct'] for g in grk], marker='_', s=70, color='k', lw=1.2, zorder=5, label='Total')
axa.axhline(0, color='k', lw=0.4); axa.set_xticks(xg)
axa.set_xticklabels([etiket(g).replace(' quarter', '\nquarter') + f'\n(n = {k.loc[g, "n_sites"]:,})' for g in grk], fontsize=5)
axa.set_ylabel('Attributed change, 1990–2019\n(100 × mean change in log ring width)')
axa.legend(loc='lower left', bbox_to_anchor=(0, 1.0), ncol=2); harf(axa, 'a', x=-0.13, y=1.12)
src4 = k.loc[grk].reset_index().assign(panel='a')
fak = [('VPD', 'VPD', '#5aae61'), ('heat', 'Heat (above optimum)', '#d6604d'), ('soil moisture', 'Soil moisture', '#8c510a'),
       ('cold', 'Cold', '#4393c3')]
gb = ['All sites', 'Region: Europe', 'Genus: Fagus']; per = ['1902-1930', '1931-1960', '1961-1990', '1991-2019']
axb = fig.add_axes([0.56, 0.16, 0.43, 0.70]); pos, lab = [], []
# limiting-factor shares on a common set of sites: only sites with at least five years in every period (Defter 21, Q4),
# so that changes between periods are not changes in the site sample
q4s = pd.read_csv(os.path.join(S21, 'Q4_sinirlayici_alan.csv'))
q4s = q4s[q4s[[f'VPD {p}' for p in per]].notna().all(axis=1)]
q4 = pd.DataFrame([dict(group=g, period=p, n_sites=len(s_), **{f: s_[f'{f} {p}'].mean() for f, _, _ in fak})
                   for g, s_ in [('All sites', q4s), ('Region: Europe', q4s[q4s.region == 'Europe']), ('Genus: Fagus', q4s[q4s.genus == 'Fagus'])]
                   for p in per])
for i, g in enumerate(gb):
    for j, p in enumerate(per):
        r = q4[(q4.group == g) & (q4.period == p)].iloc[0]; xpos = i * 5.2 + j; alt = 0
        tot_ = sum(r[f] for f, _, _ in fak)
        for f, ad, rk in fak:
            v = r[f] / tot_; axb.bar(xpos, v, 0.85, bottom=alt, color=rk, lw=0); alt += v
        pos.append(xpos); lab.append(p.replace('-', '–\n'))
    axb.text(i * 5.2 + 1.5, 1.04, f'{etiket(g)} (n = {int(q4[q4.group == g].n_sites.iloc[0]):,})', ha='center', va='bottom', fontsize=6, transform=axb.get_xaxis_transform())
axb.set_xticks(pos); axb.set_xticklabels(lab, fontsize=4.6); axb.set_ylim(0, 1); axb.set_ylabel('Share of the growing season')
axb.legend(handles=[Patch(color=rk, label=ad) for _, ad, rk in fak][::-1], loc='upper left', bbox_to_anchor=(1.0, 1.0))
harf(axb, 'b', x=-0.10, y=1.12)
kaydet(fig, 'Fig4', pd.concat([src4, q4.assign(panel='b')], ignore_index=True))

# ---------------------------------------------------------------------------------------------------------------
# Extended Data Fig. 6 | Structural sensitivity and transfer to a warmer period
KAY = [('rings (no network)', 'Rings (no network)', '#e66101', 'D'), ('main (minimum)', 'Network, law of the minimum (main)', '#1f78b4', 'o'),
       ('product rule', 'Network, product rule', '#33a02c', 's'), ('trained 1902-1960', 'Network trained on 1902–1960 only', '#999999', '^')]
fig = plt.figure(figsize=(CIFT, 0.62 * CIFT))
def nokta(ax, gruplar, harf_):
    yy = np.arange(len(gruplar))[::-1]
    for y, g in zip(yy, gruplar):
        for j, (s, ad, rk, mk) in enumerate(KAY):
            r = B3[(B3.group == g) & (B3.source == s)].iloc[0]; dy = 0.27 - j * 0.18
            ax.errorbar(r.mean_pct, y + dy, xerr=[[r.mean_pct - r.mean_lo95], [r.mean_hi95 - r.mean_pct]], fmt=mk, ms=2.6,
                        color=rk, mfc=rk if s != 'trained 1902-1960' else 'white', elinewidth=0.6, capsize=0)
    ax.axvline(0, color='k', lw=0.4); ax.set_yticks(yy)
    ax.set_yticklabels([etiket(g) + f' ({B3[B3.group == g].n_sites.iloc[0]:,})' for g in gruplar])
    ax.set_ylim(-0.6, len(gruplar) - 0.4); ax.set_xlabel('Mean growth change, 1990–2019 (% per year)'); harf(ax, harf_, x=-0.42)
axa = fig.add_axes([0.13, 0.56, 0.33, 0.36]); nokta(axa, ['Driest 25%', 'Region: Europe', 'All sites', 'Region: North America', 'Region: Asia', 'Coldest 25%'], 'a')
axb = fig.add_axes([0.63, 0.56, 0.33, 0.36]); nokta(axb, ['Genus: Cedrus', 'Genus: Fagus', 'Genus: Pseudotsuga', 'Genus: Larix'], 'b')
fig.legend(handles=[Line2D([], [], marker=mk, color=rk, mfc=rk if s != 'trained 1902-1960' else 'white', ls='', ms=2.8, label=ad)
                    for s, ad, rk, mk in KAY], loc='lower center', bbox_to_anchor=(0.5, 0.955), ncol=4)
for i, (g, baslik) in enumerate([('Driest 25%', 'Driest quarter'), ('Coldest 25%', 'Coldest quarter')]):
    ax = fig.add_axes([0.08 + i * 0.49, 0.08, 0.40, 0.33])
    for s, ad, rk, mk in KAY[1:]:
        x = B3o[(B3o.group == g) & (B3o.source == s)].sort_values('decade'); xc = x.decade + 5
        ax.fill_between(xc, x.members_p05, x.members_p95, color=rk, alpha=0.18, lw=0)
        ax.plot(xc, x.median_pct, color=rk, ls='-' if s != 'trained 1902-1960' else '--', marker=mk, ms=2,
                mfc=rk if s != 'trained 1902-1960' else 'white')
    ax.axhline(0, color='k', lw=0.4); ax.set_xlim(1900, 2020); ax.set_xlabel('Decade')
    ax.set_ylabel('Attributed growth change (% per year)'); ax.set_title(f'{baslik}, chain-linked median', loc='left', fontsize=6.5)
    harf(ax, 'cd'[i], x=-0.15)
kaydet(fig, 'ED6', pd.concat([B3.assign(panel='a,b'), B3o.assign(panel='c,d')], ignore_index=True))
print('==== SEKILLER 23 TAMAM ====')

# ---------------------------------------------------------------------------------------------------------------
# Fig. 5 | The shift accumulates over a tree's life (panel b, age at 15 cm, removed in draft 13)
F5 = pd.read_csv(f'{S22}/SOURCE_DATA_Fig5.csv'); F5 = F5[F5.diameter_difference_100yr_pct.notna()]
fig, ax = plt.subplots(figsize=(TEK, 0.62 * TEK))
for i, (_, r) in enumerate(F5.iterrows()):
    g, v = r.group, r.diameter_difference_100yr_pct; rk = RENK.get(g, '#1b7837' if v > 0 else '#8c510a')
    ax.plot([0, v], [i, i], color=rk, lw=1.4, solid_capstyle='butt'); ax.scatter([v], [i], color=rk, s=12, zorder=3)
    ax.text(v + (0.25 if v >= 0 else -0.25), i, f'{v:+.1f}%'.replace('-', '−'), va='center', ha='left' if v >= 0 else 'right', fontsize=5)
ax.set_yticks(range(len(F5))); ax.set_yticklabels([etiket(g) for g in F5.group]); ax.invert_yaxis(); ax.axvline(0, color='k', lw=0.4)
lim = max(F5.diameter_difference_100yr_pct.abs().max() * 1.35, 2); ax.set_xlim(-lim, lim)
ax.set_xlabel('Stem diameter after 100 years,\nobserved vs without climate change (%)')
kaydet(fig, 'Fig5', F5[['group', 'diameter_difference_100yr_pct', 'share_negative', 'n_sites']])

# ---------------------------------------------------------------------------------------------------------------
# Extended Data Fig. 5 | Attribution by genus, network and rings, both with 10-degree spatial-block intervals
E5 = pd.read_csv(f'{S22}/SOURCE_DATA_ED5.csv')
d = F2[F2.panel == 'a'].copy()
d['blok'] = (np.floor((d.lat + 90) / 10) * 100 + np.floor((d.lon + 180) / 10)).astype(int)
rng = np.random.default_rng(2026)
def blok_boot(x, b, B=1000):
    u = np.unique(b); idx = {k: np.where(b == k)[0] for k in u}; out = []
    for _ in range(B):
        s = rng.choice(u, len(u), replace=True); out.append(np.median(np.concatenate([x[idx[k]] for k in s])))
    return np.quantile(out, [0.025, 0.975])
gen = E5[E5.source == 'network'].copy(); src = []
for _, r in gen.iterrows():
    m = d.genus == r.group.replace('Genus: ', ''); x = d.loc[m, kol].to_numpy(); b = d.loc[m, 'blok'].to_numpy()
    lo, hi = blok_boot(x, b)
    src.append(dict(group=r.group, source='network', estimate=float(np.median(x)), lo95=lo, hi95=hi, n_sites=int(m.sum()), n_blocks=len(np.unique(b))))
net = pd.DataFrame(src).sort_values('estimate').reset_index(drop=True)
ring = E5[E5.source != 'network'].set_index('group')
fig, ax = plt.subplots(figsize=(TEK, 0.10 * TEK + 0.045 * TEK * len(net)))
for y, r in net.iterrows():
    ax.errorbar(r.estimate, y + 0.15, xerr=[[r.estimate - r.lo95], [r.hi95 - r.estimate]], fmt='o', ms=2.6, color='#1f78b4', elinewidth=0.6)
    if r.group in ring.index:
        h = ring.loc[r.group]
        ax.errorbar(h.estimate, y - 0.15, xerr=[[h.estimate - h.lo95], [h.hi95 - h.estimate]], fmt='D', ms=2.2, color='#e66101', elinewidth=0.6)
    ax.text(1.01, y, f'{int(r.n_sites)}', transform=ax.get_yaxis_transform(), fontsize=4.8, va='center', color='#666666')
ax.set_yticks(range(len(net))); ax.set_yticklabels([etiket(g) for g in net.group], fontstyle='italic'); ax.axvline(0, color='k', lw=0.4)
ax.set_xlabel('Growth change, 1990–2019 (% per year)')
ax.legend(handles=[Line2D([], [], marker='o', color='#1f78b4', ls='', ms=3, label='Network (median, 20 members)'),
                   Line2D([], [], marker='D', color='#e66101', ls='', ms=2.6, label='Rings (no network)')], loc='lower right', bbox_to_anchor=(1.0, 1.0), ncol=2)
kaydet(fig, 'ED5', pd.concat([net, E5[E5.source != 'network']], ignore_index=True))
print(net.round(2).to_string())
