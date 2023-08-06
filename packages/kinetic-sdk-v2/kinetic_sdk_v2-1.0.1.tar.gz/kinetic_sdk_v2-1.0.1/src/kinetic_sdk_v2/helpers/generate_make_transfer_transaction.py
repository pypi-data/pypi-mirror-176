from solana.publickey import PublicKey

from solders.instruction import AccountMeta, Instruction
from solders.message import Message as SoldersMessage
from solders.pubkey import Pubkey

from spl.token._layouts import INSTRUCTIONS_LAYOUT, InstructionType
from spl.token.instructions import get_associated_token_address

from kinetic_sdk_v2.helpers.sign_and_serialize_transaction import sign_and_serialize_transaction
from kinetic_sdk_v2.helpers.create_kin_memo import create_kin_memo
from kinetic_sdk_v2.models.public_key_string import PublicKeyString
from kinetic_sdk_v2.models.transaction_type import TransactionType

from kinetic_sdk_v2.models.constants import TOKEN_PROGRAM_ID
from typing import List

def create_make_transfer_instruction(
    source: Pubkey,
    source_token_account: Pubkey,
    destination_token_account: Pubkey,
    mint: Pubkey,
    amount: float,
    decimals: int,
):
    account_metas = [
        AccountMeta(source_token_account, False, True),
        AccountMeta(mint, False, False),
        AccountMeta(destination_token_account, False, True),
        AccountMeta(source, True, False),
    ]

    amount = int(amount * 10 ** decimals)
    data = INSTRUCTIONS_LAYOUT.build(
        dict(instruction_type=InstructionType.TRANSFER2, args=dict(amount=amount, decimals=decimals))
    )

    return Instruction(
        program_id=TOKEN_PROGRAM_ID,
        data=data,
        accounts=account_metas
    )


def generate_make_transfer_transaction(
    add_memo: bool,
    app_index: int,
    amount: str,
    destination: PublicKeyString,
    decimals: int,
    mint_fee_payer: str,
    mint_public_key: str,
    recent_blockhash: str,
    source,
    tx_type: TransactionType = TransactionType.NONE
):
    source_token_account = get_associated_token_address(source.public_key, PublicKey(mint_public_key))
    destination_token_account = get_associated_token_address(PublicKey(destination), PublicKey(mint_public_key))

    instructions: List[Instruction] = []

    instruction = create_make_transfer_instruction(
        source=source.public_key.to_solders(),
        source_token_account=source_token_account.to_solders(),
        destination_token_account=destination_token_account.to_solders(),
        mint=PublicKey(mint_public_key).to_solders(),
        amount=float(amount),
        decimals=decimals
    )
    instructions.append(instruction)
    
    if add_memo is True:
        instructions = [create_kin_memo(app_index=app_index, type=tx_type)] + instructions
    message = SoldersMessage(instructions, source.to_solders().pubkey())

    return sign_and_serialize_transaction(message, mint_fee_payer, source, recent_blockhash)
