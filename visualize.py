"""
=============================================================
  RETAIL SALES RECOMMENDATION SYSTEM
  Visualization Engine  —  visualize.py
  Produces 8 publication-quality charts
=============================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
from matplotlib.colors import LinearSegmentedColormap
import warnings
warnings.filterwarnings("ignore")

# ── Style & palette ─────────────────────────────────────────
plt.rcParams.update({
    "font.family":       "DejaVu Sans",
    "axes.facecolor":    "#0f1117",
    "figure.facecolor":  "#0f1117",
    "axes.edgecolor":    "#2a2d3a",
    "axes.labelcolor":   "#c9d1d9",
    "text.color":        "#c9d1d9",
    "xtick.color":       "#8b949e",
    "ytick.color":       "#8b949e",
    "grid.color":        "#1e2130",
    "grid.linewidth":    0.8,
    "axes.grid":         True,
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "font.size":         11,
})

ACCENT  = "#58a6ff"
GREEN   = "#3fb950"
YELLOW  = "#f0e68c"
ORANGE  = "#ff9f43"
RED     = "#ff6b6b"
PURPLE  = "#c084fc"
TEAL    = "#2dd4bf"

PALETTE = [ACCENT, GREEN, YELLOW, ORANGE, RED, PURPLE, TEAL,
           "#f97316","#a78bfa","#34d399","#fb7185","#fbbf24"]

# ── Load data ──────────────────────────────────────────────
df      = pd.read_csv("data/sales_data.csv")
monthly = pd.read_csv("output/monthly_trends.csv")
prod    = pd.read_csv("output/product_ranking.csv")
region  = pd.read_csv("output/regional_performance.csv")

month_labels = ["Jan","Feb","Mar","Apr","May","Jun",
                "Jul","Aug","Sep","Oct","Nov","Dec"]

def save(fig, name):
    fig.savefig(f"output/{name}.png", dpi=160, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"  ✅ Saved {name}.png")

# ══════════════════════════════════════════════════════════════
# CHART 1 — MASTER DASHBOARD (4 panels)
# ══════════════════════════════════════════════════════════════
fig = plt.figure(figsize=(20, 12))
fig.patch.set_facecolor("#0a0d14")
gs  = gridspec.GridSpec(2, 3, figure=fig, hspace=0.45, wspace=0.35)

# ── Panel A: Monthly Revenue Line ──────────────────────────
ax1 = fig.add_subplot(gs[0, :2])
ax1.set_facecolor("#0f1117")
rev = monthly["Revenue"].values / 1e6
x   = np.arange(12)
ax1.fill_between(x, rev, alpha=0.15, color=ACCENT)
ax1.plot(x, rev, color=ACCENT, lw=2.5, marker="o", ms=6, zorder=5)
# trend line
from scipy import stats as sst
slope, intercept, *_ = sst.linregress(x, rev)
trend = slope*x + intercept
ax1.plot(x, trend, "--", color=ORANGE, lw=1.5, alpha=0.8, label=f"Trend  (+₹{slope:.2f}L/mo)")
ax1.set_xticks(x); ax1.set_xticklabels(month_labels)
ax1.set_title("Monthly Revenue Trend — FY 2024", color="white", fontsize=14, fontweight="bold", pad=12)
ax1.set_ylabel("Revenue (₹ Lakhs)")
ax1.legend(framealpha=0.2, loc="upper left")
for xi, yi in zip(x, rev):
    ax1.annotate(f"₹{yi:.1f}L", (xi, yi), textcoords="offset points",
                 xytext=(0,9), ha="center", fontsize=7.5, color="#8b949e")

# ── Panel B: KPI tiles ─────────────────────────────────────
ax2 = fig.add_subplot(gs[0, 2])
ax2.set_facecolor("#0a0d14"); ax2.axis("off")
kpis = [
    ("Total Revenue", f"₹{df['Revenue'].sum()/1e6:.1f}L", ACCENT),
    ("Total Units Sold", f"{df['Units_Sold'].sum():,}", GREEN),
    ("Top Product", "Smart Watch", YELLOW),
    ("Peak Month", "December", ORANGE),
    ("Avg Order Value", f"₹{df['Revenue'].mean():,.0f}", PURPLE),
    ("Best Region", "East", TEAL),
]
for i, (label, val, col) in enumerate(kpis):
    y = 0.90 - i * 0.155
    ax2.add_patch(mpatches.FancyBboxPatch((0.02, y-0.05), 0.96, 0.12,
        boxstyle="round,pad=0.02", linewidth=1.5,
        edgecolor=col, facecolor=col+"22", transform=ax2.transAxes))
    ax2.text(0.10, y+0.015, label, transform=ax2.transAxes,
             fontsize=8.5, color="#8b949e", va="center")
    ax2.text(0.10, y-0.025, val,   transform=ax2.transAxes,
             fontsize=11, color=col, va="center", fontweight="bold")
ax2.set_title("Key Performance Indicators", color="white", fontsize=12, fontweight="bold", pad=10)

# ── Panel C: Category Revenue bars ─────────────────────────
ax3 = fig.add_subplot(gs[1, 0])
ax3.set_facecolor("#0f1117")
cat_rev = df.groupby("Category")["Revenue"].sum().sort_values() / 1e6
colors  = [ACCENT, GREEN, ORANGE, PURPLE, TEAL]
bars = ax3.barh(cat_rev.index, cat_rev.values, color=colors, height=0.6, edgecolor="none")
for bar, v in zip(bars, cat_rev.values):
    ax3.text(v + 0.5, bar.get_y() + bar.get_height()/2,
             f"₹{v:.1f}L", va="center", fontsize=9, color="white")
ax3.set_title("Revenue by Category", color="white", fontsize=12, fontweight="bold")
ax3.set_xlabel("Revenue (₹ Lakhs)")

# ── Panel D: Regional donut ────────────────────────────────
ax4 = fig.add_subplot(gs[1, 1])
ax4.set_facecolor("#0f1117")
reg_rev = df.groupby("Region")["Revenue"].sum()
wedges, texts, autotexts = ax4.pie(
    reg_rev, labels=reg_rev.index, autopct="%1.1f%%",
    colors=[ACCENT, GREEN, YELLOW, ORANGE, PURPLE],
    wedgeprops=dict(width=0.55, edgecolor="#0a0d14", linewidth=2),
    startangle=140, pctdistance=0.75,
)
for t in texts:    t.set_color("#c9d1d9"); t.set_fontsize(9)
for t in autotexts: t.set_color("white"); t.set_fontsize(8)
ax4.set_title("Regional Revenue Split", color="white", fontsize=12, fontweight="bold")

# ── Panel E: Top-5 products bar ────────────────────────────
ax5 = fig.add_subplot(gs[1, 2])
ax5.set_facecolor("#0f1117")
top5 = prod.head(5)
bars = ax5.bar(range(5), top5["Total_Revenue"]/1e6,
               color=[ACCENT, GREEN, YELLOW, ORANGE, RED],
               width=0.6, edgecolor="none")
ax5.set_xticks(range(5))
ax5.set_xticklabels([p.replace(" ","\n") for p in top5["Product"]], fontsize=8)
ax5.set_title("Top 5 Products by Revenue", color="white", fontsize=12, fontweight="bold")
ax5.set_ylabel("Revenue (₹ Lakhs)")
for bar, v in zip(bars, top5["Total_Revenue"]/1e6):
    ax5.text(bar.get_x()+bar.get_width()/2, v+0.3,
             f"₹{v:.1f}L", ha="center", fontsize=8, color="white")

fig.suptitle("RETAIL SALES RECOMMENDATION SYSTEM  |  FY 2024 Analytics Dashboard",
             color="white", fontsize=16, fontweight="bold", y=1.01)
save(fig, "01_master_dashboard")

# ══════════════════════════════════════════════════════════════
# CHART 2 — PRODUCT RANKING & ABC PARETO
# ══════════════════════════════════════════════════════════════
fig, (ax, ax_r) = plt.subplots(1, 2, figsize=(18, 7))
fig.patch.set_facecolor("#0a0d14")
for a in [ax, ax_r]: a.set_facecolor("#0f1117")

# Pareto bar
abc_colors = {"A": ACCENT, "B": GREEN, "C": ORANGE}
bar_colors  = [abc_colors[c] for c in prod["ABC_Class"]]
bars = ax.bar(range(len(prod)), prod["Total_Revenue"]/1e6, color=bar_colors, edgecolor="none", width=0.7)
ax.set_xticks(range(len(prod)))
ax.set_xticklabels(prod["Product"], rotation=40, ha="right", fontsize=8)
ax2_twin = ax.twinx()
ax2_twin.plot(range(len(prod)), prod["Cumulative_Share"], color=YELLOW, lw=2, marker="o", ms=5)
ax2_twin.axhline(70, color=ACCENT, ls="--", lw=1, alpha=0.6)
ax2_twin.axhline(90, color=GREEN,  ls="--", lw=1, alpha=0.6)
ax2_twin.set_ylabel("Cumulative Revenue %", color=YELLOW)
ax2_twin.tick_params(colors=YELLOW)
ax.set_title("ABC Pareto Analysis — All Products", color="white", fontsize=13, fontweight="bold")
ax.set_ylabel("Revenue (₹ Lakhs)")
legend_patches = [mpatches.Patch(color=c, label=f"Class {k}") for k,c in abc_colors.items()]
ax.legend(handles=legend_patches, loc="upper right", framealpha=0.2)

# Scatter: Units vs Revenue coloured by margin
sc = ax_r.scatter(prod["Total_Units"], prod["Total_Revenue"]/1e6,
                  c=prod["Avg_Margin"], cmap="RdYlGn", s=120, edgecolors="white", lw=0.5, zorder=5)
for _, row in prod.iterrows():
    ax_r.annotate(row["Product"], (row["Total_Units"], row["Total_Revenue"]/1e6),
                  textcoords="offset points", xytext=(5,3), fontsize=7, color="#8b949e")
plt.colorbar(sc, ax=ax_r, label="Avg Profit Margin %")
ax_r.set_xlabel("Total Units Sold"); ax_r.set_ylabel("Total Revenue (₹ Lakhs)")
ax_r.set_title("Units vs Revenue (coloured by Profit Margin)", color="white", fontsize=13, fontweight="bold")

fig.suptitle("Product Performance Analysis", color="white", fontsize=15, fontweight="bold")
plt.tight_layout()
save(fig, "02_product_pareto")

# ══════════════════════════════════════════════════════════════
# CHART 3 — MONTHLY HEATMAP (Category × Month)
# ══════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(15, 6))
fig.patch.set_facecolor("#0a0d14"); ax.set_facecolor("#0f1117")
pivot = df.pivot_table(values="Revenue", index="Category", columns="Month", aggfunc="sum") / 1e6
cmap  = LinearSegmentedColormap.from_list("hm", ["#0a0d14","#1a3a5c",ACCENT,"#f0e68c",ORANGE])
im    = ax.imshow(pivot.values, aspect="auto", cmap=cmap)
ax.set_xticks(range(12)); ax.set_xticklabels(month_labels)
ax.set_yticks(range(len(pivot))); ax.set_yticklabels(pivot.index)
for i in range(len(pivot)):
    for j in range(12):
        ax.text(j, i, f"₹{pivot.values[i,j]:.1f}L",
                ha="center", va="center", fontsize=7.5,
                color="white" if pivot.values[i,j] > pivot.values.mean() else "#8b949e")
plt.colorbar(im, ax=ax, label="Revenue (₹ Lakhs)")
ax.set_title("Revenue Heatmap — Category × Month", color="white", fontsize=14, fontweight="bold")
fig.tight_layout()
save(fig, "03_category_month_heatmap")

# ══════════════════════════════════════════════════════════════
# CHART 4 — REGIONAL × CATEGORY GROUPED BARS
# ══════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(16, 7))
fig.patch.set_facecolor("#0a0d14"); ax.set_facecolor("#0f1117")
reg_cat = df.groupby(["Region","Category"])["Revenue"].sum().unstack() / 1e6
x = np.arange(len(reg_cat))
w = 0.16
cats = reg_cat.columns.tolist()
for i, (cat, col) in enumerate(zip(cats, PALETTE)):
    ax.bar(x + i*w - w*2, reg_cat[cat], width=w, label=cat, color=col, edgecolor="none", alpha=0.9)
ax.set_xticks(x); ax.set_xticklabels(reg_cat.index, fontsize=10)
ax.set_ylabel("Revenue (₹ Lakhs)")
ax.set_title("Regional Performance by Category", color="white", fontsize=14, fontweight="bold")
ax.legend(framealpha=0.2, fontsize=9)
fig.tight_layout()
save(fig, "04_regional_category_bars")

# ══════════════════════════════════════════════════════════════
# CHART 5 — QUARTERLY COMPARISON + FORECASTING
# ══════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.patch.set_facecolor("#0a0d14")
for a in axes: a.set_facecolor("#0f1117")

# Quarterly grouped by category
qtr_cat = df.groupby(["Quarter","Category"])["Revenue"].sum().unstack() / 1e6
qx = np.arange(4); qw = 0.15
for i, (cat, col) in enumerate(zip(qtr_cat.columns, PALETTE)):
    axes[0].bar(qx + i*qw - qw*2, qtr_cat[cat], width=qw, label=cat, color=col, edgecolor="none", alpha=0.9)
axes[0].set_xticks(qx); axes[0].set_xticklabels(["Q1","Q2","Q3","Q4"])
axes[0].set_ylabel("Revenue (₹ Lakhs)")
axes[0].set_title("Quarterly Revenue by Category", color="white", fontsize=13, fontweight="bold")
axes[0].legend(framealpha=0.2, fontsize=8)

# 3-month forecast via linear extrapolation
from scipy.stats import linregress
x_all = np.arange(12)
rev_vals = monthly["Revenue"].values / 1e6
sl, ic, rv, *_ = linregress(x_all, rev_vals)
x_fut  = np.arange(12, 15)
y_fut  = sl * x_fut + ic
conf   = 1.96 * np.std(rev_vals - (sl*x_all + ic))
axes[1].fill_between(x_all, rev_vals - conf*0.3, rev_vals + conf*0.3, alpha=0.1, color=ACCENT)
axes[1].plot(x_all, rev_vals, color=ACCENT, lw=2.5, label="Actual", marker="o", ms=5)
axes[1].plot(x_all, sl*x_all+ic, "--", color=YELLOW, lw=1.5, alpha=0.6, label="Trend")
axes[1].fill_between(x_fut, y_fut-conf, y_fut+conf, alpha=0.15, color=GREEN)
axes[1].plot(x_fut, y_fut, color=GREEN, lw=2.5, ls="--", marker="D", ms=6, label="Forecast (Q1 2025)")
for xi, yi in zip(x_fut, y_fut):
    axes[1].annotate(f"₹{yi:.1f}L", (xi, yi), textcoords="offset points",
                     xytext=(0,9), ha="center", fontsize=9, color=GREEN)
axes[1].set_xticks(range(15))
axes[1].set_xticklabels(month_labels + ["Jan'25","Feb'25","Mar'25"], fontsize=8, rotation=30)
axes[1].set_title("Revenue Trend + 3-Month Forecast", color="white", fontsize=13, fontweight="bold")
axes[1].set_ylabel("Revenue (₹ Lakhs)")
axes[1].legend(framealpha=0.2)

fig.suptitle("Quarterly Analysis & Forecasting", color="white", fontsize=15, fontweight="bold")
plt.tight_layout()
save(fig, "05_quarterly_forecast")

# ══════════════════════════════════════════════════════════════
# CHART 6 — DISCOUNT ELASTICITY & PRICING
# ══════════════════════════════════════════════════════════════
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
fig.patch.set_facecolor("#0a0d14")
for a in [ax1, ax2]: a.set_facecolor("#0f1117")

disc = df.groupby("Discount_Pct").agg(Revenue=("Revenue","sum"), Units=("Units_Sold","sum")).reset_index()
disc["Revenue"] /= 1e6
ax1.bar(disc["Discount_Pct"].astype(str).apply(lambda x: f"{x}%"),
        disc["Revenue"], color=[ACCENT,GREEN,YELLOW,ORANGE,RED], edgecolor="none", width=0.55)
ax1.set_xlabel("Discount Level"); ax1.set_ylabel("Revenue (₹ Lakhs)")
ax1.set_title("Revenue by Discount Tier", color="white", fontsize=13, fontweight="bold")
for i, row in disc.iterrows():
    ax1.text(i, row["Revenue"]+0.3, f"₹{row['Revenue']:.1f}L", ha="center", fontsize=9)

# Price vs units scatter per product
prod_merge = df.groupby("Product").agg(Avg_Price=("Net_Price","mean"), Total_Units=("Units_Sold","sum"),
                                        Category=("Category","first")).reset_index()
cat_list = prod_merge["Category"].unique()
for cat, col in zip(cat_list, PALETTE):
    mask = prod_merge["Category"] == cat
    ax2.scatter(prod_merge[mask]["Avg_Price"], prod_merge[mask]["Total_Units"],
                color=col, s=80, label=cat, edgecolors="white", lw=0.4, zorder=5)
for _, row in prod_merge.iterrows():
    ax2.annotate(row["Product"].split()[0], (row["Avg_Price"], row["Total_Units"]),
                 textcoords="offset points", xytext=(4,2), fontsize=6.5, color="#8b949e")
ax2.set_xlabel("Avg Net Price (₹)"); ax2.set_ylabel("Total Units Sold")
ax2.set_title("Price Elasticity by Product", color="white", fontsize=13, fontweight="bold")
ax2.legend(framealpha=0.2, fontsize=8)

fig.suptitle("Pricing & Discount Analysis", color="white", fontsize=15, fontweight="bold")
plt.tight_layout()
save(fig, "06_discount_pricing")

# ══════════════════════════════════════════════════════════════
# CHART 7 — RECOMMENDATION DASHBOARD
# ══════════════════════════════════════════════════════════════
fig = plt.figure(figsize=(18, 10))
fig.patch.set_facecolor("#08090f")
gs  = gridspec.GridSpec(2, 3, figure=fig, hspace=0.55, wspace=0.40)

recs = [
    ("R-01", "Product Focus", "Smart Watch\nInventory +20%\nFlash Sale Q4", "+12–18%\nRevenue", ACCENT, "HIGH"),
    ("R-02", "Seasonal\nRestocking",  "Pre-stock\nElectronics +30%\nfrom October",  "+8% fewer\nStockouts", GREEN, "HIGH"),
    ("R-03", "Regional\nExpansion",   "East → Central\nPlaybook transfer\n+ Local Ads", "+15%\nCentral Rev", ORANGE, "MEDIUM"),
    ("R-04", "Discount\nOptimisation","Cap discounts\nat 10%; 15%+\nfor clearance only", "+4%\nGross Margin", YELLOW, "MEDIUM"),
    ("R-05", "Portfolio\nPruning",    "Bundle 6 Class-C\nproducts with\nClass-A items", "+5%\nAOV", PURPLE, "LOW"),
    ("R-06", "Cross-Sell\nEngine",   "Electronics↔Sports\naffinity pairing\n+ widget", "+7%\nBasket Size", TEAL, "HIGH"),
]
positions = [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2)]
for (r,c), (id_, title, body, impact, col, prio) in zip(positions, recs):
    ax = fig.add_subplot(gs[r, c])
    ax.set_facecolor(col+"18")
    ax.axis("off")
    ax.add_patch(mpatches.FancyBboxPatch((0,0), 1, 1,
        boxstyle="round,pad=0.04", linewidth=2,
        edgecolor=col, facecolor=col+"18", transform=ax.transAxes))
    prio_col = {"HIGH": RED, "MEDIUM": YELLOW, "LOW": GREEN}[prio]
    ax.text(0.05, 0.92, f"  {id_}  |  {prio} PRIORITY",
            transform=ax.transAxes, fontsize=8, color=prio_col,
            fontweight="bold", va="top",
            bbox=dict(boxstyle="round,pad=0.3", facecolor=prio_col+"30", edgecolor="none"))
    ax.text(0.5, 0.68, title, transform=ax.transAxes,
            ha="center", va="center", fontsize=11, color=col, fontweight="bold")
    ax.text(0.5, 0.40, body, transform=ax.transAxes,
            ha="center", va="center", fontsize=9, color="#c9d1d9", linespacing=1.5)
    ax.text(0.5, 0.08, impact, transform=ax.transAxes,
            ha="center", va="center", fontsize=12, color=col,
            fontweight="bold")

fig.suptitle("🤖  RECOMMENDATION ENGINE — Strategic Playbook FY 2025",
             color="white", fontsize=15, fontweight="bold", y=1.02)
save(fig, "07_recommendation_cards")

# ══════════════════════════════════════════════════════════════
# CHART 8 — PROFIT MARGIN DEEP DIVE
# ══════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 2, figsize=(16, 7))
fig.patch.set_facecolor("#0a0d14")
for a in axes: a.set_facecolor("#0f1117")

# Margin distribution violin
import matplotlib.pyplot as plt
cat_list = sorted(df["Category"].unique())
data_by_cat = [df[df["Category"]==c]["Profit_Margin_Pct"].values for c in cat_list]
vp = axes[0].violinplot(data_by_cat, positions=range(len(cat_list)), showmedians=True, widths=0.7)
for i, (body, col) in enumerate(zip(vp["bodies"], PALETTE)):
    body.set_facecolor(col); body.set_alpha(0.6); body.set_edgecolor("white")
vp["cmedians"].set_color("white"); vp["cmedians"].set_lw(2)
vp["cbars"].set_color("#8b949e"); vp["cmins"].set_color("#8b949e"); vp["cmaxes"].set_color("#8b949e")
axes[0].set_xticks(range(len(cat_list)))
axes[0].set_xticklabels(cat_list, rotation=20, ha="right")
axes[0].set_ylabel("Profit Margin %")
axes[0].set_title("Profit Margin Distribution by Category", color="white", fontsize=13, fontweight="bold")

# Profit waterfall by quarter
qtr_profit = df.groupby("Quarter")["Profit"].sum() / 1e6
running = 0
bars_x  = []; bar_bottoms = []; bar_heights = []; bar_colors_ = []
for i, (q, p) in enumerate(qtr_profit.items()):
    bars_x.append(i); bar_bottoms.append(running); bar_heights.append(p); bar_colors_.append(PALETTE[i])
    running += p
axes[1].bar(bars_x, bar_heights, bottom=bar_bottoms, color=bar_colors_, edgecolor="none", width=0.5)
for i, (bx, bb, bh) in enumerate(zip(bars_x, bar_bottoms, bar_heights)):
    axes[1].text(bx, bb+bh+0.3, f"₹{bh:.1f}L", ha="center", fontsize=10, color="white", fontweight="bold")
    axes[1].text(bx, bb+bh/2, f"Q{i+1}", ha="center", fontsize=10, color="white", va="center")
axes[1].plot([-0.5, 3.5], [running, running], "--", color=YELLOW, lw=1.5, label=f"Total: ₹{running:.1f}L")
axes[1].set_xticks(bars_x); axes[1].set_xticklabels(["Q1","Q2","Q3","Q4"])
axes[1].set_ylabel("Profit (₹ Lakhs)")
axes[1].set_title("Quarterly Profit Waterfall", color="white", fontsize=13, fontweight="bold")
axes[1].legend(framealpha=0.2)

fig.suptitle("Profit Analysis Deep-Dive", color="white", fontsize=15, fontweight="bold")
plt.tight_layout()
save(fig, "08_profit_analysis")

print("\n🎉  All 8 charts generated successfully in /output/")
