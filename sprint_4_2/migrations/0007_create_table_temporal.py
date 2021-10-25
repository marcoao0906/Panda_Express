"""
create table temporal
date created: 2021-10-25 01:21:08.630844
"""


def upgrade(migrator):
    with migrator.create_table('temporal') as table:
        table.primary_key('id')
        table.text('nombre')
        table.text('descripcion')
        table.int('precio')
        table.int('cantidad')


def downgrade(migrator):
    migrator.drop_table('temporal')
