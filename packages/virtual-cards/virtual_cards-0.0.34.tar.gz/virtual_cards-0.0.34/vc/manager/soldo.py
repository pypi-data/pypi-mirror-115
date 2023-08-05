import logging
from datetime import datetime,timedelta
from logging.handlers import TimedRotatingFileHandler
from decimal import Decimal
from sqlalchemy.orm import Session

from .base import BaseNetworkClient

# from vc.
from vc.client.soldo import user, wallets, card, group, order, transaction
from vc.models.soldo import WalletSo, CardSo, TransactionSo
from vc.settings import Settings
from .soldo_event import EventMixer
from vc.libs.utils import set_config, generate_list_model_search_id
from decimal import Decimal

logger = logging.getLogger(__name__)
set_config(logger)


class SoldoException(Exception):

    def __init__(self, msg: str, response_data: dict = None):
        self.msg = msg
        self.response_data = response_data

    def __str__(self):
        return f"{self.msg}, {str(self.response_data)}"


def card_issue():
    return 7


class Soldo(EventMixer, BaseNetworkClient):
    settings = Settings({
        "ACCESS_TOKEN": "dFTPdcdQqHXI3GSJhPr5b2MAihDXGqWR",
    })
    event_list = ["new_user", "wallet_created", "store_order_completed"]
    __cache = {'0765a95e-6016-43fe-a1b4-4e66713e0a00':
                   {'wallet_id': 1, 'status': 'PLACED',
                    "category": "CARD"}, }
    __card_issue = None # function get card issue

    @property
    def card_price(self):
        return self.__card_issue()

    def get_cache(self):
        return self.__cache

    def get_cache_by_key(self, key):
        return self.__cache.get(key)

    def update_cache(self, **data: dict):
        return self.__cache.update(data)

    def remove_cache(self, key):
        if self.__cache.get(key):
            return self.__cache.pop(key)

    def __init__(self, name, uri,
                 api_url: str,
                 client_id: str,
                 client_secret: str,
                 group_id: str,
                 token: str,
                 safe_wallet: str,
                 safe_user: str,
                 filepath_private_pem: str,
                 card_issue=card_issue, log_file: str = None, currency="USD", user_model=None, **config):
        data = dict(name=name, currency=currency,
                    CLIENT_ID=client_id,
                    CLIENT_SECRET=client_secret,
                    API_URL=api_url,
                    TOKEN=token,
                    SAFE_WALLET=safe_wallet,
                    SAFE_USER=safe_user,
                    USER_MODEL=user_model,
                    UPLOAD_SIZE=1000500,
                    RULES=["OpenClose", "MaxPerTx"],
                    LOG_FILE=log_file,
                    PATH_RSA_PRIVATE=filepath_private_pem,
                    GROUP_ID=group_id, **config)
        Soldo.settings.update_config(**data)

        super().__init__(uri, user_model=user_model, **config)
        self.__card_issue = card_issue
        self.set_safe(safe_wallet, safe_user)

    def set_safe(self, wallet_id: str, user_email: str):

        wallet = wallets.get(wallet_id=wallet_id).data
        with self.get_session() as session:
            user = session.query(self._user).filter(self._user.email == user_email).first()

            wallet_q = session.query(WalletSo).filter(WalletSo.search_id==wallet_id).first()
            update_data = dict(
                user_id=user.id,
                search_id=wallet.id,
                balance=wallet.available_amount,
                blocked_balance=wallet.blocked_amount,
                currency=wallet.currency_code
            )
            if not wallet_q:
                wallet_q = WalletSo()
            for field in update_data:
                setattr(wallet_q, field, update_data[field])
            self.save_obj(session, obj=wallet_q)
        return wallet_q

    def activate_service(self, db: Session, user_id: int, owner_type="company"):
        user = db.query(self._user).filter(self._user.id == user_id).first()
        logger.debug(user.__dict__)
        response_data = wallets.create(owner_type, self.settings.currency, name=user.email, custom_reference_id=user.id)
        order = response_data.data
        if not order.is_valid or order.status != "PLACED":
            raise SoldoException("Error create_wallet", response_data.dict())

        wallet = WalletSo(user_id=user.id, currency=self.settings.currency, )
        if order.items:
            wallet.search_id = order.items[0].id

        self.save_obj(db, wallet)
        return wallet

    def get_transactions_by_wallet_id(self, db: Session, wallet_id, type="wallet", page=0,  **kwargs):
        wallet_q = db.query(WalletSo).filter(WalletSo.id == wallet_id).first()
        response_data = transaction.search(type=type, publicId=wallet_q.search_id, page=page, **kwargs).data
        return response_data

    def get_statements_by_card_id(self, db: Session, card_id, page=0, **kwargs):
        card_q = db.query(CardSo).filter(CardSo.id==card_id).first()
        response_data = transaction.search(type="card", publicId=card_q.search_id, page=page, **kwargs).data
        return response_data

    def update_card_rule(self, db: Session, card_id: int, name: str, enabled: bool, amount: Decimal = None):
        card_q = db.query(CardSo).filter(CardSo.id==card_id).first()
        if name not in self.settings.RULES:
            raise SoldoException("Exception rule. name rule not enable or not exists")
        rules = card.update_card_rule(card_q.search_id, name=name, enabled=enabled, amount=amount).data
        return rules

    def get_card_rules(self, db: Session, card_id: int):
        card_q = db.query(CardSo).filter(CardSo.id == card_id).first()
        return card.get_card_rules(card_q.search_id).data

    def upload_cards(self, db: Session):
        response_cards = card.search(page_size=self.settings.UPLOAD_SIZE).data.results
        query_wallets = db.query(WalletSo).filter(WalletSo.search_id is not None).all()
        query_cards = db.query(CardSo).filter(CardSo.search_id is not None).all()

        list_model_id, list_model = generate_list_model_search_id(query_cards)
        list_wallets_id, list_wallets = generate_list_model_search_id(query_wallets)

        filter_model = list(filter(
            lambda w: w.wallet_id in list_wallets_id,
            response_cards
        ))

        update_cards = []
        create_cards_id = []
        set_add_group_cards = []
        for model in filter_model:
            card_id = list_model.get(model.id)
            if model.group_id != self.settings.SAFE_WALLET:
                set_add_group_cards.append(model.id)
            if card_id:
                update_cards.append({
                    "id": card_id,
                    "status": model.status,
                    "name": model.name
                })
            else:
                create_cards_id.append(model.id)

        create_cards = []
        for card_id in create_cards_id:
            response_card = card.get(card_id, True).data
            wallet_id = list_wallets.get(response_card.wallet_id)
            if wallet_id:
                response_card = card.get(card_id.search_id, True)
                card_obj = CardSo(wallet_id=wallet_id, search_id=response_card.id)
                card_obj.PAN = response_card.pan
                card_obj.cvv = response_card.cvv
                card_obj.name = response_card.name
                card_obj.type = response_card.type
                card_obj.created_on = response_card.creation_time
                card_obj.status = response_card.status
                card_obj.expiry = response_card.expiration_date.date()
                card_obj.PAN = response_card.pan
                create_cards.append(card_obj)

        db.bulk_update_mappings(CardSo, update_cards)
        if create_cards:
            db.bulk_save_objects(create_cards)
        db.commit()
        for card_id in set_add_group_cards:
            self.add_item_to_group(card_id, type="CARD")
        return {
            "create_list": [c.search_id for c in create_cards],
            "update_list": [c.get("id") for c in update_cards],
                }

    def internal_transfer(self, db: Session, from_wallet_id: int, to_wallet_id: int, amount: Decimal, currency: str ="EUR", **kwargs):
        from_wallet = db.query(WalletSo).filter(WalletSo.id==from_wallet_id).first()
        to_wallet = db.query(WalletSo).filter(WalletSo.id==to_wallet_id).first()
        response_data = wallets.internal_transfer(
            amount=amount,
            toWalletId=to_wallet.search_id,
            fromWalletId=from_wallet.search_id,
            currencyCode=currency,
            **kwargs
        ).data
        return response_data

    def internal_transfer_to_safe(self, db: Session, from_wallet_id: int, amount: Decimal,
                          currency: str = "EUR"):
        from_wallet = db.query(WalletSo).filter(WalletSo.id==from_wallet_id).first()
        to_wallet = db.query(WalletSo).filter(WalletSo.search_id==self.settings.SAFE_WALLET).first()
        response_data = wallets.internal_transfer(
            amount=amount,
            toWalletId=to_wallet.search_id,
            fromWalletId=from_wallet.search_id,
            currencyCode=currency
        ).data
        return response_data

    def upload_transaction_wallet(self, db: Session, **kwargs):
        date_to = datetime.now()
        date_from = date_to - timedelta(days=2)
        query_transactions = db.query(TransactionSo).filter(
            TransactionSo.date >= date_from,
            TransactionSo.date <= date_to + timedelta(days=1),
        ).all()
        query_wallets = db.query(WalletSo).filter(WalletSo.search_id is not None).all()
        print(query_transactions)

        list_trans_id, list_trans = generate_list_model_search_id(query_transactions)
        list_wallet_id, list_wallet = generate_list_model_search_id(query_wallets)

        response_data = transaction.search(
            page_size=self.settings.UPLOAD_SIZE,
            toDate=date_to.strftime(self.format_date),
            fromDate=date_from.strftime(self.format_date), **kwargs).data
        # upload safe wallet
        response_data.results += transaction.search(
            page_size=self.settings.UPLOAD_SIZE,
            toDate=date_to.strftime(self.format_date),
            fromDate=date_from.strftime(self.format_date),
            type="wallet", publicId=self.settings.SAFE_WALLET,
        ).data.results
        # filter wallet_id
        trans_by_wallet_id = list(filter(
            lambda trans: trans.wallet_id in list_wallet_id,
            response_data.results
        ))
        # return

        create_transaction = []
        update_transaction = []
        columns = [c.name for c in TransactionSo.__table__.columns]
        columns.remove("id")
        for trans in trans_by_wallet_id:
            data = {}
            for c in columns:
                data[c] = getattr(trans, c, None)
            data["search_id"] = trans.id
            data['wallet_id'] = list_wallet.get(trans.wallet_id)

            trans_id  = list_trans.get(trans.id)
            if trans_id:
                data.update(dict(
                    id=trans_id,
                    search_id=trans.id
                ))
                update_transaction.append(data)
            else:
                create_transaction.append(
                    TransactionSo(
                        **data,
                    ))


        db.bulk_update_mappings(TransactionSo, update_transaction)
        if create_transaction:
            db.bulk_save_objects(create_transaction)
        db.commit()
        return {
            "create_list": [c.search_id for c in create_transaction],
            "update_list": [c.get("id") for c in update_transaction],
                }

    def wallets_set_group(self, db: Session):
        response_wallets = wallets.search(type="company", page_size=self.settings.UPLOAD_SIZE).data.results
        query_wallets = db.query(WalletSo).filter(WalletSo.search_id is not None).all()

        list_wallets_id, list_wallets = generate_list_model_search_id(query_wallets)
        filter_wallet = list(filter(
            lambda w: w.id in list_wallets_id,
            response_wallets
        ))
        result = []
        for wallet in filter_wallet:
            if not wallet.group_id:
                self.add_item_to_group(wallet.id)
                result.append(wallet.id)
        return result

    def upload_wallets(self, db: Session):
        response_wallets = wallets.search(type="company", page_size=self.settings.UPLOAD_SIZE).data.results
        query_wallets = db.query(WalletSo).filter(WalletSo.search_id is not None).all()

        list_wallets_id, list_wallets = generate_list_model_search_id(query_wallets)
        filter_wallet = list(filter(
            lambda w: w.id in list_wallets_id,
            response_wallets
        ))
        update_wallets = []
        for wallet in filter_wallet:
            wallet_id = list_wallets.get(wallet.id)
            update_wallets.append({
                    "id": wallet_id,
                    "balance": wallet.available_amount,
                    "blocked_balance": wallet.blocked_amount,
                    "currency": wallet.currency_code
                })

        db.bulk_update_mappings(WalletSo, update_wallets)
        db.commit()
        return list_wallets

    def wallet_update_balance(self, db: Session, wallet_id: int):
        wallet = db.query(WalletSo).filter(WalletSo.id == wallet_id).first()
        response_data = wallets.get(wallet.search_id)
        wallet.balance = response_data.data.available_amount
        wallet.blocked_balance = response_data.data.blocked_amount
        self.save_obj(db, wallet)
        return wallet

    def get_wallets(self, **kwargs):
        response_data = wallets.search(**kwargs)
        print(response_data)
        return response_data

    def get_card(self, card_id: str = None, showSensitiveData: str = None, **kwargs):
        return card.get(card_id, showSensitiveData)

    def update_info_card(self, db: Session, id: int, showSensitiveData=True):
        card_obj = db.query(CardSo).filter(CardSo.id == id).first()
        response_data = card.get(card_obj.search_id, showSensitiveData)
        response_card = response_data.data
        card_obj.PAN = response_card.pan
        card_obj.cvv = response_card.cvv
        card_obj.name = response_card.name
        card_obj.type = response_card.type
        card_obj.created_on = response_card.creation_time
        card_obj.expiry = response_card.expiration_date.date()
        card_obj.PAN = response_card.pan
        card_obj.status = response_card.status
        self.save_obj(db, card_obj)
        return card_obj

    def create_card(self, db: Session, user_id: int,
                    name: str, emboss_line4: str = None, type="VIRTUAL", card_label=None):
        wallet = db.query(WalletSo).filter(WalletSo.user_id == user_id).first()
        self.internal_transfer_to_safe(db, wallet.id, amount=self.card_price)
        if not card_label:
            user = db.query(self._user).filter(self._user.id == user_id).first()
            card_label = user.email


        response_data = card.create(
            owner_public_id=None,
            wallet_id=wallet.search_id,
            name=name,
            emboss_line4=emboss_line4,
            type=type,
            card_label=card_label)
        order = response_data.data

        if not order.is_valid or order.status != "PLACED":
            raise SoldoException("Error create_card", response_data.dict())
        result = {
            "wallet_id": wallet.id,
            "status": order.status,
            "category": "CARD"
        }
        self.__cache[order.id] = result
        return {order.id: result}

    def add_item_to_group(self, id: str, type="WALLET", groupId: str = None):
        if not groupId:
            groupId = self.settings.GROUP_ID
        return group.group_write(groupId, id, type)

    def get_order(self, order_id: str):
        return order.get(order_id)
