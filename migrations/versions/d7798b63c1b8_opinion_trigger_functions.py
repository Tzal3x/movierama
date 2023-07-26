"""Opinion trigger functions

Revision ID: d7798b63c1b8
Revises: 321db695bd7d
Create Date: 2023-07-26 11:01:12.884191

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = 'd7798b63c1b8'
down_revision = '321db695bd7d'
branch_labels = None
depends_on = None

"""
Note: I am implementing trigger functions so that 
I can save network bandwitdth. If this logic of 
incrementing/decrementing happened on the web-server
side I would have to insert/delete an opinion, get 
the current likes/hates of the corresponding movie,
increment/decrement the right field and then run 
an update query on the database. 

Using trigger functions, everything happens on the 
database-server side.
"""
def upgrade() -> None:
    """Trigger function for when new opinions are added"""
    op.execute('''
        -- Create the function that will be used for in the insert trigger 
        CREATE OR REPLACE FUNCTION increment_likes_or_hates()
        RETURNS TRIGGER AS $$
        BEGIN
            IF NEW."opinion" = TRUE THEN
                UPDATE "movies"
                SET "likes" = "likes" + 1
                WHERE "id" = NEW."movie_id";
            ELSIF NEW."opinion" = FALSE THEN
                UPDATE "movies"
                SET "hates" = "hates" + 1
                WHERE "id" = NEW."movie_id";
            END IF;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    '''
    )
    op.execute('''
        -- Create the trigger on opinions for inserts
        CREATE TRIGGER increment_likes_or_hates_insert_trigger
        AFTER INSERT ON "opinions"
        FOR EACH ROW
        EXECUTE FUNCTION increment_likes_or_hates();
    ''')

    """Trigger function when old opinions are removed"""
    op.execute('''
        -- Create the trigger function for DELETE of an opinion
        CREATE OR REPLACE FUNCTION decrement_likes_or_hates()
        RETURNS TRIGGER AS $$
        BEGIN
            IF OLD."opinion" = TRUE THEN
                UPDATE "movies"
                SET "likes" = "likes" - 1
                WHERE "id" = OLD."movie_id";
            ELSIF OLD."opinion" = FALSE THEN
                UPDATE "movies"
                SET "hates" = "hates" - 1
                WHERE "id" = OLD."movie_id";
            END IF;
            RETURN OLD;
        END;
        $$ LANGUAGE plpgsql;
    ''')

    op.execute('''
        -- Create the trigger on opinions for DELETE
        CREATE TRIGGER decrement_likes_or_hates_delete_trigger
        AFTER DELETE ON "opinions"
        FOR EACH ROW
        EXECUTE FUNCTION decrement_likes_or_hates();
    ''')



def downgrade() -> None:
    op.execute('DROP TRIGGER increment_likes_or_hates_insert_trigger ON "opinions"')
    op.execute('DROP FUNCTION increment_likes_or_hates()')
    op.execute('DROP TRIGGER decrement_likes_or_hates_delete_trigger ON "opinions"')
    op.execute('DROP FUNCTION decrement_likes_or_hates()')
