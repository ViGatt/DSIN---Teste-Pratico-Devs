import { useState, useEffect } from "react";
import { useAuth } from "@clerk/clerk-react";
import { fetchMeusAgendamentos, AgendamentoItem } from "@/services/api";
import { Calendar, Clock, AlertCircle } from "lucide-react";

export function MeusAgendamentos() {
  const { getToken } = useAuth();
  const [agendamentos, setAgendamentos] = useState<AgendamentoItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadHistorico = async () => {
      try {
        const token = await getToken();
        if (!token) throw new Error("Não autenticado");
        const lista = await fetchMeusAgendamentos(token);
        setAgendamentos(lista);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    loadHistorico();
  }, [getToken]);

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
          
          // Regra de Negócio: Menos de 48 horas trava a edição no sistema
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
                    <div className="flex items-center gap-2 text-amber-600 text-sm bg-amber-50 p-2 rounded-lg border border-amber-100">
                      <AlertCircle size={16} />
                      <span className="max-w-[200px]">Faltam menos de 48h. Para alterar, ligue para o salão.</span>
                    </div>
                  ) : (
                    <button className="text-sm font-medium text-emerald-600 hover:text-emerald-700 hover:bg-emerald-50 px-3 py-1.5 rounded-md transition-colors border border-emerald-200">
                      Remarcar / Cancelar
                    </button>
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