"""Las 7 dimensiones de investigación con mega-prompt dinámico v1."""

def generar_mega_prompt(client, objetivo: str) -> str:
    """Genera un mega-prompt optimizado a partir del objetivo del usuario."""
    prompt_meta = (
        f'Eres el mejor ingeniero de prompts del mundo especializado en investigación profunda con Gemini.\n\n'
        f'OBJETIVO DEL USUARIO: "{objetivo}"\n\n'
        'Genera UN SOLO MEGA-PROMPT completo, autónomo y ultra-optimizado que servirá de base común para investigar este objetivo en 7 dimensiones exhaustivas.\n'
        'El mega-prompt debe comenzar exactamente con esta frase:\n'
        f'"Eres el mayor experto del mundo en este tema. Investiga de forma EXTREMADAMENTE detallada, objetiva y actualizada el siguiente objetivo: {objetivo}"\n\n'
        'Incluye estas instrucciones globales obligatorias en el mega-prompt:\n'
        '- Profundidad máxima con datos reales y actuales (2024-2026)\n'
        '- Uso obligatorio de formato Markdown, tablas cuando sea útil y listas numeradas\n'
        '- Citar fuentes siempre que sea posible\n'
        '- Ser brutalmente honesto, evitar optimismo infundado y destacar riesgos reales\n'
        '- Enfocarse en información accionable y concreta\n\n'
        'Devuelve **SOLO** el texto puro del mega-prompt. Sin explicaciones, sin markdown extra, sin introducciones.'
    )
    
    resultado = client.generar(prompt_meta, con_search=False)
    return resultado["texto"].strip()

def crear_dimensiones(mega_base: str) -> list[dict]:
    """Crea las 7 dimensiones usando el mega-prompt generado como base."""
    base = mega_base + "\n\nSé EXTREMADAMENTE detallado. Cita datos reales y actuales. Usa formato Markdown con secciones claras y tablas cuando corresponda.\n\n"
    
    return [
        {
            "num": 1,
            "emoji": "📖",
            "nombre": "LENGUAJE Y TERMINOLOGÍA",
            "prompt": "Eres el mayor experto terminólogo del mundo.\n\n" + base + 
                      "Investiga EXHAUSTIVAMENTE todo el lenguaje y vocabulario:\n\n"
                      "1. **GLOSARIO COMPLETO** (mín. 30 términos): Término → definición técnica → definición simple → ejemplo\n"
                      "2. **JERGA PROFESIONAL**: Palabras que usan los insiders\n"
                      "3. **ACRÓNIMOS Y SIGLAS**: Todos los relevantes\n"
                      "4. **EVOLUCIÓN TERMINOLÓGICA**: Cómo cambiaron en 5-10 años\n"
                      "5. **DIFERENCIAS REGIONALES**: Términos que cambian según país\n"
                      "6. **TÉRMINOS EN TENDENCIA 2024-2026**: Neologismos emergentes\n"
                      "7. **KEYWORDS DE BÚSQUEDA**: Palabras exactas para Google\n"
                      "8. **FRAMEWORKS Y METODOLOGÍAS**: Marcos de trabajo reconocidos\n"
                      "9. **PERSONAS CLAVE**: Referentes, empresas líderes\n"
                      "10. **ERRORES COMUNES**: Términos que se confunden frecuentemente"
        },
        {
            "num": 2,
            "emoji": "💰",
            "nombre": "ECONOMÍA Y MERCADO",
            "prompt": "Eres el mayor analista económico y de mercados del mundo.\n\n" + base + 
                      "Investiga EXHAUSTIVAMENTE la dimensión económica:\n\n"
                      "1. **TAMAÑO DEL MERCADO**: Valor global y por regiones, proyecciones, CAGR\n"
                      "2. **MODELOS DE NEGOCIO**: Monetización, pricing\n"
                      "3. **INVERSIÓN**: VC, PE, gobierno, rondas recientes, ROI típico\n"
                      "4. **COSTOS**: Estructura, costos de entrada, economías de escala\n"
                      "5. **INGRESOS**: Fuentes, márgenes, revenue streams\n"
                      "6. **IMPACTO MACRO**: PIB, empleos, cadenas de suministro\n"
                      "7. **GEOGRAFÍA ECONÓMICA**: Mercados rentables, emergentes, barreras\n\n"
                      "Incluye CIFRAS REALES de 2024-2026. Usa tablas."
        },
        {
            "num": 3,
            "emoji": "📊",
            "nombre": "DATOS, NÚMEROS Y ESTADÍSTICAS",
            "prompt": "Eres el mayor analista de datos y estadístico del mundo.\n\n" + base + 
                      "Investiga EXHAUSTIVAMENTE todos los datos:\n\n"
                      "1. **KPIs FUNDAMENTALES**: Métricas, benchmarks (bueno/promedio/excelente)\n"
                      "2. **ESTADÍSTICAS DE ADOPCIÓN**: Tasas, curva de crecimiento\n"
                      "3. **DATOS DE RENDIMIENTO**: Éxito/fracaso, eficiencia\n"
                      "4. **DATOS DEMOGRÁFICOS**: Quién usa/compra, segmentación\n"
                      "5. **RANKINGS**: Top 10 por cuota, satisfacción, calidad\n"
                      "6. **DATOS DE TENDENCIA**: Google Trends, volúmenes de búsqueda\n"
                      "7. **ESTUDIOS**: Gartner, McKinsey, papers académicos\n\n"
                      "TODO con números concretos. Tablas. Fuentes."
        },
        {
            "num": 4,
            "emoji": "🏭",
            "nombre": "SECTOR, INDUSTRIA Y COMPETENCIA",
            "prompt": "Eres el mayor analista sectorial del mundo.\n\n" + base + 
                      "Investiga EXHAUSTIVAMENTE el panorama competitivo:\n\n"
                      "1. **MAPA DEL ECOSISTEMA**: Actores, cadena de valor\n"
                      "2. **TOP 10 COMPETIDORES**: Nombre, país, propuesta, fortalezas, debilidades\n"
                      "3. **ANÁLISIS PORTER**: 5 fuerzas, barreras de entrada\n"
                      "4. **SEGMENTACIÓN**: Subsectores, nichos, verticales\n"
                      "5. **REGULACIÓN**: Leyes clave, certificaciones, compliance\n"
                      "6. **CADENA DE SUMINISTRO**: Proveedores, dependencias\n"
                      "7. **MADUREZ**: Fase del ciclo de vida, predicción\n"
                      "8. **MOVIMIENTOS RECIENTES**: M&A, alianzas 2023-2026\n\n"
                      "Sé específico con nombres, fechas y datos."
        },
        {
            "num": 5,
            "emoji": "🎯",
            "nombre": "ESTRATEGIAS Y CONSEJOS DE EXPERTOS",
            "prompt": "Eres el mayor estratega y consultor del mundo.\n\n" + base + 
                      "Investiga EXHAUSTIVAMENTE las mejores estrategias:\n\n"
                      "1. **ROADMAP PARA SER #1**: Plan paso a paso, timeline\n"
                      "2. **MEJORES PRÁCTICAS**: Top 20, casos de éxito\n"
                      "3. **DIFERENCIACIÓN**: Propuestas únicas, blue ocean\n"
                      "4. **GROWTH**: Canales de adquisición, retención\n"
                      "5. **TECNOLOGÍA**: Stack recomendado, herramientas\n"
                      "6. **EQUIPO**: Perfiles clave, dónde encontrar talento\n"
                      "7. **CONSEJOS INSIDER**: Secretos, errores al empezar\n"
                      "8. **FRAMEWORK DE DECISIÓN**: Priorización, cuándo pivotar\n\n"
                      "Ejemplos reales y frameworks accionables."
        },
        {
            "num": 6,
            "emoji": "⚠️",
            "nombre": "RIESGOS, AMENAZAS Y ERRORES",
            "prompt": "Eres el mayor analista de riesgos del mundo.\n\n" + base + 
                      "Investiga EXHAUSTIVAMENTE todos los riesgos:\n\n"
                      "1. **MAPA DE RIESGOS**: Estratégicos, operativos, financieros, tecnológicos\n"
                      "2. **FRACASOS DOCUMENTADOS**: 10 mayores, lecciones\n"
                      "3. **ERRORES DE PRINCIPIANTE**: 20 errores, sesgos, trampas\n"
                      "4. **AMENAZAS EXTERNAS**: Disrupciones, cambios regulatorios\n"
                      "5. **RIESGOS LEGALES**: Demandas, IP, compliance\n"
                      "6. **SEÑALES DE ALERTA**: Red flags, early warnings\n"
                      "7. **PLAN DE MITIGACIÓN**: Plan B-C-D, seguros\n"
                      "8. **BLACK SWANS**: Eventos devastadores, preparación\n\n"
                      "Sé BRUTALMENTE honesto. Datos reales de fracasos."
        },
        {
            "num": 7,
            "emoji": "🚀",
            "nombre": "OPORTUNIDADES, BENEFICIOS Y FUTURO",
            "prompt": "Eres el mayor futurista del mundo.\n\n" + base + 
                      "Investiga EXHAUSTIVAMENTE oportunidades y futuro:\n\n"
                      "1. **OPORTUNIDADES INMEDIATAS** (0-6 meses): Low-hanging fruit\n"
                      "2. **MEDIO PLAZO** (6-24 meses): Tendencias madurando\n"
                      "3. **LARGO PLAZO** (2-10 años): Megatendencias\n"
                      "4. **BENEFICIOS COMPROBADOS**: ROI documentado\n"
                      "5. **NICHOS INEXPLORADOS**: Submarkets, combinaciones\n"
                      "6. **TECNOLOGÍAS HABILITADORAS**: IA, blockchain, IoT\n"
                      "7. **PREDICCIONES**: Gartner, McKinsey, escenarios\n"
                      "8. **FIRST-MOVER ADVANTAGES**: Ventanas que se cierran\n"
                      "9. **SINERGIAS**: Partners, co-creación\n"
                      "10. **IMPACTO TRANSFORMADOR**: Mejor escenario posible\n\n"
                      "Visionario pero basado en datos."
        },
    ]
