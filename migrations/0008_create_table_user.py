"""
create table user
date created: 2021-10-28 14:11:37.847913
"""


def upgrade(migrator):
    with migrator.create_table('user') as table:
        table.int('id')
        table.text('Username')
        table.text('contraseņa')
        table.int('rol')
        table.text('nombre')
        table.text('apellidos')
        table.text('email')
        table.text('direccion')
        table.int('celular')
        table.bool('admin')


def downgrade(migrator):
    migrator.drop_table('user')
