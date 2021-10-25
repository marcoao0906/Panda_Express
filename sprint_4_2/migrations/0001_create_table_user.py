"""
create table user
date created: 2021-10-25 01:21:08.615222
"""


def upgrade(migrator):
    with migrator.create_table('user') as table:
        table.int('id')
        table.text('Username')
        table.text('contraseña')
        table.int('rol')
        table.text('nombre')
        table.text('apellidos')
        table.text('email')
        table.text('direccion')
        table.int('celular')


def downgrade(migrator):
    migrator.drop_table('user')
