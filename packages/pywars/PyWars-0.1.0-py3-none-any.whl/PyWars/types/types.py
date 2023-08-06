"""
A good way to start is defining data models or records  
related to chat wars kafak topics.
"""

# We import static typing stuff
from typing import Dict, List

# and faust record
from faust import Record

# and this digest object for processing "responses as list" from the api
from .digests import Digest

# ## The records

# ### 🤝 Objects on 'cw*-deals' topic
class Deal(Record, serializer="json"):
    sellerId: str
    sellerCastle: str
    sellerName: str
    buyerId: str
    buyerCastle: str
    buyerName: str
    item: str
    qty: int
    price: int


# ### 💰 Objects on 'cw*-offers' topic
class Offer(Record, serializer="json"):
    sellerId: str
    sellerCastle: str
    sellerName: str
    item: str
    qty: int
    price: int


# ### ⚔ Objects on 'cw*-duels' topic

# The duelist
class Duelist(Record, serializer="json"):
    id: str
    name: str
    tag: str
    castle: str
    level: int
    hp: int


# And the duel
class Duel(Record, serializer="json"):
    winner: Duelist
    loser: Duelist
    isChallenge: bool
    isGuildDuel: bool


# ### 🤑 Objects on 'cw*-sex_digest' topic

# The items inside the  digest list
class Item(Record, serializer="json"):
    name: str
    prices: List[int]


# and the digest
class SexDigest(Digest[Item]):
    pass


# ### 🛍 Objects on 'cw*-yellow_pages' topic

# The item offered inside the shops
class OfferItem(Record, serializer="json"):
    item: str
    price: int
    mana: int


# The specialization record inside 'specializations' if any
class Specialization(Record, serializer="json"):
    level: int
    values: Dict[str, int]


# Now the shop
class Shop(Record, serializer="json"):
    kind: str
    name: str
    ownerCastle: str
    ownerName: str
    ownerTag: str
    mana: int
    link: str

    offers: List[OfferItem]
    especialization: Dict[str, int]
    especializations: Dict[str, Specialization]

    qualityCraftLevel: int
    maintenanceEnable: bool
    maintenanceCost: int
    guildDiscount: int
    castleDiscount: int


# And in the end the yellow_page topic definition
class YellowPage(Digest[Shop]):
    pass


# ### 🛎 Objects on 'cw*-au_digest' topic

# A deal or a auction transaction
class AuctionDeal(Record, serializer="json"):
    lotId: str
    itemName: str
    sellerTag: str
    sellerName: str
    quality: str
    sellerCastle: str
    condition: str
    endAt: str  # TODO: turn this into datetime using dateutils and faust easing
    startedAt: str  # TODO: turn this into datetime using dateutils and faust easing
    buyerCastle: str
    status: str
    finishedAt: str
    buyerTag: str
    buyerName: str
    price: int
    stats: Dict[str, int]


# And the auction digest definition


class AuctionDigest(Digest[AuctionDeal]):
    pass
