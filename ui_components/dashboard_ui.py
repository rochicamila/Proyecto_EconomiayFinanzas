from nicegui import ui

class DashboardUI:
    def __init__(self, dm, charts):
        self.dm = dm
        self.charts = charts
        self._build()

    def _build(self):
        with ui.row().classes('w-full gap-4 mb-6'):
            self.income_label = ui.label('$0').classes('text-3xl text-green-400')
            self.expense_label = ui.label('$0').classes('text-3xl text-red-400')
            self.balance_label = ui.label('$0').classes('text-3xl text-blue-400')

        with ui.row().classes('w-full gap-4'):
            self.chart1 = ui.plotly(self.charts.income_vs_expenses())
            self.chart2 = ui.plotly(self.charts.expense_distribution())

        with ui.row().classes('w-full gap-4 mt-4'):
            self.chart3 = ui.plotly(self.charts.investment_performance())
            self.chart4 = ui.plotly(self.charts.debt_status())

    def refresh(self):
        self.chart1.update_figure(self.charts.income_vs_expenses())
        self.chart2.update_figure(self.charts.expense_distribution())
        self.chart3.update_figure(self.charts.investment_performance())
        self.chart4.update_figure(self.charts.debt_status())
        self.update_summary()
        ui.notify('Dashboard actualizado', type='positive')

    def update_summary(self):
        inc = self.dm.get_total_income()
        exp = self.dm.get_total_expenses()
        bal = self.dm.get_balance()
        self.income_label.text = f'${inc:,.0f}'
        self.expense_label.text = f'${exp:,.0f}'
        self.balance_label.text = f'${bal:,.0f}'
