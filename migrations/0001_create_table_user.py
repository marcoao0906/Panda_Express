"""
create table user
date created: 2021-10-28 14:10:32.144958
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
        table.bool('admin')


def downgrade(migrator):
    migrator.drop_table('user')
