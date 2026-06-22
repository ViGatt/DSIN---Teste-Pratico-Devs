import { useState, useEffect } from "react";
import { useAuth } from "@clerk/clerk-react";
import { fetchDashboardMetrics, DashboardData } from "@/services/api";

export function AdminDashboard() {
  const { getToken } = useAuth();
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadData = async () => {
      try {
        const token = await getToken();
        if (!token) throw new Error("Acesso negado: Token não encontrado");

        const metrics = await fetchDashboardMetrics(token);
        console.log("DADOS RECEBIDOS DO BACKEND:", metrics);
        setData(metrics);
      } catch (err: any) {
        console.error(err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, [getToken]);

  if (loading) return <div className="p-8 text-center text-zinc-500">Carregando painel de gestão...</div>;
  if (error) return <div className="p-8 text-center text-red-500 font-medium">Erro: {error}</div>;
  if (!data) return null;

  return (
    <div className="p-8 w-full max-w-5xl mx-auto space-y-6">
      <h2 className="text-3xl font-bold text-zinc-900">Visão Geral - Salão da Leila</h2>
      
      {/* Ver o dado em tela antes de criar os gráficos */}
      <div className="bg-zinc-900 text-emerald-400 p-6 rounded-xl overflow-auto text-sm shadow-lg">
        <pre>{JSON.stringify(data, null, 2)}</pre>
      </div>
    </div>
  );
}