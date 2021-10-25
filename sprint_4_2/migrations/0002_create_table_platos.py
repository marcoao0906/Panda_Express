"""
create table platos
date created: 2021-10-25 01:21:08.615222
"""


def upgrade(migrator):
    with migrator.create_table('platos') as table:
        table.primary_key('id')
        table.text('nombre')
        table.text('descripcion')
        table.int('precio')


def downgrade(migrator):
    migrator.drop_table('platos')
