"""empty message

Revision ID: cd6f2ad9daf6
Revises: 
Create Date: 2023-12-30 04:04:06.059881

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cd6f2ad9daf6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('file_properties',
                    sa.Column('id', sa.UUID(), nullable=False),
                    sa.Column('path_in_storage', sa.String(length=500), nullable=False),
                    sa.Column('filename', sa.String(length=255), nullable=False),
                    sa.Column('size', sa.INTEGER(), nullable=False),
                    sa.Column('file_type', sa.String(length=100), nullable=True),
                    sa.Column('short_name', sa.String(length=24), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('short_name'),
                    )


def downgrade() -> None:
    op.drop_table('file_properties')
