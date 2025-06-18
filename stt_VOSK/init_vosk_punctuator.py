from vosk import Model

from configs.settings import BASE_DIR, VOSK_PUNCTUATOR_OPTIONS
from utils_common.exec_time_decorator import execution_time_decorator
from utils_common.normalized_path import get_full_dir_normal_path


class HardSingletonPunctuatorVOSK(Model):
    singleton_instance = None
    instance_initialized = False
    """More complex and complete singleton with inheritance, but very 
    obvious and controlled. New instance cannot be created via
    __init__() method"""

    def __new__(cls, *args, **kwargs):
        if not cls.singleton_instance:
            print("HardSingletonPunctuatorVOSK.__new__()")
            cls.singleton_instance = super().__new__(cls)
        return cls.singleton_instance

    def __init__(self, model_path=None, model_name=None, lang=None):
        if not self.__class__.instance_initialized:
            print("HardSingletonPunctuatorVOSK.__init__()")
            super().__init__(model_path, model_name, lang)
            self.__class__.instance_initialized = True


class SimpleSingletonPunctuatorVOSK:
    singleton_instance = None
    """Easier singleton without inheritance, but not obvious and 
    controlled, new instance can be created via __init__() anyway"""

    def __new__(cls, model_path=None, model_name=None, lang=None):
        print("SimpleSingletonPunctuatorVOSK.__init__()")
        if not cls.singleton_instance:
            cls.singleton_instance = Model(model_path, model_name, lang)
        return cls.singleton_instance


vosk_punctuator_model_instance = None


@execution_time_decorator(in_seconds=True,
                          exec_time_logging=True,
                          new_line_after=True,
                          note="VOSK Punctuator Model initialization time")
def init_vosk_punctuator_model(model_path: str,
                               use_singleton=True,
                               use_hard_singleton=True) -> Model:
    if use_singleton:
        if use_hard_singleton:
            model = HardSingletonPunctuatorVOSK(model_path=model_path)
        else:
            model = SimpleSingletonPunctuatorVOSK(model_path=model_path)
    else:
        model = Model(model_path=model_path)
    return model


if VOSK_PUNCTUATOR_OPTIONS.VOSK_PUNCTUATOR_MODEL_INIT:
    vosk_punctuator_model_path = get_full_dir_normal_path(
        [BASE_DIR, VOSK_PUNCTUATOR_OPTIONS.VOSK_PUNCTUATOR_MODEL_PATH])

    vosk_punctuator_model_instance = init_vosk_punctuator_model(
        model_path=vosk_punctuator_model_path,
        use_singleton=True,
        use_hard_singleton=True)
