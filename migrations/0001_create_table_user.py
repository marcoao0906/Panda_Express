"""
create table user
date created: 2021-10-31 00:17:37.635162
"""


def upgrade(migrator):
    with migrator.create_table('user') as table:
        table.int('id')
        table.text('Username')
        table.text('contrasena')
        table.int('rol')
        table.text('nombre')
        table.text('apellidos')
        table.text('email')
        table.text('direccion')
        table.int('celular')
        table.bool('admin')


def downgrade(migrator):
    migrator.drop_table('user')
