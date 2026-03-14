from nicegui import ui

class InvestmentsUI:
    def __init__(self, dm, dashboard):
        self.dm = dm
        self.dashboard = dashboard
        self._build()

    def _build(self):
        with ui.row().classes('w-full gap-4'):
            with ui.card().classes('w-80'):
                ui.label('Nueva Inversión').classes('text-xl text-pink-400 font-bold mb-4')
                self.inv_type = ui.select(['acciones', 'bonos', 'cripto', 'fondos', 'otro'], value='acciones')
                self.inv_name = ui.input('Nombre')
                self.inv_amount = ui.input('Cantidad')
                self.inv_purchase = ui.input('Precio Compra')
                ui.button('➕ Agregar', on_click=self.add).props('color=positive').classes('w-full mt-3')
                ui.button('🗑️ Eliminar Seleccionado', on_click=self.delete).props('color=negative').classes('w-full mt-2')

            with ui.card().classes('flex-1'):
                ui.label('Portafolio de Inversiones').classes('text-xl text-pink-400 font-bold mb-4')
                self.table = ui.table(
                    columns=[
                        {'name': 'tipo', 'label': 'Tipo', 'field': 'tipo'},
                        {'name': 'nombre', 'label': 'Nombre', 'field': 'nombre'},
                        {'name': 'cantidad', 'label': 'Cantidad', 'field': 'cantidad'},
                        {'name': 'p_compra', 'label': 'P. Compra', 'field': 'p_compra'},
                        {'name': 'p_actual', 'label': 'P. Actual', 'field': 'p_actual'},
                        {'name': 'rendimiento', 'label': 'Rendimiento', 'field': 'rendimiento'},
                    ],
                    rows=[], selection='single', row_key='index'
                ).props('dense bordered')
        self.update_table()

    def add(self):
        try:
            amount = float(self.inv_amount.value)
            purchase = float(self.inv_purchase.value)
            current = float(self.inv_current.value) if self.inv_current.value else purchase
            self.dm.add_investment(self.inv_type.value, self.inv_name.value, amount, purchase, current)
            self.update_table()
            self.dashboard.refresh()
            ui.notify('Inversión agregada', type='positive')
        except ValueError:
            ui.notify('Datos inválidos', type='negative')

    def update_table(self):
        self.table.rows.clear()
        for i, inv in enumerate(self.dm.investments):
            perf = ((inv["current_price"] - inv["purchase_price"]) / inv["purchase_price"]) * 100
            self.table.add_row({
                'index': i,
                'tipo': inv['type'],
                'nombre': inv['name'],
                'cantidad': inv['amount'],
                'p_compra': f"${inv['purchase_price']:,.2f}",
                'p_actual': f"${inv['current_price']:,.2f}",
                'rendimiento': f"{perf:+.2f}%",
            })

    def delete(self):
        selected = self.table.selected
        if not selected:
            ui.notify('Selecciona una inversión', type='warning')
            return
        idx = selected[0]['index']
        self.dm.delete(self.dm.investments, idx)
        self.update_table()
        self.dashboard.refresh()
        ui.notify('Inversión eliminada', type='positive')
