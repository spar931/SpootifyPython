from music.adapters.repository import AbstractRepository


def sort_tracks_by_reviews(repo: AbstractRepository):

    sorted_by_reviews = sorted(repo.get_tracks(), key=lambda x: len(x.track_reviews), reverse=True)
    return sorted_by_reviews
