from app import create_app, db
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from app.models import Users, Pitches, Categories, Comments, Reactions

app = create_app('production')
manager = Manager(app)
manager.add_command('server', Server)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.shell
def make_shell_context():
    return dict(app=app, db=db, users=Users, pitches=Pitches, categories=Categories, comments=Comments,
                reactions=Reactions)


@manager.command
def deploy():
    """Run deployment tasks."""
    from flask_migrate import upgrade
    from app.models import Users, Pitches, Categories, Comments, Reactions
    # migrate database to latest revision
    upgrade()
    Users.insert_roles()
    Pitches.add_self_follows()
    Categories.add_self_follows()
    Comments.add_self_follows()
    Reactions.add_self_follows()


@manager.command
def test():
    import unittest
    tests = unittest.TestLoader().discover('test')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()
