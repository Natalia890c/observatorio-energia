# Bitácora individual de trabajo

## 1. Información general
- **Proyecto**: Observatorio Energía y Clima.
- **Actividad**: EA1 — Extracción de datos de fuentes reales con Python.
- **Integrante**: Natalia Castro Ospino.
- **Rol principal**: Líder técnico / Data Engineer.
- **Rama de trabajo**: `feature/xm-ampliado`.
- **Periodo registrado**: 21 al 27 de octubre de 2026.

## 2. Objetivo

En este proyecto, mi enfoque ha sido potenciar la capacidad de extracción de información de XM, centralizando la configuración de sus métricas y documentando los componentes que hemos desarrollado. Estas acciones son clave para tener acceso a los datos del sistema eléctrico colombiano, que luego se utilizarán en análisis relacionados con la energía y el clima.

Además, he estado involucrada en la documentación del repositorio y en el proceso de integración de cambios a través de Git y GitHub, asegurándome de que se mantenga la trazabilidad de todas las contribuciones realizadas.

## 3. Actividades desarrolladas

### 3.1. Preparación de la estructura inicial
Fecha: 21 de octubre de 2026.
Evidencia: f7f0ebc — chore: código base de la clase.

Se registró la creación de la base del proyecto, que sirvió como fundamento para el desarrollo de los componentes de extracción y documentación.

### 3.2. Ampliación de las extracciones de XM
Fecha: 22 de octubre de 2026.
Evidencia: 240808f — feat(xm): ampliar métricas y agregar catálogo de recursos.

Se expandieron las métricas configuradas para consultar información de XM y se añadió la configuración del catálogo de recursos como una extracción independiente.

Las métricas históricas que hemos considerado son las siguientes:
- Precio de la bolsa nacional.
- Demanda real.
- Volumen útil diario de embalses.
- Generación por recurso.
- Aportes de energía.
El rango establecido para estas métricas históricas abarca desde el 1 de enero de 2024 hasta el 30 de septiembre de 2026. Además, el catálogo complementa estas series con información sobre los recursos registrados en XM.

Resultado documentado: la configuración incluye cinco métricas históricas y una extracción adicional del catálogo de recursos. Es importante verificar por separado la ejecución integral y la actualización efectiva de todos los archivos.

### 3.3. Documentación del proyecto
Fecha: 23 de octubre de 2026.

He estado involucrado en la actualización y organización del README, realizando los siguientes cambios:
- 07b95d3: actualización del README y documentación de las extracciones de XM.
- 0034b7e: corrección de espacios y formato del README.
- 9e474c0: ajuste del formato de la tabla de integrantes.
Estas modificaciones han permitido documentar el propósito del proyecto, describir las extracciones de XM y mejorar la presentación de la información del equipo.

### 3.4. Integración de los cambios
Fecha: 24 de octubre de 2026.
Evidencia: e854688 — integración del PR #1.

Los cambios realizados en feature/xm-ampliado se integraron en el repositorio a través del primer pull request. Oscar Márquez fue quien registró el merge.

Este commit se presenta como evidencia del proceso colaborativo, no como una contribución de autoría individual.

## 4. Decisiones técnicas y aprendizajes
Durante el desarrollo, se utilizó una configuración centralizada para definir las métricas de XM y el periodo histórico de consulta. Esta organización facilita la identificación de las fuentes configuradas y mantiene los parámetros de extracción en un punto común.

Además, se incorporó el catálogo de recursos como un componente separado de las métricas históricas, lo que permite diferenciar la información descriptiva de los recursos de las series de datos energéticos.

El uso de ramas y pull requests ha sido clave para organizar los cambios y mantener un historial claro y verificable de todas las modificaciones realizadas.

## 5. Evidencias de trabajo individual
Fecha Evidencia de Git Contribución registrada
21/10/2026 f7f0ebc Preparación de la base del proyecto.
22/10/2026 240808f Ampliación de métricas XM y configuración del catálogo de recursos.
23/10/2026 07b95d3 Actualización de la documentación técnica.
23/10/2026 0034b7e Corrección del formato del README.
23/10/2026 9e474c0 Ajuste de la tabla de integrantes.

Los commits anteriores están registrados a mi nombre. El merge del 24 de octubre se guarda como evidencia de la integración del equipo, diferenciándose de mis commits individuales.

## 6. Verificaciones pendientes
Para cerrar esta actividad, necesito revisar o completar, junto con el equipo, los siguientes puntos:
1. Ejecutar el pipeline completo y verificar el resultado de cada extractor.
2. Confirmar la generación de archivos Parquet en la capa de bronce y la existencia de sus metadatos de linaje.
3. Comparar los rangos temporales obtenidos con los requeridos para cada fuente.
4. Ejecutar las pruebas automatizadas y registrar sus resultados.
5. Revisar la documentación, los archivos de muestra y la integración de los cambios pendientes.
6. Preparar el video individual de demostración y completar la información solicitada para la entrega.
Estos puntos permanecerán como pendientes hasta que tengamos evidencias concretas de su cumplimiento.

## 7. Conclusión
Mi contribución se ha enfocado en ampliar la configuración de las extracciones de XM, incorporar el catálogo de recursos y documentar la evolución del proyecto. Los commits registrados permiten identificar estas actividades y vincularlas con cambios específicos en el repositorio.

El siguiente paso es validar la ejecución completa del pipeline y consolidar las evidencias técnicas y académicas necesarias para la entrega final.