from alembic import op
import sqlalchemy as sa

revision = "add_teams_and_categories"
down_revision = "942ef0c78cdc_add_tournament_templates"
branch_labels = None
depends_on = None


def upgrade():

    op.create_table(
        "categories",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(100), nullable=False, unique=True),
    )

    op.create_table(
        "teams",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(150), nullable=False),
        sa.Column(
            "tournament_id",
            sa.Integer(),
            sa.ForeignKey("tournaments.id"),
            nullable=False,
        ),
        sa.Column(
            "category_id",
            sa.Integer(),
            sa.ForeignKey("categories.id"),
            nullable=False,
        ),
        sa.UniqueConstraint(
            "name",
            "tournament_id",
            name="uq_team_name_tournament",
        ),
    )


def downgrade():
    op.drop_table("teams")
    op.drop_table("categories")