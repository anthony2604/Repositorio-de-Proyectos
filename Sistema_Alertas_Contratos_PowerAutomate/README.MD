# ⏳ Sistema Automatizado de Seguimiento de Contratos (RPA)
### Power Automate | Excel Online | Office 365

![Status](https://img.shields.io/badge/Status-Production-success)
![Tool](https://img.shields.io/badge/Platform-Power_Automate-blue)

## 📖 Descripción del Problema
En la gestión administrativa, el seguimiento manual de cientos de contratos vigentes conlleva un alto riesgo de error humano. Olvidar una fecha de vencimiento puede resultar en:
* Pérdida de personal clave por falta de renovación a tiempo.
* Costos operativos adicionales por trámites de urgencia.
* Discontinuidad en el servicio a clientes.

## 🤖 Solución Implementada
Desarrollé un flujo automatizado en **Microsoft Power Automate** que actúa como un auditor virtual 24/7. El sistema monitorea una base de datos centralizada en Excel y notifica proactivamente a los gestores sobre acciones requeridas.

### ⚙️ Lógica del Flujo (Workflow)
1.  **Disparador (Trigger):** El flujo se ejecuta automáticamente cada **3 días** (Scheduled Cloud Flow).
2.  **Lectura de Datos:** Conecta con Excel Online para leer la tabla maestra de contratos.
3.  **Evaluación Lógica:**
    * Itera sobre cada fila del registro.
    * Calcula la diferencia entre la `Fecha_Vencimiento` y la `Fecha_Actual`.
    * **Condición:** `Si (Días_Restantes <= 7) Y (Estado == "Vigente")`.
4.  **Acción (Alertas):**
    * Si la condición se cumple, envía un **correo electrónico de alta prioridad** al gestor responsable.
    * El correo incluye detalles específicos: Nombre del contratista, fecha exacta de vencimiento y el monto.

## 🛠️ Tecnologías
* **Power Automate:** Orquestación del flujo y lógica de negocio.
* **Expresiones WDL:** Uso de funciones como `formatDateTime`, `sub` (resta) y `ticks` para comparaciones de fechas.
* **Excel Online (Business):** Base de datos estructurada.

## 📉 Impacto
* **100% de eliminación** de vencimientos no detectados desde su implementación.
* Reducción de la carga mental del equipo administrativo (ya no necesitan revisar el Excel manualmente todos los días).
* Optimización del proceso de adendas y renovaciones.

---
**Nota:** Por motivos de privacidad y seguridad de la información, este repositorio contiene capturas de pantalla de la lógica y datos de ejemplo (dummy data), no la información real de la empresa.