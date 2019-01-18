import requests
import re
import uuid
import os
import yaml
import glob
from bs4 import BeautifulSoup


class Filesystem:
    @staticmethod
    def glob(filename):
        return glob.glob(filename)

    @staticmethod
    def read(filename):
        with open(filename, 'r') as f:
            return ''.join(f.readlines())

    @staticmethod
    def write(filename, content):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w') as f:
            f.write(content)

class Vehicle:
    def __init__(self, vehicleId, year, model, url):
        self.vehicleId = vehicleId
        self.year = year
        self.model = model
        self.url = url


class Subscription:
    def __init__(self, email, search, subscriptionId = None):
        self.email = email
        self.search = search
        self.subscriptionId = subscriptionId

    def interested(self, vehicle):
        try:
            year = self.search['year']['minimum'] <= vehicle.year
        except:
            year = True
        try:
            model = self.search['model'] in vehicle.model
        except:
            model = True
        return year and model


class Auction:
    def __init__(self, auctionId, vehicles):
        self.auctionId = auctionId
        self.vehicles = vehicles


class Email:
    def __init__(self, to, subject, body):
        self.to = to
        self.subject = subject
        self.body = body


class VehicleFound(Email):
    def __init__(self, subscription, vehicle):
        super().__init__(
            subscription.email,
            f'We found a vehicle that matched your search criteria!',
            f'We found a {vehicle.year} {vehicle.model} that you may be interested in. Check it out at {vehicle.url}.'
        )


class EmailSender:
    def send(self, email):
        print(email)
        # Not implemented


class NotificationService:
    def __init__(self, emailSender):
        self.emailSender = emailSender

    def notify(self, notification):
        if isinstance(notification, Email):
            self.emailSender.send(notification)


class SubscriptionRepository:
    def __init__(self, storageDir):
        self.storageDir = storageDir

    def exists(self, email, search):
        for subscription in self.all():
            if subscription.email == email and subscription.search == search:
                return True

        return False

    def find(self, subscriptionId):
        serialized = Filesystem.read(self.__storageFile(subscriptionId))
        return self.__deserialize(serialized)

    def all(self):
        return list(map(self.find, self.__subscriptionIds()))

    def save(self, subscription):
        if not subscription.subscriptionId:
            subscription.subscriptionId = str(uuid.uuid4())

        Filesystem.write(
            self.__storageFile(subscription.subscriptionId),
            self.__serialize(subscription)
        )

    def __subscriptionIds(self):
        subscriptionFilenames = Filesystem.glob(
            self.__storageFile('*')
        )

        return list(map(os.path.basename, subscriptionFilenames))

    def __serialize(self, subscription):
        return yaml.dump({
            "subscriptionId": subscription.subscriptionId,
            "email": subscription.email,
            "search": subscription.search
        })

    def __deserialize(self, serialized):
        normalized = yaml.load(serialized)
        return Subscription(
            normalized['email'],
            normalized['search'],
            subscriptionId=normalized['subscriptionId']
        )

    def __storageFile(self, subscriptionId):
        return f'{self.storageDir}/{subscriptionId}'


class AuctionRepository:
    FORMAT_URL_AUCTIONS     = 'https://apps.mpi.mb.ca/salvage/salvage_data.asp'
    FORMAT_URL_AUCTION      = 'https://apps.mpi.mb.ca/salvage/auction.asp?salenm={}'
    FORMAT_URL_AUCTION_ITEM = 'https://apps.mpi.mb.ca/salvage/SlvgItmImg.asp?salenm={}&itemnm={}'

    def fetchAuctionIds(self):
        auctionIds = []

        page = requests.get(self.FORMAT_URL_AUCTIONS)
        soup = BeautifulSoup(page.content, 'lxml')

        for element in soup.find_all('a', href=True):
            matches = re.match(r'auction\.asp\?salenm=(\d+)', element['href'])
            if matches:
                auctionIds.append(int(matches.group(1)))

        return auctionIds

    def fetchAuction(self, auctionId):
        vehicles = []

        page = requests.get(self.FORMAT_URL_AUCTION.format(auctionId))
        soup = BeautifulSoup(page.content, 'lxml')

        for element in soup.select('#mpi_app_wrapper table tr:not(:first-child)'):
            columns = element.find_all('td')

            try:
                vehicleId = int(columns[0].text)
                year = int(columns[1].text)
                model = columns[2].text
                url = self.FORMAT_URL_AUCTION_ITEM.format(auctionId, vehicleId)

                if vehicleId and year and model:
                    vehicles.append(Vehicle(vehicleId, year, model, url))
            except:
                pass

        return Auction(auctionId, vehicles)


class ProcessedAuctions:
    def contains(self, auctionId):
        return False

    def add(self, auctionId):
        pass


class AuctionService:
    def __init__(self, processedAuctions, auctionRepository, subscriptionRepository, notificationService):
        self.processedAuctions = processedAuctions
        self.auctionRepository = auctionRepository
        self.subscriptionRepository = subscriptionRepository
        self.notificationService = notificationService

    def subscriptions(self):
        return self.subscriptionRepository.all()

    def subscribe(self, subscription):
        if self.subscriptionRepository.exists(subscription.email, subscription.search):
            raise Exception("Subscription already exists.")

        self.subscriptionRepository.save(subscription)

    def processNew(self):
        subscriptions = self.subscriptionRepository.all()
        auctionIds = self.auctionRepository.fetchAuctionIds()

        print(f'Found auction ids: {auctionIds}')

        for auctionId in auctionIds:
            if not self.processedAuctions.contains(auctionId):
                print(f'New auction found: {auctionId}')
                self.process(
                    subscriptions,
                    self.auctionRepository.fetchAuction(auctionId)
                )
                self.processedAuctions.add(auctionId)

    def process(self, subscriptions, auction):
        for vehicle in auction.vehicles:
            matchingSubscriptions = self.findMatchingSubscriptions(
                subscriptions,
                vehicle
            )
            if matchingSubscriptions:
                self.notify(matchingSubscriptions, vehicle)

    def notify(self, subscriptions, vehicle):
        print(f'Notifying {len(subscriptions)} subscriptions of new vehicle ({vehicle.year}, {vehicle.model}) match!')
        for subscription in subscriptions:
            self.notificationService.notify(VehicleFound(
                subscription,
                vehicle
            ))

    def findMatchingSubscriptions(self, subscriptions, vehicle):
        matchingSubscriptions = []

        for subscription in subscriptions:
            if subscription.interested(vehicle):
                matchingSubscriptions.append(subscription)

        return matchingSubscriptions
