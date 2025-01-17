from pyrogram.types import Dialog, Message as ms
from pyrogram.enums import ChatType
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Button, Label, Input
from textual.containers import (
    HorizontalGroup,
    VerticalScroll,
)
from textual import on
from datetime import datetime
import utils
import tg
import asyncio
import logging

logging.basicConfig(filename="chocolategram.log",
 level=logging.ERROR, format="%(asctime)s - %(levelname)s [%(lineno)d] - %(message)s")
loop = asyncio.get_event_loop()
client = tg.app


def pack_a_message(sender, text, date, reply_to=None, from_user="me", uid=None):
    if reply_to:
        reply_to = f"[ {reply_to}]"
    else:
        reply_to = ""
    txt = f" {sender} {reply_to}\n"
    txt += f"{text}\n"
    txt += "󰥔 " + date
    txt = Label(txt)
    txt.add_class("msg")
    txt.add_class(from_user)
    txt.add_class(f'id_{uid}')
    return txt


d_id = {}


def dialog(dg: Dialog):
    if dg.chat.type == ChatType.BOT:
        before = " "
    elif dg.chat.type == ChatType.CHANNEL:
        before = "󰦔 "
    elif dg.chat.type == ChatType.SUPERGROUP or ChatType.GROUP:
        before = " "
    elif dg.chat.type == ChatType.PRIVATE:
        before = " "
    else:
        before = " "
    f = str(dg.chat.id)
    d_id["i" + f] = dg
    l = Button(
        f"{before} {dg.chat.full_name or dg.chat.title}", id="i" + f, variant="success"
    )
    logging.info(f'Loaded user: {dg.chat.full_name or dg.chat.title} - {dg.chat.id}')
    l.add_class("dialog")
    l.add_class(f"cls_{dg.chat.id}")
    return l


dialogs = []
msg_list = []


class Chats(VerticalScroll):
    def compose(self) -> ComposeResult:
        self.inp = Input(placeholder="Type something...", id="send")
        yield Label(app.focus_name, id='profile')
        for msg in msg_list:
            yield msg
        yield self.inp

    def clear(self):
        self.inp.value = ""


class ChocolateGram(App):
    CSS_PATH = "choco.tcss"
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("ctrl+s", "send_message", "Send Message"),
        ("ctrl+r", "select_reply", "Reply to message"),
    ]

    focus = None # the chat id of the chat that user is on.
    focus_name = ''
    def compose(self) -> ComposeResult:
        self._loop.create_task(main(self))
        self.search = Input(placeholder="Search...", id="search")
        self.dialogs = VerticalScroll(self.search, *dialogs)
        self.dialogs.add_class("cont-di")
        yield Header()
        self.chat = Chats()
        yield HorizontalGroup(self.dialogs, self.chat)
        yield Footer()

    async def open_chat(self, uid):
        msg_list.clear()
        self.focus = int(uid)
        g = await client.get_chat(uid)
        name = f'{g.title or g.full_name}'
        self.focus_name = name 
    
        async for i in client.get_chat_history(int(uid), 50):
            i: ms
            txt = i.text
            if not txt:
                txt = "[MEDIA]"
            txt = utils.farsi_to_fingilish(txt)
            msg_list.append(
                pack_a_message(
                    i.from_user.full_name,
                    txt,
                    i.date.strftime("%H:%M:%S"),
                    getattr(i.reply_to_message, "text", None),
                    "me" if i.from_user.is_self else "sender",
                    i.id,
                )
            )

        msg_list.reverse()
        self.chat.refresh(recompose=True)
        self.chat.scroll_end()

    def on_button_pressed(self, event: Button.Pressed):
        if "dialog" in event.button._classes:
            for c in event.button._classes:
                if c.startswith("cls_"):
                    c = c.replace("cls_", "")
                    asyncio.Task(self.open_chat(c))
                    break

    @on(Input.Changed)
    def search_in_dialogs(self, event: Input.Changed) -> None:
        if event.input.id == "search":
            for dialog in dialogs:
                if (
                    event.input.value.lower()
                    not in (
                        d_id[dialog.id].chat.full_name or d_id[dialog.id].chat.title
                    ).lower()
                ):
                    dialog.add_class("hidden")
                else:
                    try:
                        dialog.remove_class("hidden")
                    except:
                        pass

    def action_send_message(self):
        if not self.chat.inp.value.strip():
            return
        txt = self.chat.inp.value.strip()
        if txt.startswith(".reply "):
            tt = txt.split(" ", 2)
            reply_to_message_id = msg_list[-int(tt[1])]
            for i in reply_to_message_id.classes:
                if i.startswith('id_'):
                    i = i.replace('id_', '')
                    i = int(i)
                    reply_to_message_id = i
            txt = tt[2]

        else:
            reply_to_message_id=None

        self._loop.create_task(
            client.send_message(
                self.focus, txt, reply_to_message_id=reply_to_message_id
            )
        )

        msg_list.append(
            pack_a_message(
                client.me.full_name,
                txt,
                datetime.now().strftime("%H:%M:%S"),
            )
        )
        self.chat.clear()
        self.chat.refresh(recompose=True)
        self.chat.scroll_end()

    def action_select_reply(self):
        pass

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )


@client.on_message()
async def msg_new(cl, msg):
    
    if msg.chat.id == app.focus:
        msg_list.append(
            pack_a_message(
                msg.from_user.full_name,
                msg.text or "[MEDIA]",
                msg.date.strftime("%H:%M:%S"),
                reply_to=getattr(msg.reply_to_message, "text", None),
                cls="sender",
            )
        )
        app.chat.refresh(recompose=True)
        app.chat.scroll_end()


dd = {}


async def main(app):
    global dialogs
    await client.start()
    print("Getting dialogs...")
    app.notify("Loading dialogs...")
    async for i in client.get_dialogs():
        dialogs.append(dialog(i))

    app.refresh(recompose=True)


if __name__ == "__main__":
    app = ChocolateGram()
    app.run()
