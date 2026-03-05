# Proyecto_EconomiayFinanzas
App web de escritorio tipo “dashboard” para gestionar finanzas personales (presupuesto, inversiones y deudas), con gráficos interactivos y persistencia local en JSON.

La app te permite:
1. Registrar ingresos y gastos (presupuesto): cargás transacciones con tipo (ingreso/gasto), monto, categoría, descripción y fecha; podés eliminar una transacción seleccionada. 
2. Ver un dashboard con KPIs: muestra Ingresos Totales, Gastos Totales y Balance (ingresos − gastos). 
3. Visualizar gráficos:
- Barras de Ingresos vs Gastos 
- Dona de Distribución de gastos por categoría (si no hay gastos, muestra “Sin gastos registrados”) 
- Barras de Rendimiento de inversiones en % (si no hay inversiones, muestra “Sin inversiones”) 
- Barras de Deudas pendientes (total − pagado; si no hay deudas, muestra “Sin deudas 🎉”) 
4. Gestionar inversiones: agregás inversiones (tipo, nombre, cantidad, precio compra, precio actual) y la app calcula rendimiento %; podés eliminar inversiones. 
5. Gestionar deudas: agregás deudas (nombre, total, pago mensual, categoría) y ves pendiente; podés eliminar deudas. 
6. Guardar y cargar datos automáticamente desde un archivo local finance_data.json. 

Tecnologías utilizadas:
- Python como lenguaje base (toda la app está en .py).
- NiceGUI para la interfaz (UI web con componentes: tabs, cards, tables, inputs, botones, notificaciones). 
- Plotly para gráficos interactivos embebidos en la UI (ui.plotly(...)). 
- JSON como “base de datos” local (persistencia simple en archivo). 
