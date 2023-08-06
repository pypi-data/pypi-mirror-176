__version__ = "0.0.6"

try:
    from explore.api.client import Client
except ModuleNotFoundError:
    pass
except Exception as e:
    import traceback

    traceback.print_exc()
