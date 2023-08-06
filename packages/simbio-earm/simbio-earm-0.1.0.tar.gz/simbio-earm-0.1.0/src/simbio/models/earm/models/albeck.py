from simbio.components import (
    EmptyCompartment,
    EmptyGroup,
    Override,
    Parameter,
    Reaction,
    Species,
)
from simbio.reactions.compound import (
    CatalyzeConvert,
    Equilibration,
    ReversibleSynthesis,
)
from simbio.reactions.enzymatic import MichaelisMenten


class Base(EmptyCompartment):
    KF: Parameter = 1e-6
    KR: Parameter = 1e-3
    KC: Parameter = 1

    L: Species = 3000
    R: Species = 200
    DISC: Species = 0
    flip: Species = 100

    class C8(EmptyGroup):
        pro: Species = 2e4
        A: Species = 0

    BAR: Species = 1e3

    class Bid(EmptyGroup):
        U: Species = 0
        T: Species = 0
        M: Species = 0

    class Bax(EmptyGroup):
        C: Species = 1e5
        M: Species = 0
        A: Species = 0

    Bcl2: Species = 2e4

    class CytoC(EmptyGroup):
        C: Species = 0
        M: Species = 0
        A: Species = 0

        transloc_rates: Parameter = 1e-2

        equilibrate_C_and_A = Equilibration(
            A=C,
            B=A,
            forward_rate=transloc_rates,
            reverse_rate=transloc_rates,
        )

    class Smac(EmptyGroup):
        C: Species = 0
        M: Species = 0
        A: Species = 0

        transloc_rates: Parameter = 1e-2

        equilibrate_C_and_A = Equilibration(
            A=C,
            B=A,
            forward_rate=transloc_rates,
            reverse_rate=transloc_rates,
        )

    class Apaf(EmptyGroup):
        I: Species = 1e5  # noqa: #741
        A: Species = 0

    Apop: Species = 0

    class C3(EmptyGroup):
        pro: Species = 1e4
        A: Species = 0
        ub: Species = 0

    class C6(EmptyGroup):
        pro: Species = 1e4
        A: Species = 0

    C9: Species = 1e5

    class PARP(EmptyGroup):
        U: Species = 1e6
        C: Species = 0

    XIAP: Species = 1e5

    # rec_to_bid

    # =====================
    # tBID Activation Rules
    # ---------------------
    #        L + R <--> L:R --> DISC
    #        pC8 + DISC <--> DISC:pC8 --> C8 + DISC
    #        Bid + C8 <--> Bid:C8 --> tBid + C
    convert_L_to_DISC = CatalyzeConvert(
        A=L,
        B=R,
        AB=0,
        P=DISC,
        forward_rate=4e-7,
        reverse_rate=KR,
        conversion_rate=1e-5,
    )
    DISC_activates_C8 = MichaelisMenten(
        E=DISC,
        S=C8.pro,
        ES=0,
        P=C8.A,
        forward_rate=KF,
        reverse_rate=KR,
        catalytic_rate=KC,
    )

    C8_activates_Bid = MichaelisMenten(
        E=C8.A,
        S=Bid.U,
        ES=0,
        P=Bid.T,
        forward_rate=KF,
        reverse_rate=KR,
        catalytic_rate=KC,
    )

    # ---------------------
    # Inhibition Rules
    # ---------------------
    #        flip + DISC <-->  flip:DISC
    #        C8 + BAR <--> BAR:C8
    # ---------------------
    flip_inhibits_DISC = ReversibleSynthesis(
        A=DISC,
        B=flip,
        AB=0,
        forward_rate=KF,
        reverse_rate=KR,
    )
    BAR_inhibits_C8 = ReversibleSynthesis(
        A=BAR,
        B=C8.A,
        AB=0,
        forward_rate=KF,
        reverse_rate=KR,
    )

    # Apoptosome formation
    # --------------------
    #   Apaf + cCytoC <-->  Apaf:cCytoC --> aApaf + cCytoC
    #   aApaf + pC9 <-->  Apop
    #   Apop + pC3 <-->  Apop:pC3 --> Apop + C3

    CytoC_activates_Apaf = MichaelisMenten(
        E=CytoC.A,
        S=Apaf.I,
        ES=0,
        P=Apaf.A,
        forward_rate=5e-7,
        reverse_rate=KR,
        catalytic_rate=KC,
    )
    Apaf_and_C9_to_Apop = ReversibleSynthesis(
        A=Apaf.A,
        B=C9,
        AB=Apop,
        forward_rate=5e-8,
        reverse_rate=KR,
    )
    Apop_activates_C3 = MichaelisMenten(
        E=Apop,
        S=C3.pro,
        ES=0,
        P=C3.A,
        forward_rate=5e-9,
        reverse_rate=KR,
        catalytic_rate=KC,
    )
    # Apoptosome-related inhibitors
    # -----------------------------
    #   Apop + XIAP <-->  Apop:XIAP
    #   cSmac + XIAP <-->  cSmac:XIAP

    XIAP_inhibits_Apop = ReversibleSynthesis(
        A=Apop,
        B=XIAP,
        AB=0,
        forward_rate=2e-6,
        reverse_rate=KR,
    )
    XIAP_inhibits_Smac = ReversibleSynthesis(
        A=Smac.A,
        B=XIAP,
        AB=0,
        forward_rate=7e-6,
        reverse_rate=KR,
    )

    # Caspase reactions
    # -----------------
    # Includes effectors, inhibitors, and feedback initiators:
    #
    #   pC3 + C8 <--> pC3:C8 --> C3 + C8 CSPS
    #   pC6 + C3 <--> pC6:C3 --> C6 + C3 CSPS
    #   XIAP + C3 <--> XIAP:C3 --> XIAP + C3_U CSPS
    #   PARP + C3 <--> PARP:C3 --> CPARP + C3 CSPS
    #   pC8 + C6 <--> pC8:C6 --> C8 + C6 CSPS

    C8_activates_C3 = MichaelisMenten(
        E=C8.A,
        S=C3.pro,
        ES=0,
        P=C3.A,
        forward_rate=1e-7,
        reverse_rate=KR,
        catalytic_rate=KC,
    )
    XIAP_ubiquitinizes_C3 = MichaelisMenten(
        E=XIAP,
        S=C3.A,
        ES=0,
        P=C3.ub,
        forward_rate=2e-6,
        reverse_rate=KR,
        catalytic_rate=1e-1,
    )
    C3_activates_PARP = MichaelisMenten(
        E=C3.A,
        S=PARP.U,
        ES=0,
        P=PARP.C,
        forward_rate=KF,
        reverse_rate=1e-2,
        catalytic_rate=KC,
    )
    C3_activates_C6 = MichaelisMenten(
        E=C3.A,
        S=C6.pro,
        ES=0,
        P=C6.A,
        forward_rate=KF,
        reverse_rate=KR,
        catalytic_rate=KC,
    )
    C6_activates_C8 = MichaelisMenten(
        E=C6.A,
        S=C8.pro,
        ES=0,
        P=C8.A,
        forward_rate=3e-8,
        reverse_rate=KR,
        catalytic_rate=KC,
    )


class Albeck11b(Base):
    KF: Parameter
    KR: Parameter
    KC: Parameter

    Bcl2: Species

    class Bax(Base.Bax):
        pass

    class Bid(Base.Bid):
        U: Species[Override] = 1e5

    Bid_activates_Bax = MichaelisMenten(
        E=Bid.T,
        S=Bax.C,
        ES=0,
        P=Bax.A,
        forward_rate=1e-7,
        reverse_rate=KR,
        catalytic_rate=KC,
    )
    Bcl2_inhibits_Bax = ReversibleSynthesis(
        A=Bax.A,
        B=Bcl2,
        AB=0,
        forward_rate=KF,
        reverse_rate=KR,
    )


class Albeck11c(Base):
    KF: Parameter
    KR: Parameter
    KC: Parameter

    Bcl2: Species

    class Bid(Base.Bid):
        U: Species[Override] = 4e4

    class Bax(Base.Bax):
        A: Species
        A2: Species = 0
        A4: Species = 0

        KF: Parameter = 1e-6
        KR: Parameter = 1e-3

        # Bax dimerizes/tetramerizes
        Bax_dimerization = Equilibration(
            A=2 * A,
            B=A2,
            forward_rate=KF,
            reverse_rate=KR,
        )
        Bax_tetramerization = Equilibration(
            A=2 * A2,
            B=A4,
            forward_rate=KF,
            reverse_rate=KR,
        )

    Bid_activates_Bax = MichaelisMenten(
        E=Bid.T,
        S=Bax.C,
        ES=0,
        P=Bax.A,
        forward_rate=1e-7,
        reverse_rate=KR,
        catalytic_rate=KC,
    )

    # Bcl2 inhibits Bax, Bax2, and Bax4
    Bcl2_inhibits_Bax = ReversibleSynthesis(
        A=Bax.A,
        B=Bcl2,
        AB=0,
        forward_rate=KF,
        reverse_rate=KR,
    )
    Bcl2_inhibits_Bax2 = ReversibleSynthesis(
        A=Bax.A2,
        B=Bcl2,
        AB=0,
        forward_rate=KF,
        reverse_rate=KR,
    )
    Bcl2_inhibits_Bax4 = ReversibleSynthesis(
        A=Bax.A4,
        B=Bcl2,
        AB=0,
        forward_rate=KF,
        reverse_rate=KR,
    )


class Albeck11d(Base):
    KF: Parameter
    KR: Parameter
    KC: Parameter

    Bcl2: Species

    class Bid(Base.Bid):
        U: Species[Override] = 4e4

    class Bax(Base.Bax):
        A: Species
        M: Species

        M2: Species = 0
        M4: Species = 0

        # Normalized by fractional volume of the mitochondrial membrane compartment
        KF: Parameter = 1e-6 / 0.07
        KR: Parameter = 1e-3
        transloc_rates: Parameter = 1e-2

        # Active Bax translocates to the mitochondria
        Bax_translocation_to_mitochondria = Equilibration(
            A=A,
            B=M,
            forward_rate=transloc_rates,
            reverse_rate=transloc_rates,
        )
        # Bax dimerizes/tetramerizes
        BaxM_dimerization = Equilibration(
            A=2 * M,
            B=M2,
            forward_rate=KF,
            reverse_rate=KR,
        )
        BaxM_tetramerization = Equilibration(
            A=2 * M2,
            B=M4,
            forward_rate=KF,
            reverse_rate=KR,
        )

    Bid_activates_Bax = MichaelisMenten(
        E=Bid.T,
        S=Bax.C,
        ES=0,
        P=Bax.A,
        forward_rate=1e-7,
        reverse_rate=KR,
        catalytic_rate=KC,
    )
    # Bcl2 inhibits Bax, Bax2, and Bax4
    Bcl2_inhibits_BaxM = ReversibleSynthesis(
        A=Bax.M,
        B=Bcl2,
        AB=0,
        forward_rate=Bax.KF,
        reverse_rate=KR,
    )
    Bcl2_inhibits_BaxM2 = ReversibleSynthesis(
        A=Bax.M2,
        B=Bcl2,
        AB=0,
        forward_rate=Bax.KF,
        reverse_rate=KR,
    )
    Bcl2_inhibits_BaxM4 = ReversibleSynthesis(
        A=Bax.M4,
        B=Bcl2,
        AB=0,
        forward_rate=Bax.KF,
        reverse_rate=KR,
    )


class Albeck11e(Albeck11d):
    KF: Parameter
    KR: Parameter
    KC: Parameter

    class Bax(Albeck11d.Bax):
        pass

    class Mito(EmptyGroup):
        I: Species = 5e5  # noqa: #741
        A: Species = 0

    Bax_activates_Mito = CatalyzeConvert(
        A=Bax.M4,
        B=Mito.I,
        AB=0,
        P=Mito.A,
        forward_rate=Bax.KF,
        reverse_rate=KR,
        conversion_rate=KC,
    )


class Albeck11f(Albeck11e):
    KF: Parameter
    KR: Parameter
    KC: Parameter

    class Bax(Albeck11e.Bax):
        M: Species
        M2: Species
        M4: Species
        KR: Parameter

        transloc_rates: Parameter[Override] = 1e-4

        KF2: Parameter = (1e-6 / 0.07) / 100  # KF / 100
        KF4: Parameter = (1e-6 / 0.07) / 10  # KF / 10

        BaxM_dimerization: Reaction[Override] = Equilibration(
            A=2 * M,
            B=M2,
            forward_rate=KF2,
            reverse_rate=KR,
        )
        BaxM_tetramerization: Reaction[Override] = Equilibration(
            A=2 * M2,
            B=M4,
            forward_rate=KF4,
            reverse_rate=KR,
        )
