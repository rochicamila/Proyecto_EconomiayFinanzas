def add_transaction():
    """Agrega una nueva transacción al presupuesto"""
    if not trans_amount.value or not trans_category.value:
        ui.notify("Completa todos los campos obligatorios", type="warning")
        return

    try:
        amount = float(trans_amount.value)
        dm.add_transaction(
            trans_type.value,
            amount,
            trans_category.value,
            trans_description.value or ''
        )

        # Limpiar inputs
        trans_amount.value = ''
        trans_category.value = ''
        trans_description.value = ''

        # Actualizar tabla y dashboard
        update_transaction_table()
        refresh_dashboard()
        ui.notify("✅ Transacción agregada", type="positive")

    except ValueError:
        ui.notify("Monto inválido", type="negative")


def delete_selected_transaction():
    """Elimina la transacción seleccionada de la tabla"""
    selected = trans_table.selected
    if not selected:
        ui.notify("Selecciona una transacción para eliminar", type="warning")
        return

    idx = selected[0]['index']
    dm.delete(dm.transactions, idx)
    update_transaction_table()
    refresh_dashboard()
    ui.notify("🗑️ Transacción eliminada", type="positive")


def update_transaction_table():
    """Actualiza la tabla de historial de transacciones"""
    trans_table.rows.clear()
    for i, t in enumerate(reversed(dm.transactions[-50:])):
        trans_table.add_row({
            'index': len(dm.transactions) - 1 - i,
            'tipo': t.get('type', ''),
            'categoria': t.get('category', ''),
            'descripcion': t.get('description', ''),
            'monto': f"${t.get('amount', 0):,.2f}",
            'fecha': t.get('date', ''),
        })


def add_investment():
    """Agrega una nueva inversión"""
    if not inv_name.value or not inv_amount.value or not inv_purchase.value:
        ui.notify("Completa todos los campos obligatorios", type="warning")
        return

    try:
        amount = float(inv_amount.value)
        purchase = float(inv_purchase.value)
        current = float(inv_current.value) if inv_current.value else purchase

        dm.add_investment(inv_type.value, inv_name.value, amount, purchase, current)

        # Limpiar inputs
        inv_name.value = ''
        inv_amount.value = ''
        inv_purchase.value = ''
        inv_current.value = ''

        # Actualizar tabla y dashboard
        update_investment_table()
        refresh_dashboard()
        ui.notify("✅ Inversión agregada correctamente", type="positive")

    except ValueError:
        ui.notify("Datos inválidos", type="negative")


def delete_selected_investment():
    """Elimina la inversión seleccionada"""
    selected = inv_table.selected
    if not selected:
        ui.notify("Selecciona una inversión para eliminar", type="warning")
        return

    idx = selected[0]['index']
    dm.delete(dm.investments, idx)
    update_investment_table()
    refresh_dashboard()
    ui.notify("🗑️ Inversión eliminada", type="positive")


def update_investment_table():
    """Actualiza la tabla de inversiones"""
    inv_table.rows.clear()
    for i, inv in enumerate(dm.investments):
        perf = ((inv["current_price"] - inv["purchase_price"]) / inv["purchase_price"]) * 100
        inv_table.add_row({
            'index': i,
            'tipo': inv['type'],
            'nombre': inv['name'],
            'cantidad': inv['amount'],
            'p_compra': f"${inv['purchase_price']:,.2f}",
            'p_actual': f"${inv['current_price']:,.2f}",
            'rendimiento': f"{perf:+.2f}%",
        })
