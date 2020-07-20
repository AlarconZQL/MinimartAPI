from random import randint
from datetime import time, date
from ..models import *
from . import Days

# STORES
coco_downtown = Store(
    name='COCO Downtown', address='Fake address number 1', logo_url='http://fakeimage1')
coco_bay = Store(
    name='COCO Bay', address='Fake address number 2', logo_url='http://fakeimage2')
coco_mall = Store(
    name='COCO Mall', address='Fake address number 3', logo_url='http://fakeimage3')


def seed_database():

    print('Droping all database tables...')
    db.drop_all()
    print('All tables were deleted!')

    print('Creating all database tables...')
    db.create_all()
    print('All tables were created!')

    print('Creating and setting stores working days...')
    create_and_set_store_working_days()

    print('Creating categories...')
    categories = create_categories()

    print('Creating products...')
    products = create_products(categories)

    print('Filling stores with products')
    generate_stock(products)

    # VOUCHERS
    # COCO Bay
    voucher_bay_1 = Voucher(code='COCO1V1F8XOG1MZZ',
                            start_date=date(2020, 7, 27), end_date=date(2020, 8, 13),
                            only_on_days=[VoucherDay(day=Days.Wednesday),
                                          VoucherDay(day=Days.Thursday)])

    voucher_bay_2 = Voucher(code='COCOKCUD0Z9LUKBN',
                            start_date=date(2020, 7, 24), end_date=date(2020, 8, 6))

    # COCO Mall
    voucher_mall = Voucher(code='COCOG730CNSG8ZVX',
                           start_date=date(2020, 7, 31), end_date=date(2020, 8, 9))

    # COCO Downtown
    voucher_downtown_1 = Voucher(code='COCO2O1USLC6QR22',
                                 start_date=date(2020, 8, 1), end_date=date(2020, 8, 31))

    voucher_downtown_2 = Voucher(code='COCO0FLEQ287CC05',
                                 start_date=date(2020, 7, 1), end_date=date(2020, 7, 15),
                                 only_on_days=[VoucherDay(day=Days.Monday)])

    # Set voucher's products

    sodas_products = [products['tea'], products['coffee'], products['cola'],
                      products['sprute'], products['slurm'], products['diet_slurm']]

    food_products = [products['salsa_cookies'], products['windmill_cookies'],
                     products['garlic_bread'], products['lactel_bread'],
                     products['raviolchesx12'], products['raviolchesx48'],
                     products['milanga'], products['milanga_napo']]

    cleaning_products = [products['detergent'],
                         products['virulanita'], products['sponge'], products['mop']]

    bathroom_products = [products['toilet_paper'],
                         products['soap'], products['shampoo'], products['toothpaste']]

    vouchers_info = [
        {
            "voucher": voucher_bay_1,
            "products": cleaning_products,
            "discount": 20,
            "on_unit": None,
            "max_units": None,
        },
        {
            "voucher": voucher_bay_2,
            "products": [products['windmill_cookies']],
            "discount": 100,
            "on_unit": 3,
            "max_units": 6,
        },
        {
            "voucher": voucher_mall,
            "products": bathroom_products + sodas_products,
            "discount": 10,
            "on_unit": None,
            "max_units": None,
        },
        {
            "voucher": voucher_downtown_1,
            "products": [products['cola'], products['slurm'], products['diet_slurm']],
            "discount": 30,
            "on_unit": 2,
            "max_units": 2,
        },
        {
            "voucher": voucher_downtown_2,
            "products": [products['toothpaste']],
            "discount": 50,
            "on_unit": 2,
            "max_units": 2,
        }
    ]

    for voucher_info in vouchers_info:
        for product in voucher_info['products']:
            voucher_info['voucher'].products.append(
                ProductVoucherLink(
                    product=product,
                    discount=voucher_info['discount'],
                    on_unit=voucher_info['on_unit'],
                    max_units=voucher_info['max_units']
                ))

    stores_voucher = [
        {'store': coco_bay, 'vouchers': [voucher_bay_1, voucher_bay_2]},
        {'store': coco_mall, 'vouchers': [voucher_mall]},
        {'store': coco_downtown, 'vouchers': [
            voucher_downtown_1, voucher_downtown_2]}
    ]

    for store in stores_voucher:
        for voucher in store['vouchers']:
            store['store'].vouchers.append(voucher)

    # Persist information
    stores = [coco_bay, coco_downtown, coco_mall]
    for store in stores:
        db.session.add(store)

    print('Persisting information on database...')
    db.session.commit()

    return


def create_working_days():
    return(
        {
            'monday_morning': WorkingDay(day=Days.Monday,
                                         starts_at=time(8, 0), finishes_at=time(14, 0)),
            'tuesday_morning': WorkingDay(day=Days.Tuesday,
                                          starts_at=time(8, 0), finishes_at=time(14, 0)),
            'wednesday_morning': WorkingDay(day=Days.Wednesday,
                                            starts_at=time(8, 0), finishes_at=time(14, 0)),
            'thursday_morning': WorkingDay(day=Days.Thursday,
                                           starts_at=time(8, 0), finishes_at=time(14, 0)),
            'friday_morning': WorkingDay(day=Days.Friday,
                                         starts_at=time(8, 0), finishes_at=time(14, 0)),
            'monday_afternoon': WorkingDay(day=Days.Monday,
                                           starts_at=time(14, 0), finishes_at=time(20, 0)),
            'tuesday_afternoon': WorkingDay(day=Days.Tuesday,
                                            starts_at=time(14, 0), finishes_at=time(20, 0)),
            'wednesday_afternoon': WorkingDay(day=Days.Wednesday,
                                              starts_at=time(14, 0), finishes_at=time(20, 0)),
            'thursday_afternoon': WorkingDay(day=Days.Thursday,
                                             starts_at=time(14, 0), finishes_at=time(20, 0)),
            'friday_afternoon': WorkingDay(day=Days.Friday,
                                           starts_at=time(14, 0), finishes_at=time(20, 0)),
        })


def create_and_set_store_working_days():
    working_days = create_working_days()
    stores_working_days_info = [
        {
            'store': coco_downtown,
            'working_days': ['monday_morning', 'tuesday_morning',
                             'wednesday_morning', 'thursday_morning', 'friday_morning']
        },
        {
            'store': coco_bay,
            'working_days': ['monday_afternoon', 'tuesday_afternoon',
                             'wednesday_afternoon', 'thursday_afternoon', 'friday_afternoon']
        },
        {
            'store': coco_mall,
            'working_days': ['monday_morning', 'tuesday_afternoon',
                             'wednesday_morning', 'thursday_afternoon']
        }
    ]
    for store_info in stores_working_days_info:
        for working_day_name in store_info['working_days']:
            store_info['store'].workingdays.append(
                working_days[working_day_name])


def create_categories():
    return ({
        'sodas': Category(name='Sodas'),
        'food': Category(name='Food'),
        'cleaning': Category(name='Cleaning'),
        'bathroom': Category(name='Bathroom')
    })


def create_products(categories):
    sodas = categories['sodas']
    food = categories['food']
    cleaning = categories['cleaning']
    bathroom = categories['bathroom']
    return ({
        # SODAS
        'tea': Product(name='Cold Ice Tea', categories=[sodas]),
        'coffee': Product(name='Coffee flavoured milk', categories=[sodas]),
        'cola': Product(name='Nuka-Cola', categories=[sodas]),
        'sprute': Product(name='Sprute', categories=[sodas]),
        'slurm': Product(name='Slurm', categories=[sodas]),
        'diet_slurm': Product(name='Diet Slurm', categories=[sodas]),

        # FOOD
        'salsa_cookies': Product(name='Salsa Cookies', categories=[food]),
        'windmill_cookies': Product(name='Windmill Cookies', categories=[food]),
        'garlic_bread': Product(name='Garlic-o-bread 2000', categories=[food]),
        'lactel_bread': Product(name='LACTEL bread', categories=[food]),
        'raviolchesx12': Product(name='Ravioloches x12', categories=[food]),
        'raviolchesx48': Product(name='Ravioloches x48', categories=[food]),
        'milanga': Product(name='Milanga ganga', categories=[food]),
        'milanga_napo': Product(name='Milanga ganga napo', categories=[food]),

        # CLEANING
        'detergent': Product(name='Atlantis detergent', categories=[cleaning]),
        'virulanita': Product(name='Virulanita', categories=[cleaning]),
        'sponge': Product(name='Spong, bob', categories=[cleaning]),
        'mop': Product(name='Generic mop', categories=[cleaning]),

        # BATHROOM
        'toilet_paper': Product(
            name='Pure steel toilet paper', categories=[bathroom]),
        'soap': Product(name='Generic soap', categories=[bathroom]),
        'shampoo': Product(name='PANTONE shampoo', categories=[bathroom]),
        'toothpaste': Product(name='Hang-yourself toothpaste',
                              categories=[bathroom])
    })


def generate_stock(products):
    coco_bay_no_stock = [products['diet_slurm'], products['toilet_paper'],
                         products['soap'], products['shampoo'], products['toothpaste']]
    coco_mall_no_stock = [products['raviolchesx12'], products['raviolchesx48'],
                          products['milanga'], products['milanga_napo'], products['detergent'], products['virulanita'], products['sponge'], products['mop']]
    coco_downtown_no_stock = [products['sprute'], products['slurm'],
                              products['detergent'], products['virulanita'], products['sponge'], products['mop'], products['toilet_paper']]

    stores_stock_info = [
        {'store': coco_bay, 'no_stock': coco_bay_no_stock},
        {'store': coco_mall, 'no_stock': coco_mall_no_stock},
        {'store': coco_downtown, 'no_stock': coco_downtown_no_stock}
    ]

    # Create product stock for each store

    for product in products.values():
        for store_info in stores_stock_info:
            stock = 0 if product in store_info['no_stock'] else randint(
                1, 10)
            store_info['store'].products.append(
                ProductStoreLink(stock=stock, product=product))
    return
