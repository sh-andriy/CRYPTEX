from app import create_app
from models import db, Coin


app = create_app()

coins = [
    {"index": "BTCUSDT", "abbreviation": "BTC"},
    {"index": "DOGEUSDT", "abbreviation": "DOGE"},
    {"index": "PHBUSDT", "abbreviation": "PHB"},
    {"index": "LUNAUSDT", "abbreviation": "LUNA"},
    {"index": "LUNCUSDT", "abbreviation": "LUNC"},
]

with app.app_context():
    Coin.query.delete()

    for coin in coins:
        db.session.add(
            Coin(
                index=coin['index'],
                abbreviation=coin['abbreviation'],
            )
        )

    db.session.commit()
