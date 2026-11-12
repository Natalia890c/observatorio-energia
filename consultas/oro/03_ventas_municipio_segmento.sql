-- Consulta 3. Ventas de energía por municipio y segmento.
select
    municipio_id,
    segmento_id,
    tipo_compra,
    sum(energia_kwh) as energia_total_kwh,
    sum(valor_cop) as valor_total_cop,
    sum(clientes) as clientes_reportados
from fact_ventas_mensual
group by municipio_id, segmento_id, tipo_compra
order by valor_total_cop desc;
