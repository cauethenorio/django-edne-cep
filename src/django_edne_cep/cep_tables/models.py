from django.db import models

from django_edne_cep.table_names import get_table_name


class FaixaUf(models.Model):
    ufe_sg = models.CharField(max_length=2, primary_key=True)
    ufe_cep_ini = models.CharField(max_length=8)
    ufe_cep_fim = models.CharField(max_length=8)

    class Meta:
        managed = False
        db_table = get_table_name("log_faixa_uf")
        unique_together = [("ufe_sg", "ufe_cep_ini")]


class Localidade(models.Model):
    loc_nu = models.IntegerField(primary_key=True)
    ufe_sg = models.CharField(max_length=2)
    loc_no = models.CharField(max_length=72)
    cep = models.CharField(max_length=8, null=True, blank=True)
    loc_in_sit = models.CharField(max_length=1)
    loc_in_tipo_loc = models.CharField(max_length=1)
    loc_nu_sub = models.IntegerField(null=True, blank=True)
    loc_no_abrev = models.CharField(max_length=36, null=True, blank=True)
    mun_nu = models.IntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = get_table_name("log_localidade")


class VarLoc(models.Model):
    loc_nu = models.IntegerField(primary_key=True)
    val_nu = models.IntegerField()
    val_tx = models.CharField(max_length=72)

    class Meta:
        managed = False
        db_table = get_table_name("log_var_loc")
        unique_together = [("loc_nu", "val_nu")]


class FaixaLocalidade(models.Model):
    loc_nu = models.IntegerField(primary_key=True)
    loc_cep_ini = models.CharField(max_length=8)
    loc_cep_fim = models.CharField(max_length=8, null=True, blank=True)
    loc_tipo_faixa = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = get_table_name("log_faixa_localidade")
        unique_together = [("loc_nu", "loc_cep_ini", "loc_tipo_faixa")]


class Bairro(models.Model):
    bai_nu = models.IntegerField(primary_key=True)
    ufe_sg = models.CharField(max_length=2)
    loc_nu = models.IntegerField()
    bai_no = models.CharField(max_length=72)
    bai_no_abrev = models.CharField(max_length=36, null=True, blank=True)

    class Meta:
        managed = False
        db_table = get_table_name("log_bairro")


class VarBai(models.Model):
    bai_nu = models.IntegerField(primary_key=True)
    vdb_nu = models.IntegerField()
    vdb_tx = models.CharField(max_length=72)

    class Meta:
        managed = False
        db_table = get_table_name("log_var_bai")
        unique_together = [("bai_nu", "vdb_nu")]


class FaixaBairro(models.Model):
    bai_nu = models.IntegerField(primary_key=True)
    fcb_cep_ini = models.CharField(max_length=8)
    fcb_cep_fim = models.CharField(max_length=8)

    class Meta:
        managed = False
        db_table = get_table_name("log_faixa_bairro")
        unique_together = [("bai_nu", "fcb_cep_ini")]


class CaixaPostalComunitaria(models.Model):
    cpc_nu = models.IntegerField(primary_key=True)
    ufe_sg = models.CharField(max_length=2)
    loc_nu = models.IntegerField()
    cpc_no = models.CharField(max_length=72)
    cpc_endereco = models.CharField(max_length=100)
    cep = models.CharField(max_length=8)

    class Meta:
        managed = False
        db_table = get_table_name("log_cpc")


class FaixaCpc(models.Model):
    cpc_nu = models.IntegerField(primary_key=True)
    cpc_inicial = models.CharField(max_length=6)
    cpc_final = models.CharField(max_length=6)

    class Meta:
        managed = False
        db_table = get_table_name("log_faixa_cpc")
        unique_together = [("cpc_nu", "cpc_inicial", "cpc_final")]


class Logradouro(models.Model):
    log_nu = models.IntegerField(primary_key=True)
    ufe_sg = models.CharField(max_length=2)
    loc_nu = models.IntegerField()
    bai_nu_ini = models.IntegerField()
    bai_nu_fim = models.IntegerField(null=True, blank=True)
    log_no = models.CharField(max_length=100)
    log_complemento = models.CharField(max_length=100, null=True, blank=True)
    cep = models.CharField(max_length=8)
    tlo_tx = models.CharField(max_length=36)
    log_sta_tlo = models.CharField(max_length=1, null=True, blank=True)
    log_no_abrev = models.CharField(max_length=36, null=True, blank=True)

    class Meta:
        managed = False
        db_table = get_table_name("log_logradouro")


class VarLog(models.Model):
    log_nu = models.IntegerField(primary_key=True)
    vlo_nu = models.IntegerField()
    tlo_tx = models.CharField(max_length=36, null=True, blank=True)
    vlo_tx = models.CharField(max_length=150, null=True, blank=True)

    class Meta:
        managed = False
        db_table = get_table_name("log_var_log")
        unique_together = [("log_nu", "vlo_nu")]


class NumSec(models.Model):
    log_nu = models.IntegerField(primary_key=True)
    sec_nu_ini = models.CharField(max_length=10, null=True, blank=True)
    sec_nu_fim = models.CharField(max_length=10, null=True, blank=True)
    sec_in_lado = models.CharField(max_length=1, null=True, blank=True)

    class Meta:
        managed = False
        db_table = get_table_name("log_num_sec")


class GrandeUsuario(models.Model):
    gru_nu = models.IntegerField(primary_key=True)
    ufe_sg = models.CharField(max_length=2)
    loc_nu = models.IntegerField()
    bai_nu = models.IntegerField()
    log_nu = models.IntegerField(null=True, blank=True)
    gru_no = models.CharField(max_length=72)
    gru_endereco = models.CharField(max_length=100)
    cep = models.CharField(max_length=8)
    gru_no_abrev = models.CharField(max_length=36, null=True, blank=True)

    class Meta:
        managed = False
        db_table = get_table_name("log_grande_usuario")


class UnidadeOperacional(models.Model):
    uop_nu = models.IntegerField(primary_key=True)
    ufe_sg = models.CharField(max_length=2)
    loc_nu = models.IntegerField()
    bai_nu = models.IntegerField()
    log_nu = models.IntegerField(null=True, blank=True)
    uop_no = models.CharField(max_length=100)
    uop_endereco = models.CharField(max_length=100)
    cep = models.CharField(max_length=8)
    uop_in_cp = models.CharField(max_length=1, null=True, blank=True)
    uop_no_abrev = models.CharField(max_length=36, null=True, blank=True)

    class Meta:
        managed = False
        db_table = get_table_name("log_unid_oper")


class FaixaUop(models.Model):
    upo_nu = models.IntegerField(primary_key=True)
    fnc_inicial = models.IntegerField()
    fnc_final = models.IntegerField()

    class Meta:
        managed = False
        db_table = get_table_name("log_faixa_uop")
        unique_together = [("upo_nu", "fnc_inicial")]


class Pais(models.Model):
    pai_sg = models.CharField(max_length=2, primary_key=True)
    pai_sg_alternativa = models.CharField(max_length=3, null=True, blank=True)
    pai_no_portugues = models.CharField(max_length=72, null=True, blank=True)
    pai_no_ingles = models.CharField(max_length=72, null=True, blank=True)
    pai_no_frances = models.CharField(max_length=72, null=True, blank=True)
    pai_abreviatura = models.CharField(max_length=36, null=True, blank=True)

    class Meta:
        managed = False
        db_table = get_table_name("ect_pais")
