from simbio.components import Override, Parameter, Species
from simbio.reactions.enzymatic import MichaelisMenten

from .albeck import Albeck11b, Albeck11c, Albeck11d, Albeck11e, Albeck11f, Base


class Albeck11bPoreTransport(Albeck11b):
    KF: Parameter
    KR: Parameter
    KC: Parameter

    k_pore: Parameter = 10

    class Bax(Base.Bax):
        pass

    class Smac(Albeck11b.Smac):
        M: Species[Override] = 1e6

    class CytoC(Albeck11b.CytoC):
        M: Species[Override] = 1e6

    Bax_activates_Smac = MichaelisMenten(
        E=Bax.A,
        S=Smac.M,
        ES=0,
        P=Smac.C,
        forward_rate=KF,
        reverse_rate=KR,
        catalytic_rate=k_pore,
    )
    Bax_activates_CytoC = MichaelisMenten(
        E=Bax.A,
        S=CytoC.M,
        ES=0,
        P=CytoC.C,
        forward_rate=KF,
        reverse_rate=KR,
        catalytic_rate=k_pore,
    )


class Albeck11cPoreTransport(Albeck11c):
    KF: Parameter
    KR: Parameter
    KC: Parameter

    k_pore: Parameter = 10

    class Bax(Albeck11c.Bax):
        pass

    class Smac(Albeck11c.Smac):
        M: Species[Override] = 1e6
        KF: Parameter = 2 * 1e-6

    class CytoC(Albeck11c.CytoC):
        M: Species[Override] = 1e6

    Bax4_activates_Smac = MichaelisMenten(
        E=Bax.A4,
        S=Smac.M,
        ES=0,
        P=Smac.C,
        forward_rate=Smac.KF,
        reverse_rate=KR,
        catalytic_rate=k_pore,
    )

    Bax4_activates_CytoC = MichaelisMenten(
        E=Bax.A4,
        S=CytoC.M,
        ES=0,
        P=CytoC.C,
        forward_rate=KF,
        reverse_rate=KR,
        catalytic_rate=k_pore,
    )


class Albeck11dPoreTransport(Albeck11d):
    KF: Parameter
    KR: Parameter
    KC: Parameter

    k_pore: Parameter = 10

    class Bax(Albeck11d.Bax):
        pass

    class Smac(Albeck11d.Smac):
        M: Species[Override] = 1e6
        KF: Parameter = 2 * 1e-6 / 0.07

    class CytoC(Albeck11d.CytoC):
        M: Species[Override] = 1e6

    BaxM_activates_Smac = MichaelisMenten(
        E=Bax.M4,
        S=Smac.M,
        ES=0,
        P=Smac.C,
        forward_rate=Smac.KF,
        reverse_rate=KR,
        catalytic_rate=k_pore,
    )
    BaxM_activates_CytoC = MichaelisMenten(
        E=Bax.M4,
        S=CytoC.M,
        ES=0,
        P=CytoC.C,
        forward_rate=KF,
        reverse_rate=KR,
        catalytic_rate=k_pore,
    )


class Albeck11ePoreTransport(Albeck11e):
    KF: Parameter
    KR: Parameter
    KC: Parameter

    k_pore: Parameter = 10

    class Mito(Albeck11e.Mito):
        pass

    class Smac(Albeck11e.Smac):
        M: Species[Override] = 1e6
        KF: Parameter = 2 * 1e-6 / 0.07

    class CytoC(Albeck11e.CytoC):
        M: Species[Override] = 1e6
        KF: Parameter = 2 * 1e-6 / 0.07

    Mito_activates_Smac = MichaelisMenten(
        E=Mito.A,
        S=Smac.M,
        ES=0,
        P=Smac.C,
        forward_rate=Smac.KF,
        reverse_rate=KR,
        catalytic_rate=k_pore,
    )
    Mito_activates_CytoC = MichaelisMenten(
        E=Mito.A,
        S=CytoC.M,
        ES=0,
        P=CytoC.C,
        forward_rate=CytoC.KF,
        reverse_rate=KR,
        catalytic_rate=k_pore,
    )


class Albeck11fPoreTransport(Albeck11f):
    KF: Parameter
    KR: Parameter
    KC: Parameter

    k_pore: Parameter = 10

    class Mito(Albeck11f.Mito):
        pass

    class Smac(Albeck11f.Smac):
        M: Species[Override] = 1e6
        KF: Parameter = 2 * 1e-6 / 0.07

    class CytoC(Albeck11f.CytoC):
        M: Species[Override] = 1e6
        KF: Parameter = 2 * 1e-6 / 0.07

    Mito_activates_Smac = MichaelisMenten(
        E=Mito.A,
        S=Smac.M,
        ES=0,
        P=Smac.C,
        forward_rate=Smac.KF,
        reverse_rate=KR,
        catalytic_rate=k_pore,
    )
    Mito_activates_CytoC = MichaelisMenten(
        E=Mito.A,
        S=CytoC.M,
        ES=0,
        P=CytoC.C,
        forward_rate=CytoC.KF,
        reverse_rate=KR,
        catalytic_rate=k_pore,
    )
