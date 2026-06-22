import { useState, useEffect } from "react";
import { useAuth } from "@clerk/clerk-react";
import { fetchDashboardMetrics, DashboardData } from "@/services/api";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import { TrendingUp, Calendar, Users } from "lucide-react";

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

  if (loading) return <div className="p-8 text-center text-zinc-500 animate-pulse">Carregando métricas do salão...</div>;
  if (error) return <div className="p-8 text-center text-red-500 font-medium">Erro: {error}</div>;
  if (!data) return null;

  const chartData = Object.entries(data.agendamentos_por_dia).map(([dia, quantidade]) => ({
    name: dia,
    agendamentos: quantidade
  }));

  const totalAgendamentos = chartData.reduce((acc, curr) => acc + curr.agendamentos, 0);
  const servicoTop1 = data.servicos_mais_buscados[0]?.nome || "Nenhum";

  return (
    <div className="w-full space-y-6 animate-in fade-in duration-500">
      
      {/* Cards de Resumo (KPIs) */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white p-6 rounded-xl border border-zinc-200 shadow-sm flex items-center gap-4">
          <div className="p-3 bg-emerald-100 text-emerald-600 rounded-lg">
            <Calendar size={24} />
          </div>
          <div>
            <p className="text-sm text-zinc-500 font-medium">Agendamentos na Semana</p>
            <p className="text-2xl font-bold text-zinc-900">{totalAgendamentos}</p>
          </div>
        </div>

        <div className="bg-white p-6 rounded-xl border border-zinc-200 shadow-sm flex items-center gap-4">
          <div className="p-3 bg-blue-100 text-blue-600 rounded-lg">
            <TrendingUp size={24} />
          </div>
          <div>
            <p className="text-sm text-zinc-500 font-medium">Serviço em Alta</p>
            <p className="text-xl font-bold text-zinc-900 truncate">{servicoTop1}</p>
          </div>
        </div>

        <div className="bg-white p-6 rounded-xl border border-zinc-200 shadow-sm flex items-center gap-4">
          <div className="p-3 bg-purple-100 text-purple-600 rounded-lg">
            <Users size={24} />
          </div>
          <div>
            <p className="text-sm text-zinc-500 font-medium">Melhores Clientes</p>
            <p className="text-xl font-bold text-zinc-900">{data.top_clientes.length}</p>
          </div>
        </div>
      </div>

      {/* Gráfico de Barras */}
      <div className="bg-white p-6 rounded-xl border border-zinc-200 shadow-sm">
        <h3 className="text-lg font-bold text-zinc-900 mb-6">Volume de Agendamentos por Dia</h3>
        <div className="h-72 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e4e4e7" />
              <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fill: '#71717a' }} />
              <YAxis allowDecimals={false} axisLine={false} tickLine={false} tick={{ fill: '#71717a' }} />
              <Tooltip 
                cursor={{ fill: '#f4f4f5' }}
                contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
              />
              <Bar dataKey="agendamentos" fill="#10b981" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

    </div>
  );
}