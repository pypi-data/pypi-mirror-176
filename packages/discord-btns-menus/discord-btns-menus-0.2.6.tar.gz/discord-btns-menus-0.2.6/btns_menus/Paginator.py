from btns_menus.builds.abc import run_async
from btns_menus.Buttons import SButton, DEFAULT_TIMEOUT
from btns_menus.DropMenus import SDropMenu
from btns_menus.Combinations import MultiBtnAndMenu

import discord
from discord import ui
from discord import ButtonStyle, SelectOption
from typing import Union, Optional, Dict, List


class PgTypes:
    """
    enums used to define the type of paginator you want to use

    ### Available Types
    - first/ one
    - second/ two
    - third/ three

    ### Example
    ```python
    pg_type = PgTypes.first
    ```
    """

    first = 1
    second = 2
    third = 3

    # Aliases
    one = 1
    two = 2
    three = 3


def SOption(*, name: str, embed: discord.Embed, description: str = None,
            emoji: Union[str, discord.Emoji, discord.PartialEmoji] = None
            ) -> Dict:
    """It's a decorator used to overwrite options in `discord.ui.Select`

    Args:
        name: label for option
        embed: If option is selected, the embed will be sent !
        description: Description for the option
        emoji: Emoji for the option

    Returns:
        decorator: Dictionary of options
    """
    decorator_ = {
        "name": name, "description": description, "embed": embed, "emoji": emoji
    }
    return decorator_


class Paginator:
    def __init__(self,
                 author: discord.Member,
                 embeds: List[discord.Embed],
                 commands_list: List[SOption] = None,
                 pg_type: PgTypes = PgTypes.first,
                 *,
                 buttons: List[SButton] = None,
                 menus: List[SDropMenu] = None,
                 append_before: bool = False,
                 footer: str = None,
                 timeout: Optional[Union[int, float]] = DEFAULT_TIMEOUT
                 ):
        """
        Paginator is used to show users the given embeds in pages format using **navigation Buttons and DropMenus**

        # Custom IDs for Buttons:
            home, forward, backward, skip_Tofirst, skip_Tolast, delete

        # Custom IDs for Menu:
            commands-list, cmds-list

        **Note:** These ID's can be used to modify the buttons/menus in the Paginator

        Args:
            author: User who will interact with the Paginator
            embeds: The list of embeds that acts as Pages
            commands_list: The list of options which are shown as options in a Drop Menu
            pg_type: Takes the PgTypes
            buttons: List of buttons used to navigate of interact with the pages/embeds
            menus: List of Menus used to make a user select options from it
            append_before: If true, buttons & menus will be added before default buttons & menus in Paginator and vice-versa
            footer: Used to add content into text in footer of discord.Embed
            timeout: Timeout of the interaction
        """

        self.author = author
        self.embeds = embeds
        self.cmds_list = commands_list
        self.buttons = [] if buttons is None else buttons
        self.menus = [] if menus is None else menus
        self.timeout = timeout
        self.append_before = append_before
        self.pg_type = pg_type

        self.pages: int = 0

        def footer_for_PG(content: str = None) -> Optional[str]:
            if content is not None:
                conv_content = content.replace("{user}", str(self.author))
                conv_content = conv_content.replace("{username}", self.author.display_name)
                conv_content = conv_content.replace("{pg}", str(self.pages + 1))
                conv_content = conv_content.replace("{total_pgs}", str(len(self.embeds)))
                conv_content = conv_content.replace("{guild}", self.author.guild.name)

                return conv_content
            else:
                return None

        self.footer_for_PG = footer_for_PG
        self.footer = footer

        self.home_btn: Optional[SButton] = None
        self.forward_btn: Optional[SButton] = None
        self.backward_btn: Optional[SButton] = None
        self.delete_menu: Optional[SButton] = None
        self.skip_Tofirst: Optional[SButton] = None
        self.skip_Tolast: Optional[SButton] = None
        self.cmds_menu: Optional[SDropMenu] = None

        run_async(self.create_pages)

    async def create_pages(self):
        buttons_ = []
        for button_ in self.buttons:
            if button_.id is not None:
                if button_.id == "home":
                    self.home_btn = button_
                    buttons_.append(button_)
                if button_.id == "forward":
                    self.forward_btn = button_
                    buttons_.append(button_)
                if button_.id == "backward":
                    self.backward_btn = button_
                    buttons_.append(button_)
                if button_.id == "delete":
                    self.delete_menu = button_
                    buttons_.append(button_)
                if button_.id == "skip_Tofirst":
                    self.skip_Tofirst = button_
                    buttons_.append(button_)
                if button_.id == "skip_Tolast":
                    self.skip_Tolast = button_
                    buttons_.append(button_)

        for btn in buttons_:
            self.buttons.remove(btn)

        for menu_ in self.menus:
            if menu_.id is not None:
                if menu_.id in ["commands-list", "cmds-list"]:
                    self.cmds_menu = menu_
                    self.menus.remove(menu_)

        self.home_btn = SButton(label="Home", emoji="🏠", response=self.embeds[0], style=ButtonStyle.green,
                                custom_id="home", rewrite=True,
                                disabled=True) if self.home_btn is None else self.home_btn
        self.forward_btn = SButton(emoji="➡", custom_id="forward",
                                   rewrite=True, ) if self.forward_btn is None else self.forward_btn
        self.backward_btn = SButton(emoji="⬅", custom_id="backward",
                                    rewrite=True) if self.backward_btn is None else self.backward_btn
        self.skip_Tofirst = SButton(emoji="⏪", rewrite=True, custom_id="skip_Tofirst",
                                    hidden=True) if self.skip_Tofirst is None else self.skip_Tofirst
        self.skip_Tolast = SButton(emoji="⏩", rewrite=True, custom_id="skip_Tolast",
                                   hidden=True) if self.skip_Tolast is None else self.skip_Tolast
        self.delete_menu = SButton(label='Delete Menu', emoji="🗑️", style=ButtonStyle.danger, custom_id="delete",
                                   delete_msg=True) if self.delete_menu is None else self.delete_menu
        self.cmds_menu = SDropMenu(placeholder="Select any one Module", custom_id="cmds-list",
                                   rewrite=True) if self.cmds_menu is None else self.cmds_menu

        em = self.embeds[0]
        if self.footer is not None and len(em.footer.text) == 0:
            em.set_footer(text=self.footer_for_PG(self.footer))
        self.home_btn.update(response=em, rewrite=True)

        if self.skip_Tofirst.kwargs['response'] is None:
            self.skip_Tofirst.update(response=self.embeds[0])
        if self.skip_Tolast.kwargs['response'] is None:
            self.skip_Tolast.update(response=self.embeds[-1])

        run_async(self.build_pages)

    async def build_pages(self):
        async def home_page():
            await self.home_btn.interaction.response.defer()

            self.pages = 0
            self.home_btn.update(disabled=True)
            self.forward_btn.update(disabled=False)
            self.backward_btn.update(disabled=False)

            if self.pg_type != 1:
                self.skip_Tofirst.update(disabled=False)
                self.skip_Tolast.update(disabled=False)

        async def forward_pages():
            await self.forward_btn.interaction.response.defer()

            self.pages += 1
            if self.pages >= len(self.embeds) - 1:
                self.pages = len(self.embeds) - 1
                self.forward_btn.update(disabled=True)
                self.skip_Tolast.update(disabled=True)

            self.skip_Tofirst.update(disabled=False)
            self.backward_btn.update(disabled=False)
            self.home_btn.update(disabled=False)

            em = self.embeds[self.pages]
            if self.footer is not None and len(em.footer.text) == 0:
                em.set_footer(text=self.footer_for_PG(self.footer))
            self.forward_btn.update_one(em, "response")

        async def backward_pages():
            await self.backward_btn.interaction.response.defer()

            self.pages -= 1
            if self.pages <= 0:
                self.pages = 0

                self.home_btn.update(disabled=True)
                self.backward_btn.update(disabled=True)
                self.skip_Tofirst.update(disabled=True)
            else:
                self.skip_Tofirst.update(disabled=False)
                self.backward_btn.update(disabled=False)
                self.home_btn.update(disabled=False)

            self.forward_btn.update(disabled=False)
            self.skip_Tolast.update(disabled=False)

            em = self.embeds[self.pages]
            if self.footer is not None and len(em.footer.text) == 0:
                em.set_footer(text=self.footer_for_PG(self.footer))
            self.backward_btn.update_one(em, "response")

        async def skip_to_first_pg():
            await self.skip_Tofirst.interaction.response.defer()

            self.pages = 0
            self.skip_Tofirst.update(disabled=True)
            self.backward_btn.update(disabled=True)

            self.skip_Tolast.update(disabled=False)
            self.forward_btn.update(disabled=False)
            self.home_btn.update(disabled=True)

        async def skip_to_last_pg():
            await self.skip_Tolast.interaction.response.defer()

            self.pages = len(self.embeds) - 1
            self.skip_Tofirst.update(disabled=False)
            self.backward_btn.update(disabled=False)

            self.skip_Tolast.update(disabled=True)
            self.forward_btn.update(disabled=True)
            self.home_btn.update(disabled=False)

        if self.cmds_list is not None:
            options = []
            for option in self.cmds_list:
                opt_ = SelectOption(
                    label=option['name'], description=option['description'], emoji=option['emoji'])
                options.append(opt_)

            self.cmds_menu.update(options=options)
            for option in self.cmds_list:
                self.cmds_menu.add_query((option['name'], option['embed']))

            if self.cmds_menu.kwargs['func'] is None and self.cmds_menu.kwargs['coro_func'] is None:
                async def reset_view():
                    await self.cmds_menu.interaction.response.defer()

                    self.home_btn.update(disabled=False)
                    self.forward_btn.update(disabled=True)
                    self.backward_btn.update(disabled=True)

                await self.cmds_menu.add_coro_func(reset_view)

        if self.home_btn.kwargs['func'] is None and self.home_btn.kwargs['coro_func'] is None:
            await self.home_btn.add_coro_func(home_page)
        if self.forward_btn.kwargs['func'] is None and self.forward_btn.kwargs['coro_func'] is None:
            await self.forward_btn.add_coro_func(forward_pages)
        if self.backward_btn.kwargs['func'] is None and self.backward_btn.kwargs['coro_func'] is None:
            await self.backward_btn.add_coro_func(backward_pages)
        if self.skip_Tolast.kwargs['func'] is None and self.skip_Tolast.kwargs['coro_func'] is None:
            await self.skip_Tolast.add_coro_func(skip_to_last_pg)
        if self.skip_Tofirst.kwargs['func'] is None and self.skip_Tofirst.kwargs['coro_func'] is None:
            await self.skip_Tofirst.add_coro_func(skip_to_first_pg)

        if self.pg_type == 1:
            created_btns = [self.home_btn, self.backward_btn, self.forward_btn, self.delete_menu]
            if self.append_before:
                self.buttons += created_btns
                if self.cmds_list is not None:
                    self.menus += [self.cmds_menu]
            else:
                self.buttons = created_btns + self.buttons
                if self.cmds_list is not None:
                    self.menus = [self.cmds_menu] + self.menus
        elif self.pg_type == 2:
            self.skip_Tofirst.update(hidden=False)
            self.skip_Tolast.update(hidden=False)
            created_btns = [self.home_btn, self.skip_Tofirst, self.backward_btn,
                            self.forward_btn, self.skip_Tolast, self.delete_menu]
            if self.append_before:
                self.buttons += created_btns
                if self.cmds_list is not None:
                    self.menus += [self.cmds_menu]
            else:
                self.buttons = created_btns + self.buttons
                if self.cmds_list is not None:
                    self.menus = [self.cmds_menu] + self.menus

    def view(self) -> ui.View:
        """
        Returns:
            view: discord.ui.View"""

        view_ = MultiBtnAndMenu(self.author, self.buttons, self.menus, timeout=self.timeout).view()
        return view_
