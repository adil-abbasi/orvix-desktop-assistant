from app.feature_registry.login import FEATURE as LOGIN
from app.feature_registry.dashboard import FEATURE as DASHBOARD
from app.feature_registry.products import FEATURE as PRODUCTS
from app.feature_registry.cart import FEATURE as CART
from app.feature_registry.checkout import FEATURE as CHECKOUT
from app.feature_registry.contact import FEATURE as CONTACT


FEATURES = [
    LOGIN,
    DASHBOARD,
    PRODUCTS,
    CART,
    CHECKOUT,
    CONTACT
]


def get_all_features():
    return FEATURES