import { SignedIn, SignedOut, SignInButton, UserButton, useUser, useAuth } from "@clerk/clerk-react";
import { Button } from "@/components/ui/button";
import { CustomerForm } from "@/components/CustomerForm"; 
import { DatePicker } from "@/components/DatePicker"; 
import { ServiceSelection } from "@/components/ServiceSelection"; 
import { useSchedulingStore } from "@/store/useSchedulingStore";
import { AdminDashboard } from "@/components/AdminDashboard"; 
import { useState } from "react";
import { MeusAgendamentos } from "@/components/MeusAgendamentos";

function App() {
  const clientData = useSchedulingStore((state) => state.clientData);
  const selectedDate = useSchedulingStore((state) => state.selectedDate);
  const selectedService = useSchedulingStore((state) => state.selectedService);
  
  const { user } = useUser();
  const { getToken } = useAuth();

  const [abaCliente, setAbaCliente] = useState<'novo' | 'historico'>('novo');

  const ID_DA_LEILA = "user_3FVfOWRRXJzmoa36szoO7BuE1qt"; 
  const isAdmin = user?.id === ID_DA_LEILA;

  const handleFinalize = async () => {
    if (!selectedDate || !selectedService) {
      alert("Selecione a data e o serviço.");
      return;
    }

    try {
      const token = await getToken();
      if (!token) throw new Error("Usuário não autenticado.");

      const payload = {
        data_desejada: selectedDate.toISOString(), 
        servicos: [selectedService],               
        ignorar_sugestao: false                    
      };

      const response = await fetch("http://localhost:8000/agendamentos/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: "Erro desconhecido" }));
        throw new Error(errorData.detail || "Erro ao salvar agendamento.");
      }

      alert("Agendamento confirmado com sucesso!");
      window.location.reload(); 

    } catch (error: any) {
      console.error("Erro na API:", error);
      alert(`Erro: ${error.message}`);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-zinc-50 p-4">
      
      <SignedOut>
        <div className="text-center space-y-4 bg-white p-8 rounded-xl shadow-sm border border-zinc-200">
          <h1 className="text-3xl font-bold text-zinc-900">Salão da Leila</h1>
          <p className="text-zinc-500">Faça login para agendar seu horário</p>
          <SignInButton mode="modal">
            <Button className="w-full">Entrar / Cadastrar</Button>
          </SignInButton>
        </div>
      </SignedOut>

      <SignedIn>
        {/* Se for Admin, expande a tela. Se for cliente, mantém modo mobile*/}
        <div className={`w-full flex flex-col items-center space-y-6 ${isAdmin ? 'max-w-5xl' : 'max-w-md'}`}>
          
          <div className="flex items-center gap-4 bg-white p-4 rounded-lg shadow-sm border w-full justify-between">
            <span className="font-medium">Bem-vindo(a), {user?.firstName}!</span>
            <UserButton />
          </div>
          
          {isAdmin ? (
            /* Só renderiza se o usuário for a Leila */
            <AdminDashboard />
          ) : (
            /* Renderiza o formulário e oculta o painel */
            <div className="w-full space-y-6">
              
              {/* Menu de Navegação do Cliente */}
              <div className="flex gap-2 bg-zinc-200/50 p-1 rounded-lg w-full">
                <button 
                  onClick={() => setAbaCliente('novo')}
                  className={`flex-1 py-2 text-sm font-medium rounded-md transition-colors ${abaCliente === 'novo' ? 'bg-white shadow-sm text-zinc-900 border border-zinc-200/50' : 'text-zinc-500 hover:text-zinc-700'}`}
                >
                  Novo Agendamento
                </button>
                <button 
                  onClick={() => setAbaCliente('historico')}
                  className={`flex-1 py-2 text-sm font-medium rounded-md transition-colors ${abaCliente === 'historico' ? 'bg-white shadow-sm text-zinc-900 border border-zinc-200/50' : 'text-zinc-500 hover:text-zinc-700'}`}
                >
                  Meu Histórico
                </button>
              </div>

              {/* Renderização Condicional */}
              {abaCliente === 'novo' ? (
                <>
                  {!clientData ? (
                    <CustomerForm />
                  ) : (
                    <div className="space-y-6 w-full animate-in fade-in duration-500 pb-12">
                      <div className="p-4 bg-emerald-50 border border-emerald-200 text-emerald-800 rounded-lg text-sm shadow-sm">
                        <p className="font-semibold mb-1">✓ Dados confirmados</p>
                        <p>{clientData.name}</p>
                        <p>{clientData.phone}</p>
                      </div>
                      
                      <div className="p-6 bg-white border border-zinc-200 rounded-lg shadow-sm w-full">
                        <h3 className="mb-4 font-semibold text-zinc-900">Escolha a Data</h3>
                        <DatePicker />
                      </div>

                      {selectedDate && (
                        <div className="p-6 bg-white border border-zinc-200 rounded-lg shadow-sm w-full animate-in slide-in-from-top-4 duration-500">
                          <h3 className="mb-4 font-semibold text-zinc-900">Escolha o Serviço</h3>
                          <ServiceSelection />
                        </div>
                      )}

                      {selectedService && (
                        <div className="p-6 bg-zinc-900 text-white rounded-lg shadow-lg w-full animate-in slide-in-from-bottom-4 duration-500">
                          <h3 className="mb-4 font-semibold text-zinc-100">Resumo do Agendamento</h3>
                          <div className="space-y-2 mb-6 text-sm text-zinc-300">
                            <div className="flex justify-between">
                              <span>Serviço:</span>
                              <span className="font-medium text-white">{selectedService}</span>
                            </div>
                            <div className="flex justify-between">
                              <span>Data:</span>
                              <span className="font-medium text-white">
                                {selectedDate?.toLocaleDateString('pt-BR')}
                              </span>
                            </div>
                          </div>
                          <Button 
                            className="w-full bg-emerald-500 hover:bg-emerald-600 text-white font-bold h-12"
                            onClick={handleFinalize}
                          >
                            Confirmar Agendamento
                          </Button>
                        </div>
                      )}
                    </div>
                  )}
                </>
              ) : (
                <MeusAgendamentos />
              )}
            </div>
          )}

        </div>
      </SignedIn>
      
    </div>
  );
}

export default App;