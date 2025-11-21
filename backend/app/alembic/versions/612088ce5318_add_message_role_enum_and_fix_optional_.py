"""add_message_role_enum_and_fix_optional_fields

Revision ID: 612088ce5318
Revises: 1a31ce608336
Create Date: 2025-11-21 20:46:34.000488

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = '612088ce5318'
down_revision = '1a31ce608336'
branch_labels = None
depends_on = None


def upgrade():
    # Note: MessageRole enum is enforced at the application level (Python)
    # and stored as VARCHAR in SQLite. No database schema changes required.
    # The enum values are: 'user', 'assistant', 'system', 'A', 'B'

    # Optional: Add a CHECK constraint for the role column (SQLite compatible)
    # Uncomment if you want database-level validation:
    # with op.batch_alter_table('message') as batch_op:
    #     batch_op.create_check_constraint(
    #         'message_role_check',
    #         "role IN ('user', 'assistant', 'system', 'A', 'B')"
    #     )
    pass


def downgrade():
    # Remove the CHECK constraint if it was added
    # with op.batch_alter_table('message') as batch_op:
    #     batch_op.drop_constraint('message_role_check', type_='check')
    pass
