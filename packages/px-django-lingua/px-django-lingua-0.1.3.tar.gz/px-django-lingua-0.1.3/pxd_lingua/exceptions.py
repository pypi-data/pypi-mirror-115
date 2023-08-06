__all__ = (
    'LinguaError',
    'UnsavedLanguageControlAttempt',
)


class LinguaError(Exception):
    pass


class UnsavedLanguageControlAttempt(LinguaError):
    pass
