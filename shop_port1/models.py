from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.timezone import now


class ProductGroup(models.Model):
    number = models.CharField(("Nummer"), max_length=20, unique=True)
    name = models.CharField(("Bezeichnung"), max_length=40)
    image = models.ImageField(upload_to="productgroup_images/", blank=True, null=True)

    class Meta:
        verbose_name = ("Warengruppe")
        verbose_name_plural = ("Warengruppen")
        ordering = ['number',]

    @property
    def get_sum(self):
        lst_a_group =  ArticleGroup.objects.filter(productgroup=self)
        sum = 0
        for a_group in lst_a_group:
            sum += a_group.get_sum
        return sum

    def __str__(self):
        return f"{self.number} {self.name} ({self.get_sum} €)"

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})

class ArticleGroup(models.Model):
    productgroup = models.ForeignKey(ProductGroup, verbose_name=("Produkt-Gruppe"), on_delete=models.RESTRICT)
    number = models.CharField(("Nummer"), max_length=20)
    name = models.CharField(("Bezeichnung"), max_length=40)



    class Meta:
        verbose_name = "Artikelgruppe"
        verbose_name_plural = "Artikelgruppen"
        ordering = ['productgroup', 'number',]

    @property
    def get_sum(self):
        lst_article =  Article.objects.filter(articlegroup=self)
        sum = 0
        for article in lst_article:
            sum += article.get_sum
        return sum

    def __str__(self):
        return f"({self.productgroup}) {self.number} {self.name} ({self.get_sum} €)"
#        return self.name

    def get_absolute_url(self):
       return reverse("ArticleGrop_detail", kwargs={"pk": self.pk})

class Deliver(models.Model):
    name = models.CharField(("Name"), max_length=50)
    address = models.CharField(("Adresse"), max_length=50, null=True, blank=True)
    description = models.TextField(("Beschreibung"), null=True, blank=True)

    class Meta:
        verbose_name = ("Lieferant")
        verbose_name_plural = ("Lieferanten")

    def __str__(self):
        return self.name

class Article(models.Model):
    articlegroup = models.ForeignKey(ArticleGroup, verbose_name=("Artikelgruppe"), on_delete=models.RESTRICT)
    number = models.CharField(("Nummer"), max_length=10)
    designation = models.CharField(("Bezeichnung"), max_length=100)
    ean = models.CharField(("EAN"), max_length=30)
    inventory = models.IntegerField(("Inventurbestand"))
    inv_date = models.DateTimeField("Datum letzte Inventur", default=now())
    minmum_inventory = models.IntegerField(("Mindestbestand"))
    deliver = models.ForeignKey(Deliver, verbose_name=("Lieferant"), on_delete=models.RESTRICT, null=True, blank=True)
    price = models.DecimalField(("Einkaufs-Preis"), max_digits=5, decimal_places=2)
    comment = models.TextField(("Bemerkung"), null=True, blank=True)
    available_for_sale = models.BooleanField(("Verkaufbar"), default=True)
    image = models.ImageField(upload_to='article_images/', null=True, blank=True, verbose_name="Produktbild")

    class Meta:
        verbose_name = ("Artikel")
        verbose_name_plural = ("Artikel")


    @property
    def get_status(self):
        if self.inventory == 0:
            return "red"
        if self.inventory <= self.minmum_inventory:
            return "yellow"
        else:
            return "green"

    @property
    def get_sum(self):
        return self.price * self.inventory

    def __str__(self):
        agroup_number = self.articlegroup.number
        pgroup_number = self.articlegroup.productgroup.number
        return f"{pgroup_number} {agroup_number} {self.number} - {self.designation} ({self.price} €) Status: {self.get_status} ({self.get_sum} €) - {self.deliver}"

    def get_absolute_url(self):
        return reverse("Article_detail", kwargs={"pk": self.pk})

#Ab hier ist alt: Oberhalb ist von meinem Lehrer.

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)

    def __str__(self):
        return self.name

def default_date():
    return now().date()  # Stellt sicher, dass es ein echtes Datum ist, kein String

class Product(models.Model):  # Warenzugang wurde zu Product umbenannt!
    rewe = models.BooleanField(default=False)
    stonier = models.BooleanField(default=False)
    transaktion = models.IntegerField()
    laufende_nr = models.IntegerField()

    # 🔥 Korrektur für DateField-Felder
    leistungsdatum = models.DateField(null=True, blank=True, default=default_date)
    erstellt_am = models.DateField(null=True, blank=True, default=default_date)
    periode = models.CharField(max_length=10)
    schluessel = models.CharField(max_length=10)
    produkt = models.CharField(max_length=10)
    bezeichnung = models.CharField(max_length=255)

    # 🔥 Standardwerte für problematische Felder hinzugefügt
    buch_kz = models.CharField(max_length=2, default="00")
    bw_k = models.CharField(max_length=2, default="00")

    menge = models.IntegerField()
    l_einheit = models.CharField(max_length=10)
    l_gw = models.IntegerField()
    lageplatz = models.CharField(max_length=5)
    lagerplatz = models.CharField(max_length=10)
    kostenstelle = models.CharField(max_length=10)
    kostenstelle_bezeichnung = models.CharField(max_length=255)
    kostenart = models.CharField(max_length=10)
    erstellt_von = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products", null=True, blank=True)

    # Felder von Product, damit dein Shop funktioniert
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)

    # Alias für name, damit keine Änderungen in den Templates nötig sind
    @property
    def name(self):
        return self.bezeichnung  # So kannst du weiterhin {{ product.name }} verwenden

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id])

    def __str__(self):
        return self.bezeichnung  # Der Name des Produkts

class CartItem(models.Model):
    user = models.ForeignKey(User, verbose_name="Benutzer", on_delete=models.RESTRICT)
    article = models.ForeignKey(Article, verbose_name="Produkt", on_delete=models.RESTRICT, null=True, blank=True)  # <- vorher: product
    quantity = models.PositiveIntegerField("Anzahl", default=1)

    class Meta:
        verbose_name = ("Produkt im Warenkorb")
        verbose_name_plural = ("Produkte im Warenkorb")
        ordering = ['user', 'article', ]

    def __str__(self):
        return f"({self.user}) {self.article} / {self.quantity} Stück {self.get_total_price}€"

    @property
    def get_total_price(self):
        return self.quantity * self.article.price


class Order(models.Model):
    user = models.ForeignKey(User,verbose_name="Benutzer", on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem, verbose_name="Produkt")
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=[
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Banküberweisung'),
        ('bar', 'Barzahlung'),
    ])
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = ("Bestellung")
        verbose_name_plural = ("Bestellungen")

