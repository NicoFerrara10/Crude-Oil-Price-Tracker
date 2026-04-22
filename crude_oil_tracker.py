!pip install yfinance matplotlib --quiet

import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from datetime import datetime
import pytz

WTI_ALERT_PRICE   = 85.00   # Alert if WTI crosses above this
BRENT_ALERT_PRICE = 88.00   # Alert if Brent crosses above this

wti   = yf.Ticker("CL=F")   # WTI Crude futures
brent = yf.Ticker("BZ=F")   # Brent Crude futures

wti_price   = round(wti.fast_info['last_price'], 2)
brent_price = round(brent.fast_info['last_price'], 2)
spread      = round(wti_price - brent_price, 2)


print("=" * 40)
print("  CRUDE OIL PRICE MONITOR")
eastern = pytz.timezone('America/New_York')
print(f"  {datetime.now(eastern).strftime('%b %d, %Y  %I:%M %p')} ET")
print("=" * 40)
print(f"  WTI Crude:    ${wti_price}/bbl")
print(f"  Brent Crude:  ${brent_price}/bbl")
print(f"  WTI/Brent Spread: ${spread}/bbl")
print("=" * 40)


print("\n  ALERTS:")

if wti_price >= WTI_ALERT_PRICE:
    print(f"  ⚠️  WTI above ${WTI_ALERT_PRICE} threshold!")
else:
    print(f"  ✓  WTI below alert threshold (${WTI_ALERT_PRICE})")

if brent_price >= BRENT_ALERT_PRICE:
    print(f"  ⚠️  Brent above ${BRENT_ALERT_PRICE} threshold!")
else:
    print(f"  ✓  Brent below alert threshold (${BRENT_ALERT_PRICE})")


print("\n  SPREAD NOTE:")
if spread < -3:
    print("  Brent trading at a significant premium to WTI.")
    print("  US crude is relatively cheap vs global benchmark.")
elif spread > 1:
    print("  WTI trading at a premium to Brent — unusual.")
else:
    print("  WTI/Brent spread within normal range.")

print()

wti_hist   = wti.history(period="1y")['Close']
brent_hist = brent.history(period="1y")['Close']


fig, ax = plt.subplots(figsize=(14, 6))
fig.patch.set_facecolor('#0a0e1a')
ax.set_facecolor('#0d1117')

ax.plot(wti_hist.index,   wti_hist.values,   color='#f59e0b',
        linewidth=2, label='WTI Crude')
ax.plot(brent_hist.index, brent_hist.values, color='#38bdf8',
        linewidth=2, label='Brent Crude')


ax.fill_between(wti_hist.index, wti_hist.values, brent_hist.values,
                alpha=0.1, color='#ffffff')

ax.axhline(WTI_ALERT_PRICE,   color='#f59e0b', linestyle='--',
           linewidth=1, alpha=0.6, label=f'WTI Alert (${WTI_ALERT_PRICE})')
ax.axhline(BRENT_ALERT_PRICE, color='#38bdf8', linestyle='--',
           linewidth=1, alpha=0.6, label=f'Brent Alert (${BRENT_ALERT_PRICE})')

ax.set_title('WTI vs. Brent Crude — 1 Year Price History',
             color='#f1f5f9', fontsize=14, fontweight='bold', pad=14)
ax.set_ylabel('Price ($/bbl)', color='#64748b', fontsize=11)
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('$%.0f'))
ax.tick_params(colors='#334155')
ax.spines['bottom'].set_color('#1e3a5f')
ax.spines['left'].set_color('#1e3a5f')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(color='#0f2040', linestyle='--', alpha=0.6)
ax.legend(facecolor='#0d1117', edgecolor='#1e3a5f',
          labelcolor='#e2e8f0', fontsize=10)

plt.tight_layout()
plt.savefig('crude_oil_chart.png', dpi=150, bbox_inches='tight',
            facecolor='#0a0e1a')
plt.show()
print("✓ Chart saved as crude_oil_chart.png")
