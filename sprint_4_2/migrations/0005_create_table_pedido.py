"""
create table pedido
date created: 2021-10-25 01:21:08.615222
"""


def upgrade(migrator):
    with migrator.create_table('pedido') as table:
        table.text('id')
        table.foreign_key('INT', 'user_id', on_delete=None, on_update=None, references='user.id')
        table.date('fecha')


def downgrade(migrator):
    migrator.drop_table('pedido')
