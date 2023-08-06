from typing import Any, Iterable, Optional, Union, Generator, Callable
from ..core import AnyCommand, AutoHelpTranslator
from discord.ext.commands.bot import BotBase
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from discord.ext.commands.help import HelpCommand
import discord

__all__ = (
    "AutoHelp",
    "helpful",
    "describe",
    "rename"
)


class AutoParam:
    def __init__(self, name, description, param_type, required, original_name=None):
        self.name = name
        self._type = param_type
        self.original_name = original_name or self.name
        self.description = description
        self.required = required
        self.required_trans = 'required' if self.required else 'not_required'

    @property
    def type(self):
        return self._type

    @classmethod
    def from_slash_param(cls, param: app_commands.Parameter):
        return cls(
            name=param.display_name,
            original_name=param.name,
            description=param.description,
            param_type=param.type,
            required=param.required
        )

    @classmethod
    def from_param(cls, param: commands.Parameter, command: AnyCommand):
        return cls(
            name=getattr(command, "__helping_params_name", {}).get(param.name, None) or param.name,
            original_name=param.name,
            description=getattr(command, "__helping_params_desc", {}).get(param.name, None) or "",
            param_type=param.annotation,
            required=param.required,
        )

    @classmethod
    def from_command(cls, command: commands.Command) -> Generator:
        return (cls.from_param(param, command) for param in command.clean_params.values())

    @classmethod
    def from_slash_command(cls, command: app_commands.Command) -> Generator:
        return (cls.from_slash_param(param) for param in command.parameters)


class AutoHelp(HelpCommand):
    HELP_COMMAND_NAME = 'help'

    def __init__(
            self,
            title: str = None,
            description: str = None,
            param_desc_prefix: str = '=> ',
            message_type: int = 2,
            translator: dict[Any, str] = None,
            show_commands: bool = True,
            show_slash_commands: bool = True,
            register_help_slash: bool = False,
            ephemeral: bool = False,
            private: bool = False,
            autocomplete: bool = True
    ):
        """
        Add an AutoHelp command to automatically add a good looking help command to your bot

        :param str title: The embed / message title
        :param str description: The description of your help menu
        :param int message_type: The type of menu
            Message:           1
            Embed:             2
            Embed (no fields): 3
        :param dict translator: The translator used to translate types to str
        :param bool show_slash_commands: Whether help should display help for non-slash commands
        :param bool show_commands: Whether the command should display help for slash commands (will register /help)
        :param bool ephemeral: Whether the slash should be displayed as
        :param str param_desc_prefix: The prefix of every param description
        :param bool register_help_slash: Whether the /help slash command should be registered
        :param bool autocomplete: Whether the /help command option may be autocompleted
        """
        super().__init__()
        self.bot: Optional[BotBase] = None
        self.title: str = title or "Help Menu:"
        self.description: str = description or ""
        self.param_desc_prefix = param_desc_prefix
        self.message_type = message_type  # 1: message; 2: embed; 3: embed no fields
        self.translator: AutoHelpTranslator = translator or AutoHelpTranslator()
        self.register_help_slash = register_help_slash
        self.show_slash_commands = show_slash_commands
        self.show_commands = show_commands
        self.ephemeral = ephemeral
        self.private = private
        self.autocomplete = autocomplete

    def copy(self):
        obj = self.__class__(*self.__original_args__, **self.__original_kwargs__)
        obj._command_impl = self._command_impl
        obj.bot = self.bot
        return obj

    @property
    def commands(self) -> list[AnyCommand]:
        cmds = []
        for d, t in (
                (self.show_commands, self.bot.tree._global_commands.values()),
                (self.show_slash_commands, self.bot.commands)
        ):
            if d:
                cmds.extend(t)
        return cmds

    def get_commands_by_name(self, command_name: str, command_types: AnyCommand = None, cmds: Iterable[AnyCommand] = None) -> tuple[AnyCommand]:
        if not cmds:
            cmds = self.commands
        if not command_types:
            command_types = AnyCommand.__args__
        return tuple(filter(lambda cmd: cmd.name == command_name and isinstance(cmd, command_types), cmds))

    def _add_to_bot(self, bot: BotBase) -> None:
        async def slash_command_autocomplete(interaction: discord.Interaction, current: str):
            return [
                app_commands.Choice(name=cmd.name, value=cmd.name)
                for cmd in self.commands if current.lower() in cmd.name.lower()
            ]

        @app_commands.command(
            name=self.HELP_COMMAND_NAME,
        )
        @app_commands.describe(cmd='The command you want to get help for!')
        @app_commands.rename(cmd='command')
        @app_commands.autocomplete(**({"cmd": slash_command_autocomplete} if self.autocomplete else {}))
        async def slash_command_callback(inter: discord.Interaction, cmd: Optional[str] = None):
            if cmd:
                bot_cmd = self.get_commands_by_name(cmd, None)

                # command not found
                if not bot_cmd:
                    return await self.command_not_found(
                        inter.response.send_message,
                        f"Unable to resolve command:{cmd}",
                        ephemeral=self.ephemeral
                    )

                await inter.response.send_message(**self.sendable(bot_cmd), ephemeral=self.ephemeral)
                return
            await inter.response.send_message(**self.sendable(), ephemeral=self.ephemeral)

        command = commands.help._HelpCommandImpl(self, **self.command_attrs)
        bot.add_command(command)
        self._command_impl = command
        self.bot = bot

        if self.register_help_slash:
            if self.HELP_COMMAND_NAME in bot.tree._global_commands:
                self.bot.tree.remove_command(self.HELP_COMMAND_NAME)
            self.bot.tree.add_command(slash_command_callback)

    async def send_command_help(self, command: str, /) -> None:
        cmds = self.get_commands_by_name(command, None)
        if not cmds:
            await self.command_not_found(
                self.get_destination(),
                f"Unable to resolve command: `{command}`",
            )
            return

        await self.get_destination().send(**self.sendable(cmds))

    async def command_callback(self, ctx: Context, /, *, command: Optional[str] = None) -> None:
        if command:
            bot_cmd = self.get_commands_by_name(command, None)

            # command not found
            if not bot_cmd:
                await self.command_not_found(
                    ctx.reply,
                    f"Unable to resolve command: `{command}`"
                )
                return

            await ctx.reply(**self.sendable(bot_cmd))
            return
        await ctx.reply(**self.sendable())

    async def command_not_found(self, where: Callable, string: str, **kwargs) -> None:
        await where(self.remove_mentions(string), **kwargs)

    def make_embed(self, help_for: Iterable):
        embed = discord.Embed(
            title=self.title,
            description=self.description,
            color=discord.Color.blurple()
        )
        if self.message_type == 3:
            embed.description = "\n".join([f"{x[0]}\n{x[1]}" for x in help_for])
            return embed

        for field in help_for:
            field_name, field_value = field[0], field[1]
            embed.add_field(
                name=field_name, #(f"{desc}\n{'=' * int(len(desc) * 0.81)}\n" if desc else command.short_doc or '')
                value=field_value,
                inline=False,
            )
        return embed

    def make_message(self, help_for: Iterable):
        return f"**{self.title}**" + "\n" + "\n".join([f"> {x[0]}\n```{x[1]}```" for x in help_for])

    def format_command(self, command: AnyCommand) -> Optional[tuple[str, str]]:
        all_params: Generator[AutoParam]
        is_slash_command = True if isinstance(command, app_commands.Command) else False if isinstance(command, commands.Command) else None

        if is_slash_command is True:
            all_params = AutoParam.from_slash_command(command)
        elif is_slash_command is False:
            all_params = AutoParam.from_command(command)
        else:
            raise ValueError(f"Expected {AnyCommand}, got {type(command)}")
        desc = [
                f"{p.name} {self.translator.get(p.type) or self.translator.get('not_found', 'any')} "
                f"{self.translator.get(p.required_trans)}"
                f"\n{self.param_desc_prefix + p.description if p.description else ''}" for p in all_params
            ]
        return (
            f"{'/' if is_slash_command else self.bot.command_prefix}{command.name}: {', '.join(x.name for x in all_params)}",  # field name
            f"\n".join(desc)
        )

    def format_help(self, cmds: Iterable[AnyCommand]) -> tuple[tuple[str, str], ...]:
        return tuple(filter(None, [self.format_command(cmd) for cmd in cmds]))

    def sendable(
            self,
            cmds: Union[None, Iterable[AnyCommand]] = None
    ) -> dict[str, Union[str, discord.Embed]]:
        return {
            "content": self.make_message(self.format_help(cmds or self.commands))
        } if self.message_type == 1 else {
            "embed": self.make_embed(self.format_help(cmds or self.commands))
        }

    async def send_pages(self):
        destination = self.get_destination()
        await destination.send(**self.sendable())

def helpful(*description: str) -> Any:
    def decorator(command: commands.Command):
        if getattr(command, '__helping_desc', None) is None:
            command.__helping_desc = None
        command.__helping_desc = " ".join(description)
        return command
    return decorator


def rename(**kwargs: str) -> Any:
    def decorator(command: commands.Command):
        if getattr(command, '__helping_params_name', None) is None:
            command.__helping_params_name = {}
        for k, v in kwargs.items():
            command.__helping_params_name[k] = v
        return command
    return decorator


def describe(**kwargs: str) -> Any:
    def decorator(command: commands.Command):
        if getattr(command, '__helping_params_desc', None) is None:
            command.__helping_params_desc = {}
        for k, v in kwargs.items():
            command.__helping_params_desc[k] = v
        return command
    return decorator
