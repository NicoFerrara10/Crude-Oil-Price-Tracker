# ─────────────────────────────────────────────────────────────
#  Crude Oil Price Tracker
#  Author: Nico Ferrara
#
#  Pulls live WTI and Brent crude oil prices and flags when
#  prices cross a threshold — the kind of basic monitoring
#  a supply trading desk would want running in the background.
# ─────────────────────────────────────────────────────────────

!pip install yfinance --quiet

import yfinance as yf
from datetime import datetime

# ── Settings ──────────────────────────────────────────────────
# Change these to whatever prices you want to monitor
WTI_ALERT_PRICE   = 85.00   # Alert if WTI crosses above this
BRENT_ALERT_PRICE = 88.00   # Alert if Brent crosses above this

# ── Fetch live prices ──────────────────────────────────────────
wti   = yf.Ticker("CL=F")   # WTI Crude futures
brent = yf.Ticker("BZ=F")   # Brent Crude futures

wti_price   = round(wti.fast_info['last_price'], 2)
brent_price = round(brent.fast_info['last_price'], 2)
spread      = round(wti_price - brent_price, 2)

# ── Print summary ──────────────────────────────────────────────
print("=" * 40)
print("  CRUDE OIL PRICE MONITOR")
print(f"  {datetime.now().strftime('%b %d, %Y  %I:%M %p')}")
print("=" * 40)
print(f"  WTI Crude:    ${wti_price}/bbl")
print(f"  Brent Crude:  ${brent_price}/bbl")
print(f"  WTI/Brent Spread: ${spread}/bbl")
print("=" * 40)

# ── Price alerts ───────────────────────────────────────────────
print("\n  ALERTS:")

if wti_price >= WTI_ALERT_PRICE:
    print(f"  ⚠️  WTI above ${WTI_ALERT_PRICE} threshold!")
else:
    print(f"  ✓  WTI below alert threshold (${WTI_ALERT_PRICE})")

if brent_price >= BRENT_ALERT_PRICE:
    print(f"  ⚠️  Brent above ${BRENT_ALERT_PRICE} threshold!")
else:
    print(f"  ✓  Brent below alert threshold (${BRENT_ALERT_PRICE})")

# ── Spread commentary ──────────────────────────────────────────
print("\n  SPREAD NOTE:")
if spread < -3:
    print("  Brent trading at a significant premium to WTI.")
    print("  US crude is relatively cheap vs global benchmark.")
elif spread > 1:
    print("  WTI trading at a premium to Brent — unusual.")
else:
    print("  WTI/Brent spread within normal range.")

print()
