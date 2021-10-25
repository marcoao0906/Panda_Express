"""
create table detallepedido
date created: 2021-10-25 01:21:08.615222
"""


def upgrade(migrator):
    with migrator.create_table('detallepedido') as table:
        table.primary_key('id')
        table.foreign_key('TEXT', 'pedido_id', on_delete=None, on_update=None, references='pedido.id')
        table.foreign_key('AUTO', 'plato_id', on_delete=None, on_update=None, references='platos.id')
        table.int('cantidad')


def downgrade(migrator):
    migrator.drop_table('detallepedido')
