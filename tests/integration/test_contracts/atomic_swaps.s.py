import erc20_clone

swaps = Hash()

@seneca_export
def initiate(participant: str, expiration: datetime, hashlock: str, amount: float):

    allowance = erc20_clone.allowance(ctx.caller, ctx.this)

    assert allowance >= amount, \
        "You cannot initiate an atomic swap without allowing '{}' " \
        "at least {} coins. You have only allowed {} coins".format(ctx.this, amount, allowance)

    swaps[participant, hashlock] = [expiration, amount]

    erc20_clone.transfer_from(amount, ctx.this, ctx.caller)

@seneca_export
def redeem(secret: str):

    hashlock = sha256(secret)

    result = swaps[ctx.caller, hashlock]

    assert result is not None, 'Incorrect sender or secret passed.'

    expiration, amount = result

    if expiration >= now:
        erc20_clone.transfer(ctx.signer, amount)
        swaps[ctx.signer, hashlock] = None # change this to respond to the del keyword?

@seneca_export
def refund(participant, secret):

    hashlock = sha256(secret)

    expiration, amount = swaps[participant, hashlock]

    if expiration < now:
        erc20_clone.transfer(ctx.signer, amount)
        swaps[ctx.signer, hashlock] = None
