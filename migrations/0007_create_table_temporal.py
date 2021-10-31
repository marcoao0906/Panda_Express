"""
create table temporal
date created: 2021-10-31 00:17:37.644136
"""


def upgrade(migrator):
    with migrator.create_table('temporal') as table:
        table.primary_key('id')
        table.text('nombre')
        table.text('descripcion')
        table.int('precio')
        table.int('cantidad')
        table.text('usuario')


def downgrade(migrator):
    migrator.drop_table('temporal')
