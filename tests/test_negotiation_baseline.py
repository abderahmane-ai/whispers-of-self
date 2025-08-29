from src.whispers.negotiation import Negotiation, NegotiationConfig
from src.whispers.agents.personality_agents import Altruist, Egoist


def test_negotiation_default_returns_no_agreement():
    neg = Negotiation(NegotiationConfig())
    a, b = Altruist(), Egoist()
    share_a, share_b, success = neg.negotiate(a, b, resource_size=50)
    assert (share_a, share_b, success) == (0, 0, False)


