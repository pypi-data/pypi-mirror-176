import typing as t

from sarus_data_spec.manager.ops.asyncio.base import BaseScalarOp


class PrivacyParams(BaseScalarOp):
    async def value(self) -> t.Any:
        assert self.scalar.is_privacy_params()
        params = self.scalar.protobuf().spec.privacy_params
        if len(params.epsilons) != len(params.deltas):
            raise ValueError("`epsilons` and `deltas` have different lengths.")
        return {
            "epsilons": list(params.epsilons),
            "deltas": list(params.deltas),
        }
