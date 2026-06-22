const API_BASE_URL = "http://localhost:8000";

export interface DashboardData {
  periodo: Record<string, string>;
  agendamentos_por_dia: Record<string, number>;
  servicos_mais_buscados: any[];
  horarios_pico: any[];
  top_clientes: any[];
}

export const fetchDashboardMetrics = async (token: string, dataReferencia?: Date): Promise<DashboardData> => {
  // Se a Leila escolher uma data no calendário, envia. Senão, puxa a semana atual.
  let url = `${API_BASE_URL}/agendamentos/desempenho`;
  if (dataReferencia) {
    url += `?data_referencia=${dataReferencia.toISOString()}`;
  }

  const response = await fetch(url, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`
    }
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    throw new Error(errorData?.detail || "Falha ao carregar métricas do dashboard");
  }

  return response.json();
};