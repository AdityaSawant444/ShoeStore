import os
from django.db import models
from django.urls import reverse
from django.templatetags.static import static
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    
    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('store:category_detail', args=[self.slug])

class Product(models.Model):
    GENDER_CHOICES = [
        ('M', 'Men'),
        ('W', 'Women'),
        ('U', 'Unisex'),
    ]
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='U')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    featured = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
        ]
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.slug])
    
    @property
    def is_on_sale(self):
        return self.sale_price is not None and self.sale_price < self.price
    
    @property
    def current_price(self):
        return self.sale_price if self.is_on_sale else self.price
    
    def get_static_image_path(self):
        """Get a static image path based on gender and product category"""
        # Build the image path based on gender and category
        if self.gender == 'M':
            gender_path = 'men'
        elif self.gender == 'W':
            gender_path = 'women'
        else:
            # For unisex, use men's images as fallback
            gender_path = 'men'
        
        # Map category slug to directory name
        category_mapping = {
            'athletic': 'athletic',
            'casual': 'casual', 
            'formal': 'formal'
        }
        
        category_dir = category_mapping.get(self.category.slug, 'casual')
        
        # Get the list of images in the appropriate directory
        image_dir = f'static/images/{gender_path}/{category_dir}/'
        
        try:
            # Get all image files from the directory
            image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif', '.avif'))]
            
            if image_files:
                # Use product ID to consistently select an image
                selected_image = image_files[self.id % len(image_files)]
                # Check if the image file exists and is valid
                if os.path.exists(os.path.join(image_dir, selected_image)):
                    return static(f'images/{gender_path}/{category_dir}/{selected_image}')
                else:
                    # Try to find a valid image
                    for img_file in image_files:
                        if os.path.exists(os.path.join(image_dir, img_file)):
                            return static(f'images/{gender_path}/{category_dir}/{img_file}')
            else:
                # Fallback to placeholder if no images found
                return static('images/placeholder.svg')
        except (OSError, FileNotFoundError):
            # Fallback to placeholder if directory doesn't exist
            return static('images/placeholder.svg')
        
        # Final fallback
        return static('images/placeholder.svg')
    
    def get_category_images(self, category_slug=None):
        """Get all images from a specific category (both men's and women's)"""
        # Use the provided category or the product's category
        if category_slug is None:
            category_slug = self.category.slug
        
        # Map category slug to directory name
        category_mapping = {
            'athletic': 'athletic',
            'casual': 'casual', 
            'formal': 'formal'
        }
        
        category_dir = category_mapping.get(category_slug, 'casual')
        
        # Get images from both men's and women's directories for this category
        all_images = []
        
        for gender in ['men', 'women']:
            image_dir = f'static/images/{gender}/{category_dir}/'
            
            try:
                # Get all image files from the directory
                image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif', '.avif'))]
                
                # Add images with gender prefix for identification
                for img_file in image_files:
                    all_images.append(static(f'images/{gender}/{category_dir}/{img_file}'))
                    
            except (OSError, FileNotFoundError):
                continue
        
        if all_images:
            return all_images
        else:
            # Fallback to placeholder if no images found
            return [static('images/placeholder.svg')]
    
    def get_all_category_images(self):
        """Get all images from the product's category directory (both men's and women's)"""
        return self.get_category_images(self.category.slug)
    
    def get_random_category_images(self, count=4):
        """Get a random selection of images from the product's category directory"""
        all_images = self.get_all_category_images()
        if len(all_images) <= count:
            return all_images
        else:
            # Use product ID to consistently select images
            import random
            random.seed(self.id)  # Make selection consistent for each product
            return random.sample(all_images, count)
    
    @property
    def static_image_url(self):
        """Property to get static image URL"""
        return self.get_static_image_path()
    
    def get_category_gender_images(self):
        category_mapping = {
            'athletic': 'athletic',
            'casual': 'casual',
            'formal': 'formal'
        }
        category_dir = category_mapping.get(self.category.slug, 'casual')
        gender_path = 'men' if self.gender == 'M' else 'women'
        image_dir = f'static/images/{gender_path}/{category_dir}/'
        images = []
        try:
            for fname in os.listdir(image_dir):
                if fname.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif', '.avif')):
                    images.append(static(f'images/{gender_path}/{category_dir}/{fname}'))
        except (OSError, FileNotFoundError):
            pass
        if not images:
            images = [static('images/placeholder.svg')]
        return images

    @property
    def category_images(self):
        return self.get_category_gender_images()

class ProductSize(models.Model):
    product = models.ForeignKey(Product, related_name='sizes', on_delete=models.CASCADE)
    size = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} - Size {self.size}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    order_number = models.CharField(max_length=20, unique=True)
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    shipping_address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10)
    country = models.CharField(max_length=50, default='India')
    
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=50, default='Credit Card')
    payment_status = models.CharField(max_length=20, default='pending')
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return f"Order {self.order_number}"
    
    def get_absolute_url(self):
        return reverse('store:order_detail', args=[self.order_number])
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            import random
            import string
            # Generate a unique order number
            while True:
                order_num = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
                if not Order.objects.filter(order_number=order_num).exists():
                    self.order_number = order_num
                    break
        super().save(*args, **kwargs)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=10, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.product.name} - {self.quantity}x"
    
    @property
    def subtotal(self):
        return self.price * self.quantity
