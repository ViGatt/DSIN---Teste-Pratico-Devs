import { SignedIn, SignedOut, SignInButton, UserButton } from "@clerk/clerk-react";
import { Button } from "@/components/ui/button";
import { CustomerForm } from "@/components/CustomerForm"; 
import { DatePicker } from "@/components/DatePicker"; 
import { ServiceSelection } from "@/components/ServiceSelection"; 
import { useSchedulingStore } from "@/store/useSchedulingStore"; 

function App() {
  const clientData = useSchedulingStore((state) => state.clientData);
  const selectedDate = useSchedulingStore((state) => state.selectedDate);
  const selectedService = useSchedulingStore((state) => state.selectedService);

  const handleFinalize = () => {
    const payload = {
      client: clientData,
      date: selectedDate,
      service: selectedService
    };
    console.log("Enviando para o banco de dados...", payload);
    alert("Agendamento confirmado com sucesso!");
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
        <div className="w-full max-w-md flex flex-col items-center space-y-6">
          <div className="flex items-center gap-4 bg-white p-4 rounded-lg shadow-sm border w-full justify-between">
            <span className="font-medium">Bem-vindo(a)!</span>
            <UserButton />
          </div>
          
          {!clientData ? (
            <CustomerForm />
          ) : (
            <div className="space-y-6 w-full animate-in fade-in duration-500 pb-12">
              
              {/* 1. */}
              <div className="p-4 bg-emerald-50 border border-emerald-200 text-emerald-800 rounded-lg text-sm shadow-sm">
                <p className="font-semibold mb-1">✓ Dados confirmados</p>
                <p>{clientData.name}</p>
                <p>{clientData.phone}</p>
              </div>
              
              {/* 2. Data */}
              <div className="p-6 bg-white border border-zinc-200 rounded-lg shadow-sm w-full">
                <h3 className="mb-4 font-semibold text-zinc-900">Escolha a Data</h3>
                <DatePicker />
              </div>

              {/* 3. Serviços */}
              {selectedDate && (
                <div className="p-6 bg-white border border-zinc-200 rounded-lg shadow-sm w-full animate-in slide-in-from-top-4 duration-500">
                  <h3 className="mb-4 font-semibold text-zinc-900">Escolha o Serviço</h3>
                  <ServiceSelection />
                </div>
              )}

              {/* Só aparece se o serviço foi selecionado */}
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
        </div>
      </SignedIn>
      
    </div>
  );
}

export default App;