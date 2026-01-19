from database.models.accounts import (
    UserModel,
    UserGroupModel,
    UserGroupEnum,
    UserProfileModel,
    GenderEnum,
)
from database.models.movies import (
    MovieModel,
    MoviesGenresModel,
    MoviesLanguagesModel,
    MovieStatusEnum,
    ActorModel,
    ActorsMoviesModel,
    GenreModel,
    LanguageModel,
    CountryModel,
)
from database.models.orders import Order, OrderItem, OrderStatusEnum
from database.models.cart import Cart, CartItem
from database.models.payments import Payment, PaymentItem, PaymentStatusEnum
import os
from database.models.base import Base
from database.session_sqlite import reset_sqlite_database as reset_database
from database.validators import accounts as accounts_validators

environment = os.getenv("ENVIRONMENT", "developing")

if environment == "testing":
    from database.session_sqlite import (
        get_sqlite_db_contextmanager as get_db_contextmanager,
        get_sqlite_db as get_db,
    )
else:
    from database.session_postgresql import (
        get_postgresql_db_contextmanager as get_db_contextmanager,
        get_postgresql_db as get_db,
    )
