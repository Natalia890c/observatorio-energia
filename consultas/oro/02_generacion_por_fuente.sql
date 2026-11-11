-- Consulta 2. Generación por fuente de energía.
select
    coalesce(fuente_energia, 'Sin clasificar') as fuente_energia,
    round(sum(generacion), 2) as generacion_total,
    count(*) as registros
from fact_generacion_recurso
group by 1
order by generacion_total desc;
