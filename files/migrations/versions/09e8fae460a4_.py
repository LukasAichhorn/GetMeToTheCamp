"""empty message

Revision ID: 09e8fae460a4
Revises: 738df2335ec7
Create Date: 2020-01-05 18:35:14.745591

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '09e8fae460a4'
down_revision = '738df2335ec7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reservation_req', sa.Column('seat_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'reservation_req', 'seat', ['seat_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'reservation_req', type_='foreignkey')
    op.drop_column('reservation_req', 'seat_id')
    # ### end Alembic commands ###
