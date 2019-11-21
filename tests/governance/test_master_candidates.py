from unittest import TestCase
from contracting.client import ContractingClient
from contracting.stdlib.bridge.time import Timedelta, DAYS, WEEKS, Datetime
from datetime import datetime as dt, timedelta as td


def master_candidates():
    import currency
    import election_house

    candidate_state = Hash()
    candidate_votes = Variable()

    no_confidence_state = Hash()
    no_confidence_votes = Variable()
    to_be_relinquished = Variable()

    STAMP_COST = 20_000
    MASTER_COST = 100_000

    @construct
    def seed():
        candidate_votes.set({})
        to_be_relinquished.set([])
        no_confidence_votes.set({})

    ###
    # STAKING
    ###
    @export
    def register():
        # Make sure someone is already staked
        assert not candidate_state['registered', ctx.signer], 'Already registered.'

        currency.transfer_from(MASTER_COST, ctx.this, ctx.caller)

        candidate_state['registered', ctx.signer] = True

        cv = candidate_votes.get()
        cv[ctx.signer] = 0
        candidate_votes.set(cv)

    @export
    def unregister():
        mns = election_house.get_policy('masternodes')
        assert ctx.caller not in mns, "Can't unstake if in governance."
        currency.transfer(MASTER_COST, ctx.caller)

    ### ### ###

    ###
    # VOTE CANDIDATE
    ###
    @export
    def vote_candidate(address):
        assert candidate_state['registered', address]

        # Determine if caller can vote
        v = candidate_state['last_voted', ctx.signer]
        assert now - v > DAYS * 1 or v is None, 'Voting again too soon.'

        # Deduct small vote fee
        vote_cost = STAMP_COST / election_house.get_policy('stamp_cost')
        currency.transfer_from(vote_cost, ctx.signer, 'blackhole')

        # Update last voted variable
        candidate_state['last_voted', ctx.signer] = now

        # Update vote dict
        cv = candidate_votes.get()
        cv[address] += 1
        candidate_votes.set(cv)

    @export
    def top_masternode():
        cv = candidate_votes.get()

        if len(cv) == 0:
            return None

        top = sorted(cv.items(), key=lambda x: x[1], reverse=True)

        return top[0][0]

    @export
    def pop_top():
        assert ctx.caller == 'masternodes', 'Wrong smart contract caller.'

        top = top_masternode()

        cv = candidate_votes.get()
        del cv[top]
        candidate_votes.set(cv)

    ### ### ###

    ###
    # NO CONFIDENCE VOTES
    ###
    @export
    def vote_no_confidence(address):
        # Determine if caller can vote
        v = no_confidence_state['last_voted', ctx.signer]
        assert now - v > DAYS * 1 or v is None, 'Voting again too soon.'

        # Deduct small vote fee
        vote_cost = STAMP_COST / election_house.get_policy('stamp_cost')
        currency.transfer_from(vote_cost, ctx.signer, 'blackhole')

        # Update last voted variable
        no_confidence_state['last_voted', ctx.signer] = now

        # Update vote dict
        nc = no_confidence_votes.get()

        if nc.get(address) is None:
            nc[address] = 1
        else:
            nc[address] += 1

        no_confidence_votes.set(nc)

    @export
    def last_masternode():
        r = to_be_relinquished.get()
        if len(r) > 0:
            return r[0]

        nc = no_confidence_votes.get()
        last = sorted(nc.items(), key=lambda x: x[1], reverse=True)
        return last[0][0]

    @export
    def pop_last():
        assert ctx.caller == 'masternodes', 'Wrong smart contract caller.'

        r = to_be_relinquished.get()

        if len(r) > 0:
            r.pop(0)
            to_be_relinquished.set(r)

        else:
            last = last_masternode()

            nc = no_confidence_votes.get()
            del nc[last]
            no_confidence_votes.set(nc)

    @export
    def relinquish():
        assert ctx.signer in election_house.get_policy('masternodes')

        r = to_be_relinquished.get()
        r.append(ctx.signer)
        to_be_relinquished.set(r)
    ### ### ###


class TestPendingMasters(TestCase):
    def setUp(self):
        self.client = ContractingClient()

        f = open('./contracts/currency.s.py')
        self.client.submit(f.read(), 'currency')
        f.close()

        f = open('./contracts/election_house.s.py')
        self.client.submit(f.read(), 'election_house')
        f.close()

        f = open('./contracts/stamp_cost.s.py')
        self.client.submit(f.read(), 'stamp_cost', owner='election_house', constructor_args={'initial_rate': 20_000})
        f.close()

        f = open('./contracts/masternodes.s.py')
        self.client.submit(f.read(), 'masternodes', owner='election_house', constructor_args={'initial_masternodes':
                                                                                              ['stu', 'raghu'],
                                                                                              'initial_open_seats': 0})
        f.close()

        self.client.submit(master_candidates)

        self.master_candidates = self.client.get_contract(name='master_candidates')
        self.currency = self.client.get_contract(name='currency')

        self.stamp_cost = self.client.get_contract(name='stamp_cost')
        self.election_house = self.client.get_contract(name='election_house')
        self.election_house.register_policy(policy='stamp_cost', contract='stamp_cost')

    def tearDown(self):
        self.client.flush()

    def test_register(self):
        self.currency.approve(signer='stu', amount=100_000, to='master_candidates')
        self.master_candidates.register(signer='stu')
        q = self.master_candidates.Q.get()

        self.assertEqual(q['stu'], 0)