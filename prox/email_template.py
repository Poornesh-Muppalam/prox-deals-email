from typing import Dict, List

PRIMARY = "#0FB872"
DARK = "#0A4D3C"
BG = "#F4FBF8"

def render_html(user_name: str, grouped: Dict[str, List[dict]]) -> str:
    blocks = []
    for retailer, deals in grouped.items():
        rows = []
        for d in deals:
            rows.append(f"""
              <tr>
                <td style="padding:8px 0;border-bottom:1px solid #e6f2ec;">
                  <div style="font-weight:600;color:{DARK};">{d['product_name']}</div>
                  <div style="color:#335b52;font-size:12px;">{d['size']} • {d['start_date']} to {d['end_date']}</div>
                </td>
                <td style="padding:8px 0;border-bottom:1px solid #e6f2ec;text-align:right;font-weight:700;color:{DARK};">
                  ${float(d['price']):.2f}
                </td>
              </tr>
            """)
        blocks.append(f"""
          <div style="margin-top:18px;">
            <div style="font-size:14px;font-weight:800;color:{DARK};margin-bottom:6px;">{retailer}</div>
            <table width="100%" cellspacing="0" cellpadding="0" style="border-collapse:collapse;">
              {''.join(rows)}
            </table>
          </div>
        """)

    return f"""
    <div style="font-family:Arial,Helvetica,sans-serif;background:{BG};padding:24px;">
      <div style="max-width:680px;margin:0 auto;background:#ffffff;border-radius:14px;overflow:hidden;border:1px solid #dff1e8;">
        <div style="background:{PRIMARY};padding:18px 20px;">
          <div style="font-size:18px;font-weight:800;color:#ffffff;">Prox Weekly Deals</div>
          <div style="font-size:12px;color:#eafff6;margin-top:4px;">Top picks from your preferred stores</div>
        </div>

        <div style="padding:18px 20px;color:{DARK};">
          <div style="font-size:14px;">Hi {user_name or "there"},</div>
          <div style="margin-top:8px;font-size:13px;color:#335b52;">
            Here are your top deals this week (sorted by lowest price).
          </div>
          {''.join(blocks)}

          <div style="margin-top:22px;padding-top:14px;border-top:1px solid #e6f2ec;font-size:12px;color:#335b52;">
            Manage preferences (stub): <span style="color:{PRIMARY};text-decoration:underline;">https://prox.example/preferences</span>
          </div>
          <div style="margin-top:6px;font-size:11px;color:#6b8a82;">
            You’re receiving this because you’re enrolled in weekly deal updates.
          </div>
        </div>
      </div>
    </div>
    """.strip()

def render_text(user_name: str, grouped: Dict[str, List[dict]]) -> str:
    lines = [f"Prox Weekly Deals", f"Hi {user_name or 'there'},", ""]
    for retailer, deals in grouped.items():
        lines.append(f"{retailer}")
        for d in deals:
            lines.append(f" - {d['product_name']} ({d['size']}): ${float(d['price']):.2f} [{d['start_date']} to {d['end_date']}]")
        lines.append("")
    lines.append("Manage preferences (stub): https://prox.example/preferences")
    return "\n".join(lines)
