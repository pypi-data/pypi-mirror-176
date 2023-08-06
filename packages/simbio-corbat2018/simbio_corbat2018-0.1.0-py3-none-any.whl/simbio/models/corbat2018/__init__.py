from simbio.components import Override, Parameter, Species, EmptyGroup
from simbio.reactions.enzymatic import MichaelisMenten
from simbio.models.earm import AlbeckAsMatlab


class Sensor(EmptyGroup):
    dimer: Species
    monomer: Species = 0


class Corbat2018(AlbeckAsMatlab):
    KF: Parameter
    KR: Parameter
    KC: Parameter

    Apop: Species

    class Bid(AlbeckAsMatlab.Bid):
        pass

    class C3(AlbeckAsMatlab.C3):
        pass

    class C8(AlbeckAsMatlab.C8):
        pass

    L: Species[Override] = 0  # Set extrinsic stimuli to 0
    IntrinsicStimuli: Species = 0  # Add intrinsic stimuli

    XIAP: Species[Override] = 1e2
    R: Species[Override] = 1e3

    sCas3 = Sensor(dimer=1e7)
    sCas8 = Sensor(dimer=1e7)
    sCas9 = Sensor(dimer=1e7)

    C3_cleaves_sCas3 = MichaelisMenten(
        E=C3.A,
        S=sCas3.dimer,
        ES=0,
        P=2 * sCas3.monomer,
        forward_rate=KF,
        reverse_rate=1e-2,
        catalytic_rate=KC,
    )
    Apop_cleaves_sCas9 = MichaelisMenten(
        E=Apop,
        S=sCas9.dimer,
        ES=0,
        P=2 * sCas9.monomer,
        forward_rate=5e-9,
        reverse_rate=KR,
        catalytic_rate=KC,
    )
    C8_cleaves_sCas8 = MichaelisMenten(
        E=C8.A,
        S=sCas8.dimer,
        ES=0,
        P=2 * sCas8.monomer,
        forward_rate=1e-7,
        reverse_rate=KR,
        catalytic_rate=KC,
    )
    IntrinsicStimuli_activates_Bid = MichaelisMenten(
        E=IntrinsicStimuli,
        S=Bid.U,
        ES=0,
        P=Bid.T,
        forward_rate=KF,
        reverse_rate=KR,
        catalytic_rate=KC,
    )


class Corbat2018_extrinsic(Corbat2018):
    L: Species[Override] = 1e3


class Corbat2018_intrinsic(Corbat2018):
    IntrinsicStimuli: Species[Override] = 1e2
