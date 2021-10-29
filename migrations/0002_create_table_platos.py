"""
create table platos
date created: 2021-10-28 14:10:32.144958
"""


def upgrade(migrator):
    with migrator.create_table('platos') as table:
        table.primary_key('id')
        table.text('nombre')
        table.text('descripcion')
        table.int('precio')


def downgrade(migrator):
    migrator.drop_table('platos')
