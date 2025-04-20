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
    get_user_by_email,
    create_user,
    get_regions,
    get_cities_by_region_name,
    get_bad_habits,
    get_interests,
    get_educ_dir,
    update_user,
    check_password,
    get_recommendations,
    cache_recomendations,
    get_habitation,
    create_habitation,
    update_habitation,
    get_matches,
    get_all_matches,
    store_user_relation,
    get_user_relation
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
    'create_user',
    'get_regions',
    'get_cities_by_region_name',
    'get_bad_habits',
    'get_interests',
    'get_educ_dir',
    'update_user',
    'check_password',
    'get_recommendations',
    'cache_recomendations',
    'get_habitation',
    'create_habitation',
    'update_habitation',
    'get_matches',
    'get_all_matches',
    'store_user_relation',
    'get_user_relation'
]
