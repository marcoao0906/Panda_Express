"""
create table comentarios
date created: 2021-10-31 00:17:37.638152
"""


def upgrade(migrator):
    with migrator.create_table('comentarios') as table:
        table.primary_key('id')
        table.foreign_key('INT', 'usuario_id', on_delete=None, on_update=None, references='user.id')
        table.foreign_key('AUTO', 'plato_id', on_delete=None, on_update=None, references='platos.id')
        table.text('comentario')


def downgrade(migrator):
    migrator.drop_table('comentarios')
