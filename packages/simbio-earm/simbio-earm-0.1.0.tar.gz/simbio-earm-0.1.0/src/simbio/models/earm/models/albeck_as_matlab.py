from simbio.components import Override, Parameter, Reaction, Species
from simbio.reactions.compound import ReversibleSynthesis
from simbio.reactions.enzymatic import MichaelisMenten

from .pore_transport import Albeck11ePoreTransport


class AlbeckAsMatlab(Albeck11ePoreTransport):
    KF: Parameter
    KR: Parameter
    KC: Parameter

    class Bid(Albeck11ePoreTransport.Bid):
        pass

    class C8(Albeck11ePoreTransport.C8):
        pass

    Bcl2c: Species = 2e4

    Bcl2c_inhibits_Bid = ReversibleSynthesis(
        A=Bid.T,
        B=Bcl2c,
        AB=0,
        forward_rate=KF,
        reverse_rate=KR,
    )

    C8_activates_Bid: Reaction[Override] = MichaelisMenten(
        E=C8.A,
        S=Bid.U,
        ES=0,
        P=Bid.T,
        forward_rate=1e-7,
        reverse_rate=KR,
        catalytic_rate=KC,
    )
