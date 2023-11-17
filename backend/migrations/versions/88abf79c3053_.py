"""empty message

Revision ID: 88abf79c3053
Revises: 
Create Date: 2023-11-10 19:45:28.435724

"""
from alembic import op
import sqlalchemy as sa


revision = "88abf79c3053"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "topic",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=180), nullable=True),
        sa.Column("status", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_topic_created_at"), "topic", ["created_at"], unique=False)
    op.create_index(op.f("ix_topic_id"), "topic", ["id"], unique=False)
    op.create_index(op.f("ix_topic_is_deleted"), "topic", ["is_deleted"], unique=False)
    op.create_index(op.f("ix_topic_status"), "topic", ["status"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_topic_status"), table_name="topic")
    op.drop_index(op.f("ix_topic_is_deleted"), table_name="topic")
    op.drop_index(op.f("ix_topic_id"), table_name="topic")
    op.drop_index(op.f("ix_topic_created_at"), table_name="topic")
    op.drop_table("topic")
    # ### end Alembic commands ###
