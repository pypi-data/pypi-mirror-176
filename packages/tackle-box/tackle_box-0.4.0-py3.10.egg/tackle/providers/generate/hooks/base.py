from pydantic import BaseModel
from tackle import Field


class BaseGenerateHook(BaseModel):
    """Base class for various generate functionalities."""

    extra_context: dict = Field(
        None,
        description="Extra context update the global context to render with."
    )
    render_context: dict = Field(
        None,
        description="A render context that invalidates the default context."
    )
    additional_context: dict = Field(
        None,
        description="A map to use as additional context when rendering."
    )

    def _init_context(self):
        # Update the render_context that will be used
        if self.render_context is not None:
            return

        # fmt: off
        existing_context = self.existing_context if self.existing_context is not None else {}
        temporary_context = self.temporary_context if self.temporary_context is not None else {}
        private_context = self.private_context if self.private_context is not None else {}
        public_context = self.public_context if self.public_context is not None else {}
        # fmt: on

        self.render_context = {
            **existing_context,
            **temporary_context,
            **private_context,
            **public_context,
        }

        if self.extra_context is not None:
            if isinstance(self.extra_context, list):
                for i in self.extra_context:
                    self.render_context.update(i)
            else:
                self.render_context.update(self.extra_context)
