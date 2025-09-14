

class RepositoryError(Exception):

    pass


class EntityNotFoundError(RepositoryError):
    pass


class EntityAlreadyExistsError(RepositoryError):
    pass