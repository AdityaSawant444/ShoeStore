from django.core.management.base import BaseCommand
from store.models import Category, Product
from decimal import Decimal

class Command(BaseCommand):
    help = 'Populate the database with dummy shoe products'

    def handle(self, *args, **options):
        self.stdout.write('Creating categories...')
        
        # Create categories
        categories_data = [
            {
                'name': 'Athletic Shoes',
                'slug': 'athletic',
                'description': 'Performance footwear for sports and fitness activities.'
            },
            {
                'name': 'Formal Shoes',
                'slug': 'formal',
                'description': 'Elegant footwear for professional and formal occasions.'
            },
            {
                'name': 'Casual Shoes',
                'slug': 'casual',
                'description': 'Comfortable and stylish everyday footwear.'
            }
        ]
        
        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            categories[cat_data['slug']] = category
            if created:
                self.stdout.write(f'Created category: {category.name}')
        
        self.stdout.write('Creating products...')
        
        # Men's products
        mens_products = [
            {
                'name': 'Men\'s Running Shoes',
                'slug': 'mens-running-shoes',
                'category': 'athletic',
                'gender': 'M',
                'description': 'Lightweight and breathable running shoes with excellent cushioning for maximum comfort during your runs.',
                'price': Decimal('7467.17'),
                'sale_price': Decimal('5809.17'),
                'featured': True
            },
            {
                'name': 'Men\'s Formal Oxford',
                'slug': 'mens-formal-oxford',
                'category': 'formal',
                'gender': 'M',
                'description': 'Classic Oxford shoes perfect for business meetings and formal occasions. Made from premium leather.',
                'price': Decimal('10789.17'),
                'sale_price': None,
                'featured': True
            },
            {
                'name': 'Men\'s Casual Sneakers',
                'slug': 'mens-casual-sneakers',
                'category': 'casual',
                'gender': 'M',
                'description': 'Comfortable and stylish sneakers perfect for everyday wear. Versatile design goes with any outfit.',
                'price': Decimal('6639.17'),
                'sale_price': Decimal('4979.17'),
                'featured': False
            },
            {
                'name': 'Men\'s Basketball Shoes',
                'slug': 'mens-basketball-shoes',
                'category': 'athletic',
                'gender': 'M',
                'description': 'High-performance basketball shoes with excellent ankle support and traction for the court.',
                'price': Decimal('9959.17'),
                'sale_price': None,
                'featured': False
            },
            {
                'name': 'Men\'s Dress Shoes',
                'slug': 'mens-dress-shoes',
                'category': 'formal',
                'gender': 'M',
                'description': 'Elegant dress shoes crafted from fine leather. Perfect for weddings and special events.',
                'price': Decimal('12449.17'),
                'sale_price': Decimal('9959.17'),
                'featured': False
            },
            {
                'name': 'Men\'s Loafers',
                'slug': 'mens-loafers',
                'category': 'casual',
                'gender': 'M',
                'description': 'Slip-on loafers with a comfortable fit. Great for casual office wear or weekend outings.',
                'price': Decimal('7469.17'),
                'sale_price': None,
                'featured': False
            }
        ]
        
        # Women's products
        womens_products = [
            {
                'name': 'Women\'s Running Shoes',
                'slug': 'womens-running-shoes',
                'category': 'athletic',
                'gender': 'W',
                'description': 'Lightweight and supportive running shoes designed specifically for women\'s feet.',
                'price': Decimal('7884.17'),
                'sale_price': Decimal('6224.17'),
                'featured': True
            },
            {
                'name': 'Women\'s Heels',
                'slug': 'womens-heels',
                'category': 'formal',
                'gender': 'W',
                'description': 'Elegant high heels perfect for formal events and professional settings.',
                'price': Decimal('9129.17'),
                'sale_price': None,
                'featured': True
            },
            {
                'name': 'Women\'s Ballet Flats',
                'slug': 'womens-ballet-flats',
                'category': 'casual',
                'gender': 'W',
                'description': 'Comfortable ballet flats with a classic design. Perfect for everyday wear.',
                'price': Decimal('5809.17'),
                'sale_price': Decimal('4149.17'),
                'featured': False
            },
            {
                'name': 'Women\'s Tennis Shoes',
                'slug': 'womens-tennis-shoes',
                'category': 'athletic',
                'gender': 'W',
                'description': 'Professional tennis shoes with excellent court grip and lateral support.',
                'price': Decimal('8714.17'),
                'sale_price': None,
                'featured': False
            },
            {
                'name': 'Women\'s Pumps',
                'slug': 'womens-pumps',
                'category': 'formal',
                'gender': 'W',
                'description': 'Classic pumps with a sophisticated design. Ideal for business meetings and formal occasions.',
                'price': Decimal('9879.17'),
                'sale_price': Decimal('7469.17'),
                'featured': False
            },
            {
                'name': 'Women\'s Ankle Boots',
                'slug': 'womens-ankle-boots',
                'category': 'casual',
                'gender': 'W',
                'description': 'Stylish ankle boots perfect for fall and winter. Comfortable and fashionable.',
                'price': Decimal('8299.17'),
                'sale_price': None,
                'featured': False
            }
        ]
        
        # Unisex products
        unisex_products = [
            {
                'name': 'Unisex Canvas Sneakers',
                'slug': 'unisex-canvas-sneakers',
                'category': 'casual',
                'gender': 'U',
                'description': 'Classic canvas sneakers that never go out of style. Comfortable and versatile.',
                'price': Decimal('4979.17'),
                'sale_price': Decimal('3319.17'),
                'featured': True
            },
            {
                'name': 'Unisex Hiking Boots',
                'slug': 'unisex-hiking-boots',
                'category': 'athletic',
                'gender': 'U',
                'description': 'Durable hiking boots with excellent traction and waterproof protection.',
                'price': Decimal('11619.17'),
                'sale_price': None,
                'featured': False
            }
        ]
        
        all_products = mens_products + womens_products + unisex_products
        
        for product_data in all_products:
            product, created = Product.objects.get_or_create(
                slug=product_data['slug'],
                defaults={
                    'name': product_data['name'],
                    'category': categories[product_data['category']],
                    'gender': product_data['gender'],
                    'description': product_data['description'],
                    'price': product_data['price'],
                    'sale_price': product_data['sale_price'],
                    'featured': product_data['featured'],
                    'available': True
                }
            )
            
            if created:
                self.stdout.write(f'Created product: {product.name}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated database with dummy products!')
        ) 