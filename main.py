from nicegui import ui
from data_manager import DataManager
from charts import ChartFactory
import theme

dm = DataManager()
charts = ChartFactory(dm)

# =======================
# Funciones auxiliares
# =======================

def refresh_dashboard():
    """Actualiza KPIs y gráficas con datos reales de dm."""
    total_inc = dm.get_total_income()
    total_exp = dm.get_total_expenses()
    total_bal = dm.get_balance()

    income_label.text  = f"${total_inc:,.2f}"
    expense_label.text = f"${total_exp:,.2f}"
    balance_label.text = f"${total_bal:,.2f}"

    chart1.update_figure(charts.income_vs_expenses())
    chart2.update_figure(charts.expense_distribution())
    chart3.update_figure(charts.investment_performance())
    chart4.update_figure(charts.debt_status())


# ---------- PRESUPUESTO ----------

def add_transaction():
    """Agrega una nueva transacción (presupuesto: ingreso/gasto)."""
    if not trans_amount.value or not trans_category.value:
        ui.notify("Completa todos los campos obligatorios", type="warning")
        return

    try:
        amount = float(trans_amount.value)
    except ValueError:
        ui.notify("Monto inválido", type="negative")
        return

    dm.add_transaction(
        trans_type.value,           # 'ingreso' o 'gasto'
        amount,
        trans_category.value,       # categoría elegida
        trans_description.value or ''
    )

    # Limpiar inputs
    trans_amount.value = ''
    trans_description.value = ''

    update_transaction_table()
    refresh_dashboard()
    ui.notify("✅ Transacción agregada", type="positive")


def delete_selected_transaction():
    """Elimina la transacción seleccionada en la tabla de Presupuesto."""
    selected = trans_table.selected
    if not selected:
        ui.notify("Selecciona una transacción", type="warning")
        return

    idx = selected[0]['index']
    dm.delete(dm.transactions, idx)

    update_transaction_table()
    refresh_dashboard()
    ui.notify("🗑️ Transacción eliminada", type="positive")


def update_transaction_table():
    """Refresca la tabla de Presupuesto con las transacciones guardadas."""
    trans_table.rows.clear()
    for i, t in enumerate(dm.transactions):
        trans_table.add_row({
            'index': i,
            'tipo': t['type'],
            'categoria': t['category'],
            'descripcion': t.get('description', ''),
            'monto': f"${t['amount']:,.2f}",
            'fecha': t.get('date', ''),
        })


# =======================
# UI
# =======================

# Inyectar estilos globales (glass, gradiente, tipografía)
theme.inject()

# ---------- HEADER ----------
with ui.header().classes('glass items-center justify-between px-4 py-2'):
    with ui.row().classes('items-center gap-2'):
        ui.icon('show_chart').classes('text-white')
        ui.label('Economía & Finanzas').classes('brand text-xl')




# ---------- TABS PRINCIPALES ----------
with ui.row().classes('px-3 pt-3 w-full'):
    with ui.tabs() as tabs:
        tab_dashboard = ui.tab('Dashboard')
        tab_budget    = ui.tab('Presupuesto')  # <- importante: Presupuesto, no "Transacciones"
        tab_inv       = ui.tab('Inversiones')
        tab_debt      = ui.tab('Deudas')

    with ui.tab_panels(tabs, value=tab_dashboard).classes('w-full'):

        # ===== DASHBOARD =====
        with ui.tab_panel(tab_dashboard).classes('glass p-4'):
            # KPIs
            with ui.row().classes('w-full gap-4 mb-4 kpi'):
                with ui.card().classes('kpi-card'):
                    ui.label('Ingresos Totales').classes('kpi-label')
                    income_label = ui.label('$0').classes('kpi-value')
                with ui.card().classes('kpi-card'):
                    ui.label('Gastos Totales').classes('kpi-label')
                    expense_label = ui.label('$0').classes('kpi-value')
                with ui.card().classes('kpi-card'):
                    ui.label('Balance Total').classes('kpi-label')
                    balance_label = ui.label('$0').classes('kpi-value')

            # Charts
            with ui.row().classes('charts-grid'):
                chart1 = ui.plotly(charts.income_vs_expenses()).classes('chart-box')
                chart2 = ui.plotly(charts.expense_distribution()).classes('chart-box')
                chart3 = ui.plotly(charts.investment_performance()).classes('chart-box')
                chart4 = ui.plotly(charts.debt_status()).classes('chart-box')


        # ===== PRESUPUESTO =====
        with ui.tab_panel(tab_budget).classes('glass p-4'):
            with ui.row().classes('w-full gap-4'):
                # Formulario de nueva transacción (ingreso/gasto)
                with ui.card().classes('w-96 glass p-4'):
                    ui.label('Nueva Transacción de Presupuesto').classes('text-lg text-white/90 mb-2')
                    trans_type = ui.select(['ingreso', 'gasto'], value='gasto').classes('w-full')
                    trans_amount = ui.input('Monto').classes('w-full')
                    trans_category = ui.select(
                        ['comida','servicios','salud','educación','ocio','transporte','otro'],
                        value='comida'
                    ).classes('w-full')
                    trans_description = ui.input('Descripción (opcional)').classes('w-full')

                    ui.button('➕ Agregar', on_click=add_transaction).props('color=positive').classes('w-full mt-3')
                    ui.button('🗑️ Eliminar Seleccionado', on_click=delete_selected_transaction).props('color=negative').classes('w-full mt-2')

                # Tabla de presupuesto
                with ui.card().classes('flex-1'):
                    ui.label('Presupuesto').classes('text-lg text-white/90 mb-2')
                    global trans_table
                    trans_table = ui.table(
                        columns=[
                            {'name': 'index', 'label': '#', 'field': 'index'},
                            {'name': 'tipo', 'label': 'Tipo', 'field': 'tipo'},
                            {'name': 'categoria', 'label': 'Categoría', 'field': 'categoria'},
                            {'name': 'descripcion', 'label': 'Descripción', 'field': 'descripcion'},
                            {'name': 'monto', 'label': 'Monto', 'field': 'monto'},
                            {'name': 'fecha', 'label': 'Fecha', 'field': 'fecha'},
                        ],
                        rows=[],
                        row_key='index',
                        selection='single'
                    ).classes('w-full').props('flat bordered dense')


        # ===== INVERSIONES =====
        with ui.tab_panel(tab_inv).classes('glass p-4'):
            from ui_components.investments_ui import InvestmentsUI
            class _DashProxy:
                def refresh(self):
                    refresh_dashboard()
            InvestmentsUI(dm, _DashProxy())


        # ===== DEUDAS =====
        with ui.tab_panel(tab_debt).classes('glass p-4'):
            from ui_components.debts_ui import DebtsUI
            class _DashProxy:
                def refresh(self):
                    refresh_dashboard()
            DebtsUI(dm, _DashProxy())


# Inicializar datos en pantalla
update_transaction_table()
refresh_dashboard()

ui.run(title='Gestor de Finanzas — v3 FIX', dark=True, port=8080)
