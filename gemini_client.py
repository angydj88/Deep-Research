"""Cliente de Gemini con reintentos y fallback."""

import time
import google.generativeai as genai
from config import Config


class GeminiClient:
    """Wrapper robusto para la API de Gemini."""

    def __init__(self):
        genai.configure(api_key=Config.API_KEY)
        self.model = genai.GenerativeModel(Config.MODEL)

    def generar(self, prompt: str, con_search: bool = True) -> dict:
        """
        Genera contenido con estrategia de fallback.
        Retorna: {"texto": str, "fuentes": list, "metodo": str}
        """

        estrategias = []

        if con_search:
            estrategias.append(
                ("Google Search", {"google_search": {}})
            )

        # Siempre incluir modelo base como fallback
        estrategias.append(("Modelo base", None))

        for nombre_estrategia, tool in estrategias:
            try:
                resultado = self._llamar_con_reintentos(
                    prompt, tool, nombre_estrategia
                )
                if resultado:
                    return resultado
            except Exception as e:
                print(f"   ⚠️ {nombre_estrategia} falló: {e}")
                time.sleep(1)

        raise RuntimeError("Todas las estrategias fallaron")

    def _llamar_con_reintentos(
        self, prompt: str, tool: dict | None, nombre: str
    ) -> dict | None:
        """Llama a la API con backoff exponencial."""

        generation_config = genai.types.GenerationConfig(
            temperature=Config.TEMPERATURE,
            max_output_tokens=Config.MAX_TOKENS,
        )

        tools = [tool] if tool else None

        for intento in range(1, Config.MAX_RETRIES + 1):
            try:
                response = self.model.generate_content(
                    prompt,
                    generation_config=generation_config,
                    tools=tools,
                )

                if not response.candidates:
                    raise ValueError("Respuesta sin candidatos")

                texto = response.text

                # Extraer fuentes si existen
                fuentes = self._extraer_fuentes(response)

                return {
                    "texto": texto,
                    "fuentes": fuentes,
                    "metodo": nombre,
                }

            except Exception as e:
                print(f"   ⚠️ Intento {intento}/{Config.MAX_RETRIES}: {e}")

                if intento < Config.MAX_RETRIES:
                    espera = Config.DELAY_BETWEEN_CALLS * (2 ** (intento - 1))
                    print(f"   ⏳ Esperando {espera}s...")
                    time.sleep(espera)

        return None

    def _extraer_fuentes(self, response) -> list[str]:
        """Extrae URLs de fuentes del grounding metadata."""
        fuentes = []
        try:
            candidate = response.candidates[0]
            metadata = candidate.grounding_metadata

            if metadata and metadata.grounding_chunks:
                for chunk in metadata.grounding_chunks:
                    if chunk.web:
                        titulo = chunk.web.title or "Sin título"
                        uri = chunk.web.uri or ""
                        fuentes.append(f"{titulo} — {uri}")
        except (AttributeError, IndexError):
            pass

        return fuentes

    def test_conexion(self) -> dict:
        """Prueba rápida de conexión."""
        resultado = {"base": False, "search": False, "detalle": ""}

        try:
            resp = self.model.generate_content("Responde: CONEXION OK")
            if resp.text:
                resultado["base"] = True
                resultado["detalle"] = resp.text[:200]
        except Exception as e:
            resultado["detalle"] = str(e)

        return resultado
