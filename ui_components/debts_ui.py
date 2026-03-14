from nicegui import ui

class DebtsUI:
    def __init__(self, dm, dashboard):
        self.dm = dm
        self.dashboard = dashboard
        self._build()

    def _build(self):
        with ui.row().classes('w-full gap-4'):
            with ui.card().classes('w-80'):
                ui.label('Nueva Deuda').classes('text-xl text-pink-400 font-bold mb-4')
                self.debt_name = ui.input('Nombre')
                self.debt_total = ui.input('Monto Total')
                self.debt_monthly = ui.input('Pago Mensual')
                self.debt_category = ui.select(['tarjeta', 'préstamo', 'hipoteca', 'otro'], value='tarjeta')
                ui.button('➕ Agregar', on_click=self.add).props('color=warning').classes('w-full mt-3')
                ui.button('🗑️ Eliminar Seleccionado', on_click=self.delete).props('color=negative').classes('w-full mt-2')

            with ui.card().classes('flex-1'):
                ui.label('Gestión de Deudas').classes('text-xl text-pink-400 font-bold mb-4')
                self.table = ui.table(
                    columns=[
                        {'name': 'nombre', 'label': 'Nombre', 'field': 'nombre'},
                        {'name': 'total', 'label': 'Total', 'field': 'total'},
                        {'name': 'pendiente', 'label': 'Pendiente', 'field': 'pendiente'},
                        {'name': 'mensual', 'label': 'Mensual', 'field': 'mensual'},
                        {'name': 'categoria', 'label': 'Categoría', 'field': 'categoria'},
                    ],
                    rows=[], selection='single', row_key='index'
                ).props('dense bordered')
        self.update_table()

    def add(self):
        try:
            total = float(self.debt_total.value)
            monthly = float(self.debt_monthly.value)
            self.dm.add_debt(self.debt_name.value, total, monthly, self.debt_category.value)
            self.update_table()
            self.dashboard.refresh()
            ui.notify('Deuda agregada', type='positive')
        except ValueError:
            ui.notify('Datos inválidos', type='negative')

    def update_table(self):
        self.table.rows.clear()
        for i, d in enumerate(self.dm.debts):
            paid = d.get("paid_amount", 0)
            pending = d["total_amount"] - paid
            self.table.add_row({
                'index': i,
                'nombre': d['name'],
                'total': f"${d['total_amount']:,.2f}",
                'pendiente': f"${pending:,.2f}",
                'mensual': f"${d['monthly_payment']:,.2f}",
                'categoria': d['category'],
            })

    def delete(self):
        selected = self.table.selected
        if not selected:
            ui.notify('Selecciona una deuda', type='warning')
            return
        idx = selected[0]['index']
        self.dm.delete(self.dm.debts, idx)
        self.update_table()
        self.dashboard.refresh()
        ui.notify('Deuda eliminada', type='positive')
