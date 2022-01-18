from flask import Flask, jsonify
from flask_restful import Resource, Api, abort, reqparse
from flask_sqlalchemy import SQLAlchemy

#config
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///films.db'
db = SQLAlchemy(app)
api = Api(app)


#Film class model for db
class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    year = db.Column(db.String(64))
    genre = db.Column(db.String(128))
    duration = db.Column(db.String(64))
    director = db.Column(db.String(128))
    actors = db.Column(db.String(256))
    avg_vote = db.Column(db.String(64))
    critic_vote = db.Column(db.String(64))

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'year': self.year,
            'genre': self.genre,
            'duration': self.duration,
            'director': self.director,
            'actors': self.actors,
            'avg_vote': self.avg_vote,
            'critic_vote': self.critic_vote
        }


#parser info for input parameters
parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('key', type=str, required=True, help='key is a required parameter')
parser.add_argument('title', type=str, required=True, help="title is a required parameter")
parser.add_argument('year', type=str, required=True, help="year is a required parameter")
parser.add_argument('genre', type=str, required=True, help="genre is a required parameter")
parser.add_argument('duration', type=str, required=True, help="duration is a required parameter")
parser.add_argument('director', type=str, required=True, help="director is a required parameter")
parser.add_argument('actors', type=str, required=True, help="actors is a required parameter")
parser.add_argument('avg_vote', type=str, required=True, help="avg_vote is a required parameter")
parser.add_argument('critic_vote', type=str, required=True, help="critic_vote is a required parameter")

#returns all films in db with corresponding director as JSON
class FilmsByDirector(Resource):
    def get(self, director):
        films = Film.query.filter(Film.director.like(director)).all()
        if len(films) == 0:
            return {'error': True,
                    'message': 'Could not find films with director={}'.format(director)}, 404
        else:
            return {'num_films': len(films),
                    'films': [Film.serialize(film) for film in films]}

#adds a film to the db
class AllFilms(Resource):
    def post(self):
        args = parser.parse_args()
        #check if admin key is valid
        if args['key'] != 'admin':
            return {'error': True,
                    'message': 'key is not valid for updating database'}, 404
        
        film = Film(
            title = args['title'],
            year = args['year'],
            genre = args['genre'],
            duration = args['duration'],
            director = args['director'],
            actors = args['actors'],
            avg_vote = args['avg_vote'],
            critic_vote = args['critic_vote']
        )
        db.session.add(film)
        db.session.commit()

        return Film.serialize(film), 201

class FilmsByID(Resource):
    #updates a film with specific id
    def put(self, film_id):
        args = parser.parse_args()
        if args['key'] != 'admin':
            return {'error': True,
                    'message': 'key is not valid for updating database'}, 404

        film = Film.query.filter_by(id=film_id)\
            .first_or_404(description='Film with id={} is not available'.format(film_id))

        film.title = args['title'],
        film.year = args['year'],
        film.genre = args['genre'],
        film.duration = args['duration'],
        film.director = args['director'],
        film.actors = args['actors'],
        film.avg_vote = args['avg_vote'],
        film.critic_vote = args['critic_vote']
        db.session.commit()

        return Film.serialize(film), 201

    #deletes a film with specific id
    def delete(self, film_id):
        args = parser.parse_args()
        if args['key'] != 'admin':
            return {'error': True,
                    'message': 'key is not valid for updating database'}, 404

        film = Film.query.filter_by(id=film_id)\
            .first_or_404(description='Film with id={} is not available'.format(film_id))

        db.session.delete(film)
        db.session.commit()
        return '', 204



api.add_resource(FilmsByDirector, '/by-director/<director>')
api.add_resource(AllFilms, '/films')
api.add_resource(FilmsByID, '/films/<film_id>')


if __name__ == '__main__':
    app.run(debug=True, port=4500)