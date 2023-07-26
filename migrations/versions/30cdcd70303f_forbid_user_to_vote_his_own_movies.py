"""forbid user to vote his own movies

Revision ID: 30cdcd70303f
Revises: d7798b63c1b8
Create Date: 2023-07-26 20:21:34.593346

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '30cdcd70303f'
down_revision = 'd7798b63c1b8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # User should not be able to vote for his own movies.
    # i.e. if there is a new row to be added to the opinions table
    # we have to check if the same pair of user_id and movie_id in 
    # this row exists in the movies table. If it exists, then
    # it means that this user created the movie and therefore
    # the insertion should be aborted.
    op.execute('''
        CREATE OR REPLACE FUNCTION check_movie_user_pair()
        RETURNS TRIGGER AS $$
        BEGIN
            IF EXISTS (
                SELECT 1
                FROM movies
                WHERE id = NEW.movie_id AND user_id = NEW.user_id
            ) THEN
                RAISE EXCEPTION 'A user cant vote his own movies.';
            END IF;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    '''
    )

    op.execute('''
        CREATE TRIGGER before_insert_opinions
        BEFORE INSERT ON opinions
        FOR EACH ROW
        EXECUTE FUNCTION check_movie_user_pair();
    ''')

    # Scanning the movies table everytime there is a vote will be slow
    # so it would be wise to add a multicolumn index
    op.execute("""
        CREATE INDEX movies_userid_movieid_idx ON movies (id, user_id);
    """)

def downgrade() -> None:
    op.execute('DROP TRIGGER before_insert_opinions ON "opinions"')
    op.execute('DROP FUNCTION check_movie_user_pair()')
    op.execute("DROP INDEX movies_userid_movieid_idx;")