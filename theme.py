from nicegui import ui

def inject():
    ui.add_head_html("""
    <link rel='preconnect' href='https://fonts.googleapis.com'>
    <link rel='preconnect' href='https://fonts.gstatic.com' crossorigin>
    <link href='https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap' rel='stylesheet'>
    <style>
      html, body, #app {
        height: 100%;
        font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif;
      }
      body {
        background: linear-gradient(135deg, #0f172a 0%, #111827 50%, #0b1020 100%);
        color: #fff;
      }
      .glass {
        backdrop-filter: blur(12px);
        background: rgba(17,24,39,.55);
        border: 1px solid rgba(255,255,255,.06);
        border-radius: 16px;
        box-shadow: 0 10px 30px rgba(0,0,0,.25);
      }
      .brand {
        font-weight: 800;
        letter-spacing: -0.02em;
        background: linear-gradient(90deg,#c084fc,#60a5fa,#34d399);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
      }
      .kpi {
        display:grid;
        grid-template-columns: repeat(3, minmax(0,1fr));
        gap: 16px;
      }
      .kpi-card {
        padding: 16px;
        border-radius: 16px;
        background: rgba(255,255,255,0.04);
        border:1px solid rgba(255,255,255,0.06);
      }
      .kpi-value {
        font-size: 28px;
        font-weight: 800;
        letter-spacing:-0.02em;
      }
      .kpi-label {
        opacity: .8;
        font-weight: 600;
      }
      .charts-grid {
        display:grid;
        grid-template-columns: repeat(2, minmax(0,1fr));
        gap: 16px;
      }
      .chart-box {
        height: 420px;
      }
    </style>
    """)
