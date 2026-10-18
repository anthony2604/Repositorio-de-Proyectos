# Anthony Valle Quinde
### Mecatrónica · Robótica · Datos y automatización de operaciones

**Bachiller en Ingeniería Mecatrónica por UTEC | Lima, Perú**

Desarrollo soluciones que conectan equipos, software y datos para reducir trabajo manual y mejorar la visibilidad de las operaciones. Mi experiencia combina automatización industrial, sistemas embebidos y desarrollo de aplicaciones; actualmente mi enfoque está en datos operativos y herramientas de gestión para minería.

Este portafolio reúne proyectos académicos, herramientas de automatización y resúmenes de experiencia profesional. Cada caso distingue su alcance y la evidencia disponible.

[LinkedIn](https://www.linkedin.com/in/anthony-valle-utec/) · [Correo](mailto:anthonyvallequinde@gmail.com)

---

## Proyectos destacados

Ordenados por su relación con integración de sistemas, información operativa y automatización.

### 1. Datos y software para operaciones mineras
**Experiencia profesional · Desarrollo en curso · Resumen público**

**Problema:** procesos manuales y registros dispersos dificultan consolidar información para el seguimiento operativo y las decisiones de gestión.

**Contribución:** desarrollo frontend y backend, y trabajo con **SQL Server**, en un ERP orientado a operaciones mineras. El trabajo se enfoca en centralizar registros y automatizar flujos; las comparativas automáticas y el seguimiento cercano al tiempo real son objetivos de evolución del sistema.

**Valor:** conectar la captura de información operativa con las necesidades de supervisión y negocio.

**Alcance público:** descripción funcional de mi participación. No se publican código del empleador, nombres de clientes, datos operativos, esquemas de bases de datos, credenciales ni detalles de infraestructura. No se atribuyen ahorros, disponibilidad o mejoras de productividad sin medición.

### 2. Brazo robótico con control distribuido por CAN y visión
**Tesis de Mecatrónica · Proyecto académico · Resumen técnico público**

**Problema:** integrar percepción visual, control de articulaciones y accionamiento en un manipulador con electrónica distribuida.

**Desarrollo:**

- Arquitectura con **cuatro nodos ESP32/ESP32-C3**, comunicados por **CAN** mediante transceptores SN65HVD230.
- Accionamiento de motores paso a paso con **DM556 y TMC2209**, realimentación angular mediante encoders y control de una pinza.
- Identificación de planta y trabajo con controladores **PID y LQI** en **MATLAB/Simulink**.
- Trabajo de visión con **RT-DETR y SAM 2**, orientado a detección, segmentación y selección de agarre.

**Valor técnico:** integración de comunicación, control, electrónica y percepción en un mismo proyecto. La arquitectura CAN se adoptó ante problemas de comunicación con sensores I²C sobre cableado largo y ruido eléctrico.

**Evidencia disponible:** este resumen describe el proyecto; el código, la memoria y los ensayos de la tesis no están incorporados a este repositorio. No se presentan objetivos de frecuencia de control, precisión o latencia como resultados medidos.

### 3. Ensamblaje inteligente e integración OT/IT
**Proyecto académico · Documentación pública**

**[Ver proyecto](./Industria40_Smart_Assembly_System/README.md)**

Integración de **Siemens S7-1500, Factory I/O, Node-RED, InfluxDB y Grafana** para control secuencial, almacenamiento de datos y visualización de indicadores de producción. Incluye interacción mediante Telegram.

**Valor:** demostrar el recorrido desde señales y estados de una planta simulada hasta históricos e indicadores para supervisión. El alcance corresponde a un entorno académico con simulación en Factory I/O.

### 4. Automatización documental y de procesos
**Herramientas de software · Código o documentación según el caso**

| Proyecto | Contribución y utilidad | Tecnologías |
| :--- | :--- | :--- |
| **[Gestión masiva de firmas digitales](./AUTOMATIZACION%20DE%20FIRMAS%20DIGITALES%20-%20BV/README.md)** | Carga, anulación y descarga por lotes mediante API, con registro de metadatos para seguimiento. | Python, API REST, Tkinter, Pandas, Google Sheets |
| **[Generador de documentos de vacaciones](./GENERADOR%20DE%20VACACIONES%20-%20BV/readme.md)** | Conversión de registros Excel en documentos PDF con plantillas e interfaz de escritorio. | Python, Pandas, Jinja2, WeasyPrint, Tkinter |
| **[Alertas de vencimiento de contratos](./Sistema_Alertas_Contratos_PowerAutomate/README.MD)** | Revisión programada cada tres días y alertas para contratos vigentes con siete días o menos hasta su vencimiento. | Power Automate, Excel Online |

**Impacto que puede describirse:** procesamiento por lotes, reutilización de plantillas y revisiones programadas sustituyen tareas repetitivas. No se publican porcentajes de ahorro ni garantías de eliminación de errores sin una comparación reproducible.

### 5. Instrumentación industrial e ingeniería de hardware
**Proyectos con documentación pública**

| Proyecto | Alcance |
| :--- | :--- |
| **[Automatización del módulo de bombeo HM-362](./Proyecto%20Instrumentaci%C3%B3n%20Industrial%20-%20UTEC/README.md)** | Ingeniería de detalle académica: selección de instrumentación, P&ID, dimensionamiento de válvulas, estrategia de control e interlocks con arquitectura Siemens S7-1500, PROFINET y HART. |
| **[Energizador solar para cercos ganaderos](./Solar_HighVoltage_Cattle_Energizer_Project/README.md)** | Electrónica de potencia, diseño de PCB y carcasa con KiCad y Fusion 360. Documentación de producto; archivos de diseño restringidos por propiedad intelectual. |

Las especificaciones de tensión, autonomía, protección IP y conformidad normativa requieren condiciones de ensayo y evidencia específica; este portafolio no las presenta como prestaciones certificadas.

---

## Evidencia y métricas

- **Robótica:** cuatro nodos en la arquitectura descrita; sin cifras públicas de precisión, latencia o tasa de éxito.
- **Automatización documental:** alcance funcional documentado; sin benchmark reproducible que sustente porcentajes de reducción de tiempo.
- **Alertas de contratos:** ejecución periódica cada tres días; sin afirmar vigilancia continua ni detección garantizada.
- **Operaciones mineras:** contribución y objetivos descritos de forma general; resultados empresariales y activos internos reservados.

Las métricas de rendimiento deben indicar línea base, muestra, condiciones y método de medición. Las descripciones anteriores delimitan las afirmaciones de este README; la documentación histórica de cada proyecto puede contener estimaciones que requieren validación.

---

## Stack técnico

| Área | Herramientas y tecnologías utilizadas |
| :--- | :--- |
| **Datos y software** | Python, SQL Server, Pandas, NumPy, API REST, aplicaciones frontend/backend |
| **Automatización de procesos** | Power Automate, Node-RED, Excel, Jinja2, WeasyPrint, Tkinter |
| **Control e industria** | MATLAB/Simulink, PID, LQI, Siemens S7-1200/1500, TIA Portal, Factory I/O |
| **Robótica y embebidos** | ESP32, ESP32-C3, CAN, SN65HVD230, I²C, encoders, motores paso a paso |
| **Visión e indicadores** | RT-DETR, SAM 2, TensorRT, Grafana, InfluxDB |
| **Diseño y prototipado** | KiCad, Fusion 360, impresión 3D |

## Formación y orientación profesional

Bachiller en Ingeniería Mecatrónica por **UTEC**. Experiencia de investigación en **University of Alberta** mediante el programa **ELAP**, trabajando con seguimiento de movimiento mediante IMUs y entornos de realidad virtual.

Me interesa desarrollar sistemas que conecten automatización de campo, datos confiables y decisiones de negocio, especialmente en operaciones industriales y mineras.

## Contacto

- **LinkedIn:** [Anthony Valle Quinde](https://www.linkedin.com/in/anthony-valle-utec/)
- **Correo:** [anthonyvallequinde@gmail.com](mailto:anthonyvallequinde@gmail.com)

*Actualizado: octubre de 2026.*
