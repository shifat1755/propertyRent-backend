"""fix: property images type text to json

Revision ID: 17e0b1d5d46e
Revises: ff253175511b
Create Date: 2025-10-11 08:09:40.483029

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "17e0b1d5d46e"
down_revision: Union[str, Sequence[str], None] = "ff253175511b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        ALTER TABLE properties
        ALTER COLUMN image_urls
        TYPE JSON
        USING to_json(array[image_urls])
    """)


def downgrade() -> None:
    op.execute("""
        ALTER TABLE properties
        ALTER COLUMN image_urls
        TYPE TEXT
        USING image_urls::text
    """)
