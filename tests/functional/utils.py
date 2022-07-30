def clear_tables(data_base):
    """Очистка всех таблиц без удаления самих таблиц"""
    meta = data_base.metadata
    for table in reversed(meta.sorted_tables):
        data_base.session.execute(table.delete())
    data_base.session.commit()
