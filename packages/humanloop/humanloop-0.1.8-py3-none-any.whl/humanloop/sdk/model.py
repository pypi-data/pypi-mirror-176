from humanloop.api.models.model import (
    GenerateResponse,
    ModelConfigResponse,
    ModelGenerate,
)
from humanloop.api.models.model_config import ModelConfig
from humanloop.sdk.init import _get_client, _get_settings
from humanloop.sdk.utils import deprecated


def register(*args, **kwargs) -> ModelConfigResponse:
    """Register a new model configuration for a project and optionally tag it with
    an experiment.

    If the project does not exist, a new project with the provided name will be
    automatically created.
    This function accepts a model_config: ModelConfig, or a model_config passed
    in as kwargs.
    """
    if len(args) > 0:
        if len(args) != 1:
            raise ValueError(
                "When passing arguments, only a single argument is accepted. "
                "This should be a single `ModelConfig` object."
            )
        if len(kwargs) != 0:
            raise ValueError(
                "Either pass arguments of type `ModelConfig` or the keyword arguments required, not both. "
            )
        return _register(args[0])
    elif len(kwargs) > 0:
        return _register(ModelConfig(**kwargs))
    else:
        raise ValueError(
            "Provide a ModelConfig or the keyword arguments to create a `ModelConfig` object. "
        )


def _register(model_config: ModelConfig) -> ModelConfigResponse:
    client = _get_client()
    return client.register(model_config)


@deprecated
def generate(*args, **kwargs) -> GenerateResponse:
    """Generate an output from a registered model.

    If an experiment_id is provided it will sample a model_config for a trial.
    If not, a model_config_id, or specific model config parameters, must be provided.
    If the project name is not recognised, like our log endpoint, a new project will
    be created.
    This function accepts a generate_request: ModelGenerateRequest, or a
    generate_request passed in as kwargs.
    """
    if len(args) > 0:
        if len(args) != 1:
            raise ValueError(
                "When passing arguments, only a single argument is accepted. "
                "This should be a single `ModelGenerate` object."
            )
        if len(kwargs) != 0:
            raise ValueError(
                "Either pass arguments of type `ModelGenerate` or the keyword arguments required, not both. "
            )
        return _generate(args[0])
    elif len(kwargs) > 0:
        return _generate(ModelGenerate(**kwargs))
    else:
        raise ValueError(
            "Provide a ModelGenerate or the keyword arguments to create a `ModelGenerate` object. "
        )


def _generate(generate_request: ModelGenerate) -> GenerateResponse:
    settings = _get_settings()
    provider_api_keys = settings.provider_api_keys
    generate_request.provider_api_keys = provider_api_keys
    client = _get_client()
    return client.generate(generate_request)
