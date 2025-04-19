from .connections import (
    create_models,
    init_db,
    get_session
)

try:
    from .models import (
        BadHabit,
        District,
        EducationLevel,
        Interest,
        EducationDirection,
        Region,
        EducationalInstitution,
        Locality,
        User,
        Habitation,
        t_user_bad_habits,
        t_user_interest,
        UserPhoto,
        UserResponse,
        UserScore,
        HabitationPhoto,
        Match,
        Message
    )
except (ModuleNotFoundError, ImportError) as e:
    import asyncio
    from pathlib import Path
    asyncio.run(create_models(Path(__file__).parent / "models.py"))
    from .models import (
        BadHabit,
        District,
        EducationLevel,
        Interest,
        EducationDirection,
        Region,
        EducationalInstitution,
        Locality,
        User,
        Habitation,
        t_user_bad_habits,
        t_user_interest,
        UserPhoto,
        UserResponse,
        UserScore,
        HabitationPhoto,
        Match,
        Message
    )

from .queries import (
    get_user_by_email
)

__all__ = [
    # connections
    'create_models',
    'init_db',
    'get_session',
    # models
    'BadHabit',
    'District',
    'EducationLevel',
    'Interest',
    'EducationDirection',
    'Region',
    'EducationalInstitution',
    'Locality',
    'User',
    'Habitation',
    't_user_bad_habits',
    't_user_interest',
    'UserPhoto',
    'UserResponse',
    'UserScore',
    'HabitationPhoto',
    'Match',
    'Message',
    # queries
    'get_user_by_email',
]
