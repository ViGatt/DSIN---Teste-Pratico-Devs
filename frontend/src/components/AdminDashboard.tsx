import { useState, useEffect } from "react";
import { useAuth } from "@clerk/clerk-react";
import { fetchDashboardMetrics, DashboardData, fetchAgendamentos, AgendamentoItem, remarcarAgendamentoAdmin, cancelarAgendamentoAdmin, restaurarAgendamentoAdmin } from "@/services/api";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import { TrendingUp, Calendar, Users, Edit2, Check, X, Trash2, RotateCcw } from "lucide-react";

export function AdminDashboard() {
  const { getToken } = useAuth();
  const [data, setData] = useState<DashboardData | null>(null);
  const [agendamentosList, setAgendamentosList] = useState<AgendamentoItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [editingId, setEditingId] = useState<string | null>(null);
  const [novaDataInput, setNovaDataInput] = useState<string>("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  // Controle de Abas
  const [abaAtiva, setAbaAtiva] = useState<"ativos" | "cancelados">("ativos");

  const loadData = async () => {
    try {
      const token = await getToken();
      if (!token) throw new Error("Acesso negado");
      const [metrics, lista] = await Promise.all([fetchDashboardMetrics(token), fetchAgendamentos(token)]);
      setData(metrics);
      setAgendamentosList(lista);
    } catch (err: any) { setError(err.message); } 
    finally { setLoading(false); }
  };

  useEffect(() => { loadData(); }, [getToken]);

  const handleRemarcar = async (id: string) => { /* ... (mantém igual) ... */ 
    if (!novaDataInput) return;
    try {
      setIsSubmitting(true);
      const token = await getToken();
      if (!token) throw new Error("Não autenticado");
      await remarcarAgendamentoAdmin(token, id, new Date(novaDataInput).toISOString());
      setEditingId(null); setNovaDataInput(""); await loadData();
    } catch (err: any) { alert(`Erro: ${err.message}`); } 
    finally { setIsSubmitting(false); }
  };

  const handleCancelar = async (id: string, dataHora: string) => {
    const confirmou = window.confirm(`Tem certeza que deseja CANCELAR o agendamento do dia ${dataHora}?`);
    if (!confirmou) return;
    try {
      setIsSubmitting(true);
      const token = await getToken();
      if (!token) throw new Error("Não autenticado");
      await cancelarAgendamentoAdmin(token, id);
      await loadData();
    } catch (err: any) { alert(`Erro: ${err.message}`); } 
    finally { setIsSubmitting(false); }
  };

  // Função de Restaurar
  const handleRestaurar = async (id: string) => {
    try {
      setIsSubmitting(true);
      const token = await getToken();
      if (!token) throw new Error("Não autenticado");
      await restaurarAgendamentoAdmin(token, id);
      await loadData();
    } catch (err: any) { alert(`Erro: ${err.message}`); } 
    finally { setIsSubmitting(false); }
  };

  if (loading) return <div className="p-8 text-center text-zinc-500 animate-pulse">Carregando métricas...</div>;
  if (error) return <div className="p-8 text-center text-red-500">Erro: {error}</div>;
  if (!data) return null;

  const chartData = Object.entries(data.agendamentos_por_dia).map(([dia, quantity]) => ({ name: dia, agendamentos: quantity }));
  const totalAgendamentos = chartData.reduce((acc, curr) => acc + curr.agendamentos, 0);
  const servicoTop1 = data.servicos_mais_buscados[0]?.nome || "Nenhum";

  const formatarData = (dataIso: string) => {
    return new Date(dataIso).toLocaleString('pt-BR', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' }).replace(',', ' às');
  };

  // Filtros para as Abas
  const agendamentosFiltrados = agendamentosList.filter(ag => 
    abaAtiva === "ativos" ? ag.status !== "CANCELADO" : ag.status === "CANCELADO"
  );

  return (
    <div className="w-full space-y-6 animate-in fade-in duration-500">
      {/* ... (Cards e Gráficos mantidos iguais) ... */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
         <div className="bg-white p-6 rounded-xl border border-zinc-200 shadow-sm flex items-center gap-4">
          <div className="p-3 bg-emerald-100 text-emerald-600 rounded-lg"><Calendar size={24} /></div>
          <div><p className="text-sm text-zinc-500 font-medium">Agendamentos na Semana</p><p className="text-2xl font-bold text-zinc-900">{totalAgendamentos}</p></div>
        </div>
        <div className="bg-white p-6 rounded-xl border border-zinc-200 shadow-sm flex items-center gap-4">
          <div className="p-3 bg-blue-100 text-blue-600 rounded-lg"><TrendingUp size={24} /></div>
          <div><p className="text-sm text-zinc-500 font-medium">Serviço em Alta</p><p className="text-xl font-bold text-zinc-900 truncate">{servicoTop1}</p></div>
        </div>
        <div className="bg-white p-6 rounded-xl border border-zinc-200 shadow-sm flex items-center gap-4">
          <div className="p-3 bg-purple-100 text-purple-600 rounded-lg"><Users size={24} /></div>
          <div><p className="text-sm text-zinc-500 font-medium">Melhores Clientes</p><p className="text-xl font-bold text-zinc-900">{data.top_clientes.length}</p></div>
        </div>
      </div>

      <div className="bg-white p-6 rounded-xl border border-zinc-200 shadow-sm">
        <h3 className="text-lg font-bold text-zinc-900 mb-6">Volume de Agendamentos por Dia</h3>
        <div className="h-72 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e4e4e7" />
              <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fill: '#71717a' }} />
              <YAxis allowDecimals={false} axisLine={false} tickLine={false} tick={{ fill: '#71717a' }} />
              <Tooltip cursor={{ fill: '#f4f4f5' }} contentStyle={{ borderRadius: '8px', border: 'none' }} />
              <Bar dataKey="agendamentos" fill="#10b981" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Tabela com Abas */}
      <div className="bg-white rounded-xl border border-zinc-200 shadow-sm overflow-hidden">
        
        {/* Cabeçalho com Botões de Aba */}
        <div className="p-6 border-b border-zinc-200 flex justify-between items-center">
          <h3 className="text-lg font-bold text-zinc-900">Gerenciar Agendamentos</h3>
          <div className="flex gap-2 bg-zinc-100 p-1 rounded-lg">
            <button 
              onClick={() => setAbaAtiva("ativos")}
              className={`px-4 py-1.5 text-sm font-medium rounded-md transition-colors ${abaAtiva === "ativos" ? "bg-white shadow-sm text-zinc-900" : "text-zinc-500 hover:text-zinc-700"}`}
            >
              Ativos
            </button>
            <button 
              onClick={() => setAbaAtiva("cancelados")}
              className={`px-4 py-1.5 text-sm font-medium rounded-md transition-colors ${abaAtiva === "cancelados" ? "bg-white shadow-sm text-zinc-900" : "text-zinc-500 hover:text-zinc-700"}`}
            >
              Cancelados
            </button>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm whitespace-nowrap">
            <thead className="bg-zinc-50 text-zinc-500">
              <tr>
                <th className="px-6 py-4 font-medium">Data e Hora</th>
                <th className="px-6 py-4 font-medium">Cliente (ID)</th>
                <th className="px-6 py-4 font-medium">Serviços</th>
                <th className="px-6 py-4 font-medium">Status</th>
                <th className="px-6 py-4 font-medium text-right">Ações</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-zinc-200">
              {agendamentosFiltrados.length === 0 ? (
                <tr><td colSpan={5} className="px-6 py-8 text-center text-zinc-500">Nenhum agendamento encontrado nesta categoria.</td></tr>
              ) : (
                agendamentosFiltrados.map((ag) => {
                  const dataFormatada = formatarData(ag.data_hora_agendada);
                  return (
                    <tr key={ag.id} className={`transition-colors ${abaAtiva === "cancelados" ? "bg-red-50/50 opacity-80" : "hover:bg-zinc-50"}`}>
                      
                      <td className="px-6 py-4 font-medium text-zinc-900">
                        {editingId === ag.id ? (
                          <input type="datetime-local" className="border rounded p-1 text-sm outline-none" value={novaDataInput} onChange={(e) => setNovaDataInput(e.target.value)} />
                        ) : dataFormatada}
                      </td>
                      
                      <td className="px-6 py-4 text-zinc-600 truncate max-w-[150px]">{ag.cliente_id}</td>
                      <td className="px-6 py-4 text-zinc-600">{ag.servicos.join(", ")}</td>
                      <td className="px-6 py-4">
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${ag.status === "CANCELADO" ? "bg-red-100 text-red-800" : "bg-amber-100 text-amber-800"}`}>
                          {ag.status}
                        </span>
                      </td>
                      
                      <td className="px-6 py-4 text-right">
                        {abaAtiva === "cancelados" ? (
                          // Botão de Restaurar na Lixeira
                          <button onClick={() => handleRestaurar(ag.id)} disabled={isSubmitting} className="p-1.5 text-zinc-400 hover:text-emerald-600 hover:bg-emerald-50 rounded transition-colors" title="Restaurar Agendamento">
                            <RotateCcw size={16} />
                          </button>
                        ) : (
                          // Botões Normais (Editar/Cancelar)
                          editingId === ag.id ? (
                            <div className="flex justify-end gap-2">
                              <button onClick={() => handleRemarcar(ag.id)} disabled={isSubmitting} className="p-1.5 bg-emerald-100 text-emerald-700 rounded hover:bg-emerald-200 transition-colors"><Check size={16} /></button>
                              <button onClick={() => { setEditingId(null); setNovaDataInput(""); }} disabled={isSubmitting} className="p-1.5 bg-red-100 text-red-700 rounded hover:bg-red-200 transition-colors"><X size={16} /></button>
                            </div>
                          ) : (
                            <div className="flex justify-end gap-2">
                              <button onClick={() => { setEditingId(ag.id); setNovaDataInput(ag.data_hora_agendada.slice(0, 16)); }} disabled={isSubmitting} className="p-1.5 text-zinc-400 hover:text-blue-600 hover:bg-blue-50 rounded transition-colors"><Edit2 size={16} /></button>
                              <button onClick={() => handleCancelar(ag.id, dataFormatada)} disabled={isSubmitting} className="p-1.5 text-zinc-400 hover:text-red-600 hover:bg-red-50 rounded transition-colors"><Trash2 size={16} /></button>
                            </div>
                          )
                        )}
                      </td>

                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>
      </div>

    </div>
  );
}