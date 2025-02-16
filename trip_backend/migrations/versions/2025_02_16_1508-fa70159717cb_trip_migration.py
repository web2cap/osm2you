"""trip  migration

Revision ID: fa70159717cb
Revises: 
Create Date: 2025-02-16 15:08:57.216118

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'fa70159717cb'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('trip_trips',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('marker_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('create_date', sa.Date(), nullable=False),
    sa.Column('start_date', sa.Date(), nullable=False),
    sa.Column('end_date', sa.Date(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['marker_id'], ['public.core_marker.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['public.core_user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_trip_trips_id'), 'trip_trips', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_trip_trips_id'), table_name='trip_trips')
    op.drop_table('trip_trips')
    # ### end Alembic commands ###
