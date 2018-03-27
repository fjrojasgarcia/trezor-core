from apps.common.confirm import *
from trezor import ui
from trezor.messages import ButtonRequestType
from trezor.ui.text import Text
from trezor.utils import chunks, format_amount, split_words
from .helpers import *


async def require_confirm_tx(ctx, recipient, value):
    content = Text('Confirm sending', ui.ICON_SEND,
                   ui.BOLD, format_amount(value, NEM_MAX_DIVISIBILITY) + ' NEM',
                   ui.NORMAL, 'to',
                   ui.MONO, *split_address(recipient),
                   icon_color=ui.GREEN)
    await require_hold_to_confirm(ctx, content, ButtonRequestType.SignTx)  # we use SignTx, not ConfirmOutput, for compatibility with T1


async def require_confirm_fee(ctx, fee):
    content = Text('Confirm fee', ui.ICON_SEND,
                   'Pay ', ui.BOLD, format_amount(fee, NEM_MAX_DIVISIBILITY) + ' NEM',
                   ui.NORMAL, 'for transaction fee?',
                   icon_color=ui.GREEN)
    await require_confirm(ctx, content, ButtonRequestType.ConfirmOutput)


async def require_confirm_action(ctx, payload: bytes, encrypt=False):
    payload = str(payload, 'utf-8')
    if encrypt:
        content = Text('Send encrypted?', ui.ICON_SEND,
                       ui.NORMAL, *split_words(payload, 18))
    else:
        content = Text('Send unencrypted?', ui.ICON_SEND,
                       ui.NORMAL, *split_words(payload, 18),
                       icon_color=ui.RED)
    await require_confirm(ctx, content, ButtonRequestType.ConfirmOutput)


def split_address(data):
    return chunks(data, 17)