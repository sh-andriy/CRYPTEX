"""empty message

Revision ID: 07a6c64e7baa
Revises: e58118a4ca88
Create Date: 2023-03-10 18:56:10.011542

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '07a6c64e7baa'
down_revision = 'e58118a4ca88'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('balance', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date_added', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('balance', schema=None) as batch_op:
        batch_op.drop_column('date_added')

    # ### end Alembic commands ###
