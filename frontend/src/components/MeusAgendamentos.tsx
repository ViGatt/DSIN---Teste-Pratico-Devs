import { useState, useEffect } from "react";
import { useAuth } from "@clerk/clerk-react";
import { fetchMeusAgendamentos, AgendamentoItem, cancelarAgendamentoCliente, remarcarAgendamentoCliente } from "@/services/api";
import { Calendar, AlertCircle, Edit2, Trash2, Check, X } from "lucide-react";

export function MeusAgendamentos() {
  const { getToken } = useAuth();
  const [agendamentos, setAgendamentos] = useState<AgendamentoItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  const [editingId, setEditingId] = useState<string | null>(null);
  const [novaDataInput, setNovaDataInput] = useState<string>("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const loadHistorico = async () => {
  try {
    const token = await getToken();
    const response = await fetch(`http://localhost:8000/agendamentos/meus?t=${Date.now()}`, {
      headers: { "Authorization": `Bearer ${token}` }
    });
    
    const data = await response.json();
    console.log("DADOS QUE O FRONTEND RECEBEU DO BACKEND:", data); // <--- LOG CRÍTICO
    setAgendamentos(data);
  } catch (err: any) { 
    setError(err.message); 
  } finally { 
    setLoading(false); 
  }
};

  useEffect(() => {
  loadHistorico();
}, []); 

  const handleCancelar = async (id: string) => {
    const confirmou = window.confirm("Tem certeza que deseja cancelar este agendamento?");
    if (!confirmou) return;
    try {
      setIsSubmitting(true);
      const token = await getToken();
      if (!token) return;
      await cancelarAgendamentoCliente(token, id);
      await loadHistorico();
    } catch (err: any) { alert(err.message); } 
    finally { setIsSubmitting(false); }
  };

  const handleRemarcar = async (id: string) => {
    if (!novaDataInput) return;
    try {
      setIsSubmitting(true);
      const token = await getToken();
      if (!token) return;
      await remarcarAgendamentoCliente(token, id, new Date(novaDataInput).toISOString());
      setEditingId(null);
      await loadHistorico();
    } catch (err: any) { alert(err.message); } 
    finally { setIsSubmitting(false); }
  };

  if (loading) return <div className="p-8 text-center text-zinc-500 animate-pulse">Buscando seu histórico...</div>;
  if (error) return <div className="p-8 text-center text-red-500">Erro: {error}</div>;

  const formatarData = (dataIso: string) => {
    return new Date(dataIso).toLocaleString('pt-BR', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' }).replace(',', ' às');
  };

  return (
    <div className="w-full space-y-4 animate-in fade-in duration-500">
      <h3 className="text-xl font-bold text-zinc-900 mb-4">Meu Histórico</h3>
      
      {agendamentos.length === 0 ? (
        <div className="bg-white p-8 rounded-xl border border-zinc-200 text-center text-zinc-500">
          Você ainda não possui agendamentos no Salão da Leila.
        </div>
      ) : (
        agendamentos.map((ag) => {
          const dataAgendamento = new Date(ag.data_hora_agendada);
          const agora = new Date();
          const horasDiferenca = (dataAgendamento.getTime() - agora.getTime()) / (1000 * 60 * 60);
          
          const isTravado = horasDiferenca > 0 && horasDiferenca < 48 && ag.status !== "CANCELADO";
          const isPassado = horasDiferenca <= 0;

          return (
            <div key={ag.id} className={`bg-white p-5 rounded-xl border ${ag.status === 'CANCELADO' ? 'border-red-100 bg-red-50/30' : 'border-zinc-200'} shadow-sm flex flex-col md:flex-row justify-between gap-4 transition-all hover:shadow-md`}>
              
              <div className="space-y-2">
                <div className="flex items-center gap-2">
                  <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${ag.status === 'CANCELADO' ? 'bg-red-100 text-red-800' : isPassado ? 'bg-zinc-100 text-zinc-600' : 'bg-emerald-100 text-emerald-800'}`}>
                    {ag.status === 'CANCELADO' ? 'Cancelado' : isPassado ? 'Concluído' : 'Confirmado'}
                  </span>
                </div>
                <div className="flex items-center gap-2 text-zinc-900 font-semibold text-lg">
                  <Calendar size={18} className="text-zinc-400" />
                  {formatarData(ag.data_hora_agendada)}
                </div>
                <div className="text-zinc-600 text-sm pl-6">
                  {ag.servicos.join(" • ")}
                </div>
              </div>

              {!isPassado && ag.status !== "CANCELADO" && (
                <div className="flex flex-col justify-center items-end text-right">
                  {isTravado ? (
                    <div className="flex items-center gap-2 text-amber-600 text-sm bg-amber-50 p-2 rounded-lg border border-amber-100 mt-2">
                      <AlertCircle size={16} />
                      <span className="max-w-[200px]">Faltam menos de 48h. Para alterar, ligue para o salão.</span>
                    </div>
                  ) : (
                    <div className="flex gap-2 mt-2">
                      {editingId === ag.id ? (
                        <div className="flex flex-col items-end gap-2 bg-zinc-50 p-3 rounded-lg border border-zinc-200 shadow-sm">
                          <input 
                            type="datetime-local" 
                            className="border rounded p-1.5 text-sm outline-none w-full bg-white" 
                            value={novaDataInput} 
                            onChange={(e) => setNovaDataInput(e.target.value)} 
                          />
                          <div className="flex gap-2">
                            <button onClick={() => handleRemarcar(ag.id)} disabled={isSubmitting} className="p-1.5 bg-emerald-100 text-emerald-700 rounded hover:bg-emerald-200 transition-colors" title="Confirmar nova data"><Check size={16} /></button>
                            <button onClick={() => { setEditingId(null); setNovaDataInput(""); }} disabled={isSubmitting} className="p-1.5 bg-red-100 text-red-700 rounded hover:bg-red-200 transition-colors" title="Cancelar edição"><X size={16} /></button>
                          </div>
                        </div>
                      ) : (
                        <>
                          <button 
                            onClick={() => { setEditingId(ag.id); setNovaDataInput(ag.data_hora_agendada.slice(0, 16)); }} 
                            className="flex items-center gap-1 text-sm font-medium text-blue-600 hover:bg-blue-50 px-3 py-1.5 rounded-md transition-colors border border-blue-200"
                          >
                            <Edit2 size={14} /> Remarcar
                          </button>
                          <button 
                            onClick={() => handleCancelar(ag.id)} 
                            className="flex items-center gap-1 text-sm font-medium text-red-600 hover:bg-red-50 px-3 py-1.5 rounded-md transition-colors border border-red-200"
                          >
                            <Trash2 size={14} /> Cancelar
                          </button>
                        </>
                      )}
                    </div>
                  )}
                </div>
              )}
            </div>
          );
        })
      )}
    </div>
  );
}