__version__ = "0.0.4"

try:
    from src.api.client import Client
except ModuleNotFoundError:
    pass
except Exception as e:
    import traceback

    traceback.print_exc()
