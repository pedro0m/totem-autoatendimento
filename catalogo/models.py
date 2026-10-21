import uuid
from django.db import models

# Create your models here.

class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT
    )

    def __str__(self):
        return self.nome

class Pedido(models.Model):

    class Status(models.TextChoices):
        AGUARDANDO_PAGAMENTO = "AGUARDANDO_PAGAMENTO", "Aguardando pagamento"
        RECEBIDO = "RECEBIDO", "Recebido"
        PREPARANDO = "PREPARANDO", "Em preparação"
        PRONTO = "PRONTO", "Pronto para retirada"
        ENTREGUE = "ENTREGUE", "Entregue"
        CANCELADO = "CANCELADO", "Cancelado"

    token = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )

    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.AGUARDANDO_PAGAMENTO
    )

    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido {self.token}"


class ItemPedido(models.Model):

    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name="itens"
    )

    produto = models.ForeignKey(
        Produto,
        on_delete=models.PROTECT
    )

    quantidade = models.PositiveIntegerField()

    preco_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome}"


class Pagamento(models.Model):

    class Metodo(models.TextChoices):
        CAIXA = "CAIXA", "Pagamento no caixa"
        ONLINE = "ONLINE", "Pagamento online"

    class Status(models.TextChoices):
        PENDENTE = "PENDENTE", "Pendente"
        APROVADO = "APROVADO", "Aprovado"
        RECUSADO = "RECUSADO", "Recusado"
        CANCELADO = "CANCELADO", "Cancelado"

    pedido = models.OneToOneField(
        Pedido,
        on_delete=models.PROTECT,
        related_name="pagamento"
    )

    metodo = models.CharField(
        max_length=10,
        choices=Metodo.choices
    )

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDENTE
    )

    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pagamento do pedido {self.pedido.token}"