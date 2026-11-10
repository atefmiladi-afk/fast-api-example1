from sqlalchemy.orm import Session

from app.models import Category, Word

CATEGORIES = [
    {
        "slug": "essen",
        "name_de": "Essen & Trinken",
        "name_en": "Food & Drink",
        "description": "Alltagliche Lebensmittel und Getranke.",
        "emoji": "E",
        "color": "#ea580c",
        "image_url": "https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=800&q=80",
        "words": [
            ("Milch", "die", "milk", "Ich trinke Milch.", "I drink milk.", "https://images.unsplash.com/photo-1550583724-b2692b85b150?auto=format&fit=crop&w=600&q=80"),
            ("Wasser", "das", "water", "Ich trinke Wasser.", "I drink water.", "https://images.unsplash.com/photo-1548839140-29a749e1cf4d?auto=format&fit=crop&w=600&q=80"),
            ("Brot", "das", "bread", "Das Brot ist frisch.", "The bread is fresh.", "https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=600&q=80"),
            ("Apfel", "der", "apple", "Der Apfel ist rot.", "The apple is red.", "https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?auto=format&fit=crop&w=600&q=80"),
            ("Kase", "der", "cheese", "Ich esse Kase.", "I eat cheese.", "https://images.unsplash.com/photo-1486297678162-eb2a19b0a32d?auto=format&fit=crop&w=600&q=80"),
            ("Ei", "das", "egg", "Das Ei ist gekocht.", "The egg is cooked.", "https://images.unsplash.com/photo-1582722872445-44dc5f7e3c8f?auto=format&fit=crop&w=600&q=80"),
            ("Kaffee", "der", "coffee", "Der Kaffee ist heiss.", "The coffee is hot.", "https://images.unsplash.com/photo-1511920170033-f8396924c348?auto=format&fit=crop&w=600&q=80"),
            ("Tee", "der", "tea", "Ich trinke Tee.", "I drink tea.", "https://images.unsplash.com/photo-1544787219-7f47ccb76574?auto=format&fit=crop&w=600&q=80"),
            ("Banane", "die", "banana", "Die Banane ist gelb.", "The banana is yellow.", "https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?auto=format&fit=crop&w=600&q=80"),
            ("Fleisch", "das", "meat", "Ich kaufe Fleisch.", "I buy meat.", "https://images.unsplash.com/photo-1603048297172-c92544798d5a?auto=format&fit=crop&w=600&q=80"),
            ("Reis", "der", "rice", "Reis mit Gemuse.", "Rice with vegetables.", "https://images.unsplash.com/photo-1516684669134-de6f7c473a2a?auto=format&fit=crop&w=600&q=80"),
            ("Suppe", "die", "soup", "Die Suppe ist warm.", "The soup is warm.", "https://images.unsplash.com/photo-1547592166-23acba8dcd40?auto=format&fit=crop&w=600&q=80"),
        ],
    },
    {
        "slug": "tiere",
        "name_de": "Tiere",
        "name_en": "Animals",
        "description": "Tiere aus Haus, Bauernhof und Natur.",
        "emoji": "T",
        "color": "#16a34a",
        "image_url": "https://images.unsplash.com/photo-1425082661705-1834bfd09dca?auto=format&fit=crop&w=800&q=80",
        "words": [
            ("Hund", "der", "dog", "Der Hund bellt.", "The dog barks.", "https://images.unsplash.com/photo-1552053831-71594a27632d?auto=format&fit=crop&w=600&q=80"),
            ("Katze", "die", "cat", "Die Katze schlaft.", "The cat sleeps.", "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?auto=format&fit=crop&w=600&q=80"),
            ("Vogel", "der", "bird", "Der Vogel fliegt.", "The bird flies.", "https://images.unsplash.com/photo-1444464666168-49d633b86797?auto=format&fit=crop&w=600&q=80"),
            ("Pferd", "das", "horse", "Das Pferd lauft schnell.", "The horse runs fast.", "https://images.unsplash.com/photo-1553284965-83fd3e82fa5a?auto=format&fit=crop&w=600&q=80"),
            ("Kuh", "die", "cow", "Die Kuh gibt Milch.", "The cow gives milk.", "https://images.unsplash.com/photo-1500595046743-cd271d694d30?auto=format&fit=crop&w=600&q=80"),
            ("Fisch", "der", "fish", "Der Fisch schwimmt.", "The fish swims.", "https://images.unsplash.com/photo-1524704654690-b56c05c78a00?auto=format&fit=crop&w=600&q=80"),
            ("Hase", "der", "rabbit", "Der Hase ist schnell.", "The rabbit is fast.", "https://images.unsplash.com/photo-1585110396000-c9ed5f94ca3e?auto=format&fit=crop&w=600&q=80"),
            ("Schaf", "das", "sheep", "Das Schaf ist weiss.", "The sheep is white.", "https://images.unsplash.com/photo-1484557985045-edf25e08da73?auto=format&fit=crop&w=600&q=80"),
        ],
    },
    {
        "slug": "familie",
        "name_de": "Familie",
        "name_en": "Family",
        "description": "Familienmitglieder und Beziehungen.",
        "emoji": "F",
        "color": "#db2777",
        "image_url": "https://images.unsplash.com/photo-1511895426328-dc8714191300?auto=format&fit=crop&w=800&q=80",
        "words": [
            ("Mutter", "die", "mother", "Meine Mutter kocht.", "My mother cooks.", "https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&w=600&q=80"),
            ("Vater", "der", "father", "Mein Vater liest.", "My father reads.", "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&w=600&q=80"),
            ("Kind", "das", "child", "Das Kind spielt.", "The child plays.", "https://images.unsplash.com/photo-1503454537195-1dcabb73ffb9?auto=format&fit=crop&w=600&q=80"),
            ("Bruder", "der", "brother", "Mein Bruder lacht.", "My brother laughs.", "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=600&q=80"),
            ("Schwester", "die", "sister", "Meine Schwester singt.", "My sister sings.", "https://images.unsplash.com/photo-1529626455594-4ff0802cfb7e?auto=format&fit=crop&w=600&q=80"),
            ("Oma", "die", "grandma", "Die Oma backt Kuchen.", "Grandma bakes cake.", "https://images.unsplash.com/photo-1566616213890-f8d0a0b0f1c3?auto=format&fit=crop&w=600&q=80"),
            ("Opa", "der", "grandpa", "Der Opa erzahlt Geschichten.", "Grandpa tells stories.", "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?auto=format&fit=crop&w=600&q=80"),
            ("Freund", "der", "friend", "Mein Freund ist nett.", "My friend is nice.", "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=600&q=80"),
        ],
    },
    {
        "slug": "farben",
        "name_de": "Farben",
        "name_en": "Colors",
        "description": "Grundfarben und Nuancen.",
        "emoji": "C",
        "color": "#7c3aed",
        "image_url": "https://images.unsplash.com/photo-1502691876148-a84978e59af8?auto=format&fit=crop&w=800&q=80",
        "words": [
            ("Rot", "", "red", "Die Rose ist rot.", "The rose is red.", "https://images.unsplash.com/photo-1490750967868-88aa4486c946?auto=format&fit=crop&w=600&q=80"),
            ("Blau", "", "blue", "Der Himmel ist blau.", "The sky is blue.", "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=600&q=80"),
            ("Grun", "", "green", "Das Gras ist grun.", "The grass is green.", "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?auto=format&fit=crop&w=600&q=80"),
            ("Gelb", "", "yellow", "Die Sonne ist gelb.", "The sun is yellow.", "https://images.unsplash.com/photo-1495616811223-4d98c6e9c869?auto=format&fit=crop&w=600&q=80"),
            ("Schwarz", "", "black", "Die Nacht ist schwarz.", "The night is black.", "https://images.unsplash.com/photo-1478760329108-5c3ed140d444?auto=format&fit=crop&w=600&q=80"),
            ("Weiss", "", "white", "Der Schnee ist weiss.", "The snow is white.", "https://images.unsplash.com/photo-1491002052546-bf38f186af56?auto=format&fit=crop&w=600&q=80"),
            ("Orange", "", "orange", "Die Orange ist orange.", "The orange is orange.", "https://images.unsplash.com/photo-1557800636-894a64c1696f?auto=format&fit=crop&w=600&q=80"),
            ("Lila", "", "purple", "Die Blume ist lila.", "The flower is purple.", "https://images.unsplash.com/photo-1468327768560-75b45c03eda4?auto=format&fit=crop&w=600&q=80"),
        ],
    },
    {
        "slug": "haus",
        "name_de": "Haus & Wohnen",
        "name_en": "Home",
        "description": "Raeume und Gegenstaende im Haus.",
        "emoji": "H",
        "color": "#0891b2",
        "image_url": "https://images.unsplash.com/photo-1568605114967-8130f3a36994?auto=format&fit=crop&w=800&q=80",
        "words": [
            ("Haus", "das", "house", "Das Haus ist gross.", "The house is big.", "https://images.unsplash.com/photo-1570129477492-45c003edd2be?auto=format&fit=crop&w=600&q=80"),
            ("Tur", "die", "door", "Die Tur ist offen.", "The door is open.", "https://images.unsplash.com/photo-1516455590571-18256e5bb9ff?auto=format&fit=crop&w=600&q=80"),
            ("Fenster", "das", "window", "Das Fenster ist klar.", "The window is clear.", "https://images.unsplash.com/photo-1493809842364-78817add7ffb?auto=format&fit=crop&w=600&q=80"),
            ("Tisch", "der", "table", "Der Tisch ist aus Holz.", "The table is wooden.", "https://images.unsplash.com/photo-1533090481720-856c6e3c1fdc?auto=format&fit=crop&w=600&q=80"),
            ("Stuhl", "der", "chair", "Der Stuhl ist bequem.", "The chair is comfortable.", "https://images.unsplash.com/photo-1503602642458-232111445657?auto=format&fit=crop&w=600&q=80"),
            ("Bett", "das", "bed", "Das Bett ist weich.", "The bed is soft.", "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=600&q=80"),
            ("Lampe", "die", "lamp", "Die Lampe leuchtet.", "The lamp shines.", "https://images.unsplash.com/photo-1507473885805-4c9f415bf4ba?auto=format&fit=crop&w=600&q=80"),
            ("Kuche", "die", "kitchen", "Die Kuche ist modern.", "The kitchen is modern.", "https://images.unsplash.com/photo-1556912173-46c336c7fd55?auto=format&fit=crop&w=600&q=80"),
        ],
    },
    {
        "slug": "kleidung",
        "name_de": "Kleidung",
        "name_en": "Clothes",
        "description": "Was wir jeden Tag tragen.",
        "emoji": "K",
        "color": "#ca8a04",
        "image_url": "https://images.unsplash.com/photo-1445205170230-053f83030561?auto=format&fit=crop&w=800&q=80",
        "words": [
            ("Hemd", "das", "shirt", "Das Hemd ist blau.", "The shirt is blue.", "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?auto=format&fit=crop&w=600&q=80"),
            ("Hose", "die", "pants", "Die Hose passt gut.", "The pants fit well.", "https://images.unsplash.com/photo-1542272604-787c3835535d?auto=format&fit=crop&w=600&q=80"),
            ("Schuh", "der", "shoe", "Der Schuh ist neu.", "The shoe is new.", "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=600&q=80"),
            ("Hut", "der", "hat", "Der Hut ist schwarz.", "The hat is black.", "https://images.unsplash.com/photo-1514327605112-b646c99f1c0c?auto=format&fit=crop&w=600&q=80"),
            ("Jacke", "die", "jacket", "Die Jacke ist warm.", "The jacket is warm.", "https://images.unsplash.com/photo-1551028719-00167b16eac5?auto=format&fit=crop&w=600&q=80"),
            ("Kleid", "das", "dress", "Das Kleid ist schon.", "The dress is beautiful.", "https://images.unsplash.com/photo-1595777457583-95e059d581b8?auto=format&fit=crop&w=600&q=80"),
            ("Socke", "die", "sock", "Die Socke ist weich.", "The sock is soft.", "https://images.unsplash.com/photo-1586351012965-261ae217c1c3?auto=format&fit=crop&w=600&q=80"),
            ("Mantel", "der", "coat", "Der Mantel ist lang.", "The coat is long.", "https://images.unsplash.com/photo-1539533018447-63fcce2678e3?auto=format&fit=crop&w=600&q=80"),
        ],
    },
]


def seed_if_empty(db: Session) -> None:
    if db.query(Category).count() > 0:
        return
    for cat in CATEGORIES:
        category = Category(
            slug=cat["slug"],
            name_de=cat["name_de"],
            name_en=cat["name_en"],
            description=cat["description"],
            emoji=cat["emoji"],
            color=cat["color"],
            image_url=cat["image_url"],
        )
        db.add(category)
        db.flush()
        for german, article, english, example_de, example_en, image_url in cat["words"]:
            db.add(
                Word(
                    category_id=category.id,
                    german=german,
                    article=article,
                    english=english,
                    example_de=example_de,
                    example_en=example_en,
                    image_url=image_url,
                    audio_hint=german,
                )
            )
    db.commit()
