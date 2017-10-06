"""empty message

Revision ID: cc5ef7ff8194
Revises: ccf2e14e1f1e
Create Date: 2017-10-06 16:34:30.880545

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cc5ef7ff8194'
down_revision = 'ccf2e14e1f1e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('analytics_bot_guid_fkey', 'analytics', type_='foreignkey')
    op.create_foreign_key(None, 'analytics', 'bots', ['bot_guid'], ['bot_guid'], ondelete='CASCADE')
    op.drop_constraint('bots_user_id_fkey', 'bots', type_='foreignkey')
    op.create_foreign_key(None, 'bots', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('entities_bot_guid_fkey', 'entities', type_='foreignkey')
    op.create_foreign_key(None, 'entities', 'bots', ['bot_guid'], ['bot_guid'], ondelete='CASCADE')
    op.create_foreign_key(None, 'logs', 'bots', ['bot_guid'], ['bot_guid'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'logs', type_='foreignkey')
    op.drop_constraint(None, 'entities', type_='foreignkey')
    op.create_foreign_key('entities_bot_guid_fkey', 'entities', 'bots', ['bot_guid'], ['bot_guid'])
    op.drop_constraint(None, 'bots', type_='foreignkey')
    op.create_foreign_key('bots_user_id_fkey', 'bots', 'users', ['user_id'], ['id'])
    op.drop_constraint(None, 'analytics', type_='foreignkey')
    op.create_foreign_key('analytics_bot_guid_fkey', 'analytics', 'bots', ['bot_guid'], ['bot_guid'])
    # ### end Alembic commands ###
