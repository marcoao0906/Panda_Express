"""
create table deseo
date created: 2021-10-20 19:51:09.949451
"""


def upgrade(migrator):
    with migrator.create_table('deseo') as table:
        table.primary_key('id')
        table.foreign_key('TEXT', 'Usuario_id', on_delete=None, on_update=None, references='usuario.Username')
        table.foreign_key('AUTO', 'plato_id', on_delete=None, on_update=None, references='platos.id')


def downgrade(migrator):
    migrator.drop_table('deseo')
