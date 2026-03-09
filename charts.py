import plotly.graph_objects as go

class ChartFactory:
    COLORS = {
        'primary':'#8B5CF6',
        'success':'#22C55E',
        'danger':'#F43F5E',
        'warning':'#F59E0B',
        'info':'#38BDF8'
    }

    def __init__(self, data_manager):
        self.dm = data_manager

    def _base_layout(self, title):
        return dict(
            title=title,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=24,r=24,t=50,b=24),
            font=dict(color='white'),
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='right',
                x=1,
            ),
        )

    def income_vs_expenses(self):
        inc = self.dm.get_total_income()
        exp = self.dm.get_total_expenses()
        fig = go.Figure(data=[
            go.Bar(
                x=['Ingresos','Gastos'],
                y=[inc, exp],
                marker_color=[self.COLORS['success'], self.COLORS['danger']],
                text=[f'${inc:,.0f}', f'${exp:,.0f}'],
                textposition='outside'
            )
        ])
        fig.update_layout(**self._base_layout('Ingresos vs Gastos'))
        return fig

    def expense_distribution(self):
        categories = {}
        for t in self.dm.transactions:
            if t['type'] == 'gasto':
                categories[t['category']] = categories.get(t['category'], 0) + t['amount']

        labels = list(categories.keys())
        values = list(categories.values())

        if not values:
            fig = go.Figure()
            fig.add_annotation(
                text='Sin gastos registrados',
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(size=16, color='white')
            )
            fig.update_layout(**self._base_layout('Distribución de Gastos'))
            return fig

        fig = go.Figure(data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=.5
            )
        ])
        fig.update_traces(
            textinfo='label+percent',
            hovertemplate='%{label}: %{value:$,.0f}<extra></extra>'
        )
        fig.update_layout(**self._base_layout('Distribución de Gastos'))
        return fig

    def investment_performance(self):
        if not self.dm.investments:
            fig = go.Figure()
            fig.add_annotation(
                text='Sin inversiones',
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(size=16, color='white')
            )
            fig.update_layout(**self._base_layout('Rendimiento de Inversiones'))
            return fig

        names = [i['name'] for i in self.dm.investments]
        perf = [
            ((i['current_price']-i['purchase_price'])/i['purchase_price'])*100
            for i in self.dm.investments
        ]

        fig = go.Figure(data=[
            go.Bar(
                x=names,
                y=perf,
                marker_color=self.COLORS['info']
            )
        ])
        fig.update_layout(**self._base_layout('Rendimiento de Inversiones'))
        fig.update_yaxes(ticksuffix='%')
        return fig

    def debt_status(self):
        if not self.dm.debts:
            fig = go.Figure()
            fig.add_annotation(
                text='Sin deudas 🎉',
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(size=18, color=self.COLORS['success'])
            )
            fig.update_layout(**self._base_layout('Deudas Pendientes'))
            return fig

        names = [d['name'] for d in self.dm.debts]
        pending = [
            d['total_amount'] - d.get('paid_amount', 0)
            for d in self.dm.debts
        ]

        fig = go.Figure(data=[
            go.Bar(
                x=names,
                y=pending,
                marker_color=self.COLORS['warning']
            )
        ])
        fig.update_layout(**self._base_layout('Deudas Pendientes'))
        return fig
