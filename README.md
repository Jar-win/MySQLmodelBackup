

> `c = Model( database='Test', table="test_table")` <br/>
> `c.create_connection()`              <br/>
> `c.update(change_column=['alpha'], change_to=['Gamma'], where_column='id', where_clause='1')` <br/>
> `c.push(table="test_table", alpha='); DROP TABLE test_table; --', beta='1eebbebeb2bebebe4beebebebbeb24')  `<br/>
> `c.search(search_column='alpha, beta', table='test_table', where='id', search_entity='2')`<br/>
> `c.close_connection()`

