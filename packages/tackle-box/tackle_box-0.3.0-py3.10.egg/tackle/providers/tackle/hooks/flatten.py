from tackle import BaseHook, Field
from tackle.utils.imports import get_public_or_private_hook


class FlattenHook(BaseHook):
    """
    Hook for flattening args/kwargs/flags into CLI inputs. Takes a declarative hook
    input and turns it into a string that can be used to call a generic CLI program.
    """

    hook_type: str = 'flatten'
    hook: str = Field(None, description="A hook")

    positional_args: list = Field(
        None, description="A list of args that should be considered positional.")

    args: list = ['hook']

    def exec(self) -> str:
        hook = get_public_or_private_hook(context=self, hook_type=self.hook)

        flat_items = []
        for i in hook.__fields__['function_fields'].default:
            hook_field = hook.__fields__[i]
            hook_value = self.existing_context[i]

            if hook_field.type_ == bool:
                flat_items.append("--" + hook_field.name)
                pass
            elif hook_field.type_ == (str, int, float):
                flat_items.append("--" + hook_field.name)
                flat_items.append(hook_value)
                pass
            else:
                pass
            pass

        return ' '.join(flat_items)
