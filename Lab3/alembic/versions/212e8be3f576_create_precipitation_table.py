"""create precipitation table

Revision ID: 212e8be3f576
Revises: 
Create Date: 2024-05-19 18:50:12.550637

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from data.dataProcessing import DataImporter
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('alembic.runtime.migration')

# revision identifiers, used by Alembic.
revision: str = '212e8be3f576'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    logger.info("Starting the upgrading process.")
    cols = DataImporter().variant_chosen
    op.create_table(
        'precipitation',
        sa.Column('precipitation_id', sa.Integer, nullable=False),
        sa.Column('pressure_mb', sa.Float),
        sa.Column('pressure_in', sa.Float),
        sa.Column('precip_mm', sa.Float),
        sa.Column('precip_in', sa.Float),
        sa.Column('humidity', sa.Integer),
        sa.Column('cloud', sa.Integer),
        sa.Column('can_go_outside', sa.Boolean),
        sa.PrimaryKeyConstraint('precipitation_id')
    )

    op.execute(f"""
            INSERT INTO precipitation (precipitation_id, {', '.join(cols)}, can_go_outside)
            SELECT id, {', '.join(cols)},
                CASE 
                    WHEN precip_mm < 2.0 AND cloud < 50 THEN true
                    ELSE false
                END
            FROM weather_db
        """)

    for col in cols:
        op.drop_column('weather_db', col)


def downgrade() -> None:
    logger.info("Starting the downgrade process.")
    cols = DataImporter().variant_chosen
    op.add_column('weather_db', sa.Column('pressure_mb', sa.Float))
    op.add_column('weather_db', sa.Column('pressure_in', sa.Float))
    op.add_column('weather_db', sa.Column('precip_mm', sa.Float))
    op.add_column('weather_db', sa.Column('precip_in', sa.Float))
    op.add_column('weather_db', sa.Column('humidity', sa.Integer))
    op.add_column('weather_db', sa.Column('cloud', sa.Integer))

    op.execute(f"""
        UPDATE weather_db
        SET {', '.join([f'{i} = precipitation.{i}' for i in cols])}
        FROM precipitation
        WHERE weather_db.id = precipitation.precipitation_id;
    """)

    op.drop_table('precipitation')
    logger.info("Ended the downgrade process.")
