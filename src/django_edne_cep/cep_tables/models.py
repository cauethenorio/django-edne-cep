from django.db import models

from django_edne_cep.table_names import get_table_name


class Localidade(models.Model):
    loc_nu = models.AutoField(primary_key=True)
    ufe_sg = models.CharField(max_length=2)
    loc_no = models.CharField(max_length=72)
    cep = models.CharField(max_length=8, null=True, blank=True)
    loc_in_sit = models.CharField(max_length=1)
    loc_in_tipo_loc = models.CharField(max_length=1)
    loc_nu_sub = models.ForeignKey(
        "self", models.DO_NOTHING, db_column="loc_nu_sub", null=True, blank=True
    )
    loc_no_abrev = models.CharField(max_length=36, null=True, blank=True)
    mun_nu = models.IntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = get_table_name("log_localidade")


class Bairro(models.Model):
    bai_nu = models.AutoField(primary_key=True)
    ufe_sg = models.CharField(max_length=2)
    loc_nu = models.ForeignKey(Localidade, models.DO_NOTHING, db_column="loc_nu")
    bai_no = models.CharField(max_length=72)
    bai_no_abrev = models.CharField(max_length=36, null=True, blank=True)

    class Meta:
        managed = False
        db_table = get_table_name("log_bairro")


class CaixaPostalComunitaria(models.Model):
    cpc_nu = models.AutoField(primary_key=True)
    ufe_sg = models.CharField(max_length=2)
    loc_nu = models.ForeignKey(Localidade, models.DO_NOTHING, db_column="loc_nu")
    cpc_no = models.CharField(max_length=72)
    cpc_endereco = models.CharField(max_length=100)
    cep = models.CharField(max_length=8)

    class Meta:
        managed = False
        db_table = get_table_name("log_cpc")


class Logradouro(models.Model):
    log_nu = models.AutoField(primary_key=True)
    ufe_sg = models.CharField(max_length=2)
    loc_nu = models.ForeignKey(Localidade, models.DO_NOTHING, db_column="loc_nu")
    bai_nu_ini = models.ForeignKey(Bairro, models.DO_NOTHING, db_column="bai_nu_ini")
    bai_nu_fim = models.ForeignKey(
        Bairro,
        models.DO_NOTHING,
        db_column="bai_nu_fim",
        related_name="logradouro_bai_nu_fim_set",
        null=True,
        blank=True,
    )
    log_no = models.CharField(max_length=100)
    log_complemento = models.CharField(max_length=100, null=True, blank=True)
    cep = models.CharField(max_length=8)
    tlo_tx = models.CharField(max_length=36)
    log_sta_tlo = models.CharField(max_length=1, null=True, blank=True)
    log_no_abrev = models.CharField(max_length=36, null=True, blank=True)

    class Meta:
        managed = False
        db_table = get_table_name("log_logradouro")


class GrandeUsuario(models.Model):
    gru_nu = models.AutoField(primary_key=True)
    ufe_sg = models.CharField(max_length=2)
    loc_nu = models.ForeignKey(Localidade, models.DO_NOTHING, db_column="loc_nu")
    bai_nu = models.ForeignKey(Bairro, models.DO_NOTHING, db_column="bai_nu")
    log_nu = models.ForeignKey(
        Logradouro, models.DO_NOTHING, db_column="log_nu", null=True, blank=True
    )
    gru_no = models.CharField(max_length=72)
    gru_endereco = models.CharField(max_length=100)
    cep = models.CharField(max_length=8)
    gru_no_abrev = models.CharField(max_length=36, null=True, blank=True)

    class Meta:
        managed = False
        db_table = get_table_name("log_grande_usuario")


class UnidadeOperacional(models.Model):
    uop_nu = models.AutoField(primary_key=True)
    ufe_sg = models.CharField(max_length=2)
    loc_nu = models.ForeignKey(Localidade, models.DO_NOTHING, db_column="loc_nu")
    bai_nu = models.ForeignKey(Bairro, models.DO_NOTHING, db_column="bai_nu")
    log_nu = models.ForeignKey(
        Logradouro, models.DO_NOTHING, db_column="log_nu", null=True, blank=True
    )
    uop_no = models.CharField(max_length=100)
    uop_endereco = models.CharField(max_length=100)
    cep = models.CharField(max_length=8)
    uop_in_cp = models.CharField(max_length=1, null=True, blank=True)
    uop_no_abrev = models.CharField(max_length=36, null=True, blank=True)

    class Meta:
        managed = False
        db_table = get_table_name("log_unid_oper")
