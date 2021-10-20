"""
create table usuario
date created: 2021-10-20 19:51:09.945461
"""


def upgrade(migrator):
    with migrator.create_table('usuario') as table:
        table.text('Username')
        table.text('contraseña')
        table.int('rol')
        table.text('nombre')
        table.text('apellidos')
        table.text('email')
        table.text('direccion')
        table.int('celular')


def downgrade(migrator):
    migrator.drop_table('usuario')
