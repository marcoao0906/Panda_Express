"""
create table deseo
date created: 2021-10-31 00:17:37.640149
"""


def upgrade(migrator):
    with migrator.create_table('deseo') as table:
        table.primary_key('id')
        table.foreign_key('INT', 'Usuario_id', on_delete=None, on_update=None, references='user.id')
        table.foreign_key('AUTO', 'plato_id', on_delete=None, on_update=None, references='platos.id')
        table.text('descripcion')


def downgrade(migrator):
    migrator.drop_table('deseo')
