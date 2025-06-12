from vosk import Model

from configs.settings import API_CONFIGS, BASE_DIR
from utils_common.exec_time_decorator import execution_time_decorator
from utils_common.normalized_path import get_full_dir_normal_path


class HardSingletonVOSK(Model):
    singleton_instance = None
    instance_initialized = False
    """More complex and complete singleton with inheritance, but very 
    obvious and controlled. New instance cannot be created via
    __init__() method"""

    def __new__(cls, *args, **kwargs):
        if not cls.singleton_instance:
            print("HardSingletonVOSK.__new__()")
            cls.singleton_instance = super().__new__(cls)
        return cls.singleton_instance

    def __init__(self, model_path=None, model_name=None, lang=None):
        if not self.__class__.instance_initialized:
            print("HardSingletonVOSK.__init__()")
            super().__init__(model_path, model_name, lang)
            self.__class__.instance_initialized = True


class SimpleSingletonVOSK:
    singleton_instance = None
    """Easier singleton without inheritance, but not obvious and 
    controlled, new instance can be created via __init__() anyway"""

    def __new__(cls, model_path=None, model_name=None, lang=None):
        print("SimpleSingletonVOSK.__init__()")
        if not cls.singleton_instance:
            cls.singleton_instance = Model(model_path, model_name, lang)
        return cls.singleton_instance


vosk_model_instance = None


@execution_time_decorator(in_seconds=True,
                          exec_time_logging=True,
                          new_line_after=True,
                          note="VOSK Model initialization time")
def init_vosk_model(model_path: str,
                    use_singleton=True,
                    use_hard_singleton=True) -> Model:
    if use_singleton:
        if use_hard_singleton:
            model = HardSingletonVOSK(model_path=model_path)
        else:
            model = SimpleSingletonVOSK(model_path=model_path)
    else:
        model = Model(model_path=model_path)
    return model


if API_CONFIGS.INIT_VOSK_MODEL:
    vosk_model_path = get_full_dir_normal_path(
        [BASE_DIR, API_CONFIGS.VOSK_MODEL_PATH])

    vosk_model_instance = init_vosk_model(
        model_path=vosk_model_path,
        use_singleton=True,
        use_hard_singleton=True)
