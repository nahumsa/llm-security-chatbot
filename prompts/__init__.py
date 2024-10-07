from typing import Any

import frontmatter
from jinja2 import Environment, FileSystemLoader, TemplateError, meta
from pydantic import BaseModel


class TemplateInfo(BaseModel):
    name: str
    description: str = "No discription provided"
    version: int
    author: str = "Unknown"
    variables: list[str]
    frontmatter: Any


class PromptManager:
    _env = None

    @classmethod
    def _get_env(cls, template_dir: str = "prompts/templates"):
        if cls._env is None:
            cls._env = Environment(loader=FileSystemLoader(template_dir))

        return cls._env

    @staticmethod
    def get_prompt(template_name: str, **kwargs) -> str:
        env = PromptManager._get_env()
        template_path = f"{template_name}.j2"
        with open(env.loader.get_source(env, template_path)[1]) as file:
            metadata = frontmatter.load(file)

        template = env.from_string(metadata.content)
        template_info = PromptManager.get_template_info(template_name)

        try:
            if set(kwargs.keys()) != set(template_info.variables):
                raise ValueError(
                    f"variables {list(set(template_info.variables) - set(kwargs.keys()))}"
                    + " not set for the prompt template"
                )

            return template.render(**kwargs)

        except TemplateError as e:
            raise ValueError(f"error rendering the template: {e}")

    @staticmethod
    def get_template_info(template_name: str) -> TemplateInfo:
        env = PromptManager._get_env()
        template_path = f"{template_name}.j2"
        with open(env.loader.get_source(env, template_path)[1]) as file:
            metadata = frontmatter.load(file)

        ast = env.parse(metadata.content)
        variables = meta.find_undeclared_variables(ast)

        return TemplateInfo(
            name=template_name,
            variables=list(variables),
            frontmatter=metadata.metadata,
            **metadata.metadata,
        )
