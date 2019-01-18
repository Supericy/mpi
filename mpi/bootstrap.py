from auction import (
    AuctionService,
    ProcessedAuctions,
    AuctionRepository,
    SubscriptionRepository,
    NotificationService,
    EmailSender,
    Subscription
)

config = {
    'subscription': {
        'storage': {
            'directory': '/var/lib/ckosie/mpi/subscriptions'
        }
    }
}

auctions = AuctionService(
    ProcessedAuctions(),
    AuctionRepository(),
    SubscriptionRepository(config['subscription']['storage']['directory']),
    NotificationService(EmailSender())
)