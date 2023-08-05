from sim32.errors.core_errors import UnitError


class AvatarError(UnitError):
    pass


class AnimationError(AvatarError):
    pass


class AnimationAlreadyFinishedError(AnimationError):
    pass
