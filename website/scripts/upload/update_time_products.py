from website.models import Product
from datetime import datetime
from dateutil.relativedelta import relativedelta
import random
#import warning

#warning.filterwarnings("ignore",category="DateTimeField")

# run with python3 manage.py shell < ./website/scripts/upload/update_time_products.py
now = datetime.now().date()
#Get unupdated registers
unupdated_products = Product.objects.filter(auction_end_time__lte=now)
for product in unupdated_products:
    print(f'{product.name} was updated')
    product.auction_end_time = datetime.now().date() + relativedelta(days=random.randint(5,30))
    product.save()
    #incluir quitar el ganador de la puja anterior si es que tiene