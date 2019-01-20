from config import config
from auction import (
    AuctionService,
    ProcessedAuctions,
    AuctionRepository,
    SubscriptionRepository,
    NotificationService,
    EmailSender
)

auctions = AuctionService(
    ProcessedAuctions(
        config['auction']['processed']['storage']['directory']
    ),
    AuctionRepository(),
    SubscriptionRepository(
        config['subscription']['storage']['directory']
    ),
    NotificationService(EmailSender(
        config['notification']['email']['account']['username'],
        config['notification']['email']['account']['password'],
        config['notification']['email']['smtp']
    ))
)