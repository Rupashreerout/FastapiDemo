"""Add leaves table

Revision ID: 002_add_leaves
Revises: 001_initial
Create Date: 2026-03-03 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '002_add_leaves'
down_revision = '001_initial'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create leaves table
    op.create_table(
        'leaves',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('employee_id', sa.Integer(), nullable=False),
        sa.Column('leave_type', sa.String(length=50), nullable=False),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('end_date', sa.Date(), nullable=False),
        sa.Column('days', sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False, server_default='Pending'),
        sa.Column('reason', sa.String(length=500), nullable=True),
        sa.Column('applied_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('reviewed_by', sa.Integer(), nullable=True),
        sa.Column('reviewed_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['employee_id'], ['employees.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['reviewed_by'], ['employees.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_leaves_id'), 'leaves', ['id'], unique=False)
    op.create_index(op.f('ix_leaves_employee_id'), 'leaves', ['employee_id'], unique=False)


def downgrade() -> None:
    # Drop leaves table
    op.drop_index(op.f('ix_leaves_employee_id'), table_name='leaves')
    op.drop_index(op.f('ix_leaves_id'), table_name='leaves')
    op.drop_table('leaves')
