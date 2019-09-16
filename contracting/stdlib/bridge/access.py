from ...execution.runtime import rt
from contextlib import ContextDecorator
from ...db.driver import ContractDriver


class __export(ContextDecorator):
    def __init__(self, contract):
        self.contract = contract

    def __enter__(self):
        driver = rt.env.get('__Driver') or ContractDriver()

        if rt.context._context_changed(self.contract):
            current_state = rt.context._get_state()

            state = {
                'owner': driver.get_owner(self.contract),
                'caller': current_state['this'],
                'signer': current_state['signer'],
                'this': self.contract
            }

            rt.context._add_state(state)

            if state['owner'] is not None and state['owner'] != state['caller']:
                raise Exception('Caller is not the owner!')

    def __exit__(self, *args, **kwargs):
        rt.context._pop_state()


exports = {
    '__export': __export,
    'ctx': rt.context,
    'rt': rt,
}