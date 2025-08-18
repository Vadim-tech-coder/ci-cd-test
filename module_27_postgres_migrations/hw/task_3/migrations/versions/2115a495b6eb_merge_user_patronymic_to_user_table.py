"""merge user.patronymic to user table

Revision ID: 2115a495b6eb
Revises: 28df82c9df9e, 6dd44a3a8963
Create Date: 2025-08-18 05:38:58.016200

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2115a495b6eb'
down_revision: Union[str, Sequence[str], None] = ('28df82c9df9e', '6dd44a3a8963')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
