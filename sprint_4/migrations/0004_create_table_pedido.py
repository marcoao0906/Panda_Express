"""
create table pedido
date created: 2021-10-20 19:51:09.951446
"""


def upgrade(migrator):
    with migrator.create_table('pedido') as table:
        table.text('id')
        table.foreign_key('TEXT', 'user_id', on_delete=None, on_update=None, references='usuario.Username')
        table.int('fecha')


def downgrade(migrator):
    migrator.drop_table('pedido')
